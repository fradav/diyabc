# -*- coding: utf-8 -*-

import os
import shutil
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from uis.defineNewAnalysis_ui import Ui_Frame
from comparison import Comparison
from estimation import Estimation
from genericScenarioSelection import GenericScenarioSelection
from biasScenarioSelection import BiasNEvaluateScenarioSelection
import output

class DefineNewAnalysis(QFrame):
    """ écran de définition d'une nouvelle analyse. demande
    le type d'analyse souhaitée
    """
    def __init__(self,parent=None):
        super(DefineNewAnalysis,self).__init__(parent)
        self.parent=parent
        self.createWidgets()
        self.ui.verticalLayout_2.setAlignment(Qt.AlignHCenter)
        self.ui.verticalLayout_2.setAlignment(Qt.AlignTop)



    def createWidgets(self):
        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        QObject.connect(self.ui.exitButton,SIGNAL("clicked()"),self.exit)
        QObject.connect(self.ui.okButton,SIGNAL("clicked()"),self.validate)
        QObject.connect(self.ui.pcaCheck,SIGNAL("clicked()"),self.preEvaluateCheck)
        QObject.connect(self.ui.lossCheck,SIGNAL("clicked()"),self.preEvaluateCheck)

    def preEvaluateCheck(self):
        """ empêche qu'aucune des deux cases ne soit cochée
        """
        if not self.ui.pcaCheck.isChecked() and not self.ui.lossCheck.isChecked():
            if self.sender() == self.ui.pcaCheck:
                self.ui.lossCheck.setChecked(True)
            else:
                self.ui.pcaCheck.setChecked(True)

    def checkName(self):
        """ vérifie si le nom est valide et libre
        """
        name = str(self.ui.analysisNameEdit.text())
        if name.strip() == "" or len(name.strip()) > 10:
            output.notify(self,"name error","Name cannot be empty or more than 10 characters long")
            return False
        for an in self.parent.analysisList:
            n = an[1]
            if name.strip() == n.strip():
                output.notify(self,"name error","Name already used")
                return False
        return True

    def validate(self):
        """ on poursuit la définition de l'analyse
        """
        if self.checkName():
            name = str(self.ui.analysisNameEdit.text())
            # pour les cas de comparison et estimate, la selection n'influe pas sur l'écran suivant
            # on instancie donc Comparison et Estimation maintenant
            if self.ui.comparisonRadio.isChecked():
                if len(self.parent.hist_model_win.scList) >= 2:
                    analysis = ["compare",name]
                    compFrame = Comparison(analysis,self)
                    genSel = GenericScenarioSelection(len(self.parent.hist_model_win.scList),"Select the scenarios that you wish to compare",compFrame,"Comparison of scenarios",2,self)
                    #self.parent.addTab(genSel,"Scenario selection")
                    #self.parent.removeTab(self.parent.indexOf(self))
                    #self.parent.setCurrentWidget(genSel)
                    self.parent.ui.analysisStack.addWidget(genSel)
                    self.parent.ui.analysisStack.removeWidget(self)
                    self.parent.ui.analysisStack.setCurrentWidget(genSel)
                else:
                    QMessageBox.information(self,"Scenario error","At least 2 scenarios are needed for this analysis")
            elif self.ui.estimateRadio.isChecked():
                if len(self.parent.hist_model_win.scList) >= 1:
                    analysis = ["estimate",name]
                    estimateFrame = Estimation(analysis,self)
                    genSel = GenericScenarioSelection(len(self.parent.hist_model_win.scList),"Parameters will be estimated considering data sets simulated with",estimateFrame,"ABC parameter estimation",1,self)
                    #self.parent.addTab(genSel,"Scenario selection")
                    #self.parent.removeTab(self.parent.indexOf(self))
                    #self.parent.setCurrentWidget(genSel)
                    self.parent.ui.analysisStack.addWidget(genSel)
                    self.parent.ui.analysisStack.removeWidget(self)
                    self.parent.ui.analysisStack.setCurrentWidget(genSel)
                else:
                    QMessageBox.information(self,"Scenario error","At least 1 scenario is needed for this analysis")
            elif self.ui.preEvRadio.isChecked():
                paramtxt = ""
                if self.ui.pcaCheck.isChecked():
                    paramtxt+= " PCA "
                if self.ui.pcaCheck.isChecked() and self.ui.lossCheck.isChecked():
                    paramtxt+="and"
                if self.ui.lossCheck.isChecked():
                    paramtxt+= " Locate S.S."
                self.parent.addAnalysis(["pre-ev",name,paramtxt])
                self.exit()
            elif self.ui.biasRadio.isChecked():
                analysis = ["bias",name]
                genSel = BiasNEvaluateScenarioSelection(len(self.parent.hist_model_win.scList),False,analysis,self)
                #self.parent.addTab(genSel,"Scenario selection")
                #self.parent.removeTab(self.parent.indexOf(self))
                #self.parent.setCurrentWidget(genSel)
                self.parent.ui.analysisStack.addWidget(genSel)
                self.parent.ui.analysisStack.removeWidget(self)
                self.parent.ui.analysisStack.setCurrentWidget(genSel)

            elif self.ui.evaluateRadio.isChecked():
                analysis = ["evaluate",name]
                genSel = BiasNEvaluateScenarioSelection(len(self.parent.hist_model_win.scList),True,analysis,self)
                #self.parent.addTab(genSel,"Scenario selection")
                #self.parent.removeTab(self.parent.indexOf(self))
                #self.parent.setCurrentWidget(genSel)
                self.parent.ui.analysisStack.addWidget(genSel)
                self.parent.ui.analysisStack.removeWidget(self)
                self.parent.ui.analysisStack.setCurrentWidget(genSel)

            else:
                print "NYI"

    def exit(self):
        ## reactivation des onglets
        #self.parent.setTabEnabled(1,True)
        #self.parent.setTabEnabled(0,True)
        #self.parent.removeTab(self.parent.indexOf(self))
        #self.parent.setCurrentIndex(1)
        self.parent.ui.analysisStack.removeWidget(self)
        self.parent.ui.analysisStack.setCurrentIndex(0)
