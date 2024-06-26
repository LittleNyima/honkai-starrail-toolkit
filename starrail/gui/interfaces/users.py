import json
import threading
import time
from functools import partial
from typing import Dict, List

import qfluentwidgets as qfw
from PySide6 import QtWidgets
from PySide6.QtGui import QPaintEvent

from starrail.gui.common.thread import StatefulThread
from starrail.gui.interfaces.base import BaseInterface
from starrail.gui.widgets.dialog import (
    DialogMode, MaskDialog, QrcodeLoginDialog,
)
from starrail.mihoyo.client import HoyolabClient
from starrail.mihoyo.qrcode import QrcodeStatus
from starrail.utils import babelfish
from starrail.utils.accounts import account_record as ar


class ConnectToHoyolabThread(StatefulThread):

    def __init__(self, role_id: str, dialog: QrcodeLoginDialog, parent=None):
        super().__init__(parent=parent)
        self.role_id = role_id
        self.dialog = dialog
        self.stop_event = threading.Event()
        self.client = HoyolabClient()

    def work(self):
        try:
            return self._work_impl()
        except Exception as e:
            self.dialog.updateMessageSignal.emit(f'error: {e.args}')
            raise e

    def _work_impl(self):
        qrcode_response = self.client.get_login_qrcode()
        qrcode_url = qrcode_response.pop('url')
        self.dialog.refreshQrcode(qrcode_url)
        status = QrcodeStatus.INITIAL

        while not self.stop_event.is_set():
            check_status = self.client.check_login_qrcode(**qrcode_response)

            if (
                not isinstance(check_status, dict) or
                'message' not in check_status or
                not isinstance(check_status['message'], str) or
                check_status['message'].lower() != 'ok'
            ):  # expired
                qrcode_response = self.client.get_login_qrcode()
                qrcode_url = qrcode_response.pop('url')
                self.dialog.refreshQrcode(qrcode_url)
                status = QrcodeStatus.INITIAL

            elif check_status['data']['stat'] == QrcodeStatus.SCANNED.value:
                if status == QrcodeStatus.INITIAL:
                    self.dialog.updateStatusSignal.emit(QrcodeStatus.SCANNED)
                    status = QrcodeStatus.SCANNED

            elif check_status['data']['stat'] == QrcodeStatus.CONFIRMED.value:
                self.dialog.updateStatusSignal.emit(QrcodeStatus.CONFIRMED)

                raw_payload = check_status['data']['payload']['raw']
                userinfo = self.get_user_info(
                    raw_payload=raw_payload,
                    device_id=qrcode_response['device'],
                )
                if self.bind_user_info(userinfo=userinfo):
                    self.dialog.connectFinishSignal.emit()
                    return json.dumps({'retcode': 0, 'message': 'OK'})
                else:
                    return json.dumps({'retcode': -1, 'message': 'Failed'})

            self.stop_event.wait(2.0)

        return json.dumps({'retcode': 1, 'message': 'canceled'})

    def get_user_info(self, raw_payload: str, device_id: str):
        userinfo = dict()
        userinfo['device_id'] = device_id

        payload = json.loads(raw_payload)
        userinfo['aid'] = payload['uid']
        userinfo['game_token'] = payload['token']

        cookie_token = self.client.get_cookie_token_by_game_token(
            game_token=userinfo['game_token'],
            aid=userinfo['aid'],
            device_id=userinfo['device_id'],
        )
        userinfo['cookie_token'] = cookie_token

        stoken = self.client.get_stoken_by_game_token(
            game_token=userinfo['game_token'],
            aid=userinfo['aid'],
            device_id=userinfo['device_id'],
        )
        userinfo['v2stoken'] = stoken['stoken']
        userinfo['mid'] = stoken['mid']

        return userinfo

    def bind_user_info(self, userinfo: Dict[str, str]):
        game_record = self.client.get_game_record_card(
            cookie_token=userinfo['cookie_token'],
            aid=userinfo['aid'],
            role_id=self.role_id,
            device_id=userinfo['device_id'],
        )

        for record_item in game_record['data']['list']:
            if record_item['game_id'] == 6:
                if record_item['game_role_id'] == self.role_id:
                    ar.set_secrets(self.role_id, userinfo)
                    return True
                else:
                    self.dialog.updateMessageSignal.emit(
                        'Hoyolab account incompatible with game role',
                    )
                    return False

        self.dialog.updateMessageSignal.emit('No starrail role')
        return False


class UserItemWidget(QtWidgets.QWidget):

    def __init__(self, uid: str, users: 'List[UserItemWidget]', parent=None):
        super().__init__(parent=parent)
        self.uid = uid
        self.users = users
        self.userinfo = ar.get_user_properties(self.uid)
        self.infoExpires = time.time() + 1.0

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.topHBoxLayout = QtWidgets.QHBoxLayout()
        self.uidLabel = QtWidgets.QLabel(text=uid, parent=self)
        self.lastUpdateLabel = QtWidgets.QLabel(
            text=babelfish.ui_last_update_at(babelfish.ui_unknown()),
            parent=self,
        )
        self.selectedLabel = QtWidgets.QLabel(
            text=babelfish.ui_current_account(),
            parent=self,
        )
        self.selectButton = qfw.PrimaryPushButton(
            text=babelfish.ui_switch(),
            parent=self,
        )
        self.selectButton.clicked.connect(self.__onSelectButtonClicked)

        self.bottomHBoxLayout = QtWidgets.QHBoxLayout()
        self.hoyolabConnectLabel = QtWidgets.QLabel(
            text=babelfish.ui_hoyolab_connect_status(babelfish.ui_unknown()),
            parent=self,
        )
        self.connectButton = qfw.PrimaryPushButton(
            text=babelfish.ui_connect_to_hoyolab(),
            parent=self,
        )
        self.unconnectButton = qfw.PrimaryPushButton(
            text=babelfish.ui_unconnect_to_hoyolab(),
            parent=self,
        )

        self.connectButton.clicked.connect(self.__onConnectButtonClicked)
        self.unconnectButton.clicked.connect(self.__onUnconnectButtonClicked)

        self.connectToHoyolabThread = None

        self.__initWidget()
        self.__initLayout()
        self.refreshUserInfo(force=True)

    def __initWidget(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(0, 5, 0, 5)
        self.vBoxLayout.setSpacing(0)
        self.topHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topHBoxLayout.setSpacing(0)
        self.bottomHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomHBoxLayout.setSpacing(0)

    def __initLayout(self):
        self.vBoxLayout.addLayout(self.topHBoxLayout)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addLayout(self.bottomHBoxLayout)

        self.topHBoxLayout.addWidget(self.uidLabel)
        self.topHBoxLayout.addSpacing(10)
        self.topHBoxLayout.addWidget(self.lastUpdateLabel)
        self.topHBoxLayout.addSpacing(10)
        self.topHBoxLayout.addWidget(self.selectedLabel)
        self.topHBoxLayout.addStretch(1)
        self.topHBoxLayout.addWidget(self.selectButton)

        self.bottomHBoxLayout.addWidget(self.hoyolabConnectLabel)
        self.bottomHBoxLayout.addStretch(1)
        self.bottomHBoxLayout.addWidget(self.connectButton)
        self.bottomHBoxLayout.addSpacing(10)
        self.bottomHBoxLayout.addWidget(self.unconnectButton)

    @staticmethod
    def convertTimeFmt(timestr: str):
        # %Y-%m-%d_%H:%M:%S -> %Y/%m/%d %H:%M:%S
        return timestr.replace('-', '/').replace('_', ' ')

    def setSelected(self, selected: bool):
        self.selectButton.setEnabled(not selected)
        self.selectedLabel.setVisible(selected)
        for idx in range(self.bottomHBoxLayout.count()):
            w = self.bottomHBoxLayout.itemAt(idx).widget()
            if w:
                w.setVisible(selected)

    def refreshUserInfo(self, force: bool = False):
        if force or time.time() > self.infoExpires:
            userinfo = ar.get_user_properties(self.uid)
            if force or userinfo.last_update != self.userinfo.last_update:
                self.lastUpdateLabel.setText(
                    babelfish.ui_last_update_at(
                        self.convertTimeFmt(
                            userinfo.last_update,
                        ),
                    ),
                )
            if force or userinfo.iv != self.userinfo.iv:
                if userinfo.iv:  # connected
                    self.hoyolabConnectLabel.setText(
                        babelfish.ui_hoyolab_connect_status(
                            babelfish.ui_connected(),
                        ),
                    )
                    self.connectButton.setEnabled(False)
                    self.unconnectButton.setEnabled(True)
                else:  # not connected
                    self.hoyolabConnectLabel.setText(
                        babelfish.ui_hoyolab_connect_status(
                            babelfish.ui_not_connected(),
                        ),
                    )
                    self.connectButton.setEnabled(True)
                    self.unconnectButton.setEnabled(False)
            self.userinfo = userinfo
            self.infoExpires = time.time() + 1.0

    def __onSelectButtonClicked(self):
        selectUser(self, self.users)
        ar.latest_uid = self.uid

    def __onConnectButtonClicked(self):
        dialog = QrcodeLoginDialog(parent=self.window())

        self.connectToHoyolabThread = ConnectToHoyolabThread(
            self.uid,
            dialog,
            self,
        )
        self.connectToHoyolabThread.start()

        dialog.worker = self.connectToHoyolabThread

        dialog.show()
        dialog.raise_()

    def __onUnconnectButtonClicked(self):
        dialog = MaskDialog(
            babelfish.ui_hoyolab_unconnect_title(),
            babelfish.ui_hoyolab_unconnect_msg(),
            mode=DialogMode.DANGEROUS_OK_CANCEL,
            parent=self.window(),
        )

        dialog.okSignal.connect(partial(ar.unset_secrets, self.uid))

        dialog.show()
        dialog.raise_()

    def paintEvent(self, event: QPaintEvent):
        self.refreshUserInfo()
        super().paintEvent(event)


def selectUser(select: UserItemWidget, users: List[UserItemWidget]):
    for user in users:
        user.setSelected(user is select)


class UserListWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        self.users = []

    def addUserItem(self, uid: str):
        userItem = UserItemWidget(uid=uid, users=self.users, parent=self)
        self.vBoxLayout.addWidget(userItem)
        self.users.append(userItem)
        return userItem

    def clear(self):
        for user in self.users:
            self.vBoxLayout.removeWidget(user)
        self.users.clear()


class UsersInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title, subtitle, parent)

        self.userCard = self.addCard(babelfish.ui_user_list())
        self.userList = UserListWidget(self)
        self.userCard.addWidget(self.userList)

        self.updateUserList()

    def updateUserList(self):
        self.userList.clear()
        latest = ar.latest_uid
        latestItem = None
        for account in ar.accounts:
            item = self.userList.addUserItem(account)
            if account == latest:
                latestItem = item
        selectUser(latestItem, self.userList.users)
