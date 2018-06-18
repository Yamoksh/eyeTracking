from pymouse import PyMouse
from snapShot import takeShot
from screeninfo import get_monitors
import time
for m in get_monitors() :
	hy=m.height
	wx=m.width
m = PyMouse()
listLX=[0]*25
listLY=[0]*25
listRX=[0]*25
listRY=[0]*25

print "Look at top left corner (0,0) then follow  mouse pointer"
time.sleep(1)
px=wx/2
py=hy/2
signx=1
signy=1
index=0 #for listLX increament

for y in (5,hy/4,hy/2,3*hy/4,hy-15):
	for x in (5,wx/4,wx/2,3*wx/4,wx-10):
	
		while px!=x or py!=y :
			if px-x>0 :
				signx=-1
			elif px-x==0 :
				signx=0
		 	else :
				signx=1

			if py-y>0 :
				signy=-1
			elif py-y==0 :
				signy=0
			else:
				signy=1				
				
			time.sleep(0.001)
			m.move(px,py)
			px=px+signx
			py=py+signy	

		
		print "Look at mouse pointer"
		time.sleep(0.5)
		try :
			val_l,lx,ly,val_r,rx,ry=takeShot()
		except TypeError :
			time.sleep(1)
			try :
				val_l,lx,ly,val_r,rx,ry=takeShot()
			except :
				print "Sorry...You missed Try again Calibration"
				continue
		listLX[index]=lx
		listLY[index]=ly
		listRX[index]=rx
		listRY[index]=ry
		index+=1
		time.sleep(0.2)


print "Lx ",listLX
print "LY ",listLY
print "rx ",listRX
print "ry ",listRY

l1=[x + y for x, y in zip(listLX, listRX)]
l2=[x + y for x, y in zip(listLY, listRY)]
print "lr x ",l1
print "lr y ",l2


"""
m.position() #gets mouse current position coordinates
m.move(x,y)
m.click(x,y) #the third argument "1" represents the mouse button
m.press(x,y) #mouse button press
m.release(x,y)

x,y=m.position()
print x
print y
x=100
y=200
m.move(x,y)
"""
