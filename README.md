# CrowdNav

CrowdNav is an application that analyzes crowd movement using live recordings and determines the optimal path between two points.

## Features
- **Real-time crowd movement analysis**: Uses image processing techniques to detect crowd density and movement patterns.
- **Weighted image map generation**: Converts live recordings into a heatmap representing crowd density.
- **Optimal pathfinding**: Implements Dijkstra's algorithm to compute the shortest and least crowded path from point A to point B.
- **User-friendly input**: Simply provide a live recording and select two points to generate a safe and efficient route.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/certified-compiler-boys/HackED2025.git
   cd HackED2025
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python Model/main.py
   ```

## Usage

1. Provide a live recording of a crowd.
2. Mark point A (starting location) and point B (destination).
3. CrowdNav will process the video and generate the optimal path.
4. View the suggested path overlayed on the input recording.

## Technologies Used
- Python
- React (for Front-End)
- OpenCV (for image and video processing)
- NumPy (for matrix operations)
- Dijkstra's Algorithm (for shortest path computation)

## Authors
- Saumya Patel
- Sharavan Nayak
- Rehan Shanavas
- Aditya Gupta
- Jayesh Kumar Goyal
