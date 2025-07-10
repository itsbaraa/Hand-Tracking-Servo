# Hand Tracking Controlled Servo

Control a servo motor in real time using hand tracking with MediaPipe and OpenCV. The servo angle follows the horizontal position of your index finger.

## Overview

- Uses your webcam to detect a hand.
- Tracks the X-position of your index finger.
- Converts the position into a servo angle (0°–180°).
- Sends the angle to an Arduino via serial communication.

## Components

- Arduino Uno
- Servo Motor

## Prerequisites
Python (3.9 - 3.12)
  
Install the following Python libraries:
  
`pip install opencv-python mediapipe pyserial`

## Showcase

https://github.com/user-attachments/assets/8ce73699-2a45-41c3-aed3-e1b925922194
