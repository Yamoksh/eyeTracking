import numpy as np
import cv2
import math
from camEye2 import locate 

def takeShot () :
	try:	
	    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	    eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')

	    #number signifies camera
	    #cap = cv2.VideoCapture("face1.mp4")
	    cap = cv2.VideoCapture(0)
	    temp_var=0
	
	    ret, img = cap.read()
	    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    
	    face = face_cascade.detectMultiScale(gray_img,1.3,5)
	    for (x,y,w,h) in face :
	      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	      roi_gray_face=gray_img[y:y+h-h*0.4, x:x+w*1.4]
	      roi_color_face = img[y:y+h, x:x+w]
	     
	      #roi_gray = cv2.equalizeHist(roi_gray_face)		
	      eye = eye_cascade.detectMultiScale(roi_gray_face)
	      #print len(eye)
	      	
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
		roi_gray_le = roi_gray_face[ley:ley+leh, lex:lex+lew] #for right eye

	
	
	
		#method calling (finding pupil in given eye image)--->moksh function(;_*_;)
				
		val_r,px_r,py_r=locate(roi_gray_re)
		cv2.circle(roi_gray_re,(px_r,py_r),3,(255,0,0),3)
		cv2.imwrite("Right.jpg",roi_gray_re)	
	

		val_l,px_l,py_l=locate(roi_gray_le)
		cv2.circle(roi_gray_le,(px_r,py_r),3,(255,0,0),3)
		cv2.imwrite("left.jpg",roi_gray_le)
		
		

		cap.release()
			
		return val_l,px_l,py_l,val_r,px_r,py_r
	finally :
		cap.release()		
	
	
