import numpy as np
import cv2
import math
from camEye2 import locate 
from calMax import calMax
from pymouse import PyMouse
from screeninfo import get_monitors
import time
for m in get_monitors() :
	screen_height=m.height
	screen_width=m.width

#variables for mouse control
mouse = PyMouse()
mouse.move(screen_width/2,screen_height/2)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')

#number signifies camera



"""----->> CALIBRATION OF MAXIMUM POINT OF EYE (Format-->> Top, below, left and right)"""
listLX,listLY,listRX,listRY=calMax()
"""
with open("LX.txt","r") as file:
		listLX=eval(file.readline())
with open("LY.txt","r") as file:
		listLY=eval(file.readline())
with open("RX.txt","r") as file:
		listRX=eval(file.readline())
with open("RY.txt","r") as file:
		listRY=eval(file.readline())
print listRY[0]
"""
"""--->>> START CAMERA MODE """
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("face.mp4")
temp_var=0
temp_x=0
temp_y=0
while 1:
    ret, img = cap.read()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face = face_cascade.detectMultiScale(gray_img,1.3,5)
    for (x,y,w,h) in face :
      cv2.circle(img,(x+w/2,y+h/4),3,(123,123,123),3)
      temp_x=x+w/2
      temp_y=y+h/2
      print "x ",x+w/2
      print "y ",y+h/4		
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
      roi_gray_face=gray_img[y:int(y+h-h*0.4), x:int(x+w*1.4)]
      roi_color_face = img[y:y+h, x:x+w]
     		
      eye = eye_cascade.detectMultiScale(roi_gray_face)
      
      #print "len of eye"
      #print len(eye)
	
      """BELOW IS CALCULATION FOR DECIDING left or right"""	
      i=0
      j=1
      flag=0
      if len(eye)>3:
		break
      if len(eye)==2 :
	if eye[0][1]<eye[1][1]+10 or eye[1][1]<eye[0][1]+10  :
		flag=1	
      if len(eye)==3 :
	if eye[0][1]<eye[2][1]+10 or eye[2][1]<eye[0][1]+10  :
		j=2
		flag=1
	elif eye[1][1]<eye[2][1]+10 or eye[2][1]<eye[1][1]+10  :
		j=2
		i=1
		flag=1	
      if flag==1:
      	rex=eye[i][0] 
	lex=eye[j][0]
	#right eye will be in left side with minimum x value
	if rex>lex :
		rex=eye[j][0]
		rey=eye[j][1]
		rew =eye[j][2]
		reh=eye[j][3]
		
		lex=eye[i][0]
		ley=eye[i][1]
		lew =eye[i][2]
		leh=eye[i][3]
	else :
		rey=eye[i][1]
		rew =eye[i][2]
		reh=eye[i][3]
		
		ley=eye[j][1]
		lew =eye[j][2]
		leh=eye[j][3]

	cv2.putText(roi_gray_face,'LE',(lex,ley),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
	cv2.putText(roi_gray_face,'RE',(rex,rey),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
	roi_gray_re = roi_gray_face[rey:rey+reh, rex:rex+rew] #for right eye
	
	roi_gray_le = roi_gray_face[ley:ley+leh, lex:lex+0.8*lew] #for left eye

	

	#cv2.imwrite("camEye.jpg",roi_gray_le)
	
	
	"""Method calling (finding pupil in given eye image)--->moksh function(;_*_;)"""
	val_r,px_r,py_r=locate(roi_gray_re)
	print "px_r ",px_r
	cv2.circle(roi_gray_re,(px_r,py_r),3,(255,0,0),3)
	#print "px_r ",px_r
	val_l,px_l,py_l=locate(roi_gray_le)
	cv2.circle(roi_gray_le,(px_l,py_l),3,(255,0,0),3)


	cv2.imshow("right eye",roi_gray_re)
	cv2.imshow("left eye",roi_gray_le)
	#print "px_l ",px_l
	"""MOUSE MOVEMENT CONTROL"""
	
	px,py=mouse.position()
	if temp_x<210 :
		mx=0
	elif temp_x>420:
		mx=screen_width
	else :
		mx=(temp_x-210)*screen_width/(420-210)
	
	if temp_y<200:
		my=0
	elif temp_y>280:
		my=screen_height
	else:
		my=(temp_y-200)*screen_height/(280-200)

	if abs(px_r-listRX[2])<3 and abs(px_l-listLX[2])<3:
		mx=mx+screen_width/4
	if abs(px_r-listRX[3])<3 and abs(px_l-listLX[3])<3:
		mx=mx-screen_width/4
	
	if abs(py_r-listRY[1])<3 and abs(py_l-listLY[1])<3:
		my=my-screen_height/4
	if abs(py_r-listRY[0])<3  and abs(py_l-listLY[0])<3:
		my=my+screen_height/4
	signx=1
	signy=1
	while px!=mx or py!=my :
		if px-mx>0 :
			signx=-1
		elif px-mx==0 :
			signx=0
	 	else :
			signx=1

		if py-my>0 :
			signy=-1
		elif py-my==0 :
			signy=0
		else:
			signy=1				
			
		time.sleep(0.0009)
		print "move"
		mouse.move(px,py)
		px=px+signx
		py=py+signy
	
	
    cv2.imshow("face",roi_gray_face)
    cv2.imshow('img',img)	
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

