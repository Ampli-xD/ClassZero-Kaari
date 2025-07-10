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

class LoadingOverlay(ctk.CTkToplevel):

    def __init__(self, parent, title="Processing..."):
        super().__init__(parent)
        
        # Configure window appearance
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ebeaf2")  # Base color
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        # Center the window on parent
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        
        window_width = 400
        window_height = 200
        x = parent_x + (parent_width - window_width) // 2
        y = parent_y + (parent_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure window
        self.resizable(False, False)
        
        # Main frame with modern styling
        main_frame = ctk.CTkFrame(
            self,
            fg_color="#ebeaf2",  # Base color
            corner_radius=10,
            border_width=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Loading animation with accent color
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            mode="indeterminate",
            progress_color="#db2859",  # Accent color
            determinate_speed=2
        )
        self.progress_bar.pack(pady=(30, 20))
        self.progress_bar.start()
        
        # Status label with modern typography
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Processing your request...",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#1a191f"  # Secondary color
        )
        self.status_label.pack(pady=(10, 5))
        
        # Progress details with subtle styling
        self.details_label = ctk.CTkLabel(
            main_frame,
            text="Waiting for AI processing...",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="#1a191f"  # Secondary color
        )
        self.details_label.pack(pady=5)
    
    def update_status(self, status, details=""):
        """Update the loading status"""
        self.status_label.configure(text=status)
        if details:
            self.details_label.configure(text=details)
    
    def close_overlay(self):
        """Close the overlay"""
        self.progress_bar.stop()
        self.destroy()