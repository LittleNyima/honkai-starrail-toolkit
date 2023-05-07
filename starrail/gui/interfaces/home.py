from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon, ScrollArea

from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.widgets.link_card import LinkCardView
from starrail.utils import babelfish


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel(babelfish.ui_welcome(), self)
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.BOOK_SHELF,
            babelfish.ui_get_started(),
            babelfish.ui_get_started_desc(),
            babelfish.constants.DOCS_URL,
        )

        self.linkCardView.addCard(
            FluentIcon.HELP,
            babelfish.ui_troubleshooting(),
            babelfish.ui_troubleshooting_desc(),
            'https://www.baidu.com',
        )

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            babelfish.ui_github_repo(),
            babelfish.ui_github_repo_desc(),
            babelfish.constants.REPO_URL,
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            babelfish.ui_send_feedback(),
            babelfish.ui_send_feedback_desc(),
            babelfish.constants.ISSUE_URL,
        )


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
