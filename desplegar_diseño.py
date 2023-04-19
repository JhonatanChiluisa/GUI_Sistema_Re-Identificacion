# -*- coding: utf8 -*-
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('diseño.ui', self)

        #control barra de título
        self.btn_minimizar.clicked.connect(self.control_btn_minimizar)
        self.btn_restaurar.clicked.connect(self.control_btn_normal)
        self.btn_maximizar.clicked.connect(self.control_btn_maximizar)
        self.btn_cerrar.clicked.connect(lambda: self.close())
        self.btn_cargar_BD.clicked.connect(self.gridBD)
        #eliminnar barra y de título - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #SizeGrid
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        #mover la ventana
        self.frame_titulo.mouseMoveEvent = self.mover_ventana
        self.setup()
        self.makeConnections()


    def cargarImagenesBD(self):
        lista = []
        input_images_path = "F:/RE_IDENTIFICACION/Data/Alex"
        files_names = os.listdir(input_images_path)
        for file_name in files_names:
            image_path = input_images_path + "/" + file_name
            lista.append(image_path)
        return lista

    def gridBD(self):
        listaImagenes = self.cargarImagenesBD()
        win = QWidget()
        grid = QGridLayout()
        sizelista = len(listaImagenes)
        count = 0
        for i in range(1, 32):
            for j in range(1, 7):
                label2 = QLabel()
                label2.setPixmap(QPixmap(listaImagenes[count]))
                grid.addWidget(label2,i,j)
                count = count +1
        win.setLayout(grid)
        self.scrollAreaBD.setWidget(win)
        self.scrollAreaBD.setWidgetResizable(True)
        

    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

    def makeMediaPlayer(self):
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.widget_video1.setLayout(vbox)
        return videoOutput
    
    def control_btn_abrirVideo(self):
        path = QFileDialog.getOpenFileName(self, "Abrir", "/")
        filepath = path[0]
        if filepath == "":
            return
        videoName = filepath.split("/")[-1]
        self.lbl_nombre_video.setText('{}'.format(videoName))
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()

    def makeConnections(self):
        self.btn_buscar_video.clicked.connect(self.control_btn_abrirVideo)
        self.btn_pause_video1.clicked.connect(self.mediaPlayer.pause)
        self.btn_play_video1.clicked.connect(self.mediaPlayer.play)
        self.btn_stop_video1.clicked.connect(self.mediaPlayer.stop)


    def control_btn_minimizar(self):
        self.showMinimized()
    
    def control_btn_normal(self):
        self.showNormal()
        self.btn_restaurar.hide()
        self.btn_maximizar.show()

    def control_btn_maximizar(self):
        self.showMaximized()
        self.btn_maximizar.hide()
        self.btn_restaurar.show()

    #SizeGrid
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom()- self.gripSize)
        
    #mover la ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()        

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
            self.btn_maximizar.hide()
            self.btn_restaurar.show()    
        else:
            self.showNormal()
            self.btn_restaurar.hide() 
            self.btn_maximizar.show()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())