#!/usr/bin/env python3

#colab notebook: https://colab.research.google.com/drive/1eD-FLoQEsb0ExKWYxmRYWFyGE0GbMU2j#scrollTo=wv--TgK2b2XX

import math, signal, sys, time
from threading import Timer
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QPainter, QBrush, QPainterPath, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout



class RenderArea(QWidget):
    painter = None
    stopIt = False
    ctick = 0
    def __init__(self, parent=None):
        self.parent = parent
        super(RenderArea, self).__init__(parent)
   
    def drawBox(self,X,Y,W,H,H2,D):
    
        if H != 0:
            self.painter.setPen(Qt.black)
            self.painter.setBrush(Qt.blue)
            self.painter.fillRect(QRect(X,Y+H2,W,H),QBrush(Qt.blue))

            self.painter.drawRect(QRect(X,Y+H2,W,H))
            path = QPainterPath()
            path.moveTo(X+W,Y+H2)
            path.lineTo(X+W,Y+H2+H)
            path.lineTo(X+W+D,Y+H2+H-D)
            path.lineTo(X+W+D,Y+H2-D)
            path.lineTo(X+W,Y+H2)
            path.closeSubpath()
            self.painter.setBrush(Qt.blue)
            self.painter.drawPath(path)
            
            path = QPainterPath()
            path.moveTo(X,Y+H2)
            path.lineTo(X+D,Y+H2-D)
            path.lineTo(X+D+W,Y+H2-D)
            path.lineTo(X+W,Y+H2)
            path.lineTo(X,Y+H2)
            path.closeSubpath()
            self.painter.drawPath(path)
            
        if H2 != 0:
            self.painter.setPen(Qt.black)
            self.painter.setBrush(Qt.white)
            self.painter.fillRect(QRect(X,Y,W,H2),QBrush(Qt.white))

            self.painter.drawRect(QRect(X,Y,W,H2))
            path = QPainterPath()
            path.moveTo(X+W,Y)
            path.lineTo(X+W,Y+H2)
            path.lineTo(X+W+D,Y+H2-D)
            path.lineTo(X+W+D,Y-D)
            path.lineTo(X+W,Y)
            path.closeSubpath()
            self.painter.drawPath(path)
            
            path = QPainterPath()
            path.moveTo(X,Y)
            path.lineTo(X+D,Y-D)
            path.lineTo(X+D+W,Y-D)
            path.lineTo(X+W,Y)
            path.lineTo(X,Y)
            path.closeSubpath()
            self.painter.drawPath(path)
        
    def drawArrowV(self,x1,y1,x2,y2):
        self.painter.setPen(Qt.red)
        self.painter.drawLine(x1,y1,x2,y2)
        self.painter.drawLine(x1,y1,x1+5,y1+5)
        self.painter.drawLine(x1,y1,x1-5,y1+5)
        self.painter.drawLine(x2,y2,x2+5,y2-5)
        self.painter.drawLine(x2,y2,x2-5,y2-5)

    def drawArrowH(self,x1,y1,x2,y2):
        self.painter.setPen(Qt.red)
        self.painter.drawLine(x1,y1,x2,y2)
        self.painter.drawLine(x1,y1,x1+5,y1+5)
        self.painter.drawLine(x1,y1,x1+5,y1-5)
        self.painter.drawLine(x2,y2,x2-5,y2+5)
        self.painter.drawLine(x2,y2,x2-5,y2-5)
    
    def drawVars(self,X1,X2,Y1,Y2,a,f,b,c,d,e,g,i):

        self.painter.setPen(QPen(Qt.red,  1, Qt.DashLine))
        self.painter.drawLine(X2+f,Y2+i-c,X2+f+120,Y2+i-c)
        self.painter.drawLine(X2+f,Y2+i,X2+f+200,Y2+i)
        self.painter.drawLine(X2+f+e,Y2+i-e,X2+f+e+200,Y2+i-e)
        self.painter.drawLine(X2,Y2+i,X2,Y2+i+100)
        self.painter.drawLine(X2+f,Y2+i,X2+f,Y2+i+100)

        self.painter.drawLine(X1,Y1+b,X1,Y1+b+100)
        self.painter.drawLine(X1+f,Y1+b,X1+f,Y1+b+100)
        self.painter.drawLine(X1,Y1+b,X1-200,Y1+b)
        self.painter.drawLine(X1,Y1+b-g,X1-200,Y1+b-g)
        self.painter.drawLine(X1+f+d,Y1+b-d,X1-120,Y1+b-d)
        
        self.painter.drawLine(X2,Y2+i,X2-80,Y2+i)
        self.painter.drawLine(X1+f,Y1+b,X1+f+80,Y1+b)

        self.drawArrowV(X2+f+120,Y2+i-c,X2+f+120,Y2+i)
        self.drawArrowV(X2+f+160,Y2+i-e,X2+f+160,Y2+i)
        self.drawArrowH(X2,Y2+i+50,X2+f,Y2+i+50)
        self.drawArrowH(X1,Y1+b+50,X1+f,Y1+b+50)
        
        self.drawArrowV(X1-160,Y1+b-g,X1-160,Y1+b)
        self.drawArrowV(X1-120,Y1+b-d,X1-120,Y1+b)
        
        self.drawArrowV(X2-60,Y2+i,X1+f+60,Y1+b)
        
        self.painter.setPen(QPen(Qt.red,  1, Qt.SolidLine))
        self.painter.drawText(X2+f+120+5,Y2+i-c/2,"c")
        self.painter.drawText(X2+f+160+5,Y2+i-e/2,"e")
        self.painter.drawText(X2+f/2,Y2+i+50+12,"f")
        self.painter.drawText(X1+f/2,Y1+b+50+12,"f")
        self.painter.drawText(X1-160+5,Y1+b-g/2,"g")
        self.painter.drawText(X1-120+5,Y1+b-d/2,"d")
        self.painter.drawText(X1+f+60+5,Y2+i+a/2+3,"a")
        
    def paintEvent(self, event):
        if(self.painter == None):
            self.painter = QPainter(self)
            self.painter.setRenderHint(QPainter.Antialiasing)
            self.painter.fillRect(event.rect(), QBrush(Qt.white))
        self.painter.save()
        print(self.ctick)
        
        a = 20
        f = 80
        b = 200
        d = 50
        e = 80
        #e = d
        i = b
        
        X1 = 250
        X2 = X1 + 200
        Y1 = 200
        Y2 = Y1 - a
        
        
        doDrawVars = False
        if (self.ctick//5 % 2) == 0:
            c = 0
            g = b
        elif (self.ctick//5 % 2) == 1:
            c = (d*b - d*a) / (e + d)
            g = a + c
            doDrawVars = True

            
        self.drawBox(X1,Y1,f,g,b-g,d)
        self.drawBox(X2,Y2,f,c,i-c,e)
        
        if doDrawVars:
            self.drawVars(X1,X2,Y1,Y2,a,f,b,c,d,e,g,i)
        
        self.painter.restore()
        self.ctick += 1



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
