#!/usr/bin/env python3

import math, signal, sys, time
from threading import Timer
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QPainter, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout


class RenderArea(QWidget):
    painter = None
    stopIt = False
    ctick = 0
    def __init__(self, parent=None):
        print(parent)
        self.parent = parent
        super(RenderArea, self).__init__(parent)
   
    def paintEvent(self, event):
        if(self.painter == None):
            self.painter = QPainter(self)
            self.painter.setRenderHint(QPainter.Antialiasing)
            self.painter.fillRect(event.rect(), QBrush(Qt.white))
        self.painter.save()
        K = 2
        B = K
        J = 0
        while B>1:
            B /= 1.002
            J += 1

        B = K
        N = 1
        V = 0
        D = 400
        O = 1

        MX = D+10
        MY = D+10
        T = 10
        U = 0
        E = 1

        while B>1:
            G = (-O+90.0+360.0/(J/4)*((V+self.ctick)*E))*(math.pi/180)
            O *= 1.00125
            E *= 1.00512
            D -= T*0.12
            px, py = MX + D*math.cos(G), MY + D*math.sin(G)
            color = Qt.black
            ctick = self.ctick
            if U == ctick:
                color = Qt.blue
            self.painter.fillRect(QRect(px,py,T*N,T*B), QBrush(color))
            B /= 1.004
            N *= 1.004
            V -= 1
            U += 1
        self.ctick += 1
        self.painter.restore()



    def tick(self):
        if(self.painter == None):
            t = Timer(0.01, self.tick)
            t.start()
            return
        try:
            pass
        except BaseException as e:
            self.stopIt = True
            raise BaseException() from e

        if(self.stopIt==False):
            self.parent.framePos += 1
        self.parent.update()
        QApplication.processEvents()
        t = Timer(0.5, self.tick)
        t.start()


    def minimumSizeHint(self):
        return QSize(500, 500)

class Window(QMainWindow):
    speed              = 0.0
    framePos           = 1500
    originalRenderArea = None
    def __init__(self):
        super(Window, self).__init__()
        self.originalRenderArea = RenderArea(self)
        layout = QGridLayout()
        layout.addWidget(self.originalRenderArea, 0, 0)
        self.setLayout(layout)

    def anim(self):
        t = Timer(0.01, self.originalRenderArea.tick)
        t.start()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.anim()
    window.move(0,0)
    window.setFixedWidth(900)
    window.setFixedHeight(900)
    sys.exit(app.exec_())
