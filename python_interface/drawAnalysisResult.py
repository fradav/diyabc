# -*- coding: utf-8 -*-

import os
import shutil
import codecs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from uis.drawScenario_ui import Ui_Frame
from utils.visualizescenario import *
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *

class DrawAnalysisResult(QFrame):
    """ Classe pour créer une fenêtre à l'intérieur de laquelle on dessine les resultats d'une analyse
    """
    def __init__(self,directory,parent=None):
        super(DrawAnalysisResult,self).__init__(parent)
        self.parent=parent
        self.directory=directory
        self.createWidgets()
        self.dicoPlot = {}  
        self.svgList = []
        self.tab_colors = ["#0000FF","#00FF00","#FF0000","#00FFFF","#FF00FF","#FFFF00","#000000","#808080","#008080","#800080","#808000","#000080","#008000","#800000","#A4A0A0","#A0A4A0","#A0A0A4","#A00000","#00A000","#00A0A0"]
        
        self.drawAll()

    def createWidgets(self):
        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        QObject.connect(self.ui.closeButton,SIGNAL("clicked()"),self.exit)
        QObject.connect(self.ui.saveButton,SIGNAL("clicked()"),self.save)

    def exit(self):
        self.parent.ui.analysisStack.removeWidget(self)
        self.parent.ui.analysisStack.setCurrentIndex(0)

    def drawAll(self):
        if os.path.exists("%s/analysis/%s/paramstatdens.txt"%(self.parent.dir,self.directory)):
            f = codecs.open("%s/analysis/%s/paramstatdens.txt"%(self.parent.dir,self.directory),"r","utf-8")
            lines = f.readlines()
            f.close()
            l = 0
            while l < (len(lines) - 1):
                name = lines[l].strip()
                values = lines[l+1]
                absv = lines[l+3]
                ordpr = lines[l+4]
                ordpo = lines[l+5]
                self.addDraw(name,values,absv,ordpr,ordpo)
                l += 6

        else:
            print "paramstatdens.txt not found"


    def addDraw(self,name,values,absv,ordpr,ordpo):
        
        tabvalues = values.strip().split('  ')
        av = float(tabvalues[0])
        median = float(tabvalues[1])
        mode = float(tabvalues[2])
        q2_5 = float(tabvalues[3])
        q5 = float(tabvalues[4])
        q25 = float(tabvalues[5])
        q75 = float(tabvalues[6])
        q95 = float(tabvalues[7])
        q975 = float(tabvalues[8])

        p = QwtPlot()
        p.setCanvasBackground(Qt.white)
        p.setTitle("%s [%6.2e]"%(name,median))
        legend = QwtLegend()

        labs = []
        for num in absv.strip().split('  '):
            labs.append(float(num))
        lpr = []
        for num in ordpr.strip().split('  '):
            lpr.append(float(num))
        lpo = []
        for num in ordpo.strip().split('  '):
            lpo.append(float(num))
            
        legend_txt = "prior"
        pr = QwtPlotCurve(legend_txt)
        pr.setStyle(QwtPlotCurve.Lines)
        pr.setPen(QPen(QColor(self.tab_colors[2]),2))
        pr.setSymbol(QwtSymbol(Qwt.QwtSymbol.NoSymbol,
              QBrush(QColor(self.tab_colors[1])),
                QPen(QColor(self.tab_colors[1])),
                  QSize(7, 7)))
        pr.setData(labs,lpr)
        pr.attach(p)
        pr.updateLegend(legend)

        legend_txt = "posterior"
        post = QwtPlotCurve(legend_txt)
        post.setStyle(QwtPlotCurve.Lines)
        post.setPen(QPen(QColor(self.tab_colors[1]),2))
        post.setSymbol(QwtSymbol(Qwt.QwtSymbol.NoSymbol,
              QBrush(QColor(self.tab_colors[2])),
                QPen(QColor(self.tab_colors[2])),
                  QSize(7, 7)))
        post.setData(labs,lpo)
        post.attach(p)
        post.updateLegend(legend)

        for it in legend.legendItems():
            f = it.font()
            f.setPointSize(11)
            it.setFont(f)
        #litem = legend.find(obs)
        #litem.symbol().setSize(QSize(17,17))
        #litem.setIdentifierWidth(17)
        legend.setFrameShape(QFrame.Box)
        legend.setFrameShadow(QFrame.Raised)

        p.replot()
        grid = QwtPlotGrid()
        grid.setPen(QPen(Qt.black,0.5))
        grid.attach(p)
        p.insertLegend(legend,QwtPlot.BottomLegend)

        fr = QFrame(self)
        fr.setFrameShape(QFrame.StyledPanel)
        fr.setFrameShadow(QFrame.Raised)
        fr.setObjectName("frame")
        fr.setMinimumSize(QSize(400, 0))
        fr.setMaximumSize(QSize(400, 300))
        vert = QVBoxLayout(fr)
        vert.addWidget(p)

        self.ui.horizontalLayout_2.addWidget(fr)
        self.dicoPlot[name] = p

        # frame des valeurs
        frame = QFrame(self.ui.scrollAreaWidgetContents)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setObjectName("frame")
        verticalLayout_3 = QVBoxLayout(frame)
        verticalLayout_3.setObjectName("verticalLayout_3")
        avLabel = QLabel("Average   :  %6.2e"%av,frame)
        avLabel.setObjectName("avLabel")
        avLabel.setAlignment(Qt.AlignCenter)
        avLabel.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(avLabel)
        medLabel = QLabel("Median    :  %6.2e"%median,frame)
        medLabel.setObjectName("medLabel")
        medLabel.setAlignment(Qt.AlignCenter)
        medLabel.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(medLabel)
        modeLabel = QLabel("Mode       :  %6.2e"%mode,frame)
        modeLabel.setObjectName("modeLabel")
        modeLabel.setAlignment(Qt.AlignCenter)
        modeLabel.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(modeLabel)
        q2_5Label = QLabel("q(0.025)  :  %6.2e"%q2_5,frame)
        q2_5Label.setObjectName("q2_5Label")
        q2_5Label.setAlignment(Qt.AlignCenter)
        q2_5Label.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(q2_5Label)
        q5Label = QLabel("q(0.050)  :  %6.2e"%q5,frame)
        q5Label.setObjectName("q5Label")
        q5Label.setAlignment(Qt.AlignCenter)
        q5Label.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(q5Label)
        q25Label = QLabel("q(0.250)  :  %6.2e"%q25,frame)
        q25Label.setObjectName("q25Label")
        q25Label.setAlignment(Qt.AlignCenter)
        q25Label.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(q25Label)
        q75Label = QLabel("q(0.750)  :  %6.2e"%q75,frame)
        q75Label.setObjectName("q75")
        q75Label.setAlignment(Qt.AlignCenter)
        q75Label.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(q75Label)
        q95Label = QLabel("q(0.950)  :  %6.2e"%q95,frame)
        q95Label.setObjectName("q95Label")
        q95Label.setAlignment(Qt.AlignCenter)
        q95Label.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(q95Label)
        q975Label = QLabel("q(0.975)  :  %6.2e"%q975,frame)
        q975Label.setObjectName("q975Label")
        q975Label.setAlignment(Qt.AlignCenter)
        q975Label.setFont(QFont("Courrier",10))
        verticalLayout_3.addWidget(q975Label)
        frame.setMinimumSize(QSize(400, 0))
        frame.setMaximumSize(QSize(400, 9000))
        self.ui.horizontalLayout_3.addWidget(frame)


    def DrawSvg(self,segments,scc,t,savename):
        """ dessine un scenario dans un fichier svg
        """
        
        xmax = 500
        ymax = 450
        svgpic = QSvgGenerator()
        svgpic.setFileName(savename)
        self.svgList.append(svgpic)

        painter = QPainter()
        painter.begin(svgpic)

        self.paintScenario(painter,segments,scc,t,xmax,ymax)
        
        painter.end()

    def paintScenario(self,painter,segments,scc,t,xmax,ymax,font_inc=0):
        """ dessine le scenario sur le painter
        """

    def save(self):
        """ clic sur le bouton save
        """
        # nettoyage radical : suppression du dossier
        proj_dir = self.parent.dir
        pic_dir = "%s/analysis/%s/pictures"%(proj_dir,self.directory)
        if os.path.exists(pic_dir):
            shutil.rmtree(pic_dir)
        # puis on le recrée, vide évidemment
        os.mkdir(pic_dir)

        answer = QMessageBox.question(self,"Saving option","Would you like to save all images in one file or in separated files ?",\
                "All in one","Separated")
        if answer == 0:
            self.saveDrawsToOne()
        elif answer == 1:
            self.saveEachDraws()

    def saveEachDraws(self):
        """ Sauve chaque scenario dans un fichier
        """
        proj_dir = self.parent.dir
        pic_dir = "%s/analysis/%s/pictures"%(proj_dir,self.directory)
        pic_basename = "posterior"
        pic_whole_path = "%s/%s_"%(pic_dir,pic_basename)

        pic_format = str(self.parent.parent.preferences_win.ui.formatCombo.currentText())
        if pic_format == "jpg" or pic_format == "png":
            for name in self.dicoPlot.keys():
                p = self.dicoPlot[name]
                savename = "%s%s.%s"%(pic_whole_path,name,pic_format)
                pix = QPixmap(p.rect().size().width(),p.rect().size().height())
                pix.fill(Qt.white)
                painter = QPainter(pix)
                pen = QPen(Qt.black,2)
                painter.setPen(pen)
                p.print_(painter, p.rect())
                painter.end()
                im = pix.toImage()
                im.save(savename)
        else:
            for name in self.dicoPlot.keys():
                p = self.dicoPlot[name]
                savename = "%s%s.svg"%(pic_whole_path,name)
                svg = QSvgGenerator()
                svg.setFileName(savename)
                svg.setSize(p.rect().size())

                painter = QPainter(svg)
                p.print_(painter, p.rect())
                painter.end()

    def saveDrawsToOne(self):
        """ Sauve tous les scenarios dans une seule image et un seul svg
        """
        proj_dir = self.parent.dir
        pic_dir = "%s/analysis/%s/pictures"%(proj_dir,self.directory)
        pic_basename = "posterior"
        pic_whole_path = "%s/%s_"%(pic_dir,pic_basename)

        pic_format = str(self.parent.parent.preferences_win.ui.formatCombo.currentText())

        nbPlot = len(self.dicoPlot.keys())
        largeur = 2
        # resultat de la div entière plus le reste (modulo)
        longueur = (nbPlot/largeur)+(nbPlot%largeur)
        ind = 0
        li=0

        # on prend un des graphes pour savoir ses dimensions
        size = self.dicoPlot[self.dicoPlot.keys()[0]].rect().size()

        if pic_format == "jpg" or pic_format == "png":
            self.im_result = QImage(largeur*(size.width()),longueur*(size.height()),QImage.Format_RGB32)
            self.im_result.fill(Qt.black)
            painter = QPainter(self.im_result)
            painter.fillRect(0, 0, largeur*(size.width()), longueur*(size.height()), Qt.white)
        else:
            self.pic_result = QSvgGenerator()
            #self.pic_result.setSize(QSize(largeur*500, longueur*450));
            #self.pic_result.setViewBox(QRect(0, 0, largeur*500, longueur*450));
            self.pic_result.setFileName("%sall.svg"%pic_whole_path)
            painter_svg = QPainter()
            painter_svg.begin(self.pic_result)

        keys = self.dicoPlot.keys()
        # on fait des lignes tant qu'on a des pix
        while (ind < nbPlot):
            col = 0
            # une ligne
            while (ind < nbPlot) and (col < largeur):
                plot = self.dicoPlot[keys[ind]]
                if pic_format == "jpg" or pic_format == "png":
                    plot.print_(painter, QRect(QPoint(col*size.width(),li*size.height()),QSize(size)))
                else:
                    plot.print_(painter_svg, QRect(QPoint(col*size.width(),li*size.height()),QSize(size)))
                col+=1
                ind+=1
            li+=1

        if pic_format == "jpg" or pic_format == "png":
            self.im_result.save("%sall.%s"%(pic_whole_path,pic_format))
        else:
            painter_svg.end()
