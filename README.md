# Video Overlay Application

## Overview

This application creates overlay windows to display videos in a small portion of the screen, with the ability to toggle their visibility using global keyboard shortcuts. The videos are shown at a fixed aspect ratio (9:16) and can be positioned on the left or right side of the screen. The audio from the videos is also managed and synchronized with the video playback.

## Features

- **Video Overlay**: Displays videos as overlays with a 9:16 aspect ratio.
- **Positioning**: Option to position the overlay on the left or right side of the screen.
- **Visibility Control**: Toggle visibility of the video overlays using the F6 and F7 keys.
- **Audio Playback**: Extracts and plays audio from the videos.

## Requirements

- Python 3.x
- `opencv-python`
- `numpy`
- `pygame`
- `moviepy`
- `PyQt5`
- `pynput`

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd your-repo-name
    ```

3. **Install required packages**:

    ```bash
    pip install opencv-python numpy pygame moviepy PyQt5 pynput
    ```

## Usage

1. **Prepare your video files**:
    - Place your video files in the project directory or provide their paths.

2. **Run the application**:

    ```bash
    python main.py
    ```

    Replace `main.py` with the name of your Python script if it's different.

3. **Toggle visibility**:
    - Press `F6` to show the video overlays.
    - Press `F7` to hide the video overlays.

## Configuration

- **Video Paths**: Modify the `video_path_left` and `video_path_right` variables in the script to point to your video files.

## Troubleshooting

- **FFmpeg Error**: Ensure FFmpeg is installed and added to your system's PATH. FFmpeg is used by `moviepy` for audio extraction.
- **Library Issues**: Ensure all required libraries are installed and up to date.

