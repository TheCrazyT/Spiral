#!/usr/bin/env python3

import math, signal, sys, time
from threading import Timer
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QPainter, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout


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
        device = QPainterPath()
        device.addEllipse(0.0, 0.0, 500.0, 500.0)
        K = 2
        B = K
        J = 0
        while B>1:
            B /= 1.002
            J += 1

        B = K
        N = 1
        V = 0
        D = 150
        O = 1

        MX = D+10
        MY = D+10
        T = 10
        U = 0

        while B>1:
            G = (-O+90.0+360.0/(J/8)*(V+self.ctick))*(math.pi/180)
            O *= 1.03
            D -= T*0.05
            px, py = MX + D*math.cos(G), MY + D*math.sin(G)
            color = Qt.black
            ctick = self.ctick
            if U == ctick:
                color = Qt.blue
            self.painter.fillRect(QRect(px,py,T,T*B), QBrush(color))
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

class Window(QWidget):
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
        #self.framePos = 1500
        t = Timer(0.01, self.originalRenderArea.tick)
        t.start()
        #
        #while framePos < 600:
            #if(self.originalRenderArea.stopIt==False):
            #   self.framePos += 1
            #self.update()
            #QApplication.processEvents()
            #time.sleep(1)
            #time.sleep((1.0-Speed/200.0)/10.0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.anim()
    sys.exit(app.exec_())
