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


class NewSlideDialog(ctk.CTkToplevel):

    def __init__(self, parent, slide_types, on_create_callback):
        super().__init__(parent)
        
        self.slide_types = slide_types
        self.on_create_callback = on_create_callback
        self.result = None
        
        # Configure window
        self.title("Create New Slide")
        self.transient(parent)
        self.grab_set()
        
        # Center the window
        self.geometry("600x450+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Set appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")  # Using blue as base, will override with custom colors
        
        self.configure(fg_color="#ebeaf2")  # Base color
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="#ebeaf2", corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Create a New Slide", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#1a191f"  # Secondary color
        )
        title_label.pack(pady=(0, 25))
        
        # Slide type selection
        type_label = ctk.CTkLabel(
            main_frame, 
            text="Slide Type", 
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="#1a191f"
        )
        type_label.pack(anchor="w", pady=(0, 8))
        
        self.type_var = ctk.StringVar(value=self.slide_types[0] if self.slide_types else "")
        self.type_dropdown = ctk.CTkComboBox(
            main_frame, 
            variable=self.type_var, 
            values=self.slide_types,
            fg_color="#ffffff",
            text_color="#1a191f",
            button_color="#db2859",  # Accent color
            button_hover_color="#b82048",
            dropdown_fg_color="#ffffff",
            dropdown_text_color="#1a191f",
            dropdown_hover_color="#f0e6eb",
            font=ctk.CTkFont(family="Helvetica", size=14),
            corner_radius=8
        )
        self.type_dropdown.pack(fill="x", pady=(0, 20))
        
        # Query input
        query_label = ctk.CTkLabel(
            main_frame, 
            text="AI Query", 
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="#1a191f"
        )
        query_label.pack(anchor="w", pady=(0, 8))
        
        self.query_text = ctk.CTkTextbox(
            main_frame, 
            height=160,
            fg_color="#ffffff",
            text_color="#1a191f",
            border_color="#db2859",  # Accent color
            border_width=2,
            corner_radius=8,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        self.query_text.pack(fill="both", expand=True, pady=(0, 25))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="#ebeaf2")
        button_frame.pack(fill="x")
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=self.cancel,
            fg_color="#1a191f",  # Secondary color
            hover_color="#2e2d35",
            text_color="#ebeaf2",
            font=ctk.CTkFont(family="Helvetica", size=14),
            corner_radius=8
        )
        cancel_btn.pack(side="right", padx=(15, 0))
        
        create_btn = ctk.CTkButton(
            button_frame, 
            text="Create Slide", 
            command=self.create_slide,
            fg_color="#db2859",  # Accent color
            hover_color="#b82048",
            text_color="#ebeaf2",
            font=ctk.CTkFont(family="Helvetica", size=14),
            corner_radius=8
        )
        create_btn.pack(side="right")
    
    def create_slide(self):
        """Create the slide with user input"""
        slide_type = self.type_var.get()
        query = self.query_text.get("1.0", "end-1c").strip()
        
        if not slide_type or not query:
            messagebox.showwarning("Invalid Input", "Please select a slide type and enter a query.")
            return
        
        self.result = {
            'slide_type': slide_type,
            'query': query
        }
        
        if self.on_create_callback:
            self.on_create_callback(self.result)
        
        self.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.destroy()