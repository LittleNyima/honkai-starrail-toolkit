import json
import re

import qfluentwidgets as qfw
from PySide6 import QtCore, QtGui, QtWidgets

from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.common.thread import StatefulThread
from starrail.gui.interfaces.base import BaseInterface
from starrail.mihoyo import api
from starrail.utils.download import download

AF = QtCore.Qt.AlignmentFlag


class UpdateAnnouncementsThread(StatefulThread):

    annInfoReady = QtCore.Signal(str)

    def work(self):
        content, cache = download(api.announcements, cached=False)
        if not cache:
            raise FileNotFoundError('Download announcements info failed')
        self.annInfoReady.emit(cache)

        content = content.decode('utf-8', errors='ignore')
        content = json.loads(content)
        for item in content['data']['list']:
            download(item['banner'])  # pre-download


def filterHtml(html: str):
    html = html.replace('&lt;t class="t_lc"&gt;', '')
    html = html.replace('&lt;/t&gt;', '')
    return html


class AnnouncementItem(QtWidgets.QListWidgetItem):

    def __init__(self, text, data):
        super().__init__(text)
        self.annData = data


class AnnouncementsInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title=title, subtitle=subtitle, parent=parent)

        self.annView = QtWidgets.QWidget(self)
        self.annList = qfw.ListWidget(self)
        self.annContentView = QtWidgets.QWidget(self)

        self.annHBoxLayout = QtWidgets.QHBoxLayout(self.annView)
        self.rightVBoxLayout = QtWidgets.QVBoxLayout(self.annContentView)

        self.bannerLabel = QtWidgets.QLabel(text='', parent=self)
        self.annTitleLabel = QtWidgets.QLabel(text='', parent=self)
        self.browser = QtWidgets.QTextBrowser(self)
        self.browser.anchorClicked.connect(self.onHrefAnchorClicked)

        self.updateThread = None
        self.urlPattern = re.compile(r'^(https?)://[^\s/$.?#].[^\s]*$')

        self.__initWidget()
        self.__initLayout()

        StyleSheet.ANNOUNCEMENT.apply(self.annView)
        self.updateAnnouncements()

    def __initLayout(self):
        self.annHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.rightVBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.annList.setFixedWidth(400)
        self.bannerLabel.setScaledContents(True)
        self.annTitleLabel.setWordWrap(True)
        self.rightVBoxLayout.setAlignment(AF.AlignHCenter | AF.AlignTop)

    def __initWidget(self):
        self.vBoxLayout.addWidget(self.annView)
        self.annHBoxLayout.addWidget(self.annList)
        self.annHBoxLayout.addWidget(self.annContentView)

        self.rightVBoxLayout.addWidget(self.bannerLabel)
        self.rightVBoxLayout.addWidget(self.annTitleLabel)
        self.rightVBoxLayout.addWidget(self.browser)

        self.annList.itemClicked.connect(self.onListItemClicked)

    def updateAnnouncements(self):
        self.updateThread = UpdateAnnouncementsThread(self)
        self.updateThread.annInfoReady.connect(self.announceInfoReadySlot)
        self.updateThread.start()

    def announceInfoReadySlot(self, path):
        self.annList.clear()

        with open(path, 'rb') as fin:
            info = fin.read().decode('utf-8', errors='ignore')
        info = json.loads(info)

        for item in info['data']['list']:
            listItem = AnnouncementItem(text=item['subtitle'], data=item)
            self.annList.addItem(listItem)

    def onListItemClicked(self, item: AnnouncementItem):
        self.browser.setHtml(filterHtml(item.annData['content']))
        self.annTitleLabel.setText(item.annData['title'])
        if item.annData['banner']:
            data, _ = download(item.annData['banner'])
            pixmap = QtGui.QPixmap()
            success = pixmap.loadFromData(data)
            aspectRatio = pixmap.height() / (pixmap.width() + 1e-6)
            if success:
                self.bannerLabel.setPixmap(pixmap)
                # width = self.browser.width()
                width = self.width() - self.annList.width() - 72
                height = int(width * aspectRatio)
                self.bannerLabel.setFixedSize(width, height)

    def onHrefAnchorClicked(self, qurl: QtCore.QUrl):
        self.browser.setSource(QtCore.QUrl())
        url = qurl.toString()
        jsprefix0 = "javascript:miHoYoGameJSSDK.openInBrowser('"
        jsprefix1 = "javascript:miHoYoGameJSSDK.openInWebview('"
        if re.match(self.urlPattern, url):
            QtGui.QDesktopServices.openUrl(url)
        elif url.startswith(jsprefix0) or url.startswith(jsprefix1):
            url = url[len(jsprefix0):].split("'")[0]
            QtGui.QDesktopServices.openUrl(url)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = self.bannerLabel.pixmap()
        if pixmap is not None and not pixmap.isNull():
            aspectRatio = pixmap.height() / (pixmap.width() + 1e-6)
            newWidth = self.width() - self.annList.width() - 72
            newHeight = int(newWidth * aspectRatio)
            self.bannerLabel.setFixedSize(newWidth, newHeight)
