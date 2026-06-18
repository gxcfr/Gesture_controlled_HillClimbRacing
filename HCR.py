import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

# Eliminate the PyAutoGUI delay bottleneck completely
pyautogui.PAUSE = 0

# Set up detector
detector = HandDetector(detectionCon=0.4, maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 400)

# Track the active key state to prevent spamming Windows hardware inputs
current_key = None 

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read camera")
        continue

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    action_needed = None

    if hands:
        # Get the first detected hand
        my_hand = hands[0]
        fingers = detector.fingersUp(my_hand)
        totalFingers = fingers.count(1)

        # Draw the finger count UI on stream
        cv2.putText(
            img,
            f"Fingers: {totalFingers}",
            (50, 50),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (0, 255, 0),
            2
        )

        # Map finger counts to desired keyboard states
        if totalFingers == 1:
            action_needed = "left"
        elif totalFingers == 2:
            action_needed = "right"

    # Only execute key events if your hand state actually CHANGES
    if action_needed != current_key:
        # 1. Release the previous active key
        if current_key:
            pyautogui.keyUp(current_key)
        
        # 2. Press down the new key
        if action_needed:
            pyautogui.keyDown(action_needed)
        
        # Update current state tracker
        current_key = action_needed

    cv2.imshow("Camera Feed", img)

    # Press ESC to cleanly exit
    if cv2.waitKey(1) & 0xFF == 27:
        if current_key:
            pyautogui.keyUp(current_key)
        break

cap.release()
cv2.destroyAllWindows()