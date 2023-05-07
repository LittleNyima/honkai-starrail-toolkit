import qfluentwidgets
from PySide6.QtCore import QEasingCurve, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget
from qfluentwidgets import NavigationInterface, NavigationItemPosition
from qframelesswindow import FramelessWindow

from starrail.gui.common.icon import Icon
from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.interfaces.gacha_sync import GachaSyncInterface
from starrail.gui.interfaces.home import HomeInterface
from starrail.gui.interfaces.setting import SettingInterface
from starrail.gui.interfaces.users import UsersInterface
from starrail.gui.widgets.title_bar import CustomTitleBar
from starrail.utils import babelfish


class StackedWidget(QFrame):

    currentWidgetChanged = Signal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = qfluentwidgets.PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)),
        )

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget, popOut=False):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad,
            )

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class StarRailToolkit(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        self.homeInterface = HomeInterface(self)
        self.usersInterface = UsersInterface(
            babelfish.ui_users(),
            babelfish.ui_users_desc(),
            self,
        )
        self.gachaSyncInterface = GachaSyncInterface(
            babelfish.ui_gacha_sync(),
            babelfish.ui_gacha_sync_desc(),
            self,
        )
        self.settingInterface = SettingInterface(self)

        self.initLayout()
        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        # signalBus.switchToSampleCard.connect(self.switchToSample)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_,
        )
        self.titleBar.raise_()

    def initNavigation(self):
        self.addSubInterface(
            self.homeInterface,
            'homeInterface',
            qfluentwidgets.FluentIcon.HOME,
            'Home',
            NavigationItemPosition.TOP,
        )

        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.gachaSyncInterface,
            'gachaSyncInterface',
            qfluentwidgets.FluentIcon.SYNC,
            'Gacha Sync',
            NavigationItemPosition.TOP,
        )

        self.addSubInterface(
            self.usersInterface,
            'usersInterface',
            Icon.USER,
            'Users',
            NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(
            self.settingInterface,
            'settingInterface',
            qfluentwidgets.FluentIcon.SETTING,
            'Settings',
            NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setDefaultRouteKey(
            self.homeInterface.objectName(),
        )
        self.stackWidget.currentWidgetChanged.connect(
            lambda w: self.navigationInterface.setCurrentItem(w.objectName()),
        )
        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName(),
        )
        self.stackWidget.setCurrentIndex(0)

    def addSubInterface(
        self,
        interface: QWidget,
        objectName: str,
        icon,
        text: str,
        position=NavigationItemPosition.SCROLL,
    ):
        """ add sub interface """
        interface.setObjectName(objectName)
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=objectName,
            icon=icon,
            text=text,
            onClick=lambda t: self.switchTo(interface, t),
            position=position,
            tooltip=text,
        )

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def initWindow(self):
        self.resize(960, 640)
        self.setMinimumSize(960, 600)
        self.setWindowIcon(QIcon('resources/images/logo.jpg'))
        self.setWindowTitle(babelfish.ui_title())
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        StyleSheet.STAR_RAIL_TOOLKIT.apply(self)

    def resizeEvent(self, _):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())
