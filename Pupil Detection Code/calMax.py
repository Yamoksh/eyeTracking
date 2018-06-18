from pymouse import PyMouse
from snapShot import takeShot
from screeninfo import get_monitors
import time
import sys

def calMax ():
	listLX=[0]*4
	listLY=[0]*4
	listRX=[0]*4
	listRY=[0]*4
	index=0
	for index in range(0,4):
		if index==0:		
			print "Look at above(highest point of eye without changing your head position)"
		elif index==1:
			print "\nLook at below(lowest point of eye without changing your head position)"
		elif index==2:
			print "Look at left side(Maximum left you can see without changing your head position)"
		elif index==3:
			print "Look at right side(Maximum right you can see without changing your head position)"
	
		time.sleep(3)
		try :
			val_l,lx,ly,val_r,rx,ry=takeShot()
		except TypeError :
			time.sleep(2)
			try :
				val_l,lx,ly,val_r,rx,ry=takeShot()
			except :
				print "Sorry...You missed Try again Calibration"
				sys.exit()
	
		listLX[index]=lx
		listLY[index]=ly
		listRX[index]=rx
		listRY[index]=ry
		time.sleep(1)
	
	
	with open("LX.txt","w") as file:
		file.write(str(listLX))
	with open("LY.txt","w") as file:
		file.write(str(listLY))
	with open("RX.txt","w") as file:
		file.write(str(listRX))
	with open("RY.txt","w") as file:
		file.write(str(listRY))
	
	print "Lx ",listLX
	print "LY ",listLY
	print "rx ",listRX
	print "ry ",listRY
	"""
	with open("LX.txt","r") as file:
		data=eval(file.readline())
	"""
	return listLX,listLY,listRX,listRY

