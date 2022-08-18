# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 827)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(830, 20, 271, 751))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_log = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_log.setObjectName("label_log")
        self.verticalLayout.addWidget(self.label_log)
        self.textBrowser_log = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.verticalLayout.addWidget(self.textBrowser_log)
        self.label_rece = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_rece.setObjectName("label_rece")
        self.verticalLayout.addWidget(self.label_rece)
        self.textBrowser_rece = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser_rece.setObjectName("textBrowser_rece")
        self.verticalLayout.addWidget(self.textBrowser_rece)
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(30, 100, 781, 671))
        self.label_image.setObjectName("label_image")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(47, 20, 131, 51))
        self.label.setObjectName("label")
        self.label_car = QtWidgets.QLabel(self.centralwidget)
        self.label_car.setGeometry(QtCore.QRect(0, 0, 60, 42))
        self.label_car.setPixmap(QPixmap("img_resource/2.jpeg"))
        self.label_car.setScaledContents(True)
        self.label_car.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "加密沙盘"))
        self.label_log.setText(_translate("MainWindow", "日志:"))
        self.label_rece.setText(_translate("MainWindow", "接收区:"))
        self.label_image.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "实时预览:"))

