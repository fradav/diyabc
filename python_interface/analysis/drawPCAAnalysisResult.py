# -*- coding: utf-8 -*-

import os,re
import shutil
import codecs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from uis.drawScenario_ui import Ui_Frame
from utils.visualizescenario import *
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *
import output

class DrawPCAAnalysisResult(QFrame):
    """ Classe pour créer une frame à l'intérieur de laquelle on dessine les resultats d'une analyse
    Pre-evaluate PCA
    """
    def __init__(self,directory,parent=None):
        super(DrawPCAAnalysisResult,self).__init__(parent)
        self.parent=parent
        self.directory=directory
        self.createWidgets()
        self.dicoPlot = {}  
        self.tab_colors = ["#0000FF","#00FF00","#FF0000","#00FFFF","#FF00FF","#FFFF00","#000000","#808080","#008080","#800080","#808000","#000080","#008000","#800000","#A4A0A0","#A0A4A0","#A0A0A4","#A00000","#00A000","#00A0A0"]
        
    def createWidgets(self):
        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        QObject.connect(self.ui.closeButton,SIGNAL("clicked()"),self.exit)
        QObject.connect(self.ui.saveButton,SIGNAL("clicked()"),self.saveGraph)

        QObject.connect(self.ui.scCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        QObject.connect(self.ui.compoHCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        QObject.connect(self.ui.compoVCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        QObject.connect(self.ui.nbpCombo,SIGNAL("currentIndexChanged(int)"),self.drawGraph)
        self.ui.ACProgress.setValue(0)
        self.tab_colors = ["#0000FF","#00FF00","#FF0000","#00FFFF","#FF00FF","#FFFF00","#000000","#808080","#008080","#800080","#808000","#000080","#008000","#800000","#A4A0A0","#A0A4A0","#A0A0A4","#A00000","#00A000","#00A0A0"]

        #QObject.connect(self.ui.loadButton,SIGNAL("clicked()"),self.loadACP)
        # replaced by :
        #self.loadACP()

    def loadACP(self):
        """ charge le fichier ACP dans un dico
        et initialise les combo boxes
        """
        self.ui.ACProgress.setValue(0)

        if not os.path.exists("%s/analysis/%s/pca.txt"%(self.parent.dir,self.directory)):
            output.notify(self,"error","pca.txt not found")
        else:
            f = codecs.open("%s/analysis/%s/pca.txt"%(self.parent.dir,self.directory),"r","utf-8")
            lines = f.readlines()
            f.close()
            self.dico_points = {}

            nb_composantes = (len(lines[0].split(" "))-2)
            nb_lignes = len(lines)
            self.dico_points[-1] = lines[0].split(" ")[2:]
            self.dico_points[0] = lines[1].split(" ")[1:]
            for i in range(len(self.dico_points[0])):
                self.dico_points[0][i] = float(self.dico_points[0][i])

            # pour chaque ligne
            i=2
            while i < len(lines):
            #for i,l in enumerate(lines):
                l=lines[i]
                pc = (float(i)/float(nb_lignes)*100)+1
                if (int(pc) % 2) == 0:
                    self.ui.ACProgress.setValue(pc)
                tab = l.split(" ")
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
                i+=1

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
        rp.setData([self.dico_points[0][compo_h]],[self.dico_points[0][compo_v]])
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
                    if i != 0 and i != -1:
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
            p.setAxisTitle(0,"P.C.%s (%8.2f%%)"%(compo_v+1,float(self.dico_points[-1][compo_v])))
            p.setAxisTitle(2,"P.C.%s (%8.2f%%)"%(compo_h+1,float(self.dico_points[-1][compo_h])))
            p.replot()

            fr = QFrame(self)
            fr.setFrameShape(QFrame.StyledPanel)
            fr.setFrameShadow(QFrame.Raised)
            fr.setObjectName("frame")
            fr.setMinimumSize(QSize(600, 0))
            fr.setMaximumSize(QSize(600, 600))
            vert = QVBoxLayout(fr)
            vert.addWidget(p)

            if self.ui.horizontalLayout_3.itemAt(0) != None:
                self.ui.horizontalLayout_3.itemAt(0).widget().hide()
            self.ui.horizontalLayout_3.removeItem(self.ui.horizontalLayout_3.itemAt(0))
            self.ui.horizontalLayout_3.addWidget(fr)


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
            proj_dir = self.parent.dir
            graph_dir = self.parent.parent.PCA_dir_name
            sc_txt = ""
            if self.ui.scCombo.currentText() != "all":
                sc_txt = "_sc_%s"%self.ui.scCombo.currentText()
            graph_dir_path = "%s/analysis/%s/%s"%(proj_dir,self.directory,graph_dir)
            if not os.path.exists(graph_dir_path):
                os.mkdir(graph_dir_path)

            graph_file_path = "%s/refTable_PCA_%s_%s_%s%s"%(graph_dir_path,self.ui.compoHCombo.currentText(),self.ui.compoVCombo.currentText(),self.ui.nbpCombo.currentText(),sc_txt)
            if os.path.exists(graph_file_path):
                os.remove(graph_file_path)

            p = self.ui.horizontalLayout_3.itemAt(0).widget()

            pic_format = str(self.parent.parent.preferences_win.ui.formatCombo.currentText())

            if pic_format == "svg":
                svg = QSvgGenerator()
                svg.setFileName("%s.svg"%(graph_file_path))
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
                im.save("%s.%s"%(graph_file_path,pic_format))
    def exit(self):
        self.parent.ui.analysisStack.removeWidget(self)
        self.parent.ui.analysisStack.setCurrentIndex(0)

