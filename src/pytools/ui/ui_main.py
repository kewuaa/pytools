# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainqIakdQ.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(578, 517)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.ocr_tab = QWidget()
        self.ocr_tab.setObjectName(u"ocr_tab")
        self.verticalLayout_2 = QVBoxLayout(self.ocr_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.ocr_tab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.from_file_button = QPushButton(self.frame_2)
        self.from_file_button.setObjectName(u"from_file_button")

        self.horizontalLayout_3.addWidget(self.from_file_button)

        self.from_clipboard_button = QPushButton(self.frame_2)
        self.from_clipboard_button.setObjectName(u"from_clipboard_button")

        self.horizontalLayout_3.addWidget(self.from_clipboard_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.result_textbrowser = QTextBrowser(self.frame_2)
        self.result_textbrowser.setObjectName(u"result_textbrowser")
        self.result_textbrowser.setMinimumSize(QSize(371, 261))

        self.horizontalLayout_4.addWidget(self.result_textbrowser)

        self.copy_button = QPushButton(self.frame_2)
        self.copy_button.setObjectName(u"copy_button")

        self.horizontalLayout_4.addWidget(self.copy_button, 0, Qt.AlignBottom)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.tabWidget.addTab(self.ocr_tab, "")
        self.transform_teb = QWidget()
        self.transform_teb.setObjectName(u"transform_teb")
        self.verticalLayout = QVBoxLayout(self.transform_teb)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.transform_teb)
        self.frame.setObjectName(u"frame")
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.task_listwidget = QListWidget(self.frame)
        self.task_listwidget.setObjectName(u"task_listwidget")

        self.horizontalLayout_2.addWidget(self.task_listwidget)

        self.run_button = QPushButton(self.frame)
        self.run_button.setObjectName(u"run_button")

        self.horizontalLayout_2.addWidget(self.run_button, 0, Qt.AlignBottom)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.file_choose_button = QPushButton(self.frame)
        self.file_choose_button.setObjectName(u"file_choose_button")

        self.horizontalLayout.addWidget(self.file_choose_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.tabWidget.addTab(self.transform_teb, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 578, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PyTools", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6b22\u8fce", None))
        self.from_file_button.setText(QCoreApplication.translate("MainWindow", u"\u4ece\u6587\u4ef6", None))
        self.from_clipboard_button.setText(QCoreApplication.translate("MainWindow", u"\u4ece\u526a\u5207\u677f", None))
        self.copy_button.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u5230\u526a\u5207\u677f", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ocr_tab), QCoreApplication.translate("MainWindow", u"OCR", None))
        self.run_button.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.file_choose_button.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u9009\u62e9", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6b22\u8fce", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.transform_teb), QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u8f6c\u6362", None))
    # retranslateUi

