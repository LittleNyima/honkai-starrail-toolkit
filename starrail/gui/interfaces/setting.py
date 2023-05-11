from functools import partial

import qfluentwidgets as qfw
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QWidget
from qfluentwidgets import FluentIcon

from starrail import __version__
from starrail.gui.common.config import qcfg
from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.common.utils import checkUpdate
from starrail.utils import babelfish


class SettingInterface(qfw.ScrollArea):

    checkUpdateSig = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = qfw.ExpandLayout(self.scrollWidget)

        self.settingLabel = QLabel(babelfish.ui_settings(), self)

        self.personalGroup = qfw.SettingCardGroup(
            babelfish.ui_personalization(), self.scrollWidget,
        )
        self.themeModeCard = qfw.OptionsSettingCard(
            qcfg.themeMode,
            FluentIcon.BRUSH,
            babelfish.ui_theme_mode(),
            babelfish.ui_theme_mode_settings_desc(),
            [
                babelfish.ui_theme_mode_light(),
                babelfish.ui_theme_mode_dark(),
                babelfish.ui_theme_mode_auto(),
            ],
            self.personalGroup,
        )

        self.aboutGroup = qfw.SettingCardGroup(
            babelfish.ui_about(), self.scrollWidget,
        )
        self.getStartCard = qfw.HyperlinkCard(
            babelfish.constants.DOCS_URL,
            babelfish.ui_open_docs(),
            FluentIcon.BOOK_SHELF,
            babelfish.ui_get_started(),
            babelfish.ui_get_started_desc(),
            self.aboutGroup,
        )
        self.troubleshootingCard = qfw.HyperlinkCard(
            babelfish.constants.TROUBLESHOOTING_URL,
            babelfish.ui_open_troubleshooting(),
            FluentIcon.HELP,
            babelfish.ui_troubleshooting(),
            babelfish.ui_troubleshooting_desc(),
            self.aboutGroup,
        )
        self.openSourceCard = qfw.HyperlinkCard(
            babelfish.constants.REPO_URL,
            babelfish.ui_open_repo(),
            FluentIcon.GITHUB,
            babelfish.ui_github_repo(),
            babelfish.ui_github_repo_desc(),
            self.aboutGroup,
        )
        self.feedbackCard = qfw.HyperlinkCard(
            babelfish.constants.ISSUE_URL,
            babelfish.ui_open_issues(),
            FluentIcon.FEEDBACK,
            babelfish.ui_send_feedback(),
            babelfish.ui_send_feedback_desc(),
            self.aboutGroup,
        )
        self.aboutCard = qfw.PrimaryPushSettingCard(
            babelfish.ui_check_update(),
            FluentIcon.INFO,
            babelfish.ui_about_this(),
            (
                f'{babelfish.ui_copyright(2023)} '
                f'{babelfish.ui_current_version(__version__)}'
            ),
            self.aboutGroup,
        )
        self.aboutCard.button.clicked.connect(
            partial(checkUpdate, parent=self.parent()),
        )

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.resize(1000, 800)
        SBP = Qt.ScrollBarPolicy
        self.setHorizontalScrollBarPolicy(SBP.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.personalGroup.addSettingCard(self.themeModeCard)

        self.aboutGroup.addSettingCard(self.getStartCard)
        self.aboutGroup.addSettingCard(self.troubleshootingCard)
        self.aboutGroup.addSettingCard(self.openSourceCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __connectSignalToSlot(self):
        qfw.qconfig.themeChanged.connect(qfw.setTheme)
