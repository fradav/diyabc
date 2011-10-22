# -*- coding: utf-8 -*-

import os,sys,platform,multiprocessing
import ConfigParser
import codecs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
#from uis.preferences_ui import Ui_MainWindow
from mutationModel.setMutationModelMsat import SetMutationModelMsat
from mutationModel.setMutationModelSequences import SetMutationModelSequences
import output
from utils.cbgpUtils import log

formPreferences,basePreferences = uic.loadUiType("uis/preferences.ui")

class Preferences(formPreferences,basePreferences):
    """ Classe principale qui est aussi la fenêtre principale de la GUI
    """
    def __init__(self,parent=None):
        super(Preferences,self).__init__(parent)
        self.parent = parent
        confdir = os.path.expanduser("~/.diyabc/")
        if not os.path.exists(confdir):
            os.mkdir(confdir)

        #cfgConfigFiles = [ confdir+filename for filename in ["connexion.cfg","hist_model_default_values.cfg","various.cfg"] ]

        self.config = ConfigParser.ConfigParser()
        self.configFile = confdir+"config.cfg"
        self.loadedConfigs = self.config.read(self.configFile)

        self.createWidgets()

        self.tabColor = {"green": "#c3ffa6","blue":"#7373ff","red":"#ffb2a6","yellow":"#ffffb2","pink":"#ffbff2"}

        #self.ui.tabWidget.setTabText(0,"Connexion")
        #self.ui.tabWidget.setTabText(1,"Historical")
        #self.ui.tabWidget.setTabText(2,"Various")
        self.mutmodM = SetMutationModelMsat(self)
        self.mutmodS = SetMutationModelSequences(self)
        self.ui.tabWidget.addTab(self.mutmodM,"MM Microsats")
        self.ui.tabWidget.addTab(self.mutmodS,"MM Sequences")

        self.mutmodM.ui.frame_6.hide()
        self.mutmodM.ui.setMutMsLabel.setText("Default values for mutation model of Microsatellites")
        self.mutmodS.ui.frame_6.hide()
        self.mutmodS.ui.setMutSeqLabel.setText("Default values for mutation model of Sequences")

        self.ui.connectButton.hide()

        self.styles = []
        for i in QStyleFactory.keys():
            self.styles.append(str(i))
            self.ui.styleCombo.addItem(str(i))

        ind = self.ui.styleCombo.findText("Cleanlooks")
        if ind != -1:
            self.ui.styleCombo.setCurrentIndex(ind)
        ind = self.ui.styleCombo.findText("white")
        if ind != -1:
            self.ui.bgColorCombo.setCurrentIndex(ind)

        # initialisation du combo pour le nombre max de thread
        for i in range(multiprocessing.cpu_count()):
            self.ui.maxThreadCombo.addItem("%s"%(i+1))
        self.ui.maxThreadCombo.setCurrentIndex(self.ui.maxThreadCombo.count()-1)


    def createWidgets(self):
        self.ui=self
        self.ui.setupUi(self)

        self.setWindowTitle("Settings")

        self.ui.gridLayout.setAlignment(Qt.AlignTop)
        self.ui.verticalLayout_57.setAlignment(Qt.AlignTop)
        self.ui.verticalLayout_2.setAlignment(Qt.AlignTop)
        #self.ui.verticalLayout_54.setAlignment(Qt.AlignTop)
        #self.ui.verticalLayout_29.setAlignment(Qt.AlignTop)
        #self.ui.verticalLayout_26.setAlignment(Qt.AlignTop)

        QObject.connect(self.ui.savePreferencesButton,SIGNAL("clicked()"),self.savePreferences)
        QObject.connect(self.ui.cancelPreferencesButton,SIGNAL("clicked()"),self.cancel)
        QObject.connect(self.ui.execBrowseButton,SIGNAL("clicked()"),self.browseExec)
        QObject.connect(self.ui.styleCombo,SIGNAL("currentIndexChanged(QString)"),self.changeStyle)
        QObject.connect(self.ui.bgColorCombo,SIGNAL("currentIndexChanged(QString)"),self.changeBackgroundColor)

        QObject.connect(self.ui.serverCheck,SIGNAL("toggled(bool)"),self.toggleServer)
        QObject.connect(self.ui.useDefaultExeCheck,SIGNAL("toggled(bool)"),self.toggleExeSelection)

        self.ui.addrEdit.setDisabled(True)
        self.ui.portEdit.setDisabled(True)

        self.toggleExeSelection(self.ui.useDefaultExeCheck.isChecked())


        #QObject.connect(self.ui.saveMMMButton,SIGNAL("clicked()"),self.saveMMM)
        #QObject.connect(self.ui.saveMMSButton,SIGNAL("clicked()"),self.saveMMS)

    def cancel(self):
        """ pour annuler, on recharge depuis la derniere configuration sauvée
        """
        self.loadPreferences()
        self.close()

    def toggleServer(self,state):
        self.ui.addrEdit.setDisabled(not state)
        self.ui.portEdit.setDisabled(not state)

    def toggleExeSelection(self,state):
        self.ui.execBrowseButton.setDisabled(state)
        self.ui.execPathEdit.setDisabled(state)

    def browseExec(self):
        qfd = QFileDialog()
        path = str(qfd.getOpenFileName(self,"Where is your executable file ?"))
        self.ui.execPathEdit.setText(path)

    def getMaxThreadNumber(self):
        return int(self.ui.maxThreadCombo.currentText())

    def getExecutablePath(self):
        exPath = ""
        if self.ui.useDefaultExeCheck.isChecked():
            # LINUX
            if "linux" in sys.platform:
                if "86" in platform.machine():
                    exPath = "docs/executables/diyabc-comput-linux-i386"
                else:
                    exPath = "docs/executables/diyabc-comput-linux-x64"
            # WINDOWS
            elif "win" in sys.platform:
                if os.environ.has_key("PROCESSOR_ARCHITECTURE") and "86" not in os.environ["PROCESSOR_ARCHITECTURE"]:
                    exPath = "docs/executables/diyabc-comput-win-x64"
                else:
                    exPath = "docs/executables/diyabc-comput-win-i386"
            # MACOS
            elif "darwin" in sys.platform:
                if "86" in platform.machine():
                    exPath = "docs/executables/diyabc-comput-mac-i386"
                else:
                    exPath = "docs/executables/diyabc-comput-mac-x64"
        else:
            return str(self.ui.execPathEdit.text())
        return exPath

    def changeBackgroundColor(self,colorstr):
        if str(colorstr) in self.tabColor.keys():
            self.parent.setStyleSheet("background-color: %s;"%self.tabColor[str(colorstr)])
        elif colorstr == "default":
            output.notify(self,"advice","Restart DIYABC in order to load the default color scheme")
        else:
            self.parent.setStyleSheet("background-color: %s;"%colorstr)

    def changeStyle(self,stylestr):
        """ change le style de l'application (toutes les fenêtres)
        """
        self.parent.app.setStyle(str(stylestr))


    def savePreferences(self):
        """ sauve les préférences si elles sont valides
        """
        if self.allValid():
            self.saveMMM()
            self.saveMMS()
            self.saveConnexion()
            self.saveHM()
            self.saveVarious()
            self.saveRecent()
            self.writeConfigFile()
            self.close()

    def writeConfigFile(self):
        with open(self.configFile, 'wb') as configfile:
            self.config.write(configfile)

    def allValid(self):
        """ vérifie la validité des préférences
        """
        return (self.mutmodM.allValid() and self.mutmodS.allValid() and self.histModelValid() and self.connexionValid())

    def loadPreferences(self):
        """ charge les préférences de l'utilisateur si elles existent
        """
        if os.path.exists(os.path.expanduser("~/.diyabc/")):
            self.loadMMM()
            self.loadMMS()
            self.loadConnexion()
            self.loadHM()
            self.loadVarious()
            self.loadRecent()
        #else:
        #    # c'est sans doute la première fois qu'on lance diyabc
        #    # sous linux, on appelle gconf pour voir les icones dans les menus et boutons
        #    if "linux" in sys.platform:
        #        cmd_args_list = ["gconftool-2", "--type", "boolean", "--set", "/desktop/gnome/interface/buttons_have_icons", "true"]
        #        p = subprocess.Popen(cmd_args_list) 
        #        cmd_args_list = ["gconftool-2", "--type", "boolean", "--set", "/desktop/gnome/interface/menus_have_icons", "true"]
        #        p = subprocess.Popen(cmd_args_list) 

    def loadRecent(self):
            recent_list = []
            if self.config.has_section("recent"):
                for l in self.config.options("recent"):
                    rec = self.config.get("recent",l)
                    if len(rec) > 0 and rec.strip() != "":
                        recent_list.append(rec.strip())
                        print "Loading recent : %s"%rec.strip()
                self.parent.setRecent(recent_list)

    def saveRecent(self):
        if not self.config.has_section("recent"):
            self.config.add_section("recent")
        recList = self.parent.getRecent()
        cfgRecentIndex = 0
        for ind,rec in enumerate(recList):
            # si on a qu'un seul exemplaire de ce recent ou bien, si on est le premier
            if (recList.count(rec) > 1 and recList.index(rec) == ind) or recList.count(rec) == 1 :
                log(3,"Saving recent %s"%rec)
                self.config.set("recent","%s"%cfgRecentIndex,rec)
                cfgRecentIndex += 1



    def saveVarious(self):
        """ sauvegarde de la partie various des préférences
        """
        style = str(self.ui.styleCombo.currentText())
        bgColor = str(self.ui.bgColorCombo.currentText())
        pic_format = str(self.ui.formatCombo.currentText())
        ex_path = str(self.ui.execPathEdit.text())
        ex_default = str(self.ui.useDefaultExeCheck.isChecked())
        max_thread = str(self.ui.maxThreadCombo.currentText())

        if not self.config.has_section("various"):
            self.config.add_section("various")
        self.config.set("various","style",style)
        self.config.set("various","format",pic_format)
        self.config.set("various","execPath",ex_path)
        self.config.set("various","bgColor",bgColor)
        self.config.set("various","useDefaultExecutable",ex_default)
        self.config.set("various","maxThreadNumber",max_thread)

    def loadVarious(self):
        """ chargement de la partie various des préférences
        """
        cfg = self.config
        if cfg.has_section("various"):
            if cfg.has_option("various","style"):
                style = cfg.get("various","style")
                ind = self.ui.styleCombo.findText(style.strip())
                if ind != -1:
                    self.ui.styleCombo.setCurrentIndex(ind)
            if cfg.has_option("various","format"):
                pformat = cfg.get("various","format")
                ind = self.ui.formatCombo.findText(pformat.strip())
                if ind != -1:
                    self.ui.formatCombo.setCurrentIndex(ind)
            if cfg.has_option("various","execPath"):
                exf = cfg.get("various","execPath")
                self.ui.execPathEdit.setText(exf.strip())
            if cfg.has_option("various","bgColor"):
                bg = cfg.get("various","bgColor")
                ind = self.ui.bgColorCombo.findText(bg.strip())
                if ind != -1:
                    self.ui.bgColorCombo.setCurrentIndex(ind)
            if cfg.has_option("various","useDefaultExecutable"):
                state = cfg.get("various","useDefaultExecutable")
                checked = (state == "True")
                self.ui.useDefaultExeCheck.setChecked(checked)
                self.toggleExeSelection(checked)
            if cfg.has_option("various","maxThreadNumber"):
                maxt = cfg.get("various","maxThreadNumber")
                ind = self.ui.maxThreadCombo.findText(maxt.strip())
                if ind != -1:
                    self.ui.maxThreadCombo.setCurrentIndex(ind)
        else:
            log(3,"No various conf found")

    def saveHM(self):
        """ sauvegarde de la partie historical model des préférences
        """
        if not self.config.has_section("hist_model_default_values"):
            self.config.add_section("hist_model_default_values")

        if self.ui.NUNRadio.isChecked():
            nlaw = "UN"
        elif self.ui.NLURadio.isChecked():
            nlaw = "LU"
        elif self.ui.NNORadio.isChecked():
            nlaw = "NO"
        elif self.ui.NLNRadio.isChecked():
            nlaw = "LN"
        if self.ui.TUNRadio.isChecked():
            tlaw = "UN"
        elif self.ui.TLURadio.isChecked():
            tlaw = "LU"
        elif self.ui.TNORadio.isChecked():
            tlaw = "NO"
        elif self.ui.TLNRadio.isChecked():
            tlaw = "LN"
        if self.ui.AUNRadio.isChecked():
            alaw = "UN"
        elif self.ui.ALURadio.isChecked():
            alaw = "LU"
        elif self.ui.ANORadio.isChecked():
            alaw = "NO"
        elif self.ui.ALNRadio.isChecked():
            alaw = "LN"

        toSave = {
                "nmin" : float(self.ui.NminEdit.text()),
                "nmax" : float(self.ui.NmaxEdit.text()),
                "nmean" : float(self.ui.NmeanEdit.text()),
                "nst" :float(self.ui.NstdevEdit.text()),
                "tmin" :float(self.ui.TminEdit.text()),
                "tmax" :float(self.ui.TmaxEdit.text()),
                "tmean" :float(self.ui.TmeanEdit.text()),
                "tst" :float(self.ui.TstdevEdit.text()),
                "amin" :float(self.ui.AminEdit.text()),
                "amax" :float(self.ui.AmaxEdit.text()),
                "amean" :float(self.ui.AmeanEdit.text()),
                "ast" :float(self.ui.AstdevEdit.text()),
                "nlaw" : nlaw,
                "tlaw" : tlaw,
                "alaw" : alaw
                }
        for k in toSave:
            self.config.set("hist_model_default_values",k,toSave[k])

    def loadHM(self):
        """ chargement de la partie historical model des préférences
        """
        cfg = self.config
        if cfg.has_section("hist_model_default_values"):
            dico_val = {}
            pairs = cfg.items("hist_model_default_values")
            for p in pairs:
                dico_val[p[0]] = p[1]

            self.ui.NminEdit.setText(dico_val["nmin"])
            self.ui.NmaxEdit.setText(dico_val["nmax"])
            self.ui.NmeanEdit.setText(dico_val["nmean"])
            self.ui.NstdevEdit.setText(dico_val["nst"])
            self.ui.TminEdit.setText(dico_val["tmin"])
            self.ui.TmaxEdit.setText(dico_val["tmax"])
            self.ui.TmeanEdit.setText(dico_val["tmean"])
            self.ui.TstdevEdit.setText(dico_val["tst"])
            self.ui.AminEdit.setText(dico_val["amin"])
            self.ui.AmaxEdit.setText(dico_val["amax"])
            self.ui.AmeanEdit.setText(dico_val["amean"])
            self.ui.AstdevEdit.setText(dico_val["ast"])
            if dico_val["nlaw"] == "UN":
                self.ui.NUNRadio.setChecked(True)
            if dico_val["nlaw"] == "LN":
                self.ui.NLNRadio.setChecked(True)
            if dico_val["nlaw"] == "NO":
                self.ui.NNORadio.setChecked(True)
            if dico_val["nlaw"] == "LU":
                self.ui.NLURadio.setChecked(True)
            if dico_val["alaw"] == "UN":
                self.ui.AUNRadio.setChecked(True)
            if dico_val["alaw"] == "LU":
                self.ui.ALURadio.setChecked(True)
            if dico_val["alaw"] == "NO":
                self.ui.ANORadio.setChecked(True)
            if dico_val["alaw"] == "LN":
                self.ui.ALNRadio.setChecked(True)
            if dico_val["tlaw"] == "UN":
                self.ui.TUNRadio.setChecked(True)
            if dico_val["tlaw"] == "LN":
                self.ui.TLNRadio.setChecked(True)
            if dico_val["tlaw"] == "LU":
                self.ui.TLURadio.setChecked(True)
            if dico_val["tlaw"] == "NO":
                self.ui.TNORadio.setChecked(True)
        else:
            log(3,"No hist conf found")
        
    def saveMMM(self):
        """ sauvegarde de la partie mutation model microsats des préférences
        """
        if os.path.exists(os.path.expanduser("~/.diyabc/mutationM_default_values")):
            os.remove(os.path.expanduser("~/.diyabc/mutationM_default_values"))

        lines = self.mutmodM.getMutationConf()
        f = codecs.open(os.path.expanduser("~/.diyabc/mutationM_default_values"),"w","utf-8")
        f.write(lines)
        f.close()

    def loadMMM(self):
        """ chargement de la partie mutation model microsats des préférences
        """
        if os.path.exists(os.path.expanduser("~/.diyabc/mutationM_default_values")):
            f = codecs.open(os.path.expanduser("~/.diyabc/mutationM_default_values"),"r","utf-8")
            lines = f.readlines()
            f.close()
            self.mutmodM.setMutationConf(lines)
        else:
            log(3,"No MMM conf found")



    def saveMMS(self):
        """ sauvegarde de la partie mutation model sequences des préférences
        """
        if os.path.exists(os.path.expanduser("~/.diyabc/mutationS_default_values")):
            os.remove(os.path.expanduser("~/.diyabc/mutationS_default_values"))

        lines = self.mutmodS.getMutationConf()
        f = codecs.open(os.path.expanduser("~/.diyabc/mutationS_default_values"),"w","utf-8")
        f.write(lines)
        f.close()

    def loadMMS(self):
        """ chargement de la partie mutation model sequences des préférences
        """
        if os.path.exists(os.path.expanduser("~/.diyabc/mutationS_default_values")):
            f = codecs.open(os.path.expanduser("~/.diyabc/mutationS_default_values"),"r","utf-8")
            lines = f.readlines()
            f.close()
            self.mutmodS.setMutationConf(lines)
        else:
            log(3,"No MMS conf found")

    def saveConnexion(self):
        """ sauvegarde de la partie connexion des préférences
        """
        if not self.config.has_section("connexion"):
            self.config.add_section("connexion")

        self.config.set("connexion","host",str(self.ui.addrEdit.text()))
        self.config.set("connexion","port",str(self.ui.portEdit.text()))
        self.config.set("connexion","useServer",str(self.ui.serverCheck.isChecked()))

    def loadConnexion(self):
        """ chargement de la partie connexion des préférences
        """
        cfg = self.config
        if cfg.has_section("connexion"):
            self.ui.addrEdit.setText(cfg.get("connexion","host"))
            self.ui.portEdit.setText(cfg.get("connexion","port"))
            yesno = (cfg.get("connexion","useServer") == 'True')
            self.ui.serverCheck.setChecked(yesno)
        else:
            log(3,"No connexion conf found")

    def connexionValid(self):
        """ vérifie la validité de la partie connexion
        """
        problems = ""
        try:
            port = int(self.ui.portEdit.text())
        except Exception,e:
            problems += "%s for port connexion value"%e

        if problems == "":
            return True
        else:
            QMessageBox.information(self,"Value error","%s"%problems)
            return False

    def histModelValid(self):
        """ vérifie la validité de la partie hist model
        """
        problems = ""
        try:
            nmin = float(self.ui.NminEdit.text())
            nmax = float(self.ui.NmaxEdit.text())
            nmean = float(self.ui.NmeanEdit.text())
            nst = float(self.ui.NstdevEdit.text())
            tmin = float(self.ui.TminEdit.text())
            tmax = float(self.ui.TmaxEdit.text())
            tmean = float(self.ui.TmeanEdit.text())
            tst = float(self.ui.TstdevEdit.text())
            amin = float(self.ui.AminEdit.text())
            amax = float(self.ui.AmaxEdit.text())
            amean = float(self.ui.AmeanEdit.text())
            ast = float(self.ui.AstdevEdit.text())
            if nmin > nmax or tmin > tmax or amin > amax:
                problems += "A min is superior than a max\n"
        except Exception,e:
            problems += "%s in historical model values\n"%e

        if problems == "":
            return True
        else:
            QMessageBox.information(self,"Value error","%s"%problems)
            return False

