from typing import List

import qfluentwidgets as qfw
from PySide6 import QtWidgets

from starrail.gui.interfaces.base import BaseInterface
from starrail.utils import babelfish
from starrail.utils.accounts import account_record as ar


class UserItemWidget(QtWidgets.QWidget):

    def __init__(self, uid, users, parent=None):
        super().__init__(parent=parent)
        self.uid = uid
        self.users = users

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.uidLabel = QtWidgets.QLabel(text=uid, parent=self)
        self.selectedLabel = QtWidgets.QLabel(
            text=babelfish.ui_current_account(),
            parent=self,
        )
        self.selectButton = qfw.PrimaryPushButton(
            text=babelfish.ui_switch(),
            parent=self,
        )
        self.selectButton.clicked.connect(self.onSelectButtonClicked)

        self.__initWidget()
        self.__initLayout()

    def __initWidget(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setContentsMargins(0, 5, 0, 5)
        self.hBoxLayout.setSpacing(0)

    def __initLayout(self):
        self.hBoxLayout.addWidget(self.uidLabel)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.selectedLabel)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.selectButton)

    def setSelected(self, selected):
        self.selectButton.setEnabled(not selected)
        self.selectedLabel.setVisible(selected)

    def onSelectButtonClicked(self):
        selectUser(self, self.users)
        ar.latest_uid = self.uid


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

    def addUserItem(self, uid):
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

        self.userCard = self.addCard('User List')
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
