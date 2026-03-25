# RockLook 🎸🤘

RockLook is an interactive computer vision project that turns your head movements into a music switch. Built with Python, OpenCV, and MediaPipe, this script detects your facial landmarks and calculates a geometric ratio to determine when you are looking downward. 

Conceptually, this acts as a software-based tilt sensor:
**Sensor (Webcam + MediaPipe) → Threshold (Math Ratio) → Actuator (Pygame Audio).**

## Features
✅ **Webcam Feed:** Real-time facial landmark processing.
✅ **Look Down to Rock:** Music automatically unpauses when your gaze drops.
✅ **Look Up to Pause:** Looking forward or upward instantly pauses playback.
✅ **Visual Feedback:** Real-time display of your mathematical tilt ratio and active threshold directly on the video feed.

## Tech Stack
* **Python 3.10+**
* **OpenCV (`cv2`)**: For capturing and displaying the webcam feed.
* **MediaPipe FaceMesh**: For generating 3D facial landmarks to calculate head pitch.
* **Pygame Mixer**: For handling asynchronous audio playback.

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/yourusername/RockLook.git](https://github.com/yourusername/RockLook.git)
   cd RockLook