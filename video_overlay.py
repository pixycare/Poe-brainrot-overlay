# video_overlay.py

import cv2
import numpy as np
import pygame
from pygame import mixer
from moviepy.editor import VideoFileClip
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication  # Added QApplication import
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QImage, QPixmap
import os
import tempfile
from pynput import keyboard
import threading

class VideoOverlay(QMainWindow):
    def __init__(self, video_path, position, parent=None):
        super(VideoOverlay, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Video parameters
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(self.video_path)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms

        # Setup QLabel for video display
        self.label = QLabel(self)
        self.position = position
        self.update_position()

        # Initialize pygame mixer and play audio
        pygame.init()
        mixer.init()
        self.audio_path = self.extract_audio()

        # Start a thread to listen for global key presses
        self.listener_thread = threading.Thread(target=self.listen_for_keys)
        self.listener_thread.daemon = True  # Daemonize thread
        self.listener_thread.start()

        # Initially hide the video
        self.hide_videos = True
        self.update_visibility()

    def update_position(self):
        screen_geometry = QApplication.desktop().screenGeometry()  # QApplication now recognized

        # Set overlay width to be 1/6 of the screen width
        self.overlay_width = screen_geometry.width() // 6
        # Set overlay height to maintain 9:16 aspect ratio
        self.overlay_height = int(self.overlay_width * 16 / 9)

        # Position the window based on the specified position ('left' or 'right')
        if self.position == 'right':
            x = screen_geometry.width() - self.overlay_width
            y = (screen_geometry.height() - self.overlay_height) // 2
        elif self.position == 'left':
            x = 0
            y = (screen_geometry.height() - self.overlay_height) // 2
        
        # Ensure the position is within screen boundaries
        x = max(0, min(x, screen_geometry.width() - self.overlay_width))
        y = max(0, min(y, screen_geometry.height() - self.overlay_height))
        
        # Set the geometry and label size
        self.setGeometry(QRect(x, y, self.overlay_width, self.overlay_height))
        self.label.setGeometry(self.rect())

    def update_frame(self):
        if self.hide_videos:
            return

        ret, frame = self.video_capture.read()
        if not ret:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape

        # Resize frame to fit within the QLabel while maintaining aspect ratio
        aspect_ratio = w / h
        if w > self.overlay_width or h > self.overlay_height:
            if w / self.overlay_width > h / self.overlay_height:
                w = self.overlay_width
                h = int(w / aspect_ratio)
            else:
                h = self.overlay_height
                w = int(h * aspect_ratio)

        # Resize the frame
        frame_resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)
        
        q_img = QImage(frame_resized.data, w, h, w * ch, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def extract_audio(self):
        # Create a unique temporary file for audio
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_audio_path = temp_audio_file.name
        temp_audio_file.close()

        # Extract audio from video and save as a temporary file
        clip = VideoFileClip(self.video_path)
        clip.audio.write_audiofile(temp_audio_path)

        return temp_audio_path

    def play_audio(self):
        # Load and play audio using pygame mixer
        mixer.music.load(self.audio_path)
        mixer.music.play()

    def stop_audio(self):
        # Stop audio playback
        mixer.music.stop()

    def closeEvent(self, event):
        self.video_capture.release()
        self.stop_audio()  # Stop audio playback
        pygame.quit()  # Quit pygame
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)  # Clean up the temporary audio file
        event.accept()

    def listen_for_keys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f6:
                    self.hide_videos = False
                    self.reset_video()  # Reset video to start from the beginning
                    self.update_visibility()
                elif key == keyboard.Key.f7:
                    self.hide_videos = True
                    self.update_visibility()
            except AttributeError:
                pass

        # Set up the listener for global key presses
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def reset_video(self):
        # Reset video playback to the beginning
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.stop_audio()
        self.play_audio()

    def update_visibility(self):
        if self.hide_videos:
            self.hide()
            self.stop_audio()
        else:
            self.show()
            self.play_audio()
