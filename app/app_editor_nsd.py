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
        
        # Modern color scheme
        self.colors = {
            'bg_primary': "#0f0f0f",      # Deep black
            'bg_secondary': "#1a1a1a",    # Dark gray
            'bg_tertiary': "#2d2d2d",     # Medium gray
            'accent': "#3b82f6",          # Modern blue
            'accent_hover': "#2563eb",    # Darker blue
            'text_primary': "#ffffff",    # Pure white
            'text_secondary': "#a1a1aa",  # Light gray
            'success': "#10b981",         # Green
            'error': "#ef4444",           # Red
            'input_bg': "#1f1f1f",        # Input background
            'border': "#404040"           # Border color
        }
        
        # Configure window
        self.title("✨ Create New Slide")
        self.transient(parent)
        self.grab_set()
        
        # Center the window with better size
        self.geometry("650x500+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Modern appearance
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.colors['bg_primary'])
        
        # Add subtle shadow effect
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI with modern styling"""
        # Main container with padding
        main_container = ctk.CTkFrame(
            self, 
            fg_color=self.colors['bg_primary'], 
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Content frame with border and shadow effect
        content_frame = ctk.CTkFrame(
            main_container, 
            fg_color=self.colors['bg_secondary'], 
            corner_radius=16,
            border_width=1,
            border_color=self.colors['border']
        )
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header section
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 0))
        
        # Title with icon
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎨 Create New Slide", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(anchor="w")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="Design your next presentation slide with AI assistance", 
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Form section
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Slide type selection with modern card styling
        type_card = ctk.CTkFrame(
            form_frame, 
            fg_color=self.colors['bg_tertiary'], 
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        type_card.pack(fill="x", pady=(0, 20))
        
        type_header = ctk.CTkFrame(type_card, fg_color="transparent")
        type_header.pack(fill="x", padx=20, pady=(20, 10))
        
        type_label = ctk.CTkLabel(
            type_header, 
            text="📄 Slide Type", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.colors['text_primary']
        )
        type_label.pack(side="left")
        
        type_hint = ctk.CTkLabel(
            type_header, 
            text="Choose the type of content", 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors['text_secondary']
        )
        type_hint.pack(side="right")
        
        # Enhanced dropdown with better styling
        self.type_var = ctk.StringVar(value=self.slide_types[0] if self.slide_types else "")
        self.type_dropdown = ctk.CTkComboBox(
            type_card, 
            variable=self.type_var, 
            values=self.slide_types,
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            button_color=self.colors['accent'],
            button_hover_color=self.colors['accent_hover'],
            dropdown_fg_color=self.colors['bg_tertiary'],
            dropdown_text_color=self.colors['text_primary'],
            dropdown_hover_color=self.colors['accent'],
            border_color=self.colors['border'],
            border_width=1,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            corner_radius=8,
            height=40
        )
        self.type_dropdown.pack(fill="x", padx=20, pady=(0, 20))
        
        # Query input with modern card styling
        query_card = ctk.CTkFrame(
            form_frame, 
            fg_color=self.colors['bg_tertiary'], 
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        query_card.pack(fill="both", expand=True, pady=(0, 20))
        
        query_header = ctk.CTkFrame(query_card, fg_color="transparent")
        query_header.pack(fill="x", padx=20, pady=(20, 10))
        
        query_label = ctk.CTkLabel(
            query_header, 
            text="💭 AI Query", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.colors['text_primary']
        )
        query_label.pack(side="left")
        
        query_hint = ctk.CTkLabel(
            query_header, 
            text="Describe what you want to create", 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors['text_secondary']
        )
        query_hint.pack(side="right")
        
        # Enhanced textbox with placeholder effect
        self.query_text = ctk.CTkTextbox(
            query_card, 
            height=180,
            fg_color=self.colors['input_bg'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['border'],
            border_width=1,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            scrollbar_button_color=self.colors['bg_tertiary'],
            scrollbar_button_hover_color=self.colors['accent']
        )
        self.query_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Add placeholder text
        placeholder_text = """💡 Examples:
    • "Create a slide about renewable energy with charts and statistics"
    • "Design an introduction slide for a marketing presentation"
    • "Make a comparison slide between two products"
    • "Generate a timeline slide for project milestones"

    Be specific about what content, style, and visual elements you want!"""
        
        self.query_text.insert("1.0", placeholder_text)
        self.query_text.bind("<FocusIn>", self.on_query_focus_in)
        self.query_text.bind("<FocusOut>", self.on_query_focus_out)
        self.query_text.bind("<KeyPress>", self.on_query_key_press)
        
        # Action buttons with modern styling
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        # Cancel button with subtle styling
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="✕ Cancel", 
            command=self.cancel,
            fg_color="transparent",
            hover_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            corner_radius=8,
            height=45,
            width=120
        )
        cancel_btn.pack(side="right", padx=(15, 0))
        
        # Create button with emphasis
        create_btn = ctk.CTkButton(
            button_frame, 
            text="✨ Create Slide", 
            command=self.create_slide,
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            text_color=self.colors['text_primary'],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            corner_radius=8,
            height=45,
            width=140
        )
        create_btn.pack(side="right")
        
        # Add keyboard shortcuts
        self.bind('<Return>', lambda e: self.create_slide())
        self.bind('<Control-Return>', lambda e: self.create_slide())
        self.bind('<Escape>', lambda e: self.cancel())
        
        # Focus on query text
        self.after(100, lambda: self.query_text.focus_set())

    def on_query_focus_in(self, event):
        """Handle focus in event for query textbox"""
        current_text = self.query_text.get("1.0", "end-1c")
        if current_text.startswith("💡 Examples:"):
            self.query_text.delete("1.0", "end")
            self.query_text.configure(text_color=self.colors['text_primary'])

    def on_query_focus_out(self, event):
        """Handle focus out event for query textbox"""
        current_text = self.query_text.get("1.0", "end-1c").strip()
        if not current_text:
            placeholder_text = """💡 Examples:
    • "Create a slide about renewable energy with charts and statistics"
    • "Design an introduction slide for a marketing presentation"
    • "Make a comparison slide between two products"
    • "Generate a timeline slide for project milestones"

    Be specific about what content, style, and visual elements you want!"""
            self.query_text.insert("1.0", placeholder_text)
            self.query_text.configure(text_color=self.colors['text_secondary'])

    def on_query_key_press(self, event):
        """Handle key press in query textbox"""
        current_text = self.query_text.get("1.0", "end-1c")
        if current_text.startswith("💡 Examples:"):
            self.query_text.delete("1.0", "end")
            self.query_text.configure(text_color=self.colors['text_primary'])

    def create_slide(self):
        """Create the slide with user input"""
        slide_type = self.type_var.get()
        query = self.query_text.get("1.0", "end-1c").strip()
        
        # Check if query is still placeholder text
        if query.startswith("💡 Examples:"):
            query = ""
        
        if not slide_type or not query:
            # Show modern error dialog
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("⚠️ Validation Error")
            error_dialog.geometry("400x200")
            error_dialog.configure(fg_color=self.colors['bg_secondary'])
            error_dialog.transient(self)
            error_dialog.grab_set()
            
            # Center error dialog
            error_dialog.geometry("+%d+%d" % (
                self.winfo_rootx() + 125, 
                self.winfo_rooty() + 150
            ))
            
            error_frame = ctk.CTkFrame(error_dialog, fg_color="transparent")
            error_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                error_frame,
                text="⚠️ Missing Information",
                font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                text_color=self.colors['error']
            ).pack(pady=(0, 10))
            
            ctk.CTkLabel(
                error_frame,
                text="Please select a slide type and enter a detailed query\nto help AI create your perfect slide.",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=self.colors['text_secondary'],
                justify="center"
            ).pack(pady=(0, 20))
            
            ctk.CTkButton(
                error_frame,
                text="Got it!",
                command=error_dialog.destroy,
                fg_color=self.colors['accent'],
                hover_color=self.colors['accent_hover'],
                font=ctk.CTkFont(family="Segoe UI", size=14),
                corner_radius=8,
                height=35
            ).pack()
            
            return
        
        self.result = {
            'slide_type': slide_type,
            'query': query
        }
        
        if self.on_create_callback:
            self.on_create_callback(self.result)
        
        self.destroy()

    def cancel(self):
        """Cancel dialog with confirmation if there's content"""
        query = self.query_text.get("1.0", "end-1c").strip()
        
        # Check if user has entered content
        if query and not query.startswith("💡 Examples:"):
            # Show confirmation dialog
            confirm_dialog = ctk.CTkToplevel(self)
            confirm_dialog.title("🤔 Confirm Cancel")
            confirm_dialog.geometry("350x150")
            confirm_dialog.configure(fg_color=self.colors['bg_secondary'])
            confirm_dialog.transient(self)
            confirm_dialog.grab_set()
            
            # Center confirm dialog
            confirm_dialog.geometry("+%d+%d" % (
                self.winfo_rootx() + 150, 
                self.winfo_rooty() + 175
            ))
            
            confirm_frame = ctk.CTkFrame(confirm_dialog, fg_color="transparent")
            confirm_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                confirm_frame,
                text="Are you sure you want to cancel?\nYour query will be lost.",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=self.colors['text_primary'],
                justify="center"
            ).pack(pady=(0, 20))
            
            btn_frame = ctk.CTkFrame(confirm_frame, fg_color="transparent")
            btn_frame.pack()
            
            ctk.CTkButton(
                btn_frame,
                text="Keep Editing",
                command=confirm_dialog.destroy,
                fg_color=self.colors['accent'],
                hover_color=self.colors['accent_hover'],
                font=ctk.CTkFont(family="Segoe UI", size=12),
                corner_radius=6,
                height=32,
                width=100
            ).pack(side="left", padx=(0, 10))
            
            ctk.CTkButton(
                btn_frame,
                text="Cancel",
                command=lambda: [confirm_dialog.destroy(), self.destroy()],
                fg_color=self.colors['error'],
                hover_color="#dc2626",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                corner_radius=6,
                height=32,
                width=100
            ).pack(side="left")
            
        else:
            self.destroy()