import cv2
import time
import numpy as np
import os
import HandTracingModule as htm

# Initialize variables
brushThickness = 15
eraserThickness = 100
drawColor = (244,184,218) # Default: Pink
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
last_gesture_time = 0  # Initialize last gesture time
gesture_debounce = 0.3  # Debounce time in seconds
clear_gesture_time = 0  # Initialize clear gesture time
selected_tool = 0  # Initialize selected tool (default to pink)

# Load and sort header images based on desired order
folderPath = "Header"
if not os.path.exists(folderPath):
    print(f"❌ Folder {folderPath} not found!")
    exit(1)
overlayList = []
desired_order = ['2_Pink.png', '1_blue.png', '0_Green.png', '3_BLack.png', '4_Eraser.png']  # Map to pink, blue, green, black, eraser
for filename in desired_order:
    img = cv2.imread(f'{folderPath}/{filename}')
    if img is None:
        print(f"❌ Failed to load {filename}, skipping...")
        continue
    overlayList.append(img)
if len(overlayList) != len(desired_order):
    print("❌ Not all header images loaded correctly!")
    exit(1)
header = overlayList[0]

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot open webcam!")
    exit(1)
cap.set(3, 1280)
cap.set(4, 720)

# Hand detector
detector = htm.handDetector(detectionCon=0.75, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        print("❌ Failed to read frame!")
        break
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip
        x2, y2 = lmList[12][1], lmList[12][2]  # Middle finger tip
        fingers = detector.fingersUp()

        # Selection Mode: Two fingers up
        if fingers[1] and fingers[2] and (time.time() - last_gesture_time > gesture_debounce):
            last_gesture_time = time.time()
            xp, yp = 0, 0
            if y1 < 125:  # Toolbar area
                toolbar_width = 1280 // len(overlayList)
                for i in range(len(overlayList)):
                    start_x = i * toolbar_width
                    end_x = (i + 1) * toolbar_width
                    if start_x <= x1 < end_x:
                        header = overlayList[i]
                        print(f"Debug: x1={x1}, range=[{start_x}, {end_x}), selected index={i}")
                        if i == 0:  # Pink
                            drawColor = (244,184,218)
                        elif i == 1:  # Blue
                            drawColor = (255,0,0)
                        elif i == 2:  # Green
                            drawColor = (166, 219, 188)
                        elif i == 3:  # Black
                            drawColor = (128, 128, 128)  # Draw gray
                        elif i == 4:  # Eraser
                            drawColor = (255, 255, 255)  # White for selection
                        selected_tool = i  # Update selected tool
                        break
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # Drawing Mode: Only index finger up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            # Use eraser thickness and black color for erasing when eraser is selected
            thickness = eraserThickness if selected_tool == 4 else brushThickness
            draw_color = (0, 0, 0) if selected_tool == 4 else drawColor  # Erase with black for eraser
            cv2.line(img, (xp, yp), (x1, y1), draw_color, thickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), draw_color, thickness)
            xp, yp = x1, y1

        # Clear Canvas: All five fingers up with debounce
        if fingers == [1, 1, 1, 1, 1] and (time.time() - clear_gesture_time > gesture_debounce):
            clear_gesture_time = time.time()
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)
            cv2.putText(img, "Canvas Cleared!", (400, 360), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
            print("🧼 Canvas cleared using 5-finger gesture")

    # Process image layers
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Set toolbar header
    img[0:125, 0:1280] = header

    cv2.imshow("Virtual Painter", img)
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(f"canvas_{int(time.time())}.png", imgCanvas)
        print("✅ Canvas saved!")
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
