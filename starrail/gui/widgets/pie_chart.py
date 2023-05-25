import qfluentwidgets as qfw
from PySide6 import QtCharts, QtCore, QtGui
from PySide6.QtCharts import QChart


# Moified from:
# https://github.com/leixingyu/guiUtil/blob/master/template/pieChart.py
class SmartPieChart(QChart):

    def __init__(self, title, showInner=True, parent=None):
        super().__init__(parent=parent)
        self.offset = 140

        self.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.legend().hide()
        self.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        Color = QtCore.Qt.GlobalColor
        fgColor = Color.white if qfw.isDarkTheme() else Color.black
        self.setTitle(title)
        self.setTitleBrush(QtGui.QBrush(fgColor))
        self.setBackgroundBrush(QtGui.QBrush(Color.transparent))

        self.__outer = QtCharts.QPieSeries()
        self.__outer.setHoleSize(0.35)
        self.__outer.setPieStartAngle(self.offset)
        self.__outer.setPieEndAngle(self.offset + 360)

        self.__inner = QtCharts.QPieSeries()
        self.__inner.setPieSize(0.35)
        self.__inner.setHoleSize(0.3)
        self.__inner.setPieStartAngle(self.offset)
        self.__inner.setPieEndAngle(self.offset + 360)

        self.addSeries(self.__outer)
        if showInner:
            self.addSeries(self.__inner)

    def clear(self):
        for slice in self.__outer.slices():
            self.__outer.take(slice)
        for slice in self.__inner.slices():
            self.__inner.take(slice)

    def take_by_label(self, label):
        for slice in self.__outer.slices():
            if slice.label() == label:
                self.__outer.take(slice)
        for slice in self.__inner.slices():
            if slice.label() == label:
                self.__inner.take(slice)

    def add_slice(self, name, value, color):
        outerSlice = QtCharts.QPieSlice(name, value)
        outerSlice.setColor(QtGui.QColor(color))
        outerSlice.setLabelBrush(QtGui.QColor(color))
        outerSlice.hovered.connect(
            lambda isHovered: self.__explode(outerSlice, isHovered),
        )
        self.__outer.append(outerSlice)

        innerColor = QtGui.QColor(color)
        innerSlice = QtCharts.QPieSlice(name, value)
        innerSlice.setColor(innerColor)
        innerSlice.setBorderColor(innerColor)
        self.__inner.append(innerSlice)

    def __explode(self, slice: QtCharts.QPieSlice, is_hovered: bool):
        if is_hovered:
            start = slice.startAngle()
            end = slice.startAngle() + slice.angleSpan()
            self.__inner.setPieStartAngle(end)
            self.__inner.setPieEndAngle(start + 360)
        else:
            self.__inner.setPieStartAngle(self.offset)
            self.__inner.setPieEndAngle(self.offset + 360)
        slice.setExplodeDistanceFactor(0.1)
        slice.setExploded(is_hovered)
