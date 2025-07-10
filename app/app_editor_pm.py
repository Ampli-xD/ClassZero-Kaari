import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from app_editor_vp import VideoPlayer
import time

class PresentationMode(ctk.CTkToplevel):
    def __init__(self, parent, slides):
        super().__init__(parent)
        
        self.slides = slides
        self.current_slide_index = 0
        self.parent = parent

        
        # Configure window
        self.configure(fg_color="#000000")  # Black background
        self.title("Presentation Mode")
        self.state('zoomed')  # Maximized
        self.resizable(True, True)
        
        # Remove window decorations for full-screen feel
        self.attributes('-topmost', True)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="#000000",
            corner_radius=0
        )
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Video player frame
        self.video_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#000000",
            corner_radius=0
        )
        self.video_frame.grid(row=0, column=0, sticky="nsew")
        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_rowconfigure(0, weight=1)
        
        # Initialize video player
        self.video_player = VideoPlayer(self.video_frame)
        self.video_player.grid(row=0, column=0, sticky="nsew")
        
        # Bind keyboard events
        self.bind("<KeyPress>", self.on_key_press)
        self.focus_set()  # Ensure window has focus for key events
                
        # Load first slide
        self.load_current_slide()
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_key_press(self, event):
        """Handle keyboard navigation"""
        if event.keysym == "Right":
            self.next_slide()
        elif event.keysym == "Left":
            self.previous_slide()
        elif event.keysym == "Escape":
            self.on_closing()
    
    def next_slide(self):
        """Navigate to next slide"""
        if self.current_slide_index < len(self.slides) - 1:
            self.current_slide_index += 1
            self.load_current_slide()
    
    def previous_slide(self):
        """Navigate to previous slide"""
        if self.current_slide_index > 0:
            self.current_slide_index -= 1
            self.load_current_slide()
    
    def load_current_slide(self):
        """Load and display current slide as video"""
        if not self.slides or self.current_slide_index >= len(self.slides):
            return
        
        current_slide = self.slides[self.current_slide_index]
        
        # Try to load slide video
        video_link = current_slide.get('render_video_link') or current_slide.get('video_link')
        
        if video_link:
            try:
                self.load_slide_video(video_link)
            except Exception as e:
                print(f"Error loading slide video: {e}")
                self.show_slide_fallback(current_slide)
        else:
            self.show_slide_fallback(current_slide)
    
    def load_slide_video(self, video_url):
        """Load slide video from URL"""
        try:
            # Load video in the video player
            self.video_player.load_video_from_url(video_url)
            
            # Auto-play the video
            if not self.video_player.playing:
                self.video_player.toggle_play_pause()
            
        except Exception as e:
            print(f"Error loading slide video: {e}")
            self.show_slide_fallback(self.slides[self.current_slide_index])
    
    def show_slide_fallback(self, slide):
        """Show fallback slide content when video is not available"""
        slide_type = slide.get('slide_type', 'Unknown')
        slide_pos = slide.get('slide_pos', 0)
        
        # Stop the video player
        self.video_player.stop_playback()
        
        # Show fallback in video label
        fallback_text = f"Slide {slide_pos + 1}\n\nType: {slide_type}\n\nVideo not available"
        
        self.video_player.video_label.configure(
            text=fallback_text,
            image=None,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        self.video_player.video_label.image = None
    
    def on_closing(self):
        """Handle window closing"""
        self.video_player.stop_playback()
        self.destroy()