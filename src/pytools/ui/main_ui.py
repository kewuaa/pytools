# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

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
        self.widget_2 = QWidget(self.ocr_tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setAutoFillBackground(True)
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.from_file_button = QPushButton(self.widget_2)
        self.from_file_button.setObjectName(u"from_file_button")

        self.horizontalLayout_3.addWidget(self.from_file_button)

        self.from_clipboard_button = QPushButton(self.widget_2)
        self.from_clipboard_button.setObjectName(u"from_clipboard_button")

        self.horizontalLayout_3.addWidget(self.from_clipboard_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.result_textbrowser = QTextBrowser(self.widget_2)
        self.result_textbrowser.setObjectName(u"result_textbrowser")
        self.result_textbrowser.setMinimumSize(QSize(371, 261))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.result_textbrowser.setFont(font2)
        self.result_textbrowser.setUndoRedoEnabled(True)
        self.result_textbrowser.setReadOnly(False)

        self.horizontalLayout_4.addWidget(self.result_textbrowser)

        self.copy_button = QPushButton(self.widget_2)
        self.copy_button.setObjectName(u"copy_button")

        self.horizontalLayout_4.addWidget(self.copy_button, 0, Qt.AlignBottom)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.tabWidget.addTab(self.ocr_tab, "")
        self.transform_teb = QWidget()
        self.transform_teb.setObjectName(u"transform_teb")
        self.verticalLayout = QVBoxLayout(self.transform_teb)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.transform_teb)
        self.widget.setObjectName(u"widget")
        self.widget.setAutoFillBackground(True)
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.transform_button = QPushButton(self.widget)
        self.transform_button.setObjectName(u"transform_button")

        self.horizontalLayout.addWidget(self.transform_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 4)

        self.pdf2img_radioButton = QRadioButton(self.widget)
        self.pdf2img_radioButton.setObjectName(u"pdf2img_radioButton")

        self.gridLayout_2.addWidget(self.pdf2img_radioButton, 1, 0, 1, 1)

        self.docx2pdf_radioButton = QRadioButton(self.widget)
        self.docx2pdf_radioButton.setObjectName(u"docx2pdf_radioButton")

        self.gridLayout_2.addWidget(self.docx2pdf_radioButton, 1, 3, 1, 1)

        self.img2pdf_radioButton = QRadioButton(self.widget)
        self.img2pdf_radioButton.setObjectName(u"img2pdf_radioButton")

        self.gridLayout_2.addWidget(self.img2pdf_radioButton, 1, 2, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)

        self.pdf2docx_radioButton = QRadioButton(self.widget)
        self.pdf2docx_radioButton.setObjectName(u"pdf2docx_radioButton")

        self.gridLayout_2.addWidget(self.pdf2docx_radioButton, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget)

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
        self.transform_button.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362", None))
        self.pdf2img_radioButton.setText(QCoreApplication.translate("MainWindow", u"pdf -> image", None))
        self.docx2pdf_radioButton.setText(QCoreApplication.translate("MainWindow", u"docx -> pdf", None))
        self.img2pdf_radioButton.setText(QCoreApplication.translate("MainWindow", u"image -> pdf", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6b22\u8fce", None))
        self.pdf2docx_radioButton.setText(QCoreApplication.translate("MainWindow", u"pdf -> docx", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.transform_teb), QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u8f6c\u6362", None))
    # retranslateUi

