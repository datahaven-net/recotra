import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    while True:
        ret, img = cap.read()
        cv2.imshow('img', img)
        if cv2.waitKey(30) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Alert ! Camera disconnected")
