# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/estimation.ui'
#
# Created: Mon Feb  7 17:51:41 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1100, 714)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_6 = QtGui.QFrame(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 55))
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.frame_6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.exitButton = QtGui.QPushButton(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout_9.addWidget(self.exitButton)
        self.okButton = QtGui.QPushButton(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.okButton.setFont(font)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_9.addWidget(self.okButton)
        self.verticalLayout_3.addWidget(self.frame_6)
        self.label = QtGui.QLabel(Frame)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 10, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.scenariosLabel = QtGui.QLabel(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scenariosLabel.sizePolicy().hasHeightForWidth())
        self.scenariosLabel.setSizePolicy(sizePolicy)
        self.scenariosLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.scenariosLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scenariosLabel.setFont(font)
        self.scenariosLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.scenariosLabel.setObjectName("scenariosLabel")
        self.horizontalLayout_4.addWidget(self.scenariosLabel)
        self.redefButton = QtGui.QPushButton(Frame)
        self.redefButton.setMinimumSize(QtCore.QSize(100, 0))
        self.redefButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.redefButton.setObjectName("redefButton")
        self.horizontalLayout_4.addWidget(self.redefButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 13))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 13))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.nosdEdit = QtGui.QLineEdit(Frame)
        self.nosdEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.nosdEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.nosdEdit.setObjectName("nosdEdit")
        self.gridLayout_2.addWidget(self.nosdEdit, 0, 1, 2, 1)
        self.label_3 = QtGui.QLabel(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 13))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 13))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.groupBox_2 = QtGui.QGroupBox(Frame)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.noRadio = QtGui.QRadioButton(self.groupBox_2)
        self.noRadio.setObjectName("noRadio")
        self.horizontalLayout_2.addWidget(self.noRadio)
        self.logRadio = QtGui.QRadioButton(self.groupBox_2)
        self.logRadio.setObjectName("logRadio")
        self.horizontalLayout_2.addWidget(self.logRadio)
        self.logitRadio = QtGui.QRadioButton(self.groupBox_2)
        self.logitRadio.setChecked(True)
        self.logitRadio.setObjectName("logitRadio")
        self.horizontalLayout_2.addWidget(self.logitRadio)
        self.logtgRadio = QtGui.QRadioButton(self.groupBox_2)
        self.logtgRadio.setObjectName("logtgRadio")
        self.horizontalLayout_2.addWidget(self.logtgRadio)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.line = QtGui.QFrame(Frame)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtGui.QLabel(Frame)
        self.label_7.setMinimumSize(QtCore.QSize(220, 0))
        self.label_7.setMaximumSize(QtCore.QSize(220, 16777215))
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 3)
        self.label_8 = QtGui.QLabel(Frame)
        self.label_8.setMinimumSize(QtCore.QSize(220, 0))
        self.label_8.setMaximumSize(QtCore.QSize(220, 16777215))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 3)
        self.totNumSimEdit = QtGui.QLineEdit(Frame)
        self.totNumSimEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.totNumSimEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.totNumSimEdit.setObjectName("totNumSimEdit")
        self.gridLayout.addWidget(self.totNumSimEdit, 3, 3, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(Frame)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 4, 3, 1, 1)
        self.refTableNameEdit = QtGui.QLineEdit(Frame)
        self.refTableNameEdit.setObjectName("refTableNameEdit")
        self.gridLayout.addWidget(self.refTableNameEdit, 2, 3, 1, 1)
        self.label_6 = QtGui.QLabel(Frame)
        self.label_6.setMinimumSize(QtCore.QSize(220, 0))
        self.label_6.setMaximumSize(QtCore.QSize(220, 16777215))
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.groupBox = QtGui.QGroupBox(Frame)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.oCheck = QtGui.QCheckBox(self.groupBox)
        self.oCheck.setChecked(True)
        self.oCheck.setObjectName("oCheck")
        self.horizontalLayout.addWidget(self.oCheck)
        self.cCheck = QtGui.QCheckBox(self.groupBox)
        self.cCheck.setChecked(True)
        self.cCheck.setObjectName("cCheck")
        self.horizontalLayout.addWidget(self.cCheck)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setToolTip(QtGui.QApplication.translate("Frame", "Leave this screen without loosing any change", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("Frame", "CANCEL", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setShortcut(QtGui.QApplication.translate("Frame", "Alt+E", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setToolTip(QtGui.QApplication.translate("Frame", "Test and save data (Alt+o)", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Frame", "VALIDATE", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("Frame", "Alt+V", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Frame", "ABC parameter estimation", None, QtGui.QApplication.UnicodeUTF8))
        self.scenariosLabel.setText(QtGui.QApplication.translate("Frame", "Chosen scenario :", None, QtGui.QApplication.UnicodeUTF8))
        self.redefButton.setText(QtGui.QApplication.translate("Frame", "Redefine", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Frame", "Number of selected data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Frame", "(simulated data closest to observed)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Frame", "Transformation of parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.noRadio.setText(QtGui.QApplication.translate("Frame", "no", None, QtGui.QApplication.UnicodeUTF8))
        self.logRadio.setText(QtGui.QApplication.translate("Frame", "log", None, QtGui.QApplication.UnicodeUTF8))
        self.logitRadio.setText(QtGui.QApplication.translate("Frame", "logit", None, QtGui.QApplication.UnicodeUTF8))
        self.logtgRadio.setText(QtGui.QApplication.translate("Frame", "log-tg", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Frame", "Total number of simulated data :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Frame", "Chosen number of simulted data : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Frame", "Reference table : ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Frame", "Choice of parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.oCheck.setText(QtGui.QApplication.translate("Frame", "Original", None, QtGui.QApplication.UnicodeUTF8))
        self.cCheck.setText(QtGui.QApplication.translate("Frame", "Composite", None, QtGui.QApplication.UnicodeUTF8))

