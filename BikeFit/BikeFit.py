import numpy as np
import cv2

vid_file_path = "../data/IMG_1478.MOV"

def resize(img):
    return cv2.resize(img,(960,540)[::-1])

def contour_center(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX, cY

def find_core_angle(p0,p1,p2):
    ba = p0 - p1
    bc = p2 - p1

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

cap=cv2.VideoCapture(vid_file_path)
area_threshold = 20

ret,frame=cap.read()
l_b=np.array([40,0,0][::-1])# lower hsv bound for red
u_b=np.array([200,60,60][::-1])# upper hsv bound to red

while ret==True:
    ret,frame=cap.read()

    mask=cv2.inRange(frame,l_b,u_b)

    contours,_= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    total_contours = len(contours)
    previous_contour = 'reset'
    contours_for_angle = []
    for contour in contours:
        if cv2.contourArea(contour) > area_threshold:
            approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    #         x,y,w,h=cv2.boundingRect(approx)
    #         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)
            try:
                cX, cY = contour_center(contour)
                contours_for_angle.append(np.array([cX, cY]))
#                 print('points & size: ',cX, cY, cv2.contourArea(contour))
                cv2.circle(frame, (cX, cY), 7, (0, 255, 255), -1)
            except:
                print('failed to find')
    angle_between = find_core_angle(*contours_for_angle)
    print(angle_between)
    cv2.putText(frame, str(round(angle_between,3))
                ,(contours_for_angle[1][0] - 20, contours_for_angle[1][1] - 20)
                ,cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 2)


    cv2.imshow("frame",resize(frame))
    cv2.imshow("mask",mask)

    key=cv2.waitKey(1)
    if key==ord('q'):
        break
cv2.waitKey(0)
cv2.destroyAllWindows()