# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/defineAnalysis.ui'
#
# Created: Wed Feb  2 11:54:40 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1142, 704)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
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
        self.verticalLayout_2.addWidget(self.frame_6)
        self.label = QtGui.QLabel(Frame)
        self.label.setMinimumSize(QtCore.QSize(0, 100))
        self.label.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 80))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 80))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.groupBox = QtGui.QGroupBox(Frame)
        self.groupBox.setMinimumSize(QtCore.QSize(600, 300))
        self.groupBox.setMaximumSize(QtCore.QSize(600, 300))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setMinimumSize(QtCore.QSize(0, 30))
        self.radioButton_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_3.addWidget(self.radioButton_2)
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_3.setMinimumSize(QtCore.QSize(0, 35))
        self.radioButton_3.setMaximumSize(QtCore.QSize(16777215, 35))
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_3.addWidget(self.radioButton_3)
        self.radioButton_4 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_4.setMinimumSize(QtCore.QSize(0, 35))
        self.radioButton_4.setMaximumSize(QtCore.QSize(16777215, 35))
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout_3.addWidget(self.radioButton_4)
        self.radioButton_5 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_5.setMinimumSize(QtCore.QSize(0, 35))
        self.radioButton_5.setMaximumSize(QtCore.QSize(16777215, 35))
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout_3.addWidget(self.radioButton_5)
        self.horizontalLayout_2.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

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
        self.label.setText(QtGui.QApplication.translate("Frame", "CHOOSE AN ANALYSIS", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Frame", "The reference table...\n"
"Each record includes 2 parameters\n"
"The reference table has been built", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Frame", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("Frame", "Pre-evaluate scenario-prior combinations", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("Frame", "Principal Component Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Frame", "Locate observed S.S among simulated S.S.", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("Frame", "Estimate posterior distributions of parameters and model checking", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setText(QtGui.QApplication.translate("Frame", "Compute bias and precision on parameter estimations", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_4.setText(QtGui.QApplication.translate("Frame", "Compute posterior probabilities of scenarios", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_5.setText(QtGui.QApplication.translate("Frame", "Evaluate confidence in scenario choice", None, QtGui.QApplication.UnicodeUTF8))
