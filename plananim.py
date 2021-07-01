#!/usr/bin/env python3

##TODO:  add new water on every circle, hopefully to pump water on top a bitmore (sadly forces are stopped near center)
##       even on same volume, the forces are different ... currently does not calculate that
##FIXME: its currently a wrong assumption that the boxes are filled(for example when about 3 are left)
##       it normally needs to fill from bottom to top, so force-difference could be < 0 earlier.
import math, signal, sys, time
from threading import Timer
from PyQt4.QtCore import *
from PyQt4 import *
from PyQt4.QtGui import *

class VolRes:
	V1 = 0.0
	V2 = 0.0
	def __init__(self,V1,V2):
		self.V1 = V1
		self.V2 = V2

class RenderArea(QWidget):
	lowPoint = {}
	water  = []
	HLines = []
	HLine  = None
	parent = None
	stopIt = False
	oldvolume = 0
	iPts = None
	V = None
	depths = None
	painter = None
	S = 1
	k = 250
	n = 20
	def __init__(self, parent=None):
		print(parent)
		self.parent = parent
		super(RenderArea, self).__init__(parent)

	def fillWater(self,volume,x):
		S      = self.S
		n      = self.n
		k      = self.k
		iPts   = self.iPts
		depths = self.depths
		V      = self.V


		i = 90 + x

		if volume<=0:
			raise(BaseException("WTF"))
		hy      = self.lowPoint[i]
		#print("lowpoint: %i" % self.lowPoint[i])
		fillVol = 0
		V1      = 0
		V2      = 0
		fillVolB4 = 0
		while fillVol<volume:
			fillVolB4 = fillVol
			V1B4 = V1
			V2B4 = V2
			fillVol = 0
			V1      = 0
			V2      = 0
			first = True
			c = 0
			self.HLine = QLineF(QPointF(0, hy),QPointF(500, hy))
			HLine = QLineF(self.HLine)
			HLine.translate(-k,-k)
			HLine = QTransform().rotate(x).map(HLine)
			HLine.translate(k,k)
			hy -= 1
			intersectingLastTime = False
			while fillVol<volume:
				if(first):
					pts = list(iPts[i])

					AL    = QLineF(pts[1],pts[0]) 
					BL    = QLineF(pts[2],pts[1]) 
					CL    = QLineF(pts[3],pts[2]) 
					DL    = QLineF(pts[0],pts[3]) 

					ip           = QPointF(0,0)
					res          = AL.intersect(HLine,ip)
					intersecting = False
					if(res==QLineF.BoundedIntersection):
						intersecting = True
					res = BL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						pts[3] = QPointF(ip.x(), ip.y())
						intersecting = True
					res = CL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						intersecting = True
					res = DL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						pts[2] = QPointF(ip.x(), ip.y())
						intersecting = True

					if(intersecting):
						ACL   = QLineF(pts[0],pts[2]) 
						AL    = QLineF(pts[1],pts[0]) 
						BL    = QLineF(pts[2],pts[1]) 
						CL    = QLineF(pts[3],pts[2]) 
						DL    = QLineF(pts[0],pts[3]) 

						AC    = ACL.length()
						A     = AL.length()
						B     = BL.length()
						C     = CL.length()
						D     = DL.length()

						APol1    = math.sqrt(((A+B+AC)/2)*(((A+B+AC)/2)-A)*(((A+B+AC)/2)-B)*(((A+B+AC)/2)-AC))
						APol2    = math.sqrt(((C+D+AC)/2)*(((C+D+AC)/2)-A)*(((C+D+AC)/2)-B)*(((C+D+AC)/2)-AC))
						APol     = APol1 + APol2
						fillVol += APol * depths[i]
					else:
						fillVol += V[i]

					#FIXME: strange Bug that makes value much higher ...
					if(fillVol>V[i]+100):
						print("bugfix %f > %f" % (fillVol,V[i]))
						fillVol = V[i]

					first = False
					if(intersectingLastTime and not intersecting):
						break
					intersectingLastTime = intersecting
				else:
					if n*90-S<i+c:
						print("stopped because of end circle")
						self.stopIt = True
						break
					if volume - V[i+c] - V[i-c]<0:
						break

					pts = list(iPts[i+c])

					AL = QLineF(pts[1],pts[0]) 
					BL = QLineF(pts[2],pts[1]) 
					CL = QLineF(pts[3],pts[2]) 
					DL = QLineF(pts[0],pts[3])
				
					ip           = QPointF(0,0)
					intersecting = False
					res          = AL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						intersecting = True
					res = BL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						pts[2] = QPointF(ip.x(), ip.y())
						intersecting = True
					res = CL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						intersecting = True
					res = DL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						pts[3] = QPointF(ip.x(), ip.y())
						intersecting = True

					if(intersecting):
						ACL   = QLineF(pts[0],pts[2]) 
						AL    = QLineF(pts[1],pts[0]) 
						BL    = QLineF(pts[2],pts[1]) 
						CL    = QLineF(pts[3],pts[2]) 
						DL    = QLineF(pts[0],pts[3]) 
				
						AC    = ACL.length()
						A     = AL.length()
						B     = BL.length()
						C     = CL.length()
						D     = DL.length()

						APol1    = math.sqrt(((A+B+AC)/2)*(((A+B+AC)/2)-A)*(((A+B+AC)/2)-B)*(((A+B+AC)/2)-AC))
						APol2    = math.sqrt(((C+D+AC)/2)*(((C+D+AC)/2)-A)*(((C+D+AC)/2)-B)*(((C+D+AC)/2)-AC))
						APol     = APol1 + APol2
						fillVol += APol * depths[i+c]
						V1      += V[i+c]
					else:
						V1      += V[i+c]
						fillVol += V[i+c]

					pts = list(iPts[i-c])

					AL = QLineF(pts[1],pts[0]) 
					BL = QLineF(pts[2],pts[1]) 
					CL = QLineF(pts[3],pts[2]) 
					DL = QLineF(pts[0],pts[3])
				
					ip = QPointF(0,0)
					intersecting = False
					res = AL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						intersecting = True
					res = BL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						pts[2] = QPointF(ip.x(), ip.y())
						intersecting = True
					res = CL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						intersecting = True
					res = DL.intersect(HLine,ip)
					if(res==QLineF.BoundedIntersection):
						pts[3] = QPointF(ip.x(), ip.y())
						intersecting = True

					if(intersecting):
						ACL   = QLineF(pts[0],pts[2]) 
						AL    = QLineF(pts[1],pts[0]) 
						BL    = QLineF(pts[2],pts[1]) 
						CL    = QLineF(pts[3],pts[2]) 
						DL    = QLineF(pts[0],pts[3]) 
				
						AC    = ACL.length()
						A     = AL.length()
						B     = BL.length()
						C     = CL.length()
						D     = DL.length()

						APol1    = math.sqrt(((A+B+AC)/2)*(((A+B+AC)/2)-A)*(((A+B+AC)/2)-B)*(((A+B+AC)/2)-AC))
						APol2    = math.sqrt(((C+D+AC)/2)*(((C+D+AC)/2)-A)*(((C+D+AC)/2)-B)*(((C+D+AC)/2)-AC))
						APol     = APol1 + APol2
						fillVol += APol * depths[i-c]
						V2      += APol * depths[i-c]
					else:
						V2      += V[i-c]
						fillVol += V[i-c]

					if(intersectingLastTime and intersecting):
						break
					intersectingLastTime = intersecting
				c += S
		V1 = V1B4
		V2 = V2B4
		hy += 1
		#print("hy:%i,fillVol:%f,volume:%f" % (hy,fillVol,volume))
		first = True
		c = 0
		self.HLine = QLineF(QPointF(0, hy),QPointF(500, hy))
		HLine = QLineF(self.HLine)
		HLine.translate(-k,-k)
		HLine = QTransform().rotate(x).map(HLine)
		HLine.translate(k,k)
		intersectingLastTime = False
		while True:
			if(first):
				pts = list(iPts[i])

				AL    = QLineF(pts[1],pts[0]) 
				BL    = QLineF(pts[2],pts[1]) 
				CL    = QLineF(pts[3],pts[2]) 
				DL    = QLineF(pts[0],pts[3]) 

				ip           = QPointF(0,0)
				intersecting = False
				res          = AL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					intersecting = True
				res = BL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					pts[2] = QPointF(ip.x(), ip.y())
					intersecting = True
				res = CL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					intersecting = True
				res = DL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					pts[3] = QPointF(ip.x(), ip.y())
					intersecting = True

				water  = QPainterPath()
				myPolygon = QPolygonF(pts)
				water.addPolygon(myPolygon)
				water.translate(-k,-k)
				water = QTransform().rotate(-x).map(water)
				water.translate(k,k)
				col = 100
				self.water.append((water, QColor(0,0,int(col))))
				#self.painter.fillPath(water, QColor(0,0,int(col)))
				first = False
				if(intersectingLastTime and not intersecting):
					break
				intersectingLastTime = intersecting
			else:
				if n*90-S<i+c:
					self.stopIt = True
					break
				if volume - V[i+c] - V[i-c]<0:
					break

				pts = list(iPts[i+c])

				#iPoints = QPainterPath()

				AL = QLineF(pts[1],pts[0]) 
				BL = QLineF(pts[2],pts[1]) 
				CL = QLineF(pts[3],pts[2]) 
				DL = QLineF(pts[0],pts[3])
		
				ip           = QPointF(0,0)
				res          = AL.intersect(HLine,ip)
				intersecting = False
				if(res==QLineF.BoundedIntersection):
					intersecting = True
				res = BL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					pts[2] = QPointF(ip.x(), ip.y())
					intersecting = True
				res = CL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					intersecting = True
				res = DL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					pts[3] = QPointF(ip.x(), ip.y())
					intersecting = True

				water  = QPainterPath()
				myPolygon = QPolygonF(pts)
				water.addPolygon(myPolygon)
				water.translate(-k,-k)
				water = QTransform().rotate(-x).map(water)
				water.translate(k,k)
				col = 100 + 5 * (c/S)
				if(col>255):
					col = 255
				self.water.append((water, QColor(0,0,int(col))))
				#self.painter.fillPath(water, QColor(0,0,int(col)))

				pts = list(iPts[i-c])

				AL = QLineF(pts[1],pts[0]) 
				BL = QLineF(pts[2],pts[1]) 
				CL = QLineF(pts[3],pts[2]) 
				DL = QLineF(pts[0],pts[3])
		
				ip = QPointF(0,0)
				intersecting = False
				res = AL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					intersecting = True
				res = BL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					pts[2] = QPointF(ip.x(), ip.y())
					intersecting = True
				res = CL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					intersecting = True
				res = DL.intersect(HLine,ip)
				if(res==QLineF.BoundedIntersection):
					pts[3] = QPointF(ip.x(), ip.y())
					intersecting = True

				water  = QPainterPath()
				myPolygon = QPolygonF(pts)
				water.addPolygon(myPolygon)
				water.translate(-k,-k)
				water = QTransform().rotate(-x).map(water)
				water.translate(k,k)
				col = 100 - 5  * (c/S)
				if(col<0):
					col = 0
				self.water.append((water, QColor(0,0,int(col))))
				#self.painter.fillPath(water, QColor(0,0,int(col)))

				if(intersectingLastTime and not intersecting):
					break
				intersectingLastTime = intersecting
			c += S
		print("V1: %f, V2: %f, fillVol: %f, fillVolB4: %f, volume: %f" % (V1,V2,fillVol,fillVolB4,volume))
		result = VolRes(V1,V2)
		return result

	def paintEvent(self, event):
		if(self.painter == None):
			self.painter = QPainter(self)
			self.painter.setRenderHint(QPainter.Antialiasing)
			self.painter.fillRect(event.rect(), QBrush(Qt.white))
		self.painter.save()
		device = QPainterPath()
		device.addEllipse(0.0, 0.0, 500.0, 500.0)
		self.painter.fillPath(device, Qt.black)
		if(self.space!=None):
			self.painter.fillPath(self.space, Qt.white)
		if(self.water != None):
			for (water, color) in self.water:
				self.painter.fillPath(water, color)
		if(self.HLines != None):
			for HLine in self.HLines:
				penHLines = QPen(QColor("#FF0000"))
				self.painter.setPen(penHLines)
				self.painter.drawLine(HLine)
		self.painter.restore()



	def tick(self):
		if(self.painter == None):
			t = Timer(0.01, self.tick)
			t.start()
			return
		try:
			#if(self.stopIt):
			#	return

			S = self.S
			x = self.parent.framePos*S

			k = self.k
			H = 30
			f = 0.1
			d = k-H
			n = self.n
			dg = 0.0001
			dgd = 0.000007
			depth   = 0.1
			space  = QPainterPath()
			volume = 0

			if(self.iPts == None):
				self.iPts = {}
				for i in range(0,n*90,S):
					self.iPts[i] = None

			if(self.V == None):
				self.V = {}
				for i in range(0,n*90,S):
					self.V[i] = None

			if(self.depths == None):
				self.depths = {}
				for i in range(0,n*90,S):
					self.depths[i] = None

			iPts   = self.iPts
			depths = self.depths
			V      = self.V

			for i in range(0,n*90,S):
				dg += dgd
				depth += dg
				depths[i] = depth
				d -= f
				self.lowPoint[i] = k+d-1

				if(iPts[i]==None):
					deg = 1.0
					deg  = math.pi/180
					posX = k+math.cos(float(i)*deg)*d
					posY = k+math.sin(float(i)*deg)*d
					posX2 = k+math.cos(float(i+S)*deg)*(d-f)
					posY2 = k+math.sin(float(i+S)*deg)*(d-f)
					posX3 = k+math.cos(float(i+S)*deg)*(d-H-f)
					posY3 = k+math.sin(float(i+S)*deg)*(d-H-f)
					posX4 = k+math.cos(float(i)*deg)*(d-H)
					posY4 = k+math.sin(float(i)*deg)*(d-H)
					pts = []
					pts.append(QPointF(posX , posY ))
					pts.append(QPointF(posX2, posY2))
					pts.append(QPointF(posX3, posY3))
					pts.append(QPointF(posX4, posY4))
					iPts[i] = pts
				pts = iPts[i]
				myPolygon = QPolygonF(pts)
				
				if(V[i]==None):
					ACL   = QLineF(pts[0],pts[2]) 
					AL    = QLineF(pts[1],pts[0]) 
					BL    = QLineF(pts[2],pts[1]) 
					CL    = QLineF(pts[3],pts[2]) 
					DL    = QLineF(pts[0],pts[3]) 
					
					AC    = ACL.length()
					A     = AL.length()
					B     = BL.length()
					C     = CL.length()
					D     = DL.length()

					APol1 = math.sqrt(((A+B+AC)/2)*(((A+B+AC)/2)-A)*(((A+B+AC)/2)-B)*(((A+B+AC)/2)-AC))
					APol2 = math.sqrt(((C+D+AC)/2)*(((C+D+AC)/2)-A)*(((C+D+AC)/2)-B)*(((C+D+AC)/2)-AC))
					APol  = APol1 + APol2
					V[i]  = APol * depth
				
				#if(i>0):
				#	if(V[i-S]>V[i]):
				#		print(i,V[i-S],V[i],V[i]-V[i-S])
				#		raise(BaseException("WTF"))

				if(self.oldvolume == 0):
					if(i<180):
						volume += V[i]
				else:
					volume = self.oldvolume
				space.addPolygon(myPolygon)
			#if((self.oldvolume != 0)and(self.oldvolume != volume)):
			#	print(self.oldvolume,volume)
			#	raise(BaseException("WTF"))

			if(self.oldvolume == 0):
				print("Calculated volume: %f" % (volume))
				self.oldvolume = volume
			space.translate(-k,-k)
			space = QTransform().rotate(-x).map(space)
			space.translate(k,k)
			self.space = space

			xM  = x % 360
			V1 = 0
			V2 = 0
			#print(xM,x)
			self.water = []
			self.HLines = []
			for y in range(xM,x+1,360):
				#print(y)
				V1_2 = self.fillWater(volume-1500,y) #what happens if he do not have so much water?
				self.HLines.append(self.HLine)
				#V1_2 = self.fillWater(volume-1000,y)
				V1 += V1_2.V1
				V2 += V1_2.V2
			
			if(V1<=V2):
				print("V1:%f,V2:%f,V[i]:%f,volume:%i,oldvolume:%f,x:%i" % (V1,V2,V[i],volume,self.oldvolume,x))
				self.stopIt = True
			self.parent.speed = V1 - V2
			dVi = V[i]-V[i-S]
			print("%i,%i,Speed %f,depths[i]:%f,V[i]: %f,dV[i]:%f   V1Sum:%f,V2Sum:%f" % (self.parent.framePos,i,self.parent.speed,depths[i],V[i],dVi,V1,V2))
			if(self.stopIt):
				print("DONE")
				return
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
			#	self.framePos += 1
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
