import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.5, maxHands=2)

cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 400)

while True:
    success, img = cap.read()

    if not success:
        print("Failed to read camera")
        continue

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands and hands[0]["type"] == "Left":
        fingers = detector.fingersUp(hands[0])
        totalFingers = fingers.count(1)

        cv2.putText(
            img,
            f"Fingers: {totalFingers}",
            (50, 50),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (0, 255, 0),
            2
        )

    cv2.imshow("Camera Feed", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()