# Simple Motion Detection System using Python and OpenCV

## Objective
The objective of this hands-on project is to build a real-time motion detection system using Python. It captures video from a webcam, detects moving objects, logs these events securely to a JSON file, and provides a statistical summary and visual graph upon exiting.

## Features
* **Real-Time Motion Detection**: Uses OpenCV to capture and process webcam frames, detecting and highlighting moving objects.
* **Heads-Up Display (HUD)**: Live overlay of date, time, camera status, and object count.
* **Smart JSON Logging**: Logs motion events securely without spamming using a state-transition and debounce logic.
* **Automated Analytics**: Parses the JSON logs using Pandas and generates a daily bar chart using Matplotlib.
* **Graceful Exit**: Always cleans up resources safely and triggers analysis.

## Technologies Used
* **Python**: Core programming language.
* **OpenCV (cv2)**: Image processing and webcam interaction.
* **NumPy**: Matrix operations for OpenCV.
* **Pandas**: Data aggregation and analysis.
* **Matplotlib**: Statistical graph generation.

## Project Structure
```text
Simple-Motion-Detection-System/
├── .venv/                     (Python virtual environment)
├── main.py                    (Main application loop & UI)
├── motion_detector.py         (OpenCV motion tracking logic)
├── motion_logger.py           (JSON data logging with debounce)
├── statistics.py              (Pandas analysis & Matplotlib graphing)
├── motion_data.json           (Persistent log data storage)
├── motion_statistics.png      (Generated statistical chart)
├── requirements.txt           (Project dependencies)
└── README.md                  (Project documentation)
```

## Installation Steps
1. Create a virtual environment (optional but recommended): `python -m venv .venv`
2. Activate the virtual environment.
3. Install the required dependencies: 
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Project
Start the main application by running:
```bash
python main.py
```

## Keyboard Control
* Press **`q`** or **`Q`** while focused on the video window to stop the camera, generate statistics, and exit gracefully.

## Motion Detection Algorithm
The `MotionDetector` class follows a standard computer vision pipeline:
1. **Grayscale Conversion**: Simplifies the image, removing color.
2. **Gaussian Blur**: Smooths the image to remove high-frequency noise.
3. **Absolute Difference**: Compares the current frame to the baseline previous frame.
4. **Binary Thresholding**: Isolates regions with significant changes.
5. **Dilation**: Fills in gaps in the thresholded shapes.
6. **Contour Detection**: Finds the boundaries of the isolated shapes, ignoring areas smaller than a minimum threshold to filter out noise.

## Logging and Analytics
* **JSON Logging**: `MotionLogger` records the start of every distinct motion event (with a 2-second cooldown to avoid duplicates). It handles missing or corrupt files safely.
* **Pandas Statistics**: `statistics.py` converts the JSON into a Pandas DataFrame to rapidly calculate total events, object counts, and groups data by date.
* **Matplotlib Graph**: Upon exit, a bar chart (`motion_statistics.png`) is automatically generated showing the number of events per day.

## Example Output
```text
=================================
MOTION DETECTION SYSTEM
=================================
Camera stopped.
Generating motion statistics...
Motion statistics saved to: motion_statistics.png
Motion detection system closed.
```

## Curriculum Concepts Covered (Units I-IV)
* **Unit I (Python Basics & Control Flow)**: Implementation of application loops, functions, exception handling (`try/except/finally`), and conditionals.
* **Unit II (Data Structures & OOP)**: Usage of lists, dictionaries, and organizing code into reusable object-oriented classes (`MotionDetector`, `MotionLogger`).
* **Unit III (File I/O & Modules)**: Safe file reading and writing using `json` and `pathlib`, importing standard modules (`datetime`).
* **Unit IV (Data Analysis & Visualization)**: Utilizing `pandas` DataFrames for data manipulation/aggregation and `matplotlib` for creating graphical plots.
