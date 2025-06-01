# Hand Cricket Game 🎳🖐️

A real-time “hand cricket” game that uses your webcam to count the number of fingers you show and pits you against the computer in a simple scoring match. Built with OpenCV, CVZone, and MediaPipe’s hand-tracking.

---

## Features

- Live webcam feed with split-screen UI  
- Detects 0–6 fingers (thumb-only counts as 6)  
- 5-second rounds: computer’s throw locks in at 3 seconds  
- “Out!” if player and computer show the same count  
- Score resets on “Out”, otherwise player accumulates fingers shown  

---

## Prerequisites

- Windows, macOS or Linux with a webcam  
- Conda (Miniconda or Anaconda) installed  

---

## Installation

1. Clone this repository  
   git clone https://github.com/Himanshu-Vishwas/hand-cricket.git  
   cd hand-cricket  

2. Create and activate a Python 3.9 environment  
   conda create --name hand-cricket python=3.9  
   conda activate hand-cricket  

3. Install dependencies  
   pip install opencv-python numpy cvzone mediapipe  

---

## Usage

python main.py

- A window titled **Hand Cricket Game** will open.  
- Show between 0–5 fingers on your hand; thumb up alone counts as 6.  
- After 5 seconds, the round resolves.  
- Press **q** to exit the game.

---

## Troubleshooting

- **cv2 import error**:  
  Ensure you’re in the `hand-cricket` conda env and run:  
  pip install opencv-python  

- **No module named 'cvzone'** or **No module named 'mediapipe'**:  
  Double-check that you installed both packages in the active environment:  
  pip install cvzone mediapipe  

---

## License

This project is released under the MIT License.
