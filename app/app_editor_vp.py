import customtkinter as ctk
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import time
import redis
import requests
import os
from urllib.parse import urlparse
import imageio

class VideoPlayer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  # Base color
        
        # Configure grid for full expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color="#ebeaf2")  # Base color
        
        # Video display area with modern styling
        self.video_label = ctk.CTkLabel(
            self,
            text="Ready to play video",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#ebeaf2",  # Secondary color
            fg_color="#1a191f",  # Base color
            corner_radius=10
        )
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        
        # Control frame with modern styling
        self.control_frame = ctk.CTkFrame(
            self,
            fg_color="#1a191f",  # Secondary color
            corner_radius=8
        )
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        # Play/Pause button with accent color
        self.play_pause_btn = ctk.CTkButton(
            self.control_frame,
            text="Play",
            command=self.toggle_play_pause,
            fg_color="#db2859",  # Accent color
            hover_color="#b5234a",  # Darker accent for hover
            text_color="#ebeaf2",  # Base color for text
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            corner_radius=6,
            width=100
        )
        self.play_pause_btn.grid(row=0, column=0, padx=(10, 5), pady=8)
        
        # Progress bar with accent color
        self.progress_var = ctk.DoubleVar()
        self.progress_slider = ctk.CTkSlider(
            self.control_frame,
            from_=0,
            to=100,
            variable=self.progress_var,
            fg_color="#ebeaf2",  # Base color
            progress_color="#db2859",  # Accent color
            button_color="#1a191f",  # Secondary color
            button_hover_color="#db2859"  # Accent color
        )
        self.progress_slider.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=8)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        
        # Video state variables
        self.reader = None
        self.playing = False
        self.video_source = ""
        self.total_frames = 0
        self.current_frame = 0
        self.fps = 60
        self.native_width = 0
        self.native_height = 0
        self.aspect_ratio = 0
        self.last_frame_time = 0
        self.after_id = None
        
        # Bind resize event
        self.video_label.bind("<Configure>", self.on_label_resize)
    
    def on_label_resize(self, event):
        """Handle label resize to update video display"""
        if self.reader and not self.playing:
            self.display_frame(self.current_frame)
    
    def load_video_from_url(self, video_url):
        """Load and display video from URL"""
        self._load_video(video_url)
    
    def load_video(self, video_path):
        """Load and display video from local path"""
        self._load_video(video_path)
    
    def _load_video(self, video_source):
        """Internal method to load video from source"""
        try:
            # Clean up existing player
            self.stop_playback()
            
            self.video_source = video_source
            self.playing = False
            self.play_pause_btn.configure(text="Play")
            self.progress_var.set(0)
            
            # Open video reader
            self.reader = imageio.get_reader(video_source)
            meta = self.reader.get_meta_data()
            self.fps = meta.get('fps', 60)
            self.total_frames = self.reader.count_frames()
            print(self.total_frames, self.fps)
            self.native_width = meta.get('size', (1920, 1080))[0]
            self.native_height = meta.get('size', (1920, 1080))[1]
            self.aspect_ratio = self.native_width / self.native_height
            # Show first frame
            self.current_frame = 0
            self.display_frame(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading video: {str(e)}")
    
    def stop_playback(self):
        """Stop any ongoing playback"""
        self.playing = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        if self.reader:
            self.reader.close()
    
    def display_frame(self, frame_index):
        """Display a specific video frame with optimal quality"""
        if not self.reader or frame_index < 0 or frame_index >= self.total_frames:
            return
        
        try:
            # Get the frame
            frame = self.reader.get_data(frame_index)
            self.current_frame = frame_index
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame)
            
            # Get available display area
            label_width = self.video_label.winfo_width()
            label_height = self.video_label.winfo_height()
            
            # Calculate optimal display size while preserving aspect ratio
            if label_width > 0 and label_height > 0:
                display_ratio = label_width / label_height
                
                if display_ratio > self.aspect_ratio:
                    # Fit to height
                    new_height = label_height
                    new_width = int(new_height * self.aspect_ratio)
                else:
                    # Fit to width
                    new_width = label_width
                    new_height = int(new_width / self.aspect_ratio)
                
                # Resize with high-quality Lanczos filter
                pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to CTkImage
            ctk_image = ctk.CTkImage(
                light_image=pil_image,
                size=(new_width, new_height)
            )
            
            # Update label
            self.video_label.configure(image=ctk_image, text="")
            self.video_label.image = ctk_image
            
            # Update progress
            self.progress_var.set(frame_index)
            
        except Exception as e:
            print(f"Error displaying frame: {str(e)}")
    
    def toggle_play_pause(self):
        """Toggle play/pause state"""
        if not self.reader:
            return
        
        self.playing = not self.playing
        
        if self.playing:
            self.play_pause_btn.configure(text="Pause")
            self.play_video()
        else:
            self.play_pause_btn.configure(text="Play")
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None
    
    def play_video(self):
        """Play video using main thread scheduling"""
        if not self.playing or not self.reader or self.current_frame >= self.total_frames - 1:
            self.playing = False
            self.play_pause_btn.configure(text="Play")
            return
        
        start_time = time.time()
        
        # Display current frame
        self.display_frame(self.current_frame)
        
        # Calculate processing time and frame delay
        processing_time = time.time() - start_time
        frame_delay = max(1, int(1000 / self.fps - processing_time * 1000))
        
        # Move to next frame
        self.current_frame += 1
        
        # Schedule next frame
        self.after_id = self.after(frame_delay, self.play_video)
    
    def on_slider_release(self, event):
        """Handle slider seek operation"""
        if not self.reader:
            return
        
        # Stop any ongoing playback
        was_playing = self.playing
        if self.playing:
            self.playing = False
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None
        
        # Calculate target frame
        target_frame = min(max(0, int(self.progress_var.get())), self.total_frames - 1)
        self.current_frame = target_frame
        
        # Update display
        self.display_frame(target_frame)
        
        # Restart playback if was playing
        if was_playing:
            self.playing = True
            self.play_pause_btn.configure(text="Pause")
            self.play_video()