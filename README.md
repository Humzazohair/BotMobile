# BotMobile

#### This repository contains all the code necessary for implementing a self-driving PyCar based on real-time data collected from a camera and ultrasonic sensors.

## Video Demonstration
[![Thumbnail](https://cdn.prod.website-files.com/63d04d4b1b2834390e504ddf/64f8e5421c1629c792309d26_Artboard%2013-tiny%20copy.jpg)]([(https://drive.google.com/file/d/1t-hd1w701OHVkuEkH3VGtFMHdtcwcNUX/view?t=3])

## GitHub Repository
Access the full codebase here:  
[GitHub Repo Link](https://github.com/Humzazohair/BotMobile)

- `main.py`: Combines object detection, ultrasonic mapping, A*, and sockets.
- `object_detection.py`: Object detection code.
- `mapping.py`: Ultrasonic sensor mapping code.
- `astar.py`: A* pathfinding implementation.

## Key Features

### Advanced Mapping
The mapping solution uses ultrasonic sensors to create a 100 cm x 100 cm grid, where obstacles are represented in a 2D array. We applied padding around obstacles to improve safety margins and enhance A* pathfinding. Interpolation fills in skipped sensor readings, optimizing the sensor sweep for efficiency.

### Object Detection
We implemented object detection using Google’s Mediapipe library on the Raspberry Pi, with multi-threading for efficient image capture and processing. The system can detect objects in real-time, and data is communicated between processes using sockets.

**Hardware Acceleration:** While we used CPU-based processing, a GPU could significantly improve object detection performance.

**Multithreading:** Enabled parallel tasks for image capture and processing, improving system efficiency.

**Frame Rate vs Accuracy:** A medium frame rate balanced real-time performance with detection accuracy.

### A* Pathfinding
We implemented A* pathfinding with a Manhattan distance heuristic and added a turn penalty to minimize unnecessary turns. This allowed for smoother and more efficient routing, especially given motor issues that required fewer turns for better accuracy.

### Full Self-Driving
Our self-driving system combines object detection and ultrasonic mapping with A* pathfinding. Using multithreading and socket communication, the system dynamically adjusts routes to avoid both static and moving obstacles.


## Skills Used
- Multithreading
- Sockets and Interprocess Communication
- A* Pathfinding
- Ultrasonic Sensor Mapping
- Object Detection with TensorFlow Lite
