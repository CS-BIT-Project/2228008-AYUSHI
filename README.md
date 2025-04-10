# 🎨 AI Virtual Painter

AI Virtual Painter is a computer vision-based project that allows users to draw on the screen using only hand gestures — no touch input or mouse required! This interactive tool uses your webcam to track hand movements and interprets specific finger gestures to perform painting actions like selecting colors, clearing the canvas, and drawing.

## ✨ Features

- 🖐️ Hand gesture recognition using MediaPipe
- 🎨 Real-time drawing with finger tracking
- 🌈 Color palette selection via gesture
- 🧼 Canvas clear functionality
- 📸 Webcam input for natural interaction
- 🧠 Object-oriented modular code

## 📦 Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy

## 🧠 How It Works

- The webcam captures the hand in real-time.
- MediaPipe detects hand landmarks.
- Finger positions determine the drawing mode:
  - **Index Finger Up** → Drawing Mode
  - **Index + Middle Fingers Up** → Selection Mode
  - Special gestures for clearing canvas or color selection.
- Selected color is applied to drawing strokes.

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3 installed along with the following libraries:

```bash
pip install opencv-python mediapipe numpy
