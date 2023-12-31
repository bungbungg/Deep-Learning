{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import mediapipe\n",
    "import numpy\n",
    "import autopy\n",
    "\n",
    "cap = cv2.VideoCapture(0)\n",
    "initHand = mediapipe.solutions.hands  # Initializing mediapipe\n",
    "# Object of mediapipe with \"arguments for the hands module\"\n",
    "mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)\n",
    "draw = mediapipe.solutions.drawing_utils  # Object to draw the connections between each finger index\n",
    "wScr, hScr = autopy.screen.size()  # Outputs the high and width of the screen (1920 x 1080)\n",
    "pX, pY = 0, 0  # Previous x and y location\n",
    "cX, cY = 0, 0  # Current x and y location\n",
    "\n",
    "\n",
    "def handLandmarks(colorImg):\n",
    "    landmarkList = []  # Default values if no landmarks are tracked\n",
    "\n",
    "    landmarkPositions = mainHand.process(colorImg)  # Object for processing the video input\n",
    "    landmarkCheck = landmarkPositions.multi_hand_landmarks  # Stores the out of the processing object (returns False on empty)\n",
    "    if landmarkCheck:  # Checks if landmarks are tracked\n",
    "        for hand in landmarkCheck:  # Landmarks for each hand\n",
    "            for index, landmark in enumerate(hand.landmark):  # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)\n",
    "                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)  # Draws each individual index on the hand with connections\n",
    "                h, w, c = img.shape  # Height, width and channel on the image\n",
    "                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  # Converts the decimal coordinates relative to the image for each index\n",
    "                landmarkList.append([index, centerX, centerY])  # Adding index and its coordinates to a list\n",
    "                \n",
    "    return landmarkList\n",
    "\n",
    "\n",
    "def fingers(landmarks):\n",
    "    fingerTips = []  # To store 4 sets of 1s or 0s\n",
    "    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger\n",
    "    \n",
    "    # Check if thumb is up\n",
    "    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:\n",
    "        fingerTips.append(1)\n",
    "    else:\n",
    "        fingerTips.append(0)\n",
    "    \n",
    "    # Check if fingers are up except the thumb\n",
    "    for id in range(1, 5):\n",
    "        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint\n",
    "            fingerTips.append(1)\n",
    "        else:\n",
    "            fingerTips.append(0)\n",
    "\n",
    "    return fingerTips\n",
    "\n",
    "\n",
    "while True:\n",
    "    check, img = cap.read()  # Reads frames from the camera\n",
    "    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Changes the format of the frames from BGR to RGB\n",
    "    lmList = handLandmarks(imgRGB)\n",
    "    # cv2.rectangle(img, (75, 75), (640 - 75, 480 - 75), (255, 0, 255), 2)\n",
    "    \n",
    "    if len(lmList) != 0:\n",
    "        x1, y1 = lmList[8][1:]  # Gets index 8s x and y values (skips index value because it starts from 1)\n",
    "        x2, y2 = lmList[12][1:]  # Gets index 12s x and y values (skips index value because it starts from 1)\n",
    "        finger = fingers(lmList)  # Calling the fingers function to check which fingers are up\n",
    "        x3 = numpy.interp(x1, (75, 640 - 75), (0, wScr))  # Converts the width of the window relative to the screen width\n",
    "        y3 = numpy.interp(y1, (75, 480 - 75), (0, hScr))  # Converts the height of the window relative to the screen height\n",
    "        \n",
    "        if finger[1] == 1 and finger[2] == 0:  # Checks to see if the pointing finger is up and thumb finger is dow\n",
    "            cX = pX + (x3 - pX) / 7  # Stores previous x locations to update current x location\n",
    "            cY = pY + (y3 - pY) / 7  # Stores previous y locations to update current y location\n",
    "            \n",
    "            autopy.mouse.move(wScr-cX, cY)  # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)\n",
    "            pX, pY = cX, cY  # Stores the current x and y location as previous x and y location for next loop\n",
    "\n",
    "        if finger[0] == 1 and finger[1] == 1:  # Checks to see if the pointer finger is down and thumb finger is up\n",
    "            autopy.mouse.click()  # Left click\n",
    "            \n",
    "    cv2.imshow(\"Webcam\", img)\n",
    "    if cv2.waitKey(1) & 0xFF == ord('q'):\n",
    "        break"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
