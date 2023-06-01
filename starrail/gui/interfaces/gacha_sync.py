import json
import os
import time
from collections import defaultdict

import qfluentwidgets as qfw
from PySide6 import QtCharts, QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel, QVBoxLayout

import starrail.gacha.service as service
from starrail.gacha.type import GachaType
from starrail.gui.common.icon import Icon
from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.common.thread import StatefulThread
from starrail.gui.interfaces.base import BaseInterface, CardWidget
from starrail.gui.widgets.pie_chart import SmartPieChart
from starrail.utils import babelfish, loggings
from starrail.utils.accounts import account_record, get_latest_uid

AF = Qt.AlignmentFlag
logger = loggings.get_logger(__file__)


# = FUNCTIONS =

class GachaSyncThread(StatefulThread):

    syncStateSignal = Signal(str)

    def __init__(self, api_url='', parent=None):
        super().__init__(parent=parent)
        self.api_url = api_url

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
                str(page), '20',
            )
            logger.debug(f'Requesting {api_url}')
            response, code = service.fetch_json(api_url)
            time.sleep(request_interval)
            _, should_stop, msg = service.check_response(response, code)
            logger.info(f'check_response: {msg}')
            if should_stop:
                break
            data_list = response['data']['list']
            region = response['data']['region']
            timezone = response['data']['region_time_zone']
            metainfo = dict(region=region, region_time_zone=timezone)
            for data_item in data_list:
                data_item.update(metainfo)
            r.extend(data_list)
            end_id = data_list[-1]['id']
        return r

    def work(self):
        self.logAndUpdateState(babelfish.ui_extracting_api_url())
        api_url = self.api_url or service.detect_api_url()
        response, code = service.fetch_json(api_url)
        valid, _, msg = service.check_response(response, code)
        logger.info(f'check_response (api): {msg}')
        if not valid:
            self.failureSignal.emit(babelfish.ui_extract_api_fail())
            raise ValueError(babelfish.ui_extract_api_fail_with_msg(msg))

        api_template = service.get_url_template(api_url)
        record_cache = dict()

        for gacha_type in service.GachaType:
            records = self.exportGachaType(
                api_template,
                gacha_type,
                0.15,
            )
            record_cache[gacha_type.value] = records
            logger.info(f'Finish downloading records of {gacha_type.name}')

        uid = service.deduce_uid(record_cache)
        if not uid:
            logger.critical(
                'Cannot deduce uid from records, there may be no '
                'record. Please check and try again.',
            )
            raise ValueError(babelfish.ui_deduce_uid_fail())
        manager = service.GachaDataManager(uid)
        logger.info(f'Successfully connected to cache of uid {uid}')
        manager.log_stats()

        for gacha_type in service.GachaType:
            manager.add_records(
                gacha_type.value, record_cache[gacha_type.value],
            )
            manager.gacha[gacha_type.value].sort()

        service.fileio.export_as_sql(manager, manager.cache_path)
        manager.log_stats()

        return uid


class RecordImportThread(StatefulThread):

    def __init__(self, path, parent=None):
        super().__init__(parent=parent)
        self.path = path

    def work(self):
        with open(self.path, encoding='utf-8') as f:
            data = json.load(f)
        info = data['info']
        uid = info['uid']
        update_info = dict(
            uid=info['uid'],
            lang=info['lang'],
            region='',  # unused
            region_time_zone=str(info['region_time_zone']),
        )
        record_cache = defaultdict(list)
        for item in data['list']:
            item.update(update_info)
            record_cache[int(item['gacha_type'])].append(item)

        manager = service.GachaDataManager(uid=uid)
        logger.info(f'Successfully connected to cache of uid {uid}')
        manager.log_stats()

        total = 0

        for k, v in record_cache.items():
            manager.add_records(k, v)
            manager.gacha[k].sort()
            total += len(v)

        service.fileio.export_as_sql(manager, manager.cache_path)

        timestamp = info['export_timestamp']
        timestruct = time.localtime(timestamp)
        timestr = time.strftime(babelfish.constants.TIME_FMT, timestruct)
        account_record.update_timestamp(uid, timestr)

        logger.info(f'Successfully load gacha data from {self.path}')
        msg = babelfish.ui_load_success_msg(uid=uid, cnt=total)
        # return msg: {uid: uid, msg: msg}
        return json.dumps(dict(uid=uid, msg=msg), ensure_ascii=False)


class RecordExportThread(StatefulThread):

    def __init__(self, uid, path, parent=None):
        super().__init__(parent=parent)
        self.uid = uid
        self.path = path

    def work(self):
        manager = service.GachaDataManager(self.uid)
        export_hooks = dict(
            csv=service.fileio.export_as_csv,
            html=service.fileio.export_as_html,
            json=service.fileio.export_as_json,
            md=service.fileio.export_as_md,
            srgf=service.fileio.export_as_srgf,
            xlsx=service.fileio.export_as_xlsx,
        )
        timestamp = time.strftime('%Y%m%d%H%M%S')
        for format, hook in export_hooks.items():
            if format == 'srgf':
                format = 'srgf.json'
            filename = f'HKSR-export-{self.uid}-{timestamp}.{format}'
            export_path = os.path.join(self.path, filename)
            hook(manager, export_path)

        return self.path

# = UI =


pie_chart_mapping = {
    GachaType.CHARACTER: [
        (babelfish.ui_5star_character(),  'redLegend',    '#e52f2f'),
        (babelfish.ui_4star_character(),  'orangeLegend', '#e56d2f'),
        (babelfish.ui_4star_light_cone(), 'greenLegend',  '#4ae52f'),
        (babelfish.ui_3star_light_cone(), 'blueLegend',   '#2fa5e5'),
    ],
    GachaType.DEPARTURE: [
        (babelfish.ui_5star_character(),  'redLegend',    '#e52f2f'),
        (babelfish.ui_4star_character(),  'orangeLegend', '#e56d2f'),
        (babelfish.ui_4star_light_cone(), 'greenLegend',  '#4ae52f'),
        (babelfish.ui_3star_light_cone(), 'blueLegend',   '#2fa5e5'),
    ],
    GachaType.LIGHT_CONE: [
        (babelfish.ui_5star_light_cone(), 'purpleLegend', '#b42fe5'),
        (babelfish.ui_4star_character(),  'orangeLegend', '#e56d2f'),
        (babelfish.ui_4star_light_cone(), 'greenLegend',  '#4ae52f'),
        (babelfish.ui_3star_light_cone(), 'blueLegend',   '#2fa5e5'),
    ],
    GachaType.STELLAR: [
        (babelfish.ui_5star_character(),  'redLegend',    '#e52f2f'),
        (babelfish.ui_5star_light_cone(), 'purpleLegend', '#b42fe5'),
        (babelfish.ui_4star_character(),  'orangeLegend', '#e56d2f'),
        (babelfish.ui_4star_light_cone(), 'greenLegend',  '#4ae52f'),
        (babelfish.ui_3star_light_cone(), 'blueLegend',   '#2fa5e5'),
    ],
}


class GachaRecordUI:

    def __init__(self, card: CardWidget, gachaType: GachaType):
        self.card = card
        self.gachaType = gachaType
        self.mapping = pie_chart_mapping[gachaType]

        self.chart = SmartPieChart(title='', showInner=False)
        self.leftChartView = QtCharts.QChartView(
            chart=self.chart,
            parent=self.card,
        )
        self.leftView = QtWidgets.QWidget(parent=self.card)
        self.middleView = QtWidgets.QWidget(parent=self.card)
        self.rightView = QtWidgets.QWidget(parent=self.card)

        self.leftBottomLabel = QLabel(text='', parent=self.card)

        self.middleTopView = QtWidgets.QWidget(parent=self.card)
        self.middleTopView.setObjectName('legend')

        self.infoHBox0 = QtWidgets.QHBoxLayout()
        self.infoLeftLabel0 = QLabel(
            text=babelfish.ui_total_warp(),
            parent=self.card,
        )
        self.infoRightLabel0 = QLabel(text='', parent=self.card)
        self.infoHBox1 = QtWidgets.QHBoxLayout()
        self.infoLeftLabel1 = QLabel(
            text=babelfish.ui_since_last_guarantee(),
            parent=self.card,
        )
        self.infoRightLabel1 = QLabel(text='', parent=self.card)
        self.infoHBox2 = QtWidgets.QHBoxLayout()
        self.infoLeftLabel2 = QLabel(
            text=babelfish.ui_average_warps_per_up(),
            parent=self.card,
        )
        self.infoRightLabel2 = QLabel(text='', parent=self.card)
        self.infoHBox3 = QtWidgets.QHBoxLayout()
        self.infoLeftLabel3 = QLabel(
            text=babelfish.ui_arerage_warps_per_5star(),
            parent=self.card,
        )
        self.infoRightLabel3 = QLabel(text='', parent=self.card)

        self.leftVBox = QVBoxLayout(self.leftView)
        self.middleVBox = QVBoxLayout(self.middleView)
        self.middleTopVBox = QVBoxLayout(self.middleTopView)
        self.middleBottomVBox = QVBoxLayout()
        self.rightFlow = qfw.FlowLayout(self.rightView)

        self.__initLegend()
        self.__initLayout()
        self.__initWidget()

        StyleSheet.apply(StyleSheet.GACHA_RECORD, self.card)

    def __initLegend(self):
        self.legendHBox0 = QtWidgets.QHBoxLayout()
        self.legendHBox1 = QtWidgets.QHBoxLayout()
        self.legendTopLeft = QLabel(
            text=self.mapping[0][0], parent=self.card,
        )
        self.legendTopLeft.setObjectName(self.mapping[0][1])
        self.legendTopRight = QLabel(
            text=self.mapping[1][0], parent=self.card,
        )
        self.legendTopRight.setObjectName(self.mapping[1][1])
        self.legendBottomLeft = QLabel(
            text=self.mapping[2][0], parent=self.card,
        )
        self.legendBottomLeft.setObjectName(self.mapping[2][1])
        self.legendBottomRight = QLabel(
            text=self.mapping[3][0], parent=self.card,
        )
        self.legendBottomRight.setObjectName(self.mapping[3][1])

        if self.gachaType == GachaType.STELLAR:
            self.legendHBox2 = QtWidgets.QHBoxLayout()
            self.legendBottomBottom = QLabel(
                text=self.mapping[4][0], parent=self.card,
            )
            self.legendBottomBottom.setObjectName(self.mapping[4][1])

    def __initLayout(self):
        self.leftChartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.leftChartView.setEnabled(False)
        self.leftBottomLabel.setAlignment(AF.AlignCenter)

        self.middleVBox.setContentsMargins(0, 0, 0, 0)
        self.middleTopVBox.setContentsMargins(0, 0, 0, 0)
        self.middleBottomVBox.setContentsMargins(0, 0, 0, 0)

        self.leftView.setFixedWidth(200)
        self.leftChartView.setFixedHeight(150)
        self.middleView.setFixedWidth(300)
        self.rightView.setFixedHeight(210)

        self.legendTopLeft.setAlignment(AF.AlignCenter)
        self.legendTopLeft.setFixedHeight(30)
        self.legendTopRight.setAlignment(AF.AlignCenter)
        self.legendTopRight.setFixedHeight(30)
        self.legendBottomLeft.setAlignment(AF.AlignCenter)
        self.legendBottomLeft.setFixedHeight(30)
        self.legendBottomRight.setAlignment(AF.AlignCenter)
        self.legendBottomRight.setFixedHeight(30)

        if self.gachaType == GachaType.STELLAR:
            self.legendBottomBottom.setAlignment(AF.AlignCenter)
            self.legendBottomBottom.setFixedHeight(30)

    def __initWidget(self):
        self.card.addWidget(self.leftView)
        self.card.addSpacing(10)
        self.card.addWidget(self.middleView)
        self.card.addSpacing(10)
        self.card.addWidget(self.rightView)

        self.leftVBox.addWidget(self.leftChartView)
        self.leftVBox.addWidget(self.leftBottomLabel)

        self.middleVBox.addWidget(self.middleTopView)
        self.middleTopVBox.addLayout(self.legendHBox0)
        self.middleTopVBox.addLayout(self.legendHBox1)

        self.middleVBox.addLayout(self.middleBottomVBox)
        self.middleBottomVBox.addLayout(self.infoHBox0)
        self.middleBottomVBox.addLayout(self.infoHBox1)
        self.middleBottomVBox.addLayout(self.infoHBox2)
        self.middleBottomVBox.addLayout(self.infoHBox3)

        self.legendHBox0.addWidget(self.legendTopLeft)
        self.legendHBox0.addWidget(self.legendTopRight)
        self.legendHBox1.addWidget(self.legendBottomLeft)
        self.legendHBox1.addWidget(self.legendBottomRight)

        self.infoHBox0.addWidget(self.infoLeftLabel0)
        self.infoHBox0.addStretch(1)
        self.infoHBox0.addWidget(self.infoRightLabel0)
        self.infoHBox1.addWidget(self.infoLeftLabel1)
        self.infoHBox1.addStretch(1)
        self.infoHBox1.addWidget(self.infoRightLabel1)
        self.infoHBox2.addWidget(self.infoLeftLabel2)
        self.infoHBox2.addStretch(1)
        self.infoHBox2.addWidget(self.infoRightLabel2)
        self.infoHBox3.addWidget(self.infoLeftLabel3)
        self.infoHBox3.addStretch(1)
        self.infoHBox3.addWidget(self.infoRightLabel3)

        if self.gachaType == GachaType.STELLAR:
            self.middleTopVBox.addLayout(self.legendHBox2)
            self.legendHBox2.addWidget(self.legendBottomBottom)

    def updateRecord(
        self, character5: int, character4: int, lightCone5: int,
        lightCone4: int, lightCone3: int, total: int,
        sinceLast: int, averageUp: float, average5: float,
        startTime: str, endTime: str, fiveStars: list,
    ):
        m = self.mapping
        self.chart.clear()
        if self.gachaType in [GachaType.CHARACTER, GachaType.DEPARTURE]:
            data = (character5, character4, lightCone4, lightCone3)
        elif self.gachaType == GachaType.LIGHT_CONE:
            data = (lightCone5, character4, lightCone4, lightCone3)
            self.chart.add_slice(m[0][0], lightCone5, m[0][2])
            self.chart.add_slice(m[1][0], character4, m[1][2])
            self.chart.add_slice(m[2][0], lightCone4, m[2][2])
            self.chart.add_slice(m[3][0], lightCone3, m[3][2])
        else:
            data = (character5, lightCone5, character4, lightCone4)
            self.chart.add_slice(m[4][0], lightCone3, m[4][2])
            self.legendBottomBottom.setText(f'{lightCone3}    {m[4][0]}')
        self.chart.add_slice(m[0][0], data[0], m[0][2])
        self.chart.add_slice(m[1][0], data[1], m[1][2])
        self.chart.add_slice(m[2][0], data[2], m[2][2])
        self.chart.add_slice(m[3][0], data[3], m[3][2])
        self.legendTopLeft.setText(f'{data[0]}    {m[0][0]}')
        self.legendTopRight.setText(f'{data[1]}    {m[1][0]}')
        self.legendBottomLeft.setText(f'{data[2]}    {m[2][0]}')
        self.legendBottomRight.setText(f'{data[3]}    {m[3][0]}')
        self.infoRightLabel0.setText(f'{total}')
        self.infoRightLabel1.setText(f'{sinceLast}')
        self.infoRightLabel2.setText(f'{averageUp:.1f}')
        self.infoRightLabel3.setText(f'{average5:.1f}')
        self.leftBottomLabel.setText(f'{startTime}~{endTime}')

        self.rightFlow.removeAllWidgets()
        for name, warps, _ in fiveStars:
            text = f'{name}@{warps}'
            label = QLabel(text=text, parent=self.card)
            self.rightFlow.addWidget(label)


class GachaSyncInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title, subtitle, parent)

        # Buttons
        self.buttonsCard = self.addCard(babelfish.ui_operation_zone())
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
        self.loadButton = qfw.PrimaryPushButton(
            text=babelfish.ui_load_gacha(),
            parent=self,
            icon=Icon.FILE_IMPORT,
        )
        self.loadButton.clicked.connect(self.onLoadButtonClicked)
        self.urlCard = self.addCard(babelfish.ui_customize_url())
        self.urlCheckbox = qfw.CheckBox(
            text=babelfish.ui_use_customize_url(),
            parent=self,
        )
        self.urlCheckbox.stateChanged.connect(self.onCheckboxChanged)
        self.urlLineEdit = qfw.LineEdit(parent=self)
        default_url = 'https://api-takumi.mihoyo.com/common/gacha_record/...'
        self.urlLineEdit.setText(default_url)
        self.urlLineEdit.setDisabled(True)
        self.urlLineEdit.setClearButtonEnabled(False)

        self.__initRecordCards()

        # Gacha Sync Temp Objects
        self.syncThread = None
        self.syncToolTip = None
        self.saveThread = None
        self.loadThread = None

        self.uid = get_latest_uid()
        logger.info(f'Detected current uid: {self.uid}')
        if self.uid:
            self.saveButton.setEnabled(True)
            self.updateRecordDisplay()

        self.__initWidget()

    def __initWidget(self):
        self.buttonsCard.addWidget(self.syncButton)
        self.buttonsCard.addSpacing(10)
        self.buttonsCard.addWidget(self.saveButton)
        self.buttonsCard.addSpacing(10)
        self.buttonsCard.addWidget(self.loadButton)
        self.buttonsCard.addStretch(1)

        self.urlCard.addWidget(self.urlCheckbox)
        self.urlCard.addSpacing(20)  # 10 (from line edit) + 10 (spacing)
        self.urlCard.addWidget(self.urlLineEdit)

    def __initRecordCards(self):
        self.characterCard = self.addResultCard(
            GachaType.CHARACTER,
            babelfish.translate('CHARACTER'),
        )
        self.lightConeCard = self.addResultCard(
            GachaType.LIGHT_CONE,
            babelfish.translate('LIGHT_CONE'),
        )
        self.stellarCard = self.addResultCard(
            GachaType.STELLAR,
            babelfish.translate('STELLAR'),
        )
        self.departureCard = self.addResultCard(
            GachaType.DEPARTURE,
            babelfish.translate('DEPARTURE'),
        )
        self.cardMapping = {
            GachaType.CHARACTER: self.characterCard,
            GachaType.LIGHT_CONE: self.lightConeCard,
            GachaType.STELLAR: self.stellarCard,
            GachaType.DEPARTURE: self.departureCard,
        }

    def addResultCard(self, gachaType, title):
        card = self.addCard(title)
        ui = GachaRecordUI(card, gachaType)
        return ui

    def updateRecordDisplay(self):
        manager = service.GachaDataManager(self.uid)
        for gt in GachaType:
            stats = manager.gacha[gt.value].stats_v2
            self.cardMapping[gt].updateRecord(
                character5=stats['character5'],
                character4=stats['character4'],
                lightCone5=stats['lightcone5'],
                lightCone4=stats['lightcone4'],
                lightCone3=stats['lightcone3'],
                total=stats['total'],
                sinceLast=stats['since_last'],
                averageUp=stats['average_up'],
                average5=stats['average_5'],
                startTime=stats['start_time'],
                endTime=stats['end_time'],
                fiveStars=stats['five_stars'],  # (name, warps, is_up)
            )

    def resizeEvent(self, e):
        if self.syncToolTip:
            self.syncToolTip.move(self.syncToolTip.getSuitablePos())
        return super().resizeEvent(e)

    def disableButtons(self):
        self.syncButton.setDisabled(True)
        self.saveButton.setDisabled(True)
        self.loadButton.setDisabled(True)

    def enableButtons(self):
        self.syncButton.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.loadButton.setEnabled(True)

    # == HOOKS ==

    def updateUidHook(self, uid):
        self.uid = uid
        self.updateRecordDisplay()

    # == SLOTS ==

    def onSyncButtonClicked(self):
        logger.info('[GUI] Start gacha data synchronization')

        self.disableButtons()

        self.syncToolTip = qfw.StateToolTip(
            babelfish.ui_synchronizing_gacha(),
            babelfish.ui_sync_gacha_initial(),
            self.window(),
        )
        self.syncToolTip.move(self.syncToolTip.getSuitablePos())
        self.syncToolTip.show()

        api_url = ''
        if self.urlCheckbox.checkState() == Qt.CheckState.Checked:
            api_url = self.urlLineEdit.text().strip()
        self.syncThread = GachaSyncThread(api_url=api_url, parent=self)
        self.syncThread.syncStateSignal.connect(
            lambda s: self.setToolTipContentSlot(self.syncToolTip, s),
        )
        self.syncThread.successSignal.connect(self.syncSuccessSlot)
        self.syncThread.failureSignal.connect(self.syncFailureSlot)
        self.syncThread.start()

    def onSaveButtonClicked(self):
        logger.info('[GUI] Start gacha data exporting')

        self.disableButtons()

        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Export Folder', os.path.expanduser('~'),
        )
        if path:
            self.saveThread = RecordExportThread(self.uid, path, self)
            self.saveThread.successSignal.connect(self.saveSuccessSlot)
            self.saveThread.failureSignal.connect(self.saveFailureSlot)
            self.saveThread.start()
        else:
            self.enableButtons()

    def onLoadButtonClicked(self):
        logger.info('[GUI] Trying to load gacha data')

        self.disableButtons()

        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select Import File',
            dir=os.path.expanduser('~'),
            filter='JSON Files (*.json);;All Files (*)',
        )
        if path:
            self.loadThread = RecordImportThread(path=path, parent=self)
            self.loadThread.successSignal.connect(self.loadSuccessSlot)
            self.loadThread.failureSignal.connect(self.loadFailureSlot)
            self.loadThread.start()
        else:
            self.enableButtons()

    def onCheckboxChanged(self, status):
        if status == Qt.CheckState.Checked.value:  # enabled
            self.urlLineEdit.setEnabled(True)
            self.urlLineEdit.setClearButtonEnabled(True)
        elif status == Qt.CheckState.Unchecked.value:  # disabled
            self.urlLineEdit.setDisabled(True)
            self.urlLineEdit.setClearButtonEnabled(False)

    def setToolTipContentSlot(self, tooltip: qfw.StateToolTip, content: str):
        tooltip.setContent(content)

    def syncSuccessSlot(self, uid: str):
        logger.info('[GUI] Gacha data synchronization success')

        self.uid = uid
        account_record.update_timestamp(uid)

        self.syncToolTip.setTitle(babelfish.ui_sync_gacha_success())
        self.syncToolTip.setContent('')
        self.syncToolTip.setState(True)
        self.syncToolTip = None
        self.syncThread = None

        self.enableButtons()
        self.updateRecordDisplay()

    def syncFailureSlot(self, message: str):
        logger.info(f'[GUI] Gacha data sync fail with message {message}')

        if self.syncToolTip is not None:
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

        self.enableButtons()

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

        self.enableButtons()

    def saveFailureSlot(self, msg):
        self.saveThread = None

        qfw.InfoBar.error(
            title=babelfish.ui_save_failure(),
            content=msg,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

        self.enableButtons()

    def loadSuccessSlot(self, msg):
        self.loadThread = None
        msg = json.loads(msg)
        self.uid = msg['uid']

        qfw.InfoBar.success(
            title=babelfish.ui_load_success(),
            content=msg['msg'],
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

        self.enableButtons()
        self.updateRecordDisplay()

    def loadFailureSlot(self, msg):
        self.loadThread = None

        qfw.InfoBar.error(
            title=babelfish.ui_load_failure(),
            content=msg,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

        self.enableButtons()
