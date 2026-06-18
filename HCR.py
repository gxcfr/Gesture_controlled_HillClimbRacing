import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
pyautogui.PAUSE = 0

detector = HandDetector(detectionCon=0.3, maxHands=2)

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

    # Track if an action was taken this frame
    action_taken = False

    if hands:
        # Note: If it doesn't detect your hand, try changing "Left" to "Right"
        if hands[0]["type"]:
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

            # 0 Fingers -> Move Left
            if totalFingers == 0:
                pyautogui.keyDown("left")
                pyautogui.keyUp("right")
                action_taken = True
            
            # 1 Finger -> Move Right
            elif totalFingers == 1:
                pyautogui.keyDown("right")
                pyautogui.keyUp("left")
                action_taken = True

    # If no action was taken (hand missing, or 2+ fingers), release all keys
    if not action_taken:
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")

    cv2.imshow("Camera Feed", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        # Safety reset before exiting
        pyautogui.keyUp("left")
        pyautogui.keyUp("right")
        break

cap.release()
cv2.destroyAllWindows()