import sys
import os
from PyQt5.QtWidgets import QApplication
from video_overlay import VideoOverlay

def main():
    app = QApplication(sys.argv)
    
    # Get the directory where the current script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to the videos using absolute paths
    video_path_left = os.path.join(base_dir, 'videos', 'parkour.mp4')
    video_path_right = os.path.join(base_dir, 'videos', 'subways.mp4')
    
    # Create overlay instances for left and right
    overlay_left = VideoOverlay(video_path_left, 'left')
    overlay_right = VideoOverlay(video_path_right, 'right')
    
    # Start with the videos hidden
    overlay_left.hide()
    overlay_right.hide()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
