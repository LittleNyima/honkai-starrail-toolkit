import json
import os
import time
import traceback
from typing import List

import qfluentwidgets as qfw
from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, QObject, Qt, QThread, Signal
from PySide6.QtWidgets import QLabel, QTableWidgetItem, QVBoxLayout

import starrail.gacha.service as service
from starrail.config import configuration as cfg
from starrail.gacha.type import GachaType
from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.common.utils import get_current_uid
from starrail.gui.interfaces.base import BaseInterface
from starrail.utils import babelfish, loggings

AF = Qt.AlignmentFlag
logger = loggings.get_logger(__file__)


class GachaSyncThread(QThread):

    syncStateSignal = Signal(str)
    syncSuccessSignal = Signal(str)
    syncFailSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        try:
            uid = self.syncGachaData()
            self.syncSuccessSignal.emit(uid)
        except Exception:
            self.syncFailSignal.emit(
                f'{babelfish.ui_traceback()}:\n{traceback.format_exc()}',
            )

    def logAndUpdateState(self, message, level=loggings.logging.INFO):
        logger.log(level=level, msg=f'[GUI] {message}')
        self.syncStateSignal.emit(message)

    def exportGachaType(self, api_template, gacha_type, request_interval):
        r = []
        end_id = '0'
        for page in service.integers():
            self.logAndUpdateState(
                babelfish.ui_downloading_gacha(
                    name=babelfish.translate(gacha_type.name),
                    page=page,
                ),
            )
            api_url = service.get_api_url(
                api_template, end_id, str(gacha_type.value),
                str(page), '5',
            )
            logger.debug(f'Requesting {api_url}')
            response, code = service.fetch_json(api_url)
            time.sleep(request_interval)
            if not service.check_response(response, code):
                break
            data_list = response['data']['list']
            r.extend(data_list)
            end_id = data_list[-1]['id']
        return r

    def syncGachaData(self):
        self.logAndUpdateState(babelfish.ui_extracting_api_url())
        api_url = service.detect_api_url()
        response, code = service.fetch_json(api_url)
        valid = service.check_response(response, code)
        if not valid:
            self.syncFailSignal.emit(babelfish.ui_extract_api_fail())
            raise ValueError(babelfish.ui_extract_api_fail())

        api_template = service.get_url_template(api_url)

        uid = response['data']['list'][0]['uid']
        manager = service.GachaDataManager(uid)
        manager.log_stats()

        for gacha_type in service.GachaType:
            records = self.exportGachaType(
                api_template,
                gacha_type,
                0.15,
            )
            manager.add_records(gacha_type.value, records)
            manager.gacha[gacha_type.value].sort()

        service.fileio.export_as_sql(manager, manager.cache_path)
        manager.log_stats()

        return uid


class RecordExportThread(QThread):

    saveSuccessSignal = Signal(str)

    def __init__(self, uid, path, parent=None):
        super().__init__(parent=parent)
        self.uid = uid
        self.path = path

    def run(self):
        manager = service.GachaDataManager(self.uid)
        export_hooks = dict(
            csv=service.fileio.export_as_csv,
            html=service.fileio.export_as_html,
            json=service.fileio.export_as_json,
            md=service.fileio.export_as_md,
            xlsx=service.fileio.export_as_xlsx,
        )
        for format, hook in export_hooks.items():
            filename = f'HKSR-export-{self.uid}.{format}'
            export_path = os.path.join(self.path, filename)
            hook(manager, export_path)
        self.saveSuccessSignal.emit(self.path)


class ResultTableWidget(QtWidgets.QWidget):

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.labelsLayout = qfw.FlowLayout()

        self.titleLabel = QLabel(title)
        self.table = qfw.TableWidget(self)

        self.__initWidgets()
        self.__initTable()

    def __initWidgets(self):
        self.table.verticalHeader().hide()
        self.table.setColumnCount(5)
        self.table.setRowCount(3)
        self.table.setHorizontalHeaderLabels([
            babelfish.ui_gacha_type(), babelfish.ui_gacha_count(),
            babelfish.ui_gacha_basic_prob(), babelfish.ui_gacha_true_prob(),
            babelfish.ui_gacha_since_last(),
        ])
        self.table.setEnabled(False)
        SM = QtWidgets.QAbstractItemView.ScrollMode
        self.table.setHorizontalScrollMode(SM.ScrollPerPixel)
        self.table.setVerticalScrollMode(SM.ScrollPerPixel)

        self.labelsLayout.setContentsMargins(0, 0, 0, 10)
        self.labelsLayout.setHorizontalSpacing(10)
        self.labelsLayout.setVerticalSpacing(20)

        self.vBoxLayout.setContentsMargins(10, 10, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.table)
        self.vBoxLayout.addLayout(self.labelsLayout)

        self.setFixedWidth(580)
        self.setObjectName('frame')
        self.titleLabel.setObjectName('titleLabel')
        self.table.setObjectName('table')
        StyleSheet.RESULT_TABLE_WIDGET.apply(self)

    def __initTable(self):
        self.setTableData([
            ['5'] + [babelfish.ui_no_data()] * 4,
            ['4'] + [babelfish.ui_no_data()] * 4,
            ['3'] + [babelfish.ui_no_data()] * 4,
        ])

    def setTableData(self, data: List[List[str]]):
        # data: 3x5
        logger.debug(f'[GUI] {data}')
        for idx0, row in enumerate(data):
            for idx1, item in enumerate(row):
                self.table.setItem(idx0, idx1, QTableWidgetItem(item))

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event is QEvent.Type.Scroll:
            self.parent().eventFilter(watched, event)
        return super().eventFilter(watched, event)


class GachaSyncInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title, subtitle, parent)

        # Buttons
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.syncButton = qfw.PrimaryPushButton(
            text=babelfish.ui_sync(),
            parent=self,
            icon=qfw.FluentIcon.SYNC,
        )
        self.syncButton.clicked.connect(self.onSyncButtonClicked)
        self.saveButton = qfw.PrimaryPushButton(
            text=babelfish.ui_save_data(),
            parent=self,
            icon=qfw.FluentIcon.SAVE_AS,
        )
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.saveButton.setDisabled(True)

        # Tables
        self.tableLayout = qfw.FlowLayout()
        self.stellarTable = ResultTableWidget(
            babelfish.translate('STELLAR'),
            self,
        )
        self.departureTable = ResultTableWidget(
            babelfish.translate('DEPARTURE'),
            self,
        )
        self.characterTable = ResultTableWidget(
            babelfish.translate('CHARACTER'),
            self,
        )
        self.lightConeTable = ResultTableWidget(
            babelfish.translate('LIGHT_CONE'),
            self,
        )

        # Gacha Sync Temp Objects
        self.syncThread = None
        self.syncToolTip = None
        self.saveThread = None

        self.uid = get_current_uid()
        logger.info(f'Detected current uid: {self.uid}')
        if self.uid:
            self.updateTableDisplay()
            self.saveButton.setEnabled(True)

        self.__initWidget()

    def __initWidget(self):
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(AF.AlignLeft)
        self.buttonLayout.addWidget(self.syncButton)
        self.buttonLayout.addSpacing(10)
        self.buttonLayout.addWidget(self.saveButton)

        self.tableLayout.addWidget(self.stellarTable)
        self.tableLayout.addWidget(self.departureTable)
        self.tableLayout.addWidget(self.characterTable)
        self.tableLayout.addWidget(self.lightConeTable)

        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addLayout(self.tableLayout)

    def resizeEvent(self, e):
        if self.syncToolTip:
            self.syncToolTip.move(self.syncToolTip.getSuitablePos())
        return super().resizeEvent(e)

    def updateTableDisplay(self):
        manager = service.GachaDataManager(self.uid)
        mapping = {
            GachaType.STELLAR.name: self.stellarTable,
            GachaType.DEPARTURE.name: self.departureTable,
            GachaType.CHARACTER.name: self.characterTable,
            GachaType.LIGHT_CONE.name: self.lightConeTable,
        }
        for gacha_type in GachaType:
            stats = manager.gacha[gacha_type.value].stats
            table = [
                [
                    item['rank_type'], item['count'],
                    item['basic_prob'], item['compr_prob'],
                    item['since_last'],
                ] for item in stats
            ]
            mapping[gacha_type.name].setTableData(table)

    def onSyncButtonClicked(self):
        logger.info('[GUI] Start gacha data synchronization')

        self.syncButton.setDisabled(True)
        self.saveButton.setDisabled(True)

        self.syncToolTip = qfw.StateToolTip(
            babelfish.ui_synchronizing_gacha(),
            babelfish.ui_sync_gacha_initial(),
            self.window(),
        )
        self.syncToolTip.move(self.syncToolTip.getSuitablePos())
        self.syncToolTip.show()

        self.syncThread = GachaSyncThread(self)
        self.syncThread.syncStateSignal.connect(
            lambda s: self.setToolTipContentSlot(self.syncToolTip, s),
        )
        self.syncThread.syncSuccessSignal.connect(self.syncSuccessSlot)
        self.syncThread.syncFailSignal.connect(self.syncFailSlot)
        self.syncThread.start()

    def onSaveButtonClicked(self):
        logger.info('[GUI] Start gacha data exporting')

        self.syncButton.setDisabled(True)
        self.saveButton.setDisabled(True)

        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Export Folder', os.path.expanduser('~'),
        )
        if path:
            self.saveThread = RecordExportThread(self.uid, path, self)
            self.saveThread.saveSuccessSignal.connect(self.saveSuccessSlot)
            self.saveThread.start()
        else:
            self.syncButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def onSyncSuccess(self):
        self.updateTableDisplay()

    def setToolTipContentSlot(self, tooltip: qfw.StateToolTip, content: str):
        tooltip.setContent(content)

    def syncSuccessSlot(self, uid: int):
        logger.info('[GUI] Gacha data synchronization success')

        self.uid = uid
        cfg.uid = uid

        self.syncToolTip.setTitle(babelfish.ui_sync_gacha_success())
        self.syncToolTip.setContent('')
        self.syncToolTip.setState(True)
        self.syncToolTip = None
        self.syncThread = None

        self.syncButton.setEnabled(True)
        self.saveButton.setEnabled(True)

        self.onSyncSuccess()

    def syncFailSlot(self, message: str):
        logger.info(f'[GUI] Gacha data sync fail with message {message}')

        self.syncToolTip.setTitle(babelfish.ui_sync_gacha_fail())
        self.syncToolTip.setContent('')
        self.syncToolTip.setState(True)
        self.syncToolTip = None
        self.syncThread = None

        qfw.InfoBar.error(
            title=babelfish.ui_sync_gacha_fail(),
            content=message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

        self.syncButton.setEnabled(True)
        self.saveButton.setEnabled(True)

    def tableDisplaySlot(self, data):
        mapping = {
            GachaType.STELLAR.name: self.stellarTable,
            GachaType.DEPARTURE.name: self.departureTable,
            GachaType.CHARACTER.name: self.characterTable,
            GachaType.LIGHT_CONE.name: self.lightConeTable,
        }
        for key, value in json.loads(data).items():
            mapping[key].setTableData(value)

    def saveSuccessSlot(self, path):
        self.saveThread = None

        qfw.InfoBar.success(
            title=babelfish.ui_save_success(),
            content=babelfish.ui_save_success_msg(path),
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

        self.syncButton.setEnabled(True)
        self.saveButton.setEnabled(True)
