# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/Project.ui'
#
# Created: Fri Apr  8 14:02:57 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName(_fromUtf8("TabWidget"))
        TabWidget.resize(975, 810)
        self.tabRefTable = QtGui.QWidget()
        self.tabRefTable.setObjectName(_fromUtf8("tabRefTable"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabRefTable)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.refTableStack = QtGui.QStackedWidget(self.tabRefTable)
        self.refTableStack.setObjectName(_fromUtf8("refTableStack"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.verticalLayout = QtGui.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalFrame = QtGui.QFrame(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy)
        self.horizontalFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.horizontalFrame.setObjectName(_fromUtf8("horizontalFrame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.horizontalFrame)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.projNameLabel = QtGui.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.projNameLabel.setFont(font)
        self.projNameLabel.setObjectName(_fromUtf8("projNameLabel"))
        self.gridLayout_4.addWidget(self.projNameLabel, 0, 0, 1, 1)
        self.projNameLabelValue = QtGui.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.projNameLabelValue.setFont(font)
        self.projNameLabelValue.setFrameShape(QtGui.QFrame.Box)
        self.projNameLabelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.projNameLabelValue.setObjectName(_fromUtf8("projNameLabelValue"))
        self.gridLayout_4.addWidget(self.projNameLabelValue, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.horizontalFrame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.browseDataFileButton = QtGui.QPushButton(self.horizontalFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browseDataFileButton.sizePolicy().hasHeightForWidth())
        self.browseDataFileButton.setSizePolicy(sizePolicy)
        self.browseDataFileButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.browseDataFileButton.setObjectName(_fromUtf8("browseDataFileButton"))
        self.gridLayout_4.addWidget(self.browseDataFileButton, 1, 1, 1, 1)
        self.dataFileEdit = QtGui.QLineEdit(self.horizontalFrame)
        self.dataFileEdit.setObjectName(_fromUtf8("dataFileEdit"))
        self.gridLayout_4.addWidget(self.dataFileEdit, 1, 2, 1, 1)
        self.dirEdit = QtGui.QLineEdit(self.horizontalFrame)
        self.dirEdit.setObjectName(_fromUtf8("dirEdit"))
        self.gridLayout_4.addWidget(self.dirEdit, 0, 5, 1, 1)
        self.browseDirButton = QtGui.QPushButton(self.horizontalFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browseDirButton.sizePolicy().hasHeightForWidth())
        self.browseDirButton.setSizePolicy(sizePolicy)
        self.browseDirButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.browseDirButton.setObjectName(_fromUtf8("browseDirButton"))
        self.gridLayout_4.addWidget(self.browseDirButton, 0, 4, 1, 1)
        self.label = QtGui.QLabel(self.horizontalFrame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 0, 3, 1, 1)
        self.dataFileInfoLabel = QtGui.QLabel(self.horizontalFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataFileInfoLabel.sizePolicy().hasHeightForWidth())
        self.dataFileInfoLabel.setSizePolicy(sizePolicy)
        self.dataFileInfoLabel.setMinimumSize(QtCore.QSize(0, 40))
        self.dataFileInfoLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.dataFileInfoLabel.setText(_fromUtf8(""))
        self.dataFileInfoLabel.setObjectName(_fromUtf8("dataFileInfoLabel"))
        self.gridLayout_4.addWidget(self.dataFileInfoLabel, 1, 5, 1, 1)
        self.label_10 = QtGui.QLabel(self.horizontalFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(0, 20))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.horizontalFrame)
        self.groupBox = QtGui.QGroupBox(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(541, 0))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox_7 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_7.setTitle(_fromUtf8(""))
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.gridLayout_10 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.label_19 = QtGui.QLabel(self.groupBox_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QtCore.QSize(0, 25))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_10.addWidget(self.label_19, 0, 0, 1, 1)
        self.setHistoricalButton = QtGui.QPushButton(self.groupBox_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setHistoricalButton.sizePolicy().hasHeightForWidth())
        self.setHistoricalButton.setSizePolicy(sizePolicy)
        self.setHistoricalButton.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setHistoricalButton.setFont(font)
        self.setHistoricalButton.setIconSize(QtCore.QSize(50, 50))
        self.setHistoricalButton.setObjectName(_fromUtf8("setHistoricalButton"))
        self.gridLayout_10.addWidget(self.setHistoricalButton, 2, 0, 1, 1)
        self.frame = QtGui.QFrame(self.groupBox_7)
        self.frame.setFrameShape(QtGui.QFrame.HLine)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_10.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_5 = QtGui.QFrame(self.groupBox_7)
        self.frame_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.nbScLabel = QtGui.QLabel(self.frame_5)
        self.nbScLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nbScLabel.setObjectName(_fromUtf8("nbScLabel"))
        self.horizontalLayout.addWidget(self.nbScLabel)
        self.nbParamLabel = QtGui.QLabel(self.frame_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nbParamLabel.sizePolicy().hasHeightForWidth())
        self.nbParamLabel.setSizePolicy(sizePolicy)
        self.nbParamLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nbParamLabel.setObjectName(_fromUtf8("nbParamLabel"))
        self.horizontalLayout.addWidget(self.nbParamLabel)
        self.gridLayout_10.addWidget(self.frame_5, 3, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_7)
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_6.setAutoFillBackground(False)
        self.groupBox_6.setTitle(_fromUtf8(""))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.label_15 = QtGui.QLabel(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(0, 25))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_8.addWidget(self.label_15, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(self.groupBox_6)
        self.frame_2.setFrameShape(QtGui.QFrame.HLine)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_8.addWidget(self.frame_2, 1, 0, 1, 1)
        self.setGeneticButton = QtGui.QPushButton(self.groupBox_6)
        self.setGeneticButton.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setGeneticButton.setFont(font)
        self.setGeneticButton.setIconSize(QtCore.QSize(50, 50))
        self.setGeneticButton.setObjectName(_fromUtf8("setGeneticButton"))
        self.gridLayout_8.addWidget(self.setGeneticButton, 2, 0, 1, 1)
        self.frame_6 = QtGui.QFrame(self.groupBox_6)
        self.frame_6.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frame_6)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.nbMicrosatLabel = QtGui.QLabel(self.frame_6)
        self.nbMicrosatLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nbMicrosatLabel.setObjectName(_fromUtf8("nbMicrosatLabel"))
        self.gridLayout_5.addWidget(self.nbMicrosatLabel, 0, 0, 1, 1)
        self.nbSequencesLabel = QtGui.QLabel(self.frame_6)
        self.nbSequencesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nbSequencesLabel.setObjectName(_fromUtf8("nbSequencesLabel"))
        self.gridLayout_5.addWidget(self.nbSequencesLabel, 0, 1, 1, 1)
        self.nbGroupLabel = QtGui.QLabel(self.frame_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nbGroupLabel.sizePolicy().hasHeightForWidth())
        self.nbGroupLabel.setSizePolicy(sizePolicy)
        self.nbGroupLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.nbGroupLabel.setBaseSize(QtCore.QSize(0, 0))
        self.nbGroupLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nbGroupLabel.setObjectName(_fromUtf8("nbGroupLabel"))
        self.gridLayout_5.addWidget(self.nbGroupLabel, 1, 0, 1, 1)
        self.nbSumStatsLabel = QtGui.QLabel(self.frame_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nbSumStatsLabel.sizePolicy().hasHeightForWidth())
        self.nbSumStatsLabel.setSizePolicy(sizePolicy)
        self.nbSumStatsLabel.setMinimumSize(QtCore.QSize(0, 80))
        self.nbSumStatsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nbSumStatsLabel.setObjectName(_fromUtf8("nbSumStatsLabel"))
        self.gridLayout_5.addWidget(self.nbSumStatsLabel, 1, 1, 1, 1)
        self.gridLayout_8.addWidget(self.frame_6, 3, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.groupBox_8 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_8.setTitle(_fromUtf8(""))
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.gridLayout_11 = QtGui.QGridLayout(self.groupBox_8)
        self.gridLayout_11.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.label_20 = QtGui.QLabel(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_11.addWidget(self.label_20, 0, 0, 1, 1)
        self.frame_4 = QtGui.QFrame(self.groupBox_8)
        self.frame_4.setFrameShape(QtGui.QFrame.HLine)
        self.frame_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.gridLayout_11.addWidget(self.frame_4, 1, 0, 1, 1)
        self.frame_8 = QtGui.QFrame(self.groupBox_8)
        self.frame_8.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_8.setObjectName(_fromUtf8("frame_8"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_8)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_8 = QtGui.QLabel(self.frame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 40))
        self.label_8.setMaximumSize(QtCore.QSize(200, 40))
        self.label_8.setTextFormat(QtCore.Qt.AutoText)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.frame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 40))
        self.label_9.setMaximumSize(QtCore.QSize(200, 40))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.nbSetsReqEdit = QtGui.QLineEdit(self.frame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nbSetsReqEdit.sizePolicy().hasHeightForWidth())
        self.nbSetsReqEdit.setSizePolicy(sizePolicy)
        self.nbSetsReqEdit.setMinimumSize(QtCore.QSize(0, 26))
        self.nbSetsReqEdit.setMaximumSize(QtCore.QSize(120, 26))
        self.nbSetsReqEdit.setObjectName(_fromUtf8("nbSetsReqEdit"))
        self.gridLayout.addWidget(self.nbSetsReqEdit, 2, 2, 1, 1)
        self.nbSetsDoneEdit = QtGui.QLineEdit(self.frame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nbSetsDoneEdit.sizePolicy().hasHeightForWidth())
        self.nbSetsDoneEdit.setSizePolicy(sizePolicy)
        self.nbSetsDoneEdit.setMinimumSize(QtCore.QSize(0, 26))
        self.nbSetsDoneEdit.setMaximumSize(QtCore.QSize(120, 26))
        self.nbSetsDoneEdit.setReadOnly(True)
        self.nbSetsDoneEdit.setObjectName(_fromUtf8("nbSetsDoneEdit"))
        self.gridLayout.addWidget(self.nbSetsDoneEdit, 3, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.gridLayout_11.addWidget(self.frame_8, 2, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 25))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_11.addWidget(self.progressBar, 3, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(self.groupBox_8)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setMargin(1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.progressLabel = QtGui.QLabel(self.frame_3)
        self.progressLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.progressLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.progressLabel.setText(_fromUtf8(""))
        self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.horizontalLayout_3.addWidget(self.progressLabel)
        self.runButton = QtGui.QPushButton(self.frame_3)
        self.runButton.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.runButton.setFont(font)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.horizontalLayout_3.addWidget(self.runButton)
        self.stopButton = QtGui.QPushButton(self.frame_3)
        self.stopButton.setMinimumSize(QtCore.QSize(60, 50))
        self.stopButton.setMaximumSize(QtCore.QSize(60, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.stopButton.setFont(font)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.horizontalLayout_3.addWidget(self.stopButton)
        self.gridLayout_11.addWidget(self.frame_3, 4, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_8)
        self.verticalLayout.addWidget(self.groupBox)
        self.refTableStack.addWidget(self.page)
        self.verticalLayout_5.addWidget(self.refTableStack)
        TabWidget.addTab(self.tabRefTable, _fromUtf8(""))
        self.tabAnalyses = QtGui.QWidget()
        self.tabAnalyses.setObjectName(_fromUtf8("tabAnalyses"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tabAnalyses)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.analysisStack = QtGui.QStackedWidget(self.tabAnalyses)
        self.analysisStack.setObjectName(_fromUtf8("analysisStack"))
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.page_2)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tableWidget = QtGui.QTableWidget(self.page_2)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.frame_9 = QtGui.QFrame(self.page_2)
        self.frame_9.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_9.setObjectName(_fromUtf8("frame_9"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_17 = QtGui.QLabel(self.frame_9)
        self.label_17.setMinimumSize(QtCore.QSize(50, 0))
        self.label_17.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_17.setText(_fromUtf8(""))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_4.addWidget(self.label_17)
        self.label_16 = QtGui.QLabel(self.frame_9)
        self.label_16.setMinimumSize(QtCore.QSize(50, 0))
        self.label_16.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_16.setText(_fromUtf8(""))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_4.addWidget(self.label_16)
        self.label_13 = QtGui.QLabel(self.frame_9)
        self.label_13.setMinimumSize(QtCore.QSize(100, 0))
        self.label_13.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_4.addWidget(self.label_13)
        self.label_12 = QtGui.QLabel(self.frame_9)
        self.label_12.setMinimumSize(QtCore.QSize(200, 0))
        self.label_12.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_4.addWidget(self.label_12)
        self.label_11 = QtGui.QLabel(self.frame_9)
        self.label_11.setMinimumSize(QtCore.QSize(200, 0))
        self.label_11.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_4.addWidget(self.label_11)
        self.label_14 = QtGui.QLabel(self.frame_9)
        self.label_14.setMinimumSize(QtCore.QSize(40, 0))
        self.label_14.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_4.addWidget(self.label_14)
        self.label_18 = QtGui.QLabel(self.frame_9)
        self.label_18.setMinimumSize(QtCore.QSize(70, 0))
        self.label_18.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_18.setText(_fromUtf8(""))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_4.addWidget(self.label_18)
        self.verticalLayout_2.addWidget(self.frame_9)
        self.scrollArea = QtGui.QScrollArea(self.page_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 929, 264))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_9.setSpacing(1)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.newAnButton = QtGui.QPushButton(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newAnButton.sizePolicy().hasHeightForWidth())
        self.newAnButton.setSizePolicy(sizePolicy)
        self.newAnButton.setMinimumSize(QtCore.QSize(581, 101))
        self.newAnButton.setBaseSize(QtCore.QSize(581, 101))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.newAnButton.setFont(font)
        self.newAnButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.newAnButton.setObjectName(_fromUtf8("newAnButton"))
        self.verticalLayout_2.addWidget(self.newAnButton)
        self.frame_10 = QtGui.QFrame(self.page_2)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_10.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_10.setObjectName(_fromUtf8("frame_10"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.frame_10)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.analysisListCombo = QtGui.QComboBox(self.frame_10)
        self.analysisListCombo.setObjectName(_fromUtf8("analysisListCombo"))
        self.horizontalLayout_7.addWidget(self.analysisListCombo)
        self.analysisResultsButton = QtGui.QPushButton(self.frame_10)
        self.analysisResultsButton.setObjectName(_fromUtf8("analysisResultsButton"))
        self.horizontalLayout_7.addWidget(self.analysisResultsButton)
        self.verticalLayout_2.addWidget(self.frame_10)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
        self.analysisStack.addWidget(self.page_2)
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.analysisStack.addWidget(self.page_3)
        self.verticalLayout_7.addWidget(self.analysisStack)
        TabWidget.addTab(self.tabAnalyses, _fromUtf8(""))

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        TabWidget.setWindowTitle(QtGui.QApplication.translate("TabWidget", "TabWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.projNameLabel.setText(QtGui.QApplication.translate("TabWidget", "Project name :", None, QtGui.QApplication.UnicodeUTF8))
        self.projNameLabelValue.setText(QtGui.QApplication.translate("TabWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("TabWidget", "Data file : ", None, QtGui.QApplication.UnicodeUTF8))
        self.browseDataFileButton.setText(QtGui.QApplication.translate("TabWidget", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browseDirButton.setText(QtGui.QApplication.translate("TabWidget", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TabWidget", "Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("TabWidget", "Data file info :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("TabWidget", "Historical model", None, QtGui.QApplication.UnicodeUTF8))
        self.setHistoricalButton.setToolTip(QtGui.QApplication.translate("TabWidget", "(Alt+h)", None, QtGui.QApplication.UnicodeUTF8))
        self.setHistoricalButton.setText(QtGui.QApplication.translate("TabWidget", "            Set", None, QtGui.QApplication.UnicodeUTF8))
        self.setHistoricalButton.setShortcut(QtGui.QApplication.translate("TabWidget", "Alt+H", None, QtGui.QApplication.UnicodeUTF8))
        self.nbScLabel.setText(QtGui.QApplication.translate("TabWidget", "X scenarios", None, QtGui.QApplication.UnicodeUTF8))
        self.nbParamLabel.setText(QtGui.QApplication.translate("TabWidget", "X parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("TabWidget", "Genetic data and Summary statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.setGeneticButton.setToolTip(QtGui.QApplication.translate("TabWidget", "(Alt+g)", None, QtGui.QApplication.UnicodeUTF8))
        self.setGeneticButton.setText(QtGui.QApplication.translate("TabWidget", "            Set", None, QtGui.QApplication.UnicodeUTF8))
        self.setGeneticButton.setShortcut(QtGui.QApplication.translate("TabWidget", "Alt+G", None, QtGui.QApplication.UnicodeUTF8))
        self.nbMicrosatLabel.setText(QtGui.QApplication.translate("TabWidget", "X microsatellite loci", None, QtGui.QApplication.UnicodeUTF8))
        self.nbSequencesLabel.setText(QtGui.QApplication.translate("TabWidget", "X DNA sequence loci", None, QtGui.QApplication.UnicodeUTF8))
        self.nbGroupLabel.setText(QtGui.QApplication.translate("TabWidget", "X locus groups", None, QtGui.QApplication.UnicodeUTF8))
        self.nbSumStatsLabel.setText(QtGui.QApplication.translate("TabWidget", "X summary statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("TabWidget", "Simulated data sets", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("TabWidget", "Number of simulated data sets in the reference table", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("TabWidget", "Required number of simulated data sets", None, QtGui.QApplication.UnicodeUTF8))
        self.nbSetsDoneEdit.setText(QtGui.QApplication.translate("TabWidget", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.runButton.setText(QtGui.QApplication.translate("TabWidget", "Run computations", None, QtGui.QApplication.UnicodeUTF8))
        self.stopButton.setText(QtGui.QApplication.translate("TabWidget", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        TabWidget.setTabText(TabWidget.indexOf(self.tabRefTable), QtGui.QApplication.translate("TabWidget", "Reference table", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("TabWidget", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("TabWidget", "type", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("TabWidget", "parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("TabWidget", "priority", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("TabWidget", "status", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("TabWidget", "results", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("TabWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("TabWidget", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("TabWidget", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("TabWidget", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.newAnButton.setText(QtGui.QApplication.translate("TabWidget", "Define new analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.analysisResultsButton.setText(QtGui.QApplication.translate("TabWidget", "View results", None, QtGui.QApplication.UnicodeUTF8))
        TabWidget.setTabText(TabWidget.indexOf(self.tabAnalyses), QtGui.QApplication.translate("TabWidget", "Analyses", None, QtGui.QApplication.UnicodeUTF8))

