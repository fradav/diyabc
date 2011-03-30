# -*- coding: utf-8 -*-

import hashlib,pickle,array
import socket
from socket import *
import time
import os
import shutil
import codecs
import subprocess
import tarfile,stat
from subprocess import Popen, PIPE, STDOUT 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from uis.project_ui import *
from setHistoricalModel import SetHistoricalModel
from setGenDataRefTable import SetGeneticDataRefTable
from mutationModel.setMutationModelMsat import SetMutationModelMsat
from mutationModel.setMutationModelSequences import SetMutationModelSequences
from summaryStatistics.setSummaryStatisticsMsat import SetSummaryStatisticsMsat
from summaryStatistics.setSummaryStatisticsSeq import SetSummaryStatisticsSeq
from analysis.defineNewAnalysis import DefineNewAnalysis
from analysis.drawEstimationAnalysisResult import DrawEstimationAnalysisResult
from analysis.drawComparisonAnalysisResult import DrawComparisonAnalysisResult
from utils.data import Data
from datetime import datetime 
import os.path
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *
import output


class Project(QTabWidget):
    """ classe qui représente un projet
    par defaut, un projet est considéré comme nouveau, cad que l'affichage est celui d'un projet vierge
    pour un projet chargé, on modifie l'affichage en conséquence dans loadFromDir
    """
    def __init__(self,name,dir=None,parent=None):
        self.parent=parent
        self.name=name
        self.dir=dir
        self.dataFileSource = ""
        self.dataFileName = ""
        self.hist_state_valid = False
        self.gen_state_valid = False
        self.data = None
        self.analysisList = []
        self.dicoFrameAnalysis = {}

        # utile seulement si on derive de QTabWidget
        super(Project,self).__init__(parent)
        # on peut aussi instancier un tabwidget
        #self.tab = QTabWidget()

        # instanciation du widget project_ui
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)

        # desactivation des boutons
        self.ui.setHistoricalButton.setDisabled(True)
        self.ui.setGeneticButton.setDisabled(True)
        self.ui.runButton.setDisabled(True)
        self.ui.browseDirButton.setDisabled(True)
        self.ui.dataFileEdit.setReadOnly(True)
        self.ui.dirEdit.setReadOnly(True)
        self.ui.groupBox.hide()
        #self.ui.groupBox.setVisible(False)

        # creation des onglets "set ..."
        self.hist_model_win = SetHistoricalModel(self)
        self.hist_model_win.hide()
        #self.addTab(self.hist_model_win,"Set historical model")
        #self.setTabEnabled(2,False)

        self.gen_data_win = SetGeneticDataRefTable(self)
        self.gen_data_win.hide()
        #self.addTab(self.gen_data_win,"Set genetic data")
        #self.setTabEnabled(3,False)


        # manual alignment set
        #self.ui.verticalLayout.setAlignment(self.ui.horizontalFrame,Qt.AlignTop)
        #self.ui.verticalLayout.setAlignment(self.ui.groupBox,Qt.AlignTop)
        self.ui.verticalLayout_2.setAlignment(self.ui.newAnButton,Qt.AlignCenter)
        self.ui.verticalLayout_3.setAlignment(self.ui.progressBar,Qt.AlignCenter)
        self.ui.projNameLabelValue.setText(name)
        self.ui.tableWidget.setColumnWidth(1,150)
        self.ui.tableWidget.setColumnWidth(2,300)
        self.ui.tableWidget.setColumnWidth(3,70)

        QObject.connect(self.ui.newAnButton,SIGNAL("clicked()"),self.defineNewAnalysis)
        #QObject.connect(self.ui.tableWidget,SIGNAL("cellClicked(int,int)"),self.clcl)
        QObject.connect(self.ui.setHistoricalButton,SIGNAL("clicked()"),self.setHistorical)
        QObject.connect(self.ui.setGeneticButton,SIGNAL("clicked()"),self.setGenetic)
        QObject.connect(self.ui.browseDataFileButton,SIGNAL("clicked()"),self.dataFileSelection)
        QObject.connect(self.ui.browseDirButton,SIGNAL("clicked()"),self.dirSelection)

        #QObject.connect(self.ui.drawButton,SIGNAL("clicked()"),self.drawGraph)
        QObject.connect(self.ui.loadButton,SIGNAL("clicked()"),self.loadACP)
        QObject.connect(self.ui.saveGraphButton,SIGNAL("clicked()"),self.saveGraph)
        QObject.connect(self.ui.scCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        QObject.connect(self.ui.compoHCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        QObject.connect(self.ui.compoVCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        QObject.connect(self.ui.nbpCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        self.ui.ACProgress.setValue(0)
        self.tab_colors = ["#0000FF","#00FF00","#FF0000","#00FFFF","#FF00FF","#FFFF00","#000000","#808080","#008080","#800080","#808000","#000080","#008000","#800000","#A4A0A0","#A0A4A0","#A0A0A4","#A00000","#00A000","#00A0A0"]

        # inserer image
        self.ui.setHistoricalButton.setIcon(QIcon("docs/redcross.png"))
        self.ui.setGeneticButton.setIcon(QIcon("docs/redcross.png"))

        self.setTabIcon(0,QIcon("docs/redcross.png"))
        self.setTabIcon(1,QIcon("/usr/share/pixmaps/baobab.xpm"))


        #for i in range(self.ui.tableWidget.columnCount()):
        #    for j in range(self.ui.tableWidget.rowCount()):
        #        it = QTableWidgetItem("%i,%i"%(j,i))
        #        self.ui.tableWidget.setItem(j,i,it)

        self.connect(self.ui.runButton, SIGNAL("clicked()"),self,SLOT("on_btnStart_clicked()"))
        #self.connect(self.ui.cancelButton, SIGNAL("clicked()"),self.cancelTh)

        self.th = None

        self.ui.verticalLayout_9.setAlignment(Qt.AlignTop)
        self.ui.tableWidget.hide()

        # remplissage du combo liste des analyses deja effectuées
        self.fillAnalysisCombo()
        QObject.connect(self.ui.analysisResultsButton,SIGNAL("clicked()"),self.viewAnalysisResult)

    def fillAnalysisCombo(self):
        self.ui.analysisListCombo.clear()
        if os.path.exists("%s/analysis/"%self.dir):
            l = os.listdir("%s/analysis/"%self.dir)
            for e in l:
                self.ui.analysisListCombo.addItem(e.replace('_',' '))

    def viewAnalysisResult(self):
        anDir = str(self.ui.analysisListCombo.currentText())
        if anDir.strip() != "":
            directory = anDir.replace(' ','_')
            if directory.split('_')[0] == 'estimation':
                self.drawAnalysisFrame = DrawEstimationAnalysisResult(directory,self)
            else:
                self.drawAnalysisFrame = DrawComparisonAnalysisResult(directory,self)
            self.ui.analysisStack.addWidget(self.drawAnalysisFrame)
            self.ui.analysisStack.setCurrentWidget(self.drawAnalysisFrame)


    def loadACP(self):
        """ charge le fichier ACP dans un dico
        et initialise les combo boxes
        """
        self.ui.ACProgress.setValue(0)

        f = open("docs/ACP.out","r")
        lines = f.readlines()
        f.close()
        self.dico_points = {}

        nb_composantes = (len(lines[0].split("  "))-1)
        nb_lignes = len(lines)

        # pour chaque ligne
        for i,l in enumerate(lines):
            pc = (float(i)/float(nb_lignes)*100)+1
            if (int(pc) % 2) == 0:
                self.ui.ACProgress.setValue(pc)
            tab = l.split("  ")
            num_sc = int(tab[0])
            # si le sc n'est pas encore dans le dico
            if num_sc not in self.dico_points.keys():
                self.dico_points[num_sc] = []
                # on y ajoute ce qui va etre la liste des coords pour chaque composante
                for j in range(nb_composantes):
                    self.dico_points[num_sc].append([])

            # on ajoute chaque coordonnée dans la composante correspondante
            c = 1
            while c < len(tab):
                #print "compo %s"%c
                #print "x: %s"%float(tab[c])
                #print "y: %s"%float(tab[c+1])
                self.dico_points[num_sc][c-1].append( float(tab[c]) )
                c+=1

            #if i == 10000: break

        # initialisation des combo
        self.ui.compoHCombo.clear()
        self.ui.compoVCombo.clear()
        for i in range(nb_composantes):
            self.ui.compoHCombo.addItem("%s"%(i+1))
            self.ui.compoVCombo.addItem("%s"%(i+1))
        if nb_composantes > 1:
            self.ui.compoHCombo.setCurrentIndex(0)
            self.ui.compoVCombo.setCurrentIndex(1)
        self.ui.scCombo.clear()
        self.ui.scCombo.addItem("all")
        for sc in self.dico_points.keys():
            if sc != 0:
                self.ui.scCombo.addItem("%s"%sc)

    def drawGraphToPlot(self,legend,plot,num_sc,compo_h,compo_v,nbp):
        """ dessine les points pour un scenario, deux components, sur plot et met à jour legend
        le tout limité à nbp points
        """
        legend_txt = "Scenario %s"%num_sc
        c = QwtPlotCurve(legend_txt)
        c.setStyle(QwtPlotCurve.Dots)
        c.setSymbol(QwtSymbol(Qwt.QwtSymbol.Ellipse,
              QBrush(QColor(self.tab_colors[(num_sc%20)])),
                QPen(Qt.black),
                  QSize(7, 7)))
        c.setData(self.dico_points[num_sc][compo_h][:nbp], self.dico_points[num_sc][compo_v][:nbp])
        c.attach(plot)
        c.updateLegend(legend)

    def drawObservedToPlot(self,legend,plot,compo_h,compo_v):
        """ dessine le point observé sur plot pour les deux components donnés
        """
        rp = QwtPlotCurve("Observed data set")
        rp.setStyle(QwtPlotCurve.Dots)
        rp.setSymbol(QwtSymbol(Qwt.QwtSymbol.Ellipse,
             QBrush(Qt.yellow),
               QPen(Qt.black),
                 QSize(17, 17)))
        rp.setData(self.dico_points[0][compo_h],self.dico_points[0][compo_v])
        rp.attach(plot)
        rp.updateLegend(legend)
        return rp

    def drawGraph(self):
        """ dessine le graphe entier en fonction des valeurs selectionnées
        """
        # on attend que les combo soient initialisés pour dessiner
        if self.ui.scCombo.currentText() != '':
            compo_h = int(self.ui.compoHCombo.currentText())-1
            compo_v = int(self.ui.compoVCombo.currentText())-1
            nbp = int(self.ui.nbpCombo.currentText())+1

            sc_txt = ""
            if self.ui.scCombo.currentText() != "all":
                sc_txt = "_sc_%s"%self.ui.scCombo.currentText()
            graph_file_name = "PCA_%s_%s_%s%s"%(self.ui.compoHCombo.currentText(),self.ui.compoVCombo.currentText(),self.ui.nbpCombo.currentText(),sc_txt)

            # le conteneur auquel on va ajouter des curves
            p = QwtPlot()
            p.setCanvasBackground(Qt.white)
            p.setTitle("Components %s and %s (%s)"%(compo_h+1,compo_v+1,graph_file_name))
            legend = QwtLegend()
            #legend.setItemMode(QwtLegend.CheckableItem)


            if self.ui.scCombo.currentText() == "all":
                for i in self.dico_points.keys():
                    # on ne fait pas le observed pour l'instant
                    if i != 0:
                        self.drawGraphToPlot(legend,p,i,compo_h,compo_v,nbp)
            else:
                num_sc = int(self.ui.scCombo.currentText())
                self.drawGraphToPlot(legend,p,num_sc,compo_h,compo_v,nbp)

            # on fait le observed à la fin pour qu'il soit au dessus des autres
            # et donc visible
            obs = self.drawObservedToPlot(legend,p,compo_h,compo_v)

            self.fancyfyGraph(legend,p,obs)
            p.insertLegend(legend,QwtPlot.RightLegend)
            pm = QwtPlotMagnifier(p.canvas())
            pp = QwtPlotPanner(p.canvas())
            #pz = QwtPlotZoomer(p.canvas())
            #ppi = QwtPlotPicker(p.canvas())
            p.setAxisTitle(0,"P.C.%s (50%%)"%(compo_v+1))
            p.setAxisTitle(2,"P.C.%s (60%%)"%(compo_h+1))
            p.replot()

            if self.ui.horizontalLayout_3.itemAt(0) != None:
                self.ui.horizontalLayout_3.itemAt(0).widget().hide()
            self.ui.horizontalLayout_3.removeItem(self.ui.horizontalLayout_3.itemAt(0))
            self.ui.horizontalLayout_3.addWidget(p)

    def fancyfyGraph(self,legend,p,obs):
        """ met en forme la légende et calcule l'intervale des divisions des axes
        """
        for it in legend.legendItems():
            f = it.font()
            f.setPointSize(14)
            it.setFont(f)
        litem = legend.find(obs)
        litem.symbol().setSize(QSize(17,17))
        litem.setIdentifierWidth(17)
        legend.setFrameShape(QFrame.Box)
        legend.setFrameShadow(QFrame.Raised)

        p.replot()
        sd = p.axisScaleDiv(0)
        interval = sd.interval()
        minv = interval.minValue()
        maxv = interval.maxValue()
        inc = 1.0
        if maxv-minv < 9:
            inc = 0.5
        if maxv-minv < 5:
            inc = 0.2
        if maxv-minv < 3:
            inc = 0.1
        ticks = []
        vv = minv
        while vv < maxv:
            ticks.append(round(vv,1))
            vv += inc
        #print sd.ticks(QwtScaleDiv.MajorTick)
        sd.setTicks(QwtScaleDiv.MajorTick,ticks)
        p.setAxisScaleDiv(0,sd)
        grid = QwtPlotGrid()
        grid.attach(p)

    def saveGraph(self):
        """ sauvegarde le graphe dans le dossier PCA_pictures du projet
        """
        if self.ui.horizontalLayout_3.itemAt(0) != None:
            proj_dir = self.dir
            graph_dir = self.parent.PCA_dir_name
            sc_txt = ""
            if self.ui.scCombo.currentText() != "all":
                sc_txt = "_sc_%s"%self.ui.scCombo.currentText()
            if not os.path.exists("%s/%s"%(proj_dir,graph_dir)):
                os.mkdir("%s/%s"%(proj_dir,graph_dir))

            graph_file_name = "refTable_PCA_%s_%s_%s%s"%(self.ui.compoHCombo.currentText(),self.ui.compoVCombo.currentText(),self.ui.nbpCombo.currentText(),sc_txt)
            if os.path.exists(graph_file_name):
                os.remove(graph_file_name)

            p = self.ui.horizontalLayout_3.itemAt(0).widget()

            pic_format = str(self.parent.preferences_win.ui.formatCombo.currentText())

            if pic_format == "svg":
                svg = QSvgGenerator()
                svg.setFileName("%s/%s/%s.svg"%(proj_dir,graph_dir,graph_file_name))
                svg.setSize(p.rect().size())

                painter = QPainter(svg)
                p.print_(painter, p.rect())
                painter.end()
            elif pic_format == "jpg" or pic_format == "png":
                pix = QPixmap(p.rect().size().width(),p.rect().size().height())
                pix.fill(Qt.white)

                painter = QPainter(pix)
                pen = QPen(Qt.black,2)
                painter.setPen(pen)
                p.print_(painter, p.rect())
                painter.end()
                im = pix.toImage()
                im.save("%s/%s/%s.%s"%(proj_dir,graph_dir,graph_file_name,pic_format))


    def defineNewAnalysis(self):
        """ démarre la définition d'une nouvelle analyse
        """
        def_analysis = DefineNewAnalysis(self)
        #self.addTab(def_analysis,"Define new analysis")

        #self.setTabEnabled(0,False)
        #self.setTabEnabled(1,False)
        #self.setCurrentWidget(def_analysis)
        self.ui.analysisStack.addWidget(def_analysis)
        self.ui.analysisStack.setCurrentWidget(def_analysis)

    def genMasterScript(self):
        """ génération du script à exécuter sur le noeud maitre
        """
        nbToGen = int(self.ui.nbSetsReqEdit.text())
        nbFullQsub = nbToGen / 10000
        nbLastQsub = nbToGen % 10000

        if nbLastQsub == 0:
            nbQsub = nbFullQsub
        else:
            nbQsub = nbFullQsub+1

        res = '\n\
function progress(){\n\
res=0\n\
nbfin=%s\n\
sum=0\n\
# for each log file, if it exists, do the sum of done values\n\
for i in $(seq 1 $1); do\n\
    if [ -e reftable_$i.log ]; then\n\
        let sum=$sum+`head -n 2 reftable_$i.log | tail -n 1`\n\
    fi\n\
done\n\
let pct=$sum*100\n\
let pct=$pct/$nbfin\n\
echo `nbOk $1` "/ $1 finished"\n\
echo " $pct %%"\n\
echo "somme $sum"\n\
}\n\
function nbOk(){\n\
nb=0\n\
# for each log file, check if the computation is terminated\n\
for i in $(seq 1 $1); do\n\
    if [ -e reftable_$i.log ]; then\n\
        numdone=`head -n 2 reftable_$i.log | tail -n 1`\n'%nbToGen

        if nbLastQsub != 0:
            res+='        # case of last computation, less thant 10000\n\
        if [ $i -eq %s ]; then\n\
            if [ $numdone -eq %s ]; then\n\
                let nb=$nb+1\n\
            fi\n\
        else\n\
            if [ $numdone -eq 10000 ]; then\n\
                let nb=$nb+1\n\
            fi\n\
        fi\n'%(nbFullQsub+1,nbLastQsub)
        else:
            res+='        if [ $numdone -eq 10000 ]; then\n\
            let nb=$nb+1\n\
        fi\n'

        res+='    fi\n\
done\n\
echo $nb\n\
}\n\
for i in $(seq 1 %s); do \n\
qsub -q short_queue.q -cwd node.sh 10000 `pwd` $i\n\
done;\n'%nbFullQsub
        
        if nbLastQsub != 0:
            res+='let last=$i+1\n\
qsub -q short_queue.q -cwd node.sh %s `pwd` $last\n'%nbLastQsub
        
        res+='while ! [ "`nbOk %s`" = "%s" ]; do\n\
echo `progress %s`\n\
sleep 3\n\
done\n\
echo `progress %s`\n\
./general -p "`pwd`"/ -q\n\
'%(nbQsub,nbQsub,nbQsub,nbQsub)
        
        return res

    def genNodeScript(self):
        """ génération du script a exécuter sur chaque noeud
        """

        return 'if ! [ -d $TMPDIR ]; then mkdir -p $TMPDIR ; fi \n\
cp general $TMPDIR\n\
cp %s $TMPDIR\n\
cp %s $TMPDIR\n\
$TMPDIR/general -s "$3" -p $TMPDIR/ -r $1 & \n\
while ! [ "`head -n 2 $TMPDIR/reftable.log | tail -n 1`" -eq $1 ]; do\n\
    cp $TMPDIR/reftable.log $2/reftable_$3.log\n\
    sleep 5\n\
done\n\
cp $TMPDIR/reftable.bin $2/reftable_$3.bin\n\
cp $TMPDIR/reftable.log $2/reftable_$3.log\n\
'%(self.parent.reftableheader_name, self.dataFileName)

    def generateComputationTar(self,tarname=None):
        """ génère une archive tar contenant l'exécutable, les scripts node et master,
        le datafile et le reftableheader.
        """
        if tarname == None:
            tarname = str(QFileDialog.getSaveFileName(self,"Saving","Reftable generation archive","(TAR archive) *.tar"))
        if tarname != "":
            executablePath = str(self.parent.preferences_win.ui.execPathEdit.text())
            # generation du master script
            script = self.genMasterScript()
            if os.path.exists('scmf'):
                os.remove('scmf')
            scmf = open('scmf','w')
            scmf.write(script)
            scmf.close()
            os.chmod('scmf',stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IWOTH|stat.S_IXOTH)
            tar = tarfile.open(tarname,"w")
            # generation du node script
            script = self.genNodeScript()
            if os.path.exists('scnf'):
                os.remove('scnf')
            scnf = open('scnf','w')
            scnf.write(script)
            scnf.close()
            os.chmod('scnf',stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IWOTH|stat.S_IXOTH)

            # ajout des fichiers dans l'archive
            tarRepName = self.dir.split('/')[-1]
            if os.path.exists(tarname):
                os.remove(tarname)
            tar = tarfile.open(tarname,"w")
            tar.add('scmf','%s/launch.sh'%tarRepName)
            tar.add('scnf','%s/node.sh'%tarRepName)
            tar.add("%s/%s"%(self.dir,self.parent.reftableheader_name),"%s/%s"%(tarRepName,self.parent.reftableheader_name))
            tar.add(self.dataFileSource,"%s/%s"%(tarRepName,self.dataFileName))
            tar.add(executablePath,"%s/general"%tarRepName)
            tar.close()

            # nettoyage des fichiers temporaires de script
            if os.path.exists('scmf'):
                os.remove('scmf')
            if os.path.exists('scnf'):
                os.remove('scnf')

        return tarname

    @pyqtSignature("")
    def on_btnStart_clicked(self):
        """ Lance un thread de generation de la reftable
        """
        self.writeRefTableHeader()
        tname = self.generateComputationTar("/tmp/aaaa.tar")
        if self.th == None:
            try:
                nb_to_gen = int(self.ui.nbSetsReqEdit.text())
            except Exception,e:
                output.notify(self,"value error","Check the value of required number of data sets")
                return
            # on demarre le thread local ou cluster
            if self.parent.preferences_win.ui.serverCheck.isChecked():
                self.th = RefTableGenThreadCluster(self,tname,nb_to_gen)
            else:
                self.th = RefTableGenThread(self,nb_to_gen)
            self.th.connect(self.th,SIGNAL("increment"),self.incProgress)
            self.th.connect(self.th,SIGNAL("refTableProblem"),self.refTableProblem)
            #self.ui.progressBar.connect (self, SIGNAL("canceled()"),self.th,SLOT("cancel()"))
            self.th.start()
        else:
            # si l'ancien thread a fini, on en relance un
            if not self.th.isRunning():
                self.th = None
                self.on_btnStart_clicked()
            #self.cancelTh()

    def refTableProblem(self):
        output.notify(self,"reftable problem","Something append during the reftable generation : %s"%(self.th.problem))
 
    def incProgress(self):
        """Increment the progress dialog"""
        done = self.th.nb_done
        nb_to_do = self.th.nb_to_gen
        pc = (float(done)/float(nb_to_do))*100
        self.ui.progressBar.setValue(int(pc))
        self.ui.nbSetsDoneEdit.setText("%s"%done)
        # si on a fini, on met à jour l'affichage de la taille de la reftable
        # et on verrouille eventuellement histmodel et gendata
        if int(pc) == 100:
            self.putRefTableSize()

    def cancelTh(self):
        #print 'plop'
        self.emit(SIGNAL("canceled()"))

    def writeRefTableHeader(self):
        """ écriture du header.txt à partir des conf
        """
        if os.path.exists(self.dir+"/%s"%self.parent.main_conf_name) and os.path.exists(self.dir+"/%s"%self.parent.hist_conf_name) and os.path.exists(self.dir+"/%s"%self.parent.gen_conf_name) and os.path.exists(self.dir+"/%s"%self.parent.table_header_conf_name):
            if os.path.exists(self.dir+"/%s"%self.parent.reftableheader_name):
                os.remove("%s/%s" %(self.dir,self.parent.reftableheader_name))
            f1 = codecs.open(self.dir+"/%s"%self.parent.main_conf_name,"r","utf-8")
            f1lines = f1.read()
            f1.close()
            f2 = codecs.open(self.dir+"/%s"%self.parent.hist_conf_name,"r","utf-8")
            f2lines = f2.read()
            f2.close()
            f3 = codecs.open(self.dir+"/%s"%self.parent.gen_conf_name,"r","utf-8")
            f3lines = f3.read()
            f3.close()
            f4 = codecs.open(self.dir+"/%s"%self.parent.table_header_conf_name,"r","utf-8")
            f4lines = f4.read()
            f4.close()

            f = codecs.open(self.dir+"/%s"%self.parent.reftableheader_name,"w","utf-8")
            f.write(f1lines)
            f.write(f2lines)
            f.write(f3lines)
            f.write(f4lines)
            f.close()
        else:
            output.notify(self,"Header generation problem","One conf file is missing in order to generate the reference table header")


    def dataFileSelection(self,name=None):
        """ dialog pour selectionner le fichier à lire
        il est lu et vérifié. S'il est invalide, on garde la sélection précédente
        """
        if name == None:
            qfd = QFileDialog()
            qfd.setDirectory(self.ui.dirEdit.text())
            name = qfd.getOpenFileName()
        if self.loadDataFile(name):
            # si on a reussi a charger le data file, on vire le bouton browse
            self.ui.browseDataFileButton.hide()
        # comme on a lu le datafile, on peut remplir le tableau de locus dans setGeneticData
        self.gen_data_win.fillLocusTableFromData()

    def loadDataFile(self,name):
        """ Charge le fichier de données passé en paramètre. Cette fonction est appelée lors
        de l'ouverture d'un projet existant et lors du choix du fichier de données pour un nouveau projet
        """
        new_data = Data(name)
        try:
            new_data.loadfromfile()
            # on ne garde le data que si le load n'a pas déclenché d'exception
            self.data = new_data
            microsat = ""
            sequences = ""
            et = ""
            if self.data.nloc_mic > 0:
                microsat = "%s microsat"%self.data.nloc_mic
            if self.data.nloc_seq > 0:
                sequences = "%s sequences"%self.data.nloc_seq
            if self.data.nloc_mic > 0 and self.data.nloc_seq > 0:
                et = " and "
            self.ui.dataFileInfoLabel.setText("%s loci (%s%s%s)\n%s individuals in %s samples" % (self.data.nloc,microsat,et,sequences,self.data.nindtot,self.data.nsample))
            self.ui.dataFileEdit.setText(name)
            self.dataFileSource = name
            self.ui.browseDirButton.setDisabled(False)
        except Exception,e:
            keep = ""
            if self.ui.dataFileEdit.text() != "":
                #keep = "\n\nKeeping previous selected file"
                keep = "\n\nThe file was not loaded, nothing was changed"
            output.notify(self,"Data file error","%s%s"%(e,keep))
            return False
        return True


    def dirSelection(self,name=None):
        """ selection du repertoire pour un nouveau projet et copie du fichier de données
        """
        if name == None:
            qfd = QFileDialog()
            #qfd.setDirectory("~/")
            name = str(qfd.getExistingDirectory())
        if name != "":
            if not self.parent.isProjDir(name):
                # name_YYYY_MM_DD-num le plus elevé
                dd = datetime.now()
                #num = 36
                cd = 100
                while cd > 0 and not os.path.exists(name+"/%s_%i_%i_%i-%i"%(self.name,dd.year,dd.month,dd.day,cd)):
                    cd -= 1
                if cd == 100:
                    output.notify(self,"Error","With this version, you cannot have more than 100 \
                                project directories\nfor the same project name and in the same directory")
                else:
                    newdir = name+"/%s_%i_%i_%i-%i"%(self.name,dd.year,dd.month,dd.day,(cd+1))
                    self.ui.dirEdit.setText(newdir)
                    try:
                        os.mkdir(newdir)
                        self.ui.groupBox.show()
                        self.ui.setHistoricalButton.setDisabled(False)
                        self.ui.setGeneticButton.setDisabled(False)
                        self.dir = newdir
                        shutil.copy(self.dataFileSource,"%s/%s"%(self.dir,self.dataFileSource.split('/')[-1]))
                        self.dataFileName = self.dataFileSource.split('/')[-1]
                        # verrouillage du projet
                        self.lock()
                        # on a reussi a creer le dossier, on vire le bouton browse
                        self.ui.browseDirButton.hide()
                    except OSError,e:
                        output.notify(self,"Error",str(e))
            else:
                output.notify(self,"Incorrect directory","A project can not be in a project directory")

    def addAnalysis(self,analysis):
        """ ajoute, dans la liste d'analyses et dans la GUI , l'analyse passée en paramètre
        """
        type_analysis = analysis.category
        self.analysisList.append(analysis)

        print analysis.computationParameters
        if type_analysis == "pre-ev":
            #self.addRow("scenario prior combination",analysis[1],"4","new")
            self.addAnalysisGui(analysis,analysis.name,"scenario prior combination",analysis.computationParameters,"new")
        elif type_analysis == "estimate":
            print "\n",analysis.computationParameters,"\n"
            #self.addRow("parameter estimation","params","5","new")
            self.addAnalysisGui(analysis,analysis.name,"parameter estimation","params","new")
        elif type_analysis == "bias":
            #self.addRow("bias and precision",str(analysis[2]),"3","new")
            self.addAnalysisGui(analysis,analysis.name,"bias and precision",str(analysis.chosenSc),"new")
        elif type_analysis == "compare":
            #print "\n",analysis[-1],"\n"
            #self.addRow("scenario choice",analysis[2]["de"],"4","new")
            self.addAnalysisGui(analysis,analysis.name,"scenario choice","%s | %s"%(analysis.candidateScList,analysis.chosenSc),"new")
        elif type_analysis == "evaluate":
            #self.addRow("evaluate confidence","%s | %s"%(analysis[2],analysis[3]),"3","new")
            self.addAnalysisGui(analysis,analysis.name,"evaluate confidence","%s | %s"%(analysis.candidateScList,analysis.chosenSc),"new")

    def addAnalysisGui(self,analysis,name,atype,params,status):

        frame_9 = QtGui.QFrame(self.ui.scrollAreaWidgetContents)
        frame_9.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_9.setFrameShadow(QtGui.QFrame.Raised)
        frame_9.setObjectName("frame_9")
        frame_9.setMinimumSize(QtCore.QSize(0, 32))
        frame_9.setMaximumSize(QtCore.QSize(9999, 32))
        horizontalLayout_4 = QtGui.QHBoxLayout(frame_9)
        horizontalLayout_4.setObjectName("horizontalLayout_4")
        analysisUpButton = QtGui.QPushButton("up",frame_9)
        analysisUpButton.setMinimumSize(QtCore.QSize(50, 0))
        analysisUpButton.setMaximumSize(QtCore.QSize(50, 16777215))
        analysisUpButton.setObjectName("analysisUpButton")
        horizontalLayout_4.addWidget(analysisUpButton)
        analysisDownButton = QtGui.QPushButton("down",frame_9)
        analysisDownButton.setMinimumSize(QtCore.QSize(50, 0))
        analysisDownButton.setMaximumSize(QtCore.QSize(50, 16777215))
        analysisDownButton.setObjectName("analysisDownButton")
        horizontalLayout_4.addWidget(analysisDownButton)
        analysisNameLabel = QtGui.QLabel(name,frame_9)
        analysisNameLabel.setAlignment(Qt.AlignCenter)
        analysisNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        analysisNameLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        analysisNameLabel.setObjectName("analysisNameLabel")
        analysisNameLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        analysisNameLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        horizontalLayout_4.addWidget(analysisNameLabel)
        analysisTypeLabel = QtGui.QLabel(atype,frame_9)
        analysisTypeLabel.setAlignment(Qt.AlignCenter)
        analysisTypeLabel.setObjectName("analysisTypeLabel")
        analysisTypeLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        analysisTypeLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        analysisTypeLabel.setMinimumSize(QtCore.QSize(200, 0))
        horizontalLayout_4.addWidget(analysisTypeLabel)
        analysisParamsLabel = QtGui.QLabel(str(params),frame_9)
        analysisParamsLabel.setAlignment(Qt.AlignCenter)
        analysisParamsLabel.setObjectName("analysisParamsLabel")
        analysisParamsLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        analysisParamsLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        analysisParamsLabel.setMinimumSize(QtCore.QSize(200, 0))
        horizontalLayout_4.addWidget(analysisParamsLabel)
        analysisStatusLabel = QtGui.QLabel(status,frame_9)
        analysisStatusLabel.setMinimumSize(QtCore.QSize(40, 0))
        analysisStatusLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        analysisStatusLabel.setAlignment(Qt.AlignCenter)
        analysisStatusLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        analysisStatusLabel.setObjectName("analysisStatusLabel")
        analysisParamsLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        horizontalLayout_4.addWidget(analysisStatusLabel)
        analysisButton = QtGui.QPushButton("launch",frame_9)
        analysisButton.setObjectName("analysisButton")
        analysisButton.setMinimumSize(QtCore.QSize(70, 0))
        analysisButton.setMaximumSize(QtCore.QSize(70, 16777215))
        horizontalLayout_4.addWidget(analysisButton)
        horizontalLayout_4.setContentsMargins(-1, 1, -1, 1)
        self.ui.verticalLayout_9.addWidget(frame_9)

        self.dicoFrameAnalysis[frame_9] = analysis
        QObject.connect(analysisDownButton,SIGNAL("clicked()"),self.moveAnalysisDown)
        QObject.connect(analysisUpButton,SIGNAL("clicked()"),self.moveAnalysisUp)
        QObject.connect(analysisButton,SIGNAL("clicked()"),self.launchAnalysis)

    def launchAnalysis(self):
        """ clic sur le bouton launch d'une analyse
        """
        if not os.path.exists("%s/analysis/"%self.dir):
            os.mkdir("%s/analysis/"%self.dir)

        frame = self.sender().parent()
        # on associe l'analyse a sa frame
        analysis = self.dicoFrameAnalysis[frame]
        self.thAnalysis = AnalysisThread(self,analysis)
        self.thAnalysis.connect(self.thAnalysis,SIGNAL("analysisProgress"),self.analysisProgress)
        self.thAnalysis.start()
        frame.findChild(QPushButton,"analysisButton").setText("Running")

    def analysisProgress(self):
        """ met à jour l'indicateur de progression de l'analyse en cours
        """
        prog = self.thAnalysis.progress
        frame = None
        for fr in self.dicoFrameAnalysis.keys():
            if self.dicoFrameAnalysis[fr] == self.thAnalysis.analysis:
                frame = fr
                break
        frame.findChild(QLabel,"analysisStatusLabel").setText("%s%%"%prog)

        if str(prog) == "100":
            print "terminate analysis"
            frame.findChild(QPushButton,"analysisButton").setText("Done")
            self.terminateAnalysis()

    def terminateAnalysis(self):
        """ arrête le thread de l'analyse et range les résultats
        dans un dossier
        """
        self.thAnalysis.terminate()
        aid = self.thAnalysis.analysis.name
        atype = self.thAnalysis.analysis.category
        self.thAnalysis = None

        if atype == "estimate":
            if os.path.exists("%s/%s_phistar.txt"%(self.dir,aid))\
                    and os.path.exists("%s/%s_paramstatdens.txt"%(self.dir,aid)):
                # deplacement des fichiers de résultat
                aDirName = "estimation_%s"%aid
                os.mkdir("%s/analysis/%s"%(self.dir,aDirName))
                shutil.move("%s/%s_phistar.txt"%(self.dir,aid),"%s/analysis/%s/phistar.txt"%(self.dir,aDirName))
                shutil.move("%s/%s_paramstatdens.txt"%(self.dir,aid),"%s/analysis/%s/paramstatdens.txt"%(self.dir,aDirName))
                shutil.move("%s/%s_psd.txt"%(self.dir,aid),"%s/analysis/%s/psd.txt"%(self.dir,aDirName))
                os.remove("%s/%s_progress.txt"%(self.dir,aid))

        if atype == "compare":
            if os.path.exists("%s/%s_compdirect.txt"%(self.dir,aid)) and\
                    os.path.exists("%s/%s_complogreg.txt"%(self.dir,aid)):
                # deplacement des fichiers de résultat
                aDirName = "comparison_%s"%aid
                os.mkdir("%s/analysis/%s"%(self.dir,aDirName))
                shutil.move("%s/%s_compdirect.txt"%(self.dir,aid),"%s/analysis/%s/compdirect.txt"%(self.dir,aDirName))
                shutil.move("%s/%s_complogreg.txt"%(self.dir,aid),"%s/analysis/%s/complogreg.txt"%(self.dir,aDirName))
                os.remove("%s/%s_progress.txt"%(self.dir,aid))

        # on met à jour la liste des analyses terminées
        self.fillAnalysisCombo()



    def moveAnalysisDown(self):
        """ déplace d'un cran vers le bas une analyse
        """
        frame = self.sender().parent()
        cur_index = self.ui.verticalLayout_9.indexOf(frame)
        nb_items = self.ui.verticalLayout_9.count()
        if cur_index < (nb_items-1):
            self.ui.verticalLayout_9.removeWidget(frame)
            self.ui.verticalLayout_9.insertWidget(cur_index+1,frame)

    def moveAnalysisUp(self):
        """ déplace d'un cran vers le haut une analyse
        """
        frame = self.sender().parent()
        cur_index = self.ui.verticalLayout_9.indexOf(frame)
        if cur_index > 0:
            self.ui.verticalLayout_9.removeWidget(frame)
            self.ui.verticalLayout_9.insertWidget(cur_index-1,frame)

    def addRow(self,atype,params,prio,status):
        """ ajoute une ligne dans le tableau d'analyses
        """
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,1,QTableWidgetItem("%s"%atype))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,2,QTableWidgetItem("%s"%params))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,3,QTableWidgetItem("%s"%prio))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,4,QTableWidgetItem("%s"%status))

        self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,1).setFlags(self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,1).flags() & ~Qt.ItemIsEditable)
        self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,2).setFlags(self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,2).flags() & ~Qt.ItemIsEditable)
        self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,4).setFlags(self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,4).flags() & ~Qt.ItemIsEditable)

        self.ui.tableWidget.setCellWidget(self.ui.tableWidget.rowCount()-1,5,QPushButton("View"))
            #self.ui.tableWidget.item(self.ui.tableWidget.rowCount()-1,i).setText("new")
        #self.ui.tableWidget.insertRow(2)

    def setHistorical(self):
        """ passe sur l'onglet correspondant
        """
        #self.addTab(self.hist_model_win,"Set historical model")

        #self.setTabEnabled(0,False)
        #self.setTabEnabled(1,False)
        ## nécéssaire seulement sous windows
        ## on dirait que sous linux, le simple setCurrentWidget rend l'onglet enabled
        #self.setTabEnabled(self.count()-1,True)
        #self.setCurrentWidget(self.hist_model_win)
        self.ui.refTableStack.addWidget(self.hist_model_win)
        self.ui.refTableStack.setCurrentWidget(self.hist_model_win)
        self.setHistValid(False)

    def setGenetic(self):
        """ passe sur l'onglet correspondant
        """
        #self.setTabEnabled(0,False)
        #self.setTabEnabled(1,False)
        #self.addTab(self.gen_data_win,"Set genetic data")
        #self.setCurrentWidget(self.gen_data_win)
        self.ui.refTableStack.addWidget(self.gen_data_win)
        self.ui.refTableStack.setCurrentWidget(self.gen_data_win)
        self.setGenValid(False)

    def setNbScenarios(self,nb):
        """ ecrit le nombre de scenarios dans la zone "historical model"
        """
        self.ui.nbScLabel.setText(nb)

    def setNbParams(self,nb):
        """ écrit le nombre de paramètres dans la zone "historical model"
        """ 
        self.ui.nbParamLabel.setText(nb)

    def clearHistoricalModel(self):
        """ détruit le modèle historique et en instancie un nouveau
        """
        #self.removeTab(self.indexOf(self.hist_model_win))
        self.ui.refTableStack.removeWidget(self.hist_model_win)
        self.hist_model_win = SetHistoricalModel(self)
        #self.insertTab(2,self.hist_model_win,"Set historical model")
        self.ui.refTableStack.insertWidget(0,self.hist_model_win)
        #self.setCurrentWidget(self.hist_model_win)
        self.ui.refTableStack.setCurrentWidget(self.hist_model_win)

    def loadFromDir(self):
        """ charge les infos à partir du répertoire self.dir
        """
        # GUI
        self.ui.dirEdit.setText(self.dir)
        self.ui.browseDataFileButton.setDisabled(True)
        self.ui.browseDataFileButton.hide()
        self.ui.browseDirButton.hide()
        self.ui.groupBox.show()
        self.ui.setHistoricalButton.setDisabled(False)
        self.ui.setGeneticButton.setDisabled(False)

        # lecture du meta project
        if self.loadMyConf():
            # lecture de conf.hist.tmp
            self.hist_model_win.loadHistoricalConf()
            self.gen_data_win.loadGeneticConf()
            self.loadAnalysis()
        else:
            output.notify(self,"Load error","Impossible to read the project configuration")

    def putRefTableSize(self):
        """ met à jour l'affichage de la taille de la reftable
        et verrouille les modèles hist et gen si une reftable existe
        """
        size = self.readRefTableSize()
        if size != None:
            self.ui.nbSetsDoneEdit.setText("%s"%size)
            self.freezeHistModel()
            self.freezeGenData()

    def freezeGenData(self,yesno=True):
        self.gen_data_win.ui.clearButton.setDisabled(yesno)
        self.gen_data_win.ui.exitButton.setDisabled(yesno)
        self.gen_data_win.ui.tableWidget.setDisabled(yesno)
        self.gen_data_win.ui.addGroupButton.setDisabled(yesno)
        for g in self.gen_data_win.groupList:
            for b in g.findChildren(QPushButton,"rmFromButton"):
                b.setDisabled(yesno)
            for b in g.findChildren(QPushButton,"addToButton"):
                b.setDisabled(yesno)
            for b in g.findChildren(QPushButton,"rmButton"):
                b.setDisabled(yesno)

            for e in self.gen_data_win.setMutation_dico[g].findChildren(QLineEdit):
                e.setDisabled(yesno)
            for e in self.gen_data_win.setMutation_dico[g].findChildren(QRadioButton):
                e.setDisabled(yesno)
            self.gen_data_win.setMutation_dico[g].ui.clearButton.setDisabled(yesno)
            self.gen_data_win.setMutation_dico[g].ui.exitButton.setDisabled(yesno)

            for e in self.gen_data_win.setMutationSeq_dico[g].findChildren(QLineEdit):
                e.setDisabled(yesno)
            for e in self.gen_data_win.setMutationSeq_dico[g].findChildren(QRadioButton):
                e.setDisabled(yesno)
            self.gen_data_win.setMutationSeq_dico[g].ui.clearButton.setDisabled(yesno)
            self.gen_data_win.setMutationSeq_dico[g].ui.exitButton.setDisabled(yesno)

            for e in self.gen_data_win.setSum_dico[g].findChildren(QLineEdit):
                e.setDisabled(yesno)
            for e in self.gen_data_win.setSum_dico[g].findChildren(QCheckBox):
                e.setDisabled(yesno)
            self.gen_data_win.setSum_dico[g].ui.clearButton.setDisabled(yesno)
            self.gen_data_win.setSum_dico[g].ui.exitButton.setDisabled(yesno)
            self.gen_data_win.setSum_dico[g].ui.addAdmixButton.setDisabled(yesno)

            for e in self.gen_data_win.setSumSeq_dico[g].findChildren(QLineEdit):
                e.setDisabled(yesno)
            for e in self.gen_data_win.setSumSeq_dico[g].findChildren(QCheckBox):
                e.setDisabled(yesno)
            self.gen_data_win.setSumSeq_dico[g].ui.clearButton.setDisabled(yesno)
            self.gen_data_win.setSumSeq_dico[g].ui.exitButton.setDisabled(yesno)
            self.gen_data_win.setSumSeq_dico[g].ui.addAdmixButton.setDisabled(yesno)

    def freezeHistModel(self,yesno=True):
        self.hist_model_win.ui.clearButton.setDisabled(yesno)
        self.hist_model_win.ui.exitButton.setDisabled(yesno)
        for e in self.hist_model_win.findChildren(QLineEdit):
            e.setReadOnly(yesno)
        for e in self.hist_model_win.findChildren(QRadioButton):
            e.setDisabled(yesno)
        for e in self.hist_model_win.findChildren(QPushButton,"remove"):
            e.setDisabled(yesno)
        self.hist_model_win.findChild(QPushButton,"addScButton").setDisabled(yesno) 
        self.hist_model_win.findChild(QPushButton,"defPrButton").setDisabled(yesno)
        for param in self.hist_model_win.paramList:
            for e in param.findChildren(QLineEdit):
                e.setReadOnly(yesno)
            for e in param.findChildren(QPushButton):
                e.setDisabled(yesno)
        for e in self.hist_model_win.findChildren(QPlainTextEdit):
            e.setReadOnly(yesno)

    def readRefTableSize(self):
        """ lit la table de référence binaire pour en extraire la taille et la retourner
        """
        reftablefile = "%s/reftable.bin"%self.dir
        if os.path.exists(reftablefile):
            binint = array.array('i')
            f = open(reftablefile,'rb')
            binint.read(f,1)
            f.close()
            rtSize = binint[0]
            return rtSize
        else:
            return None


    def loadMyConf(self):
        """ lit le fichier conf.tmp pour charger le fichier de données
        """
        if os.path.exists(self.ui.dirEdit.text()+"/%s"%self.parent.main_conf_name):
            f = open("%s/%s"%(self.dir,self.parent.main_conf_name),"r")
            lines = f.readlines()
            self.dataFileName = lines[0].strip()
            self.ui.dataFileEdit.setText(lines[0].strip())
            # lecture du dataFile pour les infos de Gui Projet
            self.loadDataFile("%s/%s"%(self.dir,lines[0].strip()))
            # comme on a lu le datafile, on peut remplir le tableau de locus dans setGeneticData
            self.gen_data_win.fillLocusTableFromData()
            return True
        return False


    def saveAnalysis(self):
        l_to_save = []
        for a in self.analysisList:
            l_to_save.append(a)
        f=open("%s/%s"%(self.dir,self.parent.analysis_conf_name),"wb")
        pickle.dump(l_to_save,f)
        f.close()

    def loadAnalysis(self):
        if os.path.exists("%s/%s"%(self.dir,self.parent.analysis_conf_name)):
            f=open("%s/%s"%(self.dir,self.parent.analysis_conf_name),"rb")
            l = pickle.load(f)
            f.close()
            for a in l:
                self.addAnalysis(a)

    def save(self):
        """ sauvegarde du projet -> mainconf, histconf, genconf, theadconf
        Si le gen et hist sont valides, on génère le header
        """
        #print "je me save"
        if self.dir != None:
            # save meta project
            if os.path.exists(self.dir+"/%s"%self.parent.main_conf_name):
                os.remove("%s/%s"%(self.dir,self.parent.main_conf_name))

            f = codecs.open(self.dir+"/%s"%self.parent.main_conf_name,'w',"utf-8")
            f.write("%s\n"%self.dataFileName)
            # recup du nombre de params (depuis historical model et les mutational qui varient)
            nb_param = self.hist_model_win.getNbParam()
            nb_param += self.gen_data_win.getNbParam()
            nb_sum_stats = self.gen_data_win.getNbSumStats()
            f.write("%s parameters and %s summary statistics\n\n"%(nb_param,nb_sum_stats))
            f.close()

            # save hist conf
            self.hist_model_win.writeHistoricalConfFromGui()
            # save gen conf
            self.gen_data_win.writeGeneticConfFromGui()
            # save th conf et production du reftable header
            if self.gen_state_valid and self.hist_state_valid:
                self.writeThConf()
                self.writeRefTableHeader()
            self.saveAnalysis()
        else:
            output.notify(self,"Saving is impossible","Choose a directory before saving the project")

    def writeThConf(self):
        """ ecrit le header du tableau de resultat qui sera produit par les calculs
        il contient, les paramètres historicaux, les paramètres mutationnels, les summary stats
        """
        hist_params_txt = self.hist_model_win.getParamTableHeader()
        mut_params_txt = self.gen_data_win.getParamTableHeader()
        sum_stats_txt = self.gen_data_win.getSumStatsTableHeader()
        if os.path.exists(self.dir+"/%s"%self.parent.table_header_conf_name):
            os.remove("%s/%s"%(self.dir,self.parent.table_header_conf_name))
        f = codecs.open(self.dir+"/%s"%self.parent.table_header_conf_name,'w',"utf-8")
        f.write("scenario    %s%s%s"%(hist_params_txt,mut_params_txt,sum_stats_txt))
        f.close()


    def setHistValid(self,valid):
        """ met à jour l'état du modèle historique
        et change l'icone du bouton en fonction de sa validité
        """
        self.hist_state_valid = valid
        self.verifyRefTableValid()
        if valid:
            self.ui.setHistoricalButton.setIcon(QIcon("docs/ok.png"))
        else:
            self.ui.setHistoricalButton.setIcon(QIcon("docs/redcross.png"))

    def setGenValid(self,valid):
        """ met à jour l'état des genetic data
        et change l'icone du bouton en fonction de la validité
        """
        self.gen_state_valid = valid
        self.verifyRefTableValid()
        if valid:
            self.ui.setGeneticButton.setIcon(QIcon("docs/ok.png"))
        else:
            self.ui.setGeneticButton.setIcon(QIcon("docs/redcross.png"))

    def verifyRefTableValid(self):
        """ Vérifie si tout est valide pour mettre à jour l'icone de l'onglet reference table
        """
        if self.gen_state_valid and self.hist_state_valid:
            self.setTabIcon(0,QIcon("docs/ok.png"))
            self.ui.runButton.setDisabled(False)
        else:
            self.setTabIcon(0,QIcon("docs/redcross.png"))
            self.ui.runButton.setDisabled(True)

    def lock(self):
        """ crée le fichier de verrouillage pour empêcher l'ouverture 
        du projet par une autre instance de DIYABC
        """
        f = open("%s/.DIYABC_lock"%self.dir,"w")
        f.write("%s"%os.getpid())
        f.close()

    def unlock(self):
        """ supprime le verrouillage sur le projet ssi le verrouillage 
        a été effectué par notre instance de DIYABC
        """
        if os.path.exists("%s/.DIYABC_lock"%self.dir):
            f = open("%s/.DIYABC_lock"%self.dir)
            pid = f.read()
            f.close()
            # on ne deverrouille que si c'est nous qui avons verrouillé
            if pid == str(os.getpid()):
                os.remove("%s/.DIYABC_lock"%self.dir)

    def checkAll(self):
        """ vérification du modèle historique et mutationnel
        cette fonction est appelée au chargement du projet pour restituer l'etat du projet
        """
        # historical model : 
        self.hist_model_win.definePriors(silent=True)
        if self.hist_model_win.checkAll(silent=True):
            self.setHistValid(True)
            self.hist_model_win.majProjectGui()
        # mutation model : plus facile d'utiliser directement la validation
        self.gen_data_win.validate(silent=True)

class RefTableGenThreadCluster(QThread):
    """ thread de traitement qui met à jour la progressBar en fonction de l'avancée de
    la génération de la reftable sur le cluster
    """
    def __init__(self,parent,tarname,nb_to_gen):
        super(RefTableGenThreadCluster,self).__init__(parent)
        self.parent = parent
        self.tarname = tarname
        self.nb_done = 0
        self.nb_to_gen = nb_to_gen


    def run (self):
        filename = self.tarname
        host = str(self.parent.parent.preferences_win.ui.addrEdit.text())
        port = int(str(self.parent.parent.preferences_win.ui.portEdit.text()))


        f=open(filename, 'rb')
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((host, port))
        except error,msg:
            print "could not contact any server on %s:%s"%(host, port)
            return

        #size = os.path.getsize(filename)
        #s.send(str(size))

        data = f.read()
        f.close()
        s.send("%s"%str(hashlib.md5(data).hexdigest()))
        size = str(len(data))
        while len(size)<20:
            size+=" "
        s.send("%s"%size)
        time.sleep(1)

        s.sendall(data)
        #s.shutdown(SHUT_WR)


        #while True:
        #    if not data:
        #        break
        #    else:
        #        s.sendall(data)

        print filename, " Sent!\n"
        while True:
            line = s.recv(8000)
            print line
            if len(line.split('somme '))>1:
                self.nb_done = int(line.split('somme ')[1].strip())
                self.emit(SIGNAL("increment"))
            if "durée" in line:
                self.nb_done = int(str(self.parent.ui.nbSetsReqEdit.text()))
                self.emit(SIGNAL("increment"))
            # TODO fix on ne va pas jusqu'à 100 parce qu'on lit la ligne du temps de merge au lieu de la derniere (modifs dans launch)
            if self.nb_done == int(str(self.parent.ui.nbSetsReqEdit.text())):
                break

        s.close()

class RefTableGenThread(QThread):
    """ thread de traitement qui met à jour la progressBar en fonction de l'avancée de
    la génération de la reftable
    """
    def __init__(self,parent,nb_to_gen):
        super(RefTableGenThread,self).__init__(parent)
        self.parent = parent
        self.nb_to_gen = nb_to_gen
        self.cancel = False

    def run (self):
        # lance l'executable
        try:
            #print "/home/julien/vcs/git/diyabc/src-JMC-C++/gen -r %s -p %s"%(self.nb_to_gen,self.parent.dir)
            exPath = str(self.parent.parent.preferences_win.ui.execPathEdit.text())
            cmd_args_list = [exPath,"-p", "%s/"%self.parent.dir, "-r", "%s"%self.nb_to_gen, "-m"]
            print cmd_args_list
            p = subprocess.Popen(cmd_args_list, stdout=PIPE, stdin=PIPE, stderr=STDOUT) 
        except Exception,e:
            print "Cannot find the executable of the computation program %s"%e
            self.problem = "Cannot find the executable of the computation program \n%s"%e
            self.emit(SIGNAL("refTableProblem"))
            #output.notify(self.parent(),"computation problem","Cannot find the executable of the computation program")
            return

        # boucle toutes les secondes pour verifier les valeurs dans le fichier
        self.nb_done = 0
        while self.nb_done < self.nb_to_gen:
            time.sleep(1)
            #self.nb_done += 1
            #print "plop"
            #self.emit(SIGNAL("increment"))
            # lecture 
            if os.path.exists("%s/reftable.log"%(self.parent.dir)):
                #print 'open'
                f = open("%s/reftable.log"%(self.parent.dir),"r")
                lines = f.readlines()
                f.close()
            else:
                lines = ["OK","0"]
            if len(lines) > 1:
                if lines[0].strip() == "OK":
                    red = int(lines[1])
                    if red > self.nb_done:
                        self.nb_done = red
                        self.emit(SIGNAL("increment"))
                else:
                    print "lines != OK"
                    self.problem = lines[0].strip()
                    self.emit(SIGNAL("refTableProblem"))
                    #output.notify(self,"problem",lines[0])
                    return
            else:
                self.problem = "unknown problem"
                self.emit(SIGNAL("refTableProblem"))
                print "unknown problem"
                #output.notify(self,"problem","Unknown problem")
                return


        #for i in range(1000):
        #    if self.cancel: break
        #    time.sleep(0.01)
        #    self.emit(SIGNAL("increment"))
        #    #print "%d "%(i),

    @pyqtSignature("")
    def cancel(self):
        """SLOT to cancel treatment"""
        self.cancel = True

class AnalysisThread(QThread):
    """ classe qui gère l'execution du programme qui effectue une analyse
    """
    def __init__(self,parent,analysis):
        super(AnalysisThread,self).__init__(parent)
        self.parent = parent
        self.analysis = analysis
        self.progress = 0

    def run(self):
        executablePath = str(self.parent.parent.preferences_win.ui.execPathEdit.text())
        if self.analysis.category == "estimate":
            params = self.analysis.computationParameters
            cmd_args_list = [executablePath,"-p", "%s/"%self.parent.dir, "-e", '%s'%params, "-i", '%s'%self.analysis.name, "-m"]
            print cmd_args_list
            f = open("estimation.out","w")
            p = subprocess.Popen(cmd_args_list, stdout=f, stdin=PIPE, stderr=STDOUT) 
            f.close()
            print "popen ok"

            f = open("estimation.out","r")
            data= f.read()
            f.close()

        elif self.analysis.category == "compare":
            params = self.analysis.computationParameters
            cmd_args_list = [executablePath,"-p", "%s/"%self.parent.dir, "-c", '%s'%params, "-i", '%s'%self.analysis.name, "-m"]
            print cmd_args_list
            f = open("comparison.out","w")
            p = subprocess.Popen(cmd_args_list, stdout=f, stdin=PIPE, stderr=STDOUT) 
            f.close()
            print "popen ok"

            f = open("comparison.out","r")
            data= f.read()
            f.close()

        elif self.analysis.category == "bias":
            params = self.analysis.computationParameters
            cmd_args_list = [executablePath,"-p", "%s/"%self.parent.dir, "-b", '%s'%params, "-i", '%s'%self.analysis.name, "-m"]
            print cmd_args_list
            f = open("comparison.out","w")
            p = subprocess.Popen(cmd_args_list, stdout=f, stdin=PIPE, stderr=STDOUT) 
            f.close()
            print "popen ok"

            f = open("comparison.out","r")
            data= f.read()
            f.close()

        # la scrutation de la progression est identique pour toutes les analyses
        self.progress = 1
        tmpp = 1
        self.emit(SIGNAL("analysisProgress"))
        while True:
            a=os.popen("head -n 1 %s/%s_progress.txt"%(self.parent.dir,self.analysis.name))
            b=a.read()
            a.close()
            # on a bougé
            if len(b.split(' ')) > 1:
                t1 = float(b.split(' ')[0])
                t2 = float(b.split(' ')[1])
                tmpp = int(t1*100/t2)
            if tmpp != self.progress:
                print "on a progressé"
                self.progress = tmpp
                self.emit(SIGNAL("analysisProgress"))
            time.sleep(5)
