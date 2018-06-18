import cv2
import numpy as np
import sys

def locate (img) :
	#img=cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)
	#print type(img)
	#print img.shape
	eq=cv2.equalizeHist(img)
	#cv2.imshow("eq",eq)
	val=[0]*9
	h,w=eq.shape
	for i in range(0,h-3):
		for j in range(0,w-3):
			#set value in window		
			for k in range(i,i+3):
				for l in range(j,j+3):
					val[(k-i)*3+(l-j)]=eq[k][l]
			#sort the window
			val.sort()
			#now assign value 
			eq[i][j]=val[4]


	h=h+5
	max_val=-1000
	max_black=0
	locx=0
	locy=0
	i=h/2
	win_h=3
	add=0
	black=0
	black_locx=0
	black_locy=0
	for i in range(h/2,h/2+h/6):
		for j in range(0,w-5):
			#set value in window
			add=0
			black=0
			for k in range(i,i+5):
				for l in range(j,j+5):
					if k==i or k==i+4 or l==j or l==j+4 :
						add-=eq[k,l]
					else :
						add+=eq[k,l]
					if eq[k,l]<=30 :
						black+=1
			if black>15 :
				if black>max_black:
					max_black=black
					black_locy=i
					#locy=i				
					black_locx=j		
			if add>max_val:
				max_val=add
				locy=i				
				locx=j		

	locx+=2
	locy+=2
	
	black_locx+=2
	black_locy+=2
	"""	
	print "Maximum add value ",max_val		
	print "Max locx : ",locx
	print "Max locy : ",locy

	print "Maximum black value ",max_black		
	print "Max black locx : ",black_locx
	print "Max black locy : ",black_locy
	"""
	if abs(black_locx-locx)>10 or abs(black_locy-locy)>6 :
		val=0
		locx=black_locx
		locy=black_locy
	else :
		val=1
	return val,locx,locy

"""
cv2.imshow("img",img)
cv2.imshow("eq 2",eq)
cv2.waitKey(0)
cv2.destroyAllWindow()
"""

