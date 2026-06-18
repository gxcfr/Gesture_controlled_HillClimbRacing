import cv2

cap= cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4,400)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    cv2.imshow('Camera Feed', img)
    cv2.waitKey(1)