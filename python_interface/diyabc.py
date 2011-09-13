#!/usr/bin/python
# -*- coding: utf-8 -*-

# variable qui sera changée par le générateur d'exécutable
VERSION='development version'
from datetime import datetime
VERSION_DATE='01/01/1970'

#import dataImages
import shutil
import sys
import os
if sys.platform.startswith('win'):
    sys.path.append("Python26/Lib/site-packages")
# pour connaitre les modules, on manipule le pythonpath
sys.path.append("/".join(os.getcwd().split('/')[:-1]))
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import uic
#from uis.diyabc_ui import Ui_MainWindow
#from project import *
from project import Project
from preferences import Preferences
from showLogFile import ShowLogFile
from documentator import Documentator
import output
from output import log

formDiyabc,baseDiyabc = uic.loadUiType("uis/diyabc.ui")

class Diyabc(formDiyabc,baseDiyabc):
    """ Classe principale qui est aussi la fenêtre principale de la GUI
    """
    def __init__(self,app,parent=None,projects=None):
        super(Diyabc,self).__init__(parent)
        self.app = app
        self.project_list = []
        
        self.main_conf_name = "conf.tmp"
        self.hist_conf_name = "conf.hist.tmp"
        self.gen_conf_name = "conf.gen.tmp"
        self.analysis_conf_name = "conf.analysis"
        self.table_header_conf_name = "conf.th.tmp"
        self.reftableheader_name = "header.txt"

        self.scenario_pix_dir_name = "scenario_pictures"
        self.scenario_pix_basename = "scenario"
        self.PCA_dir_name = "PCA_pictures"

        self.preferences_win = Preferences(self)
        self.preferences_win.loadPreferences()
        #self.defaultMMMValues = self.preferences.getDicoMMM()

        self.showLogFile_win = ShowLogFile(self)
        self.showLogFile_win.setWindowTitle("Logfile viewer")

        self.createWidgets()
        self.setWindowIcon(QIcon("docs/accueil_pictures/coccicon.png"))

        self.illegalProjectNameCharacters = ['_','-',"'",'"','.','/']

        self.documentator = Documentator("docs/documentation.xml",self)

        # ouverture des projets donnés en paramètre au lancement
        if len(projects) > 0:
            self.switchToMainStack()
        for projDirName in projects:
            self.openProject(projDirName)

    def createWidgets(self):
        self.ui=self
        self.ui.setupUi(self)

        #pal = QPalette()
        #pal.setBrush(self.backgroundRole(), QBrush(QImage("docs/accueil_pictures/correct.png")))
        #self.setPalette(pal)

        #im = QImage(dataImages.dada,200,200)
        #pic = QPixmap()
        #pic.convertFromImage(im)
        pic = QPixmap("docs/accueil_pictures/black_red.png")
        self.ui.imgLabel.setPixmap(pic)
        self.switchToWelcomeStack()

        # about window
        self.aboutWindow = uic.loadUi("uis/about.ui")
        self.aboutWindow.parent = self
        self.aboutWindow.setWindowTitle('About DIYABC')
        ui = self.aboutWindow
        ui.logoLabel.setPixmap(QPixmap("docs/accueil_pictures/coccicon.png"))
        txt = str(self.aboutWindow.infoLabel.text())
        txt = txt.replace('vvv',VERSION).replace('ddd',VERSION_DATE)
        self.aboutWindow.infoLabel.setText(txt)
        QObject.connect(ui.okButton,SIGNAL("clicked()"),self.aboutWindow.close)

        #proj1 = Project(self.ui,"ploproj")
        self.ui.tab_6.hide()
        self.ui.tabWidget.removeTab(0)

        # gestion du menu
        file_menu = self.ui.menubar.addMenu("&File")
        self.file_menu = file_menu
        file_menu.addAction(QIcon("docs/icons/folder-new.png"),"&New project",self.newProject,QKeySequence(Qt.CTRL + Qt.Key_N))
        file_menu.addAction(QIcon("docs/icons/fileopen.png"),"&Open project",self.openProject,QKeySequence(Qt.CTRL + Qt.Key_O))
        self.saveProjActionMenu = file_menu.addAction(QIcon("docs/icons/document-save.png"),"&Save current project",self.saveCurrentProject,QKeySequence(Qt.CTRL + Qt.Key_S))
        self.deleteProjActionMenu = file_menu.addAction(QIcon("docs/icons/edit-delete.png"),"&Delete current project",self.deleteCurrentProject,QKeySequence(Qt.CTRL + Qt.Key_D))
        self.cloneProjActionMenu = file_menu.addAction(QIcon("docs/icons/tab-duplicate.png"),"&Clone current project",self.cloneCurrentProject,QKeySequence(Qt.CTRL + Qt.Key_K))
        self.closeProjActionMenu = file_menu.addAction(QIcon("docs/icons/project-close.png"),"C&lose current project",self.closeCurrentProject,QKeySequence(Qt.CTRL + Qt.Key_W))
        self.closeProjActionMenu.setDisabled(True)
        self.saveProjActionMenu.setDisabled(True)
        self.deleteProjActionMenu.setDisabled(True)
        self.cloneProjActionMenu.setDisabled(True)
        file_menu.addAction(QIcon("docs/icons/redhat-system_settings.png"),"&Settings",self.setPreferences,QKeySequence(Qt.CTRL + Qt.Key_P))
        action = file_menu.addAction(QIcon("docs/icons/window-close.png"),"&Quit",self.close,QKeySequence(Qt.CTRL + Qt.Key_Q))
        #mettre plusieurs raccourcis claviers pour le meme menu
        action.setShortcuts([QKeySequence(Qt.CTRL + Qt.Key_Q),QKeySequence(Qt.Key_Escape)])
        #style_menu = self.ui.menubar.addMenu("Style")
        #action_group = QActionGroup(style_menu)
        #for stxt in self.styles:
        #    self.style_actions[stxt] = style_menu.addAction(stxt,self.changeStyle)
        #    self.style_actions[stxt].setActionGroup(action_group)
        #    self.style_actions[stxt].setCheckable(True)
        navigate_menu = self.ui.menubar.addMenu("&Navigate")
        self.prevProjectActionMenu = navigate_menu.addAction(QIcon("docs/icons/arrow-up.png"),"&Previous project",self.prevProject,QKeySequence(Qt.CTRL + Qt.Key_PageUp))
        self.nextProjectActionMenu = navigate_menu.addAction(QIcon("docs/icons/arrow-down.png"),"&Next project",self.nextProject,QKeySequence(Qt.CTRL + Qt.Key_PageDown))
        self.nextProjectActionMenu.setDisabled(True)
        self.prevProjectActionMenu.setDisabled(True)
        help_menu = self.ui.menubar.addMenu("&Help")
        #help_menu.addAction("&About DIYABC",self.switchToWelcomeStack)
        help_menu.addAction(QIcon("docs/icons/dialog-question.png"),"&About DIYABC",self.aboutWindow.show)
        help_menu.addAction(QIcon("docs/icons/gnome-mime-text.png"),"&Show logfile",self.showLogFile)
	
        QObject.connect(self.ui.tabWidget,SIGNAL("tabCloseRequested(int)"),self.closeProject)

        QObject.connect(self.ui.openProjectButton,SIGNAL("clicked()"),self.openProject)
        QObject.connect(self.ui.newProjectButton,SIGNAL("clicked()"),self.newProject)
        #QObject.connect(self.ui.skipWelcomeButton,SIGNAL("clicked()"),self.switchToMainStack)
        self.ui.versionLabel.setText('%s'%VERSION)
        #self.ui.frame.setDisabled(True)
        #self.ui.frame.setAutoFillBackground(True)
        #self.ui.frame.setBackgroundColor(Qt.Blue)

        #self.setCursor(QCursor(QPixmap("/home/julien/vcs/git/diyabc.git/python_interface/docs/accueil_pictures/coccicon.png").scaled(32,32)))

        #statusLabel = QLabel("No info",self)
        #statusLabel.setAlignment(Qt.AlignLeft)
        #self.statusBar.setAlignment(Qt.AlignLeft)
        #self.ui.statusBar.hide()


    def showLogFile(self):
        self.showLogFile_win.show()
        
    def showStatus(self,msg,time=None):
        if time!=None:
            self.ui.statusBar.showMessage(msg,time)
        else:
            self.ui.statusBar.showMessage(msg)
        QCoreApplication.processEvents()

    def clearStatus(self):
        self.ui.statusBar.clearMessage()


    def switchToMainStack(self):
        #self.ui.menubar.show()
        self.ui.stackedWidget.setCurrentIndex(0)

    def switchToWelcomeStack(self):
        #self.ui.menubar.hide()
        self.ui.stackedWidget.setCurrentIndex(1)

    def setPreferences(self):
        self.preferences_win.show()


    #def changeStyle(self):
    #    for stxt in self.styles:
    #        if self.sender() == self.style_actions[stxt]:
    #            self.app.setStyle(stxt)

    def openProject(self,dir=None):
        """ ouverture d'un projet existant
        """
        if dir == None:
            qfd = QFileDialog()
            dir = str(qfd.getExistingDirectory())
        # on enlève le dernier '/' s'il y en a un
        if dir != "" and dir[-1] == "/":
            dir = dir[:-1]
        log(1,"attempting to open the project : %s"%dir)
        #self.ui.infoPlain.setPlainText("Opening project %s"%dir)
        #self.ui.infoPlain.show()
        self.showStatus("Loading project %s"%dir.split('/')[-1])

        proj_name = str(dir).split('/')[-1].split('_')[0]
        # si le dossier existe et qu'il contient conf.hist.tmp
        if dir != "":
            if os.path.exists(dir) and os.path.exists("%s/%s"%(dir,self.main_conf_name)):
                project_name = dir.split('/')[-1].split('_')[0]
                proj_name_list = []
                for p in self.project_list:
                    proj_name_list.append(p.name)
                if not project_name in proj_name_list:
                    proj_ready_to_be_opened = True
                    # si le projet est verrouillé
                    if os.path.exists("%s/.DIYABC_lock"%dir):
                        if not output.debug:
                            reply = QMessageBox.question(self,"Project is locked","The %s project is currently locked.\
    \nThere are two possible reasons for that : \
    \n- The project is currently opened in another instance of DIYABC\
    \n- The last time you opened this project, DIYABC was closed unregularly\n\
    \nWould you like to open the project anyway and get the lock with this DIYABC ?\
    \nIf you say YES, think about closing potential other DIYABCs which manipulate this project"%proj_name,
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.Yes:
                                os.remove("%s/.DIYABC_lock"%dir)
                            else:
                                proj_ready_to_be_opened = False
                        else:
                            # si on est en mode debug, on vire le verrou sans sommation
                            os.remove("%s/.DIYABC_lock"%dir)
                    if proj_ready_to_be_opened:
                        proj_to_open = Project(project_name,dir,self)
                        try:
                            proj_to_open.loadFromDir()
                        except Exception,e:
                            output.notify(self,"opening error","An error occured during the opening of the project\
 %s :\n\n%s\n\nThe cause may be a dirty user handmade modification of the project files or a bug"%(dir,e))
                            return
                        self.project_list.append(proj_to_open)
                        self.ui.tabWidget.addTab(proj_to_open,proj_to_open.name)
                        self.ui.tabWidget.setCurrentWidget(proj_to_open)
                        # verification generale pour mettre a jour l'etat du modèle historique et mutationnel
                        proj_to_open.checkAll()
                        # si la reftable existe, on affiche le nombre d'enregistrement de celle ci et on 
                        # verrouille (freeze) les modèles historique et génétique
                        proj_to_open.putRefTableSize()
                        # si c'est le premier projet, on permet la fermeture/del/save par le menu
                        if len(self.project_list) == 1:
                            self.closeProjActionMenu.setDisabled(False)
                            self.saveProjActionMenu.setDisabled(False)
                            self.deleteProjActionMenu.setDisabled(False)
                            self.cloneProjActionMenu.setDisabled(False)
                        if len(self.project_list) == 2:
                            self.nextProjectActionMenu.setDisabled(False)
                            self.prevProjectActionMenu.setDisabled(False)
                        # on quitte la page d'accueil si on y était
                        self.switchToMainStack()
                        # creation du lock
                        proj_to_open.lock()
                        log(1,"Project '%s' openend successfully"%dir)
                else:
                    output.notify(self,"Name error","A project named \"%s\" is already loaded"%proj_name)
            else:
               output.notify(self,"Load error","\"%s\" is not a project directory"%dir)
        self.clearStatus()

    def cloneCurrentProject(self,cloneBaseName=None,cloneDir=None):
        """ duplique un projet vers un autre répertoire
        demande le nom du clone puis le répertoire dans lequel mettre le clone du projet
        """ 
        self.saveCurrentProject()
        cloneName = cloneBaseName
        current_project = self.ui.tabWidget.currentWidget()
        log(1,"attempting to clone the project : %s"%current_project.dir)
        ok = True
        if cloneBaseName == None:
            fileDial = QtGui.QFileDialog(self,"Select location of the clone project")
            fileDial.setLabelText(QtGui.QFileDialog.Accept,"Clone project")
            fileDial.setLabelText(QtGui.QFileDialog.FileName,"Clone project name")
            ok = (fileDial.exec_() == 1)
            if not ok:
                return
            result = fileDial.selectedFiles()
            if len(result) > 0:
                path = result[0]
            #path = fileDial.getSaveFileName(self,"Project location")
            path = "%s"%path
            # on enleve l'eventuel '/' de fin et on extrait le nom du projet
            if path != None and len(path) > 0 and len(path.split('/')) > 0 :
                if path[-1] == "/":
                    path = path[:-1]
                cloneName = path.split("/")[-1]
        if ok:
            if self.checkProjectName(cloneName):
                # on vire le nom à la fin du path pour obtenir le dossier du clone
                cloneDir = "/".join(path.split("/")[:-1])
                if cloneDir != "" and os.path.exists(cloneDir):
                    if not self.isProjDir(cloneDir):
                        # name_YYYY_MM_DD-num le plus elevé
                        dd = datetime.now()
                        #num = 36
                        cd = 100
                        while cd > 0 and not os.path.exists(cloneDir+"/%s_%i_%i_%i-%i"%(cloneName,dd.year,dd.month,dd.day,cd)):
                            cd -= 1
                        if cd == 100:
                                output.notify(self,"Error","With this version, you cannot have more than 100 \
                                        project directories\nfor the same project name and in the same directory")
                        else:
                            clonedir = cloneDir+"/%s_%i_%i_%i-%i"%(cloneName,dd.year,dd.month,dd.day,(cd+1))
                            #self.ui.dirEdit.setText(newdir)
                            try:
                                #print current_project.dir, " to ", clonedir
                                #shutil.copytree(current_project.dir,clonedir)
                                #os.remove("%s/reftable.bin"%clonedir)

                                # on crée le dossier de destination et on y copie les fichiers utiles
                                os.mkdir(clonedir)
                                for filepath in [self.main_conf_name,
                                        self.hist_conf_name,
                                        self.gen_conf_name,
                                        self.table_header_conf_name,
                                        self.reftableheader_name,
                                        current_project.dataFileName,
                                        self.analysis_conf_name]:
                                    if os.path.exists("%s/%s"%(current_project.dir,filepath)):
                                         shutil.copy("%s/%s"%(current_project.dir,filepath),"%s/%s"%(clonedir,filepath))

                                #shutil.copy("%s/%s"%(current_project.dir,self.main_conf_name),"%s/%s"%(clonedir,self.main_conf_name))
                                #shutil.copy("%s/%s"%(current_project.dir,self.hist_conf_name),"%s/%s"%(clonedir,self.hist_conf_name))
                                #shutil.copy("%s/%s"%(current_project.dir,self.gen_conf_name),"%s/%s"%(clonedir,self.gen_conf_name))
                                #shutil.copy("%s/%s"%(current_project.dir,self.table_header_conf_name),"%s/%s"%(clonedir,self.table_header_conf_name))
                                #shutil.copy("%s/%s"%(current_project.dir,self.reftableheader_name),"%s/%s"%(clonedir,self.reftableheader_name))
                                #shutil.copy("%s/%s"%(current_project.dir,current_project.dataFileName),"%s/%s"%(clonedir,current_project.dataFileName))
                                #shutil.copy("%s/%s"%(current_project.dir,self.analysis_conf_name),"%s/%s"%(clonedir,self.analysis_conf_name))

                                # si les noms sont différents, on le charge
                                if cloneName != current_project.name:
                                    self.openProject(clonedir)
                                else:
                                    output.notify(self,"Load error","The clone project was successfully created but can not be opened because\
                                                it has the same name than the origin project\nClose the origin project if you want to open the clone")
                                log(1,"Project %s was successfully cloned in %s"%(current_project.dir,clonedir))
                            except OSError,e:
                                output.notify(self,"Error",str(e))
                    else:
                        output.notify(self,"Incorrect directory","A project can not be in a project directory")



    def checkProjectName(self,name):
        """ vérifie si le nom de projet ne comporte pas de caractères illégaux et s'il n'est pas vide
        """
        if name == "":
            output.notify(self,"Name error","The project name cannot be empty.")
            return False
        for c in self.illegalProjectNameCharacters:
            if c in name:
                output.notify(self,"Name error","The following characters are not allowed in project name : . \" ' _ - /")
                return False
        return True


    def newProject(self,name=None):
        """ Création d'un projet
        """
        log(1,'Attempting to create a new project')
        ok = True
        #if name == None:
        #    name, ok = QtGui.QInputDialog.getText(self, 'New project', 'Enter the name of the new project:')
        if name == None:
            fileDial = QtGui.QFileDialog(self,"Select location of the new project")
            fileDial.setLabelText(QtGui.QFileDialog.Accept,"Create project")
            fileDial.setLabelText(QtGui.QFileDialog.FileName,"Project name")
            ok = (fileDial.exec_() == 1)
            result = fileDial.selectedFiles()
            if len(result) > 0:
                path = result[0]
            #path = fileDial.getSaveFileName(self,"Project location")
            path = "%s"%path
            # on enleve l'eventuel '/' de fin et on extrait le nom du projet
            if path != None and len(path) > 0 and len(path.split('/')) > 0 :
                if path[-1] == "/":
                    path = path[:-1]
                name = path.split("/")[-1]

        if ok:
            log(1,'The name of the new project will be %s\nIt will be saved in %s'%(name,path))
            if self.checkProjectName(name):
                proj_name_list = []
                for p in self.project_list:
                    proj_name_list.append(p.name)
                if not name in proj_name_list:
                    newProj = Project(name,None,self)
                    # un nouveau projet a au moins un scenario
                    newProj.hist_model_win.addSc()
                    self.project_list.append(newProj)
                    # si c'est le premier projet, on permet la fermeture par le menu
                    # ajout au tabwidget de l'ui principale
                    # ajout de l'onglet
                    self.ui.tabWidget.addTab(newProj,newProj.name)
                    self.ui.tabWidget.setCurrentWidget(newProj)

                    # creation du dir en attendant la selection du datafile
                    newProj.dirCreation(path)

                    if len(self.project_list) == 1:
                        self.closeProjActionMenu.setDisabled(False)
                        self.saveProjActionMenu.setDisabled(False)
                        self.deleteProjActionMenu.setDisabled(False)
                        self.cloneProjActionMenu.setDisabled(False)
                    if len(self.project_list) == 2:
                        self.nextProjectActionMenu.setDisabled(False)
                        self.prevProjectActionMenu.setDisabled(False)
                    self.switchToMainStack()
                    log(1,'Project %s successfully created in %s'%(newProj.name,newProj.dir))
                else:
                    output.notify(self,"Name error","A project named \"%s\" is already loaded."%name)

    def closeProject(self,index,save=None):
        """ ferme le projet qui est à l'index "index" du tabWidget
        le sauvegarde si save == True et le déverrouille
        """
        if save == None:
            if not output.debug:
                reply = QtGui.QMessageBox.question(self, 'Message',
                    "Do you want to save the Project ?", QtGui.QMessageBox.Yes | 
                    QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                save = (reply == QtGui.QMessageBox.Yes)
            else:
                save = True
        
        # est ce que l'index est out of range?
        if self.ui.tabWidget.widget(index) != 0:
            # deverrouillage du projet
            self.ui.tabWidget.widget(index).unlock()
            # suppression du projet dans la liste locale
            self.project_list.remove(self.ui.tabWidget.widget(index))
            if save:
                self.ui.tabWidget.widget(index).save()
        self.ui.tabWidget.removeTab(index)
        # si c'est le dernier projet, on désactive la fermeture par le menu
        if len(self.project_list) == 0:
            self.closeProjActionMenu.setDisabled(True)
            self.saveProjActionMenu.setDisabled(True)
            self.deleteProjActionMenu.setDisabled(True)
            self.cloneProjActionMenu.setDisabled(True)
            self.switchToWelcomeStack()
        if len(self.project_list) == 1:
            self.nextProjectActionMenu.setDisabled(True)
            self.prevProjectActionMenu.setDisabled(True)

    def closeCurrentProject(self,save=None):
        """ ferme le projet courant, celui de l'onglet séléctionné
        """
        cdir = self.ui.tabWidget.currentWidget().dir
        self.closeProject(self.ui.tabWidget.currentIndex(),save)
        log(1,"Project '%s' closed"%(cdir))

    def saveCurrentProject(self):
        """ sauve le projet courant, cad ecrit les fichiers temporaires de conf
        """
        self.ui.tabWidget.currentWidget().save()
        log(1,"Project '%s' saved"%(self.ui.tabWidget.currentWidget().name))

    def deleteCurrentProject(self):
        """ efface le projet courant
        """
        ddir = self.ui.tabWidget.currentWidget().dir
        self.deleteProject(self.ui.tabWidget.currentIndex())
        log(1,"Project '%s' deleted"%(ddir))

    def deleteProject(self,index):
        """ efface le projet dont l'index est donné en paramètre
        """
        projdir = str(self.ui.tabWidget.widget(index).dir)
        shutil.rmtree(projdir)
        # on ferme le projet sans sauver
        self.closeProject(index,False)
    def nextProject(self):
        if self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.setCurrentIndex((self.ui.tabWidget.currentIndex() + 1) % self.ui.tabWidget.count())

    def prevProject(self):
        if self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.setCurrentIndex((self.ui.tabWidget.currentIndex() - 1) % self.ui.tabWidget.count())

    def isProjDir(self,dir):
        """ retourne vrai si le répertoire donné en paramètre est un 
        repertoire de projet ou s'il est dans un répertoire de projet
        """
        if os.path.exists("%s/%s"%(dir,self.main_conf_name))\
                or os.path.exists("%s/%s"%(os.path.abspath(os.path.join(dir, '..')),self.main_conf_name)):
            return True
        else:
            return False


    def closeEvent(self, event):
        for proj in self.project_list:
            # si le projet est bien créé (et pas en cours de création)
            if proj.dir != None:
                proj.stopRefTableGen()
                proj.stopAnalysis()
                proj.unlock()
        event.accept()
    #    reply = QtGui.QMessageBox.question(self, 'Message',
    #        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
    #        QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

    #    if reply == QtGui.QMessageBox.Yes:
    #        event.accept()
    #    else:
    #        event.ignore()

    #def mousePressEvent(self,event):
    #    print self.sender()
    #    print "plop"
    def event(self,event):
        if event.type() == QEvent.MouseButtonRelease and event.button() == 2:
            elemList = self.findChildren(QLabel)
            elemList += self.findChildren(QPushButton)
            for c in elemList:
                if c.underMouse():
                    self.file_menu.popup(QCursor.pos())

                    on = str(c.objectName())
                    log(1,"Asking documentation of %s"%on)
                    if self.documentator.getDocString(on) != None:
                        output.notify(self,"Documentation",self.documentator.getDocString(on))
                    else:
                        output.notify(self,"Documentation","No documentation found")
            log(3,"Button '%s' pressed"%event.button())
        return QWidget.event(self,event)

    def dropEvent(self,event):
        """ Ouverture du projet par glisser deposer
        """
        for url in event.mimeData().urls():
            path = url.toString()
            log(1,"Folder %s was dragNdroped to be opened"%path)
            # WINDOWS n'a pas de /
            if "win" in sys.platform and len(path) > 0:
                self.openProject(path.replace("file:///",""))
            else:
                self.openProject(path.replace("file://",""))
        event.acceptProposedAction()

    def dragEnterEvent(self,event):
        event.acceptProposedAction()

if __name__ == "__main__":
    nargv = sys.argv
    projects_to_open = nargv[1:]
    #nargv.extend(["-title","DIYABC v%s"%VERSION])
    app = QApplication(nargv)
    myapp = Diyabc(app,projects=projects_to_open)
    myapp.setWindowTitle("DIYABC %s"%VERSION)
    myapp.show()
    # pour le dragNdrop des dossier projet
    myapp.setAcceptDrops(True)
    # pour les logs dans un fichier et sur le terminal
    if not os.path.exists(os.path.expanduser("~/.diyabc/")):
        os.mkdir(os.path.expanduser("~/.diyabc/"))
    if not os.path.exists(os.path.expanduser("~/.diyabc/logs/")):
        os.mkdir(os.path.expanduser("~/.diyabc/logs/"))
    dd = datetime.now()
    logfile = os.path.expanduser("~/.diyabc/logs/%02d_%02d_%s-%s.log"%(dd.day,dd.month,dd.year,os.getpid()))
    # chaque TeeLogger remplace une sortie et écrit dans 
    # le fichier qu'on lui donne
    myOut = output.TeeLogger(logfile,"a",myapp,True)
    myErr = output.TeeLogger(logfile,"a",myapp,False)
    sys.stdout = myOut
    sys.stderr = myErr
    log(1,"DIYABC launched")
    #QTest.mouseClick(myapp.ui.skipWelcomeButton,Qt.LeftButton)
    sys.exit(app.exec_())

