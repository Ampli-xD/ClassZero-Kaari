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

class SlideCard(ctk.CTkFrame):

    def __init__(self, parent, slide_data, on_select_callback, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.slide_data = slide_data
        self.on_select_callback = on_select_callback
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="#ebeaf2")  # Base color
        
        # Slide preview frame with modern styling
        self.preview_frame = ctk.CTkFrame(
            self,
            fg_color="#1a191f",  # Secondary color
            corner_radius=10,
            height=100,
            border_width=2,
            border_color="#db2859"  # Accent color
        )
        self.preview_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Configure preview frame grid for better text placement
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Slide info with modern typography
        slide_type = slide_data.get('slide_type', 'Unknown')
        slide_pos = slide_data.get('slide_pos', 0)
        
        # Check if slide has been processed
        has_data = slide_data.get('slide_data') not in [None, '{}', {}]
        has_video = slide_data.get('render_video_link') is not None
        has_image = slide_data.get('render_img_link') is not None
        
        status = "✓ Ready" if (has_data and has_video and has_image) else "⏳ Processing"
        
        # Slide type and status label
        self.type_label = ctk.CTkLabel(
            self.preview_frame,
            text=f"{slide_type} - {status}",
            font=("Roboto", 16, "bold"),
            text_color="#ebeaf2",  # Base color for text
            anchor="w"
        )
        self.type_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
        
        # Position label
        self.pos_label = ctk.CTkLabel(
            self.preview_frame,
            text=f"Position: {slide_pos}",
            font=("Roboto", 12),
            text_color="#ebeaf2",  # Base color for text
            anchor="w"
        )
        self.pos_label.grid(row=1, column=0, sticky="w", padx=10, pady=(2, 10))
        
        # Bind click event
        self.preview_frame.bind("<Button-1>", self.on_click)
        self.type_label.bind("<Button-1>", self.on_click)
        self.pos_label.bind("<Button-1>", self.on_click)
    
    def on_click(self, event=None):
        """Handle slide selection"""
        if self.on_select_callback:
            self.on_select_callback(self.slide_data)
    
    def update_slide_data(self, new_slide_data):
        """Update the slide data and refresh display"""
        self.slide_data = new_slide_data
        
        slide_type = new_slide_data.get('slide_type', 'Unknown')
        slide_pos = new_slide_data.get('slide_pos', 0)
        
        # Check if slide has been processed
        has_data = new_slide_data.get('slide_data') not in [None, '{}', {}]
        has_video = new_slide_data.get('render_video_link') is not None
        has_image = new_slide_data.get('render_img_link') is not None
        
        status = "✓ Ready" if (has_data and has_video and has_image) else "⏳ Processing"
        
        self.type_label.configure(text=f"{slide_type} - {status}")
        self.pos_label.configure(text=f"Position: {slide_pos}")