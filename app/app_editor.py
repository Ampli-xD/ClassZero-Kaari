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

from app_editor_dbm import DatabaseManager
from app_editor_ol import LoadingOverlay
from app_editor_vp import VideoPlayer
from app_editor_sc import SlideCard
from app_editor_nsd import NewSlideDialog
from app_editor_pm import PresentationMode

from HostPortMapping import *

class EditorApp(ctk.CTkToplevel):

    def __init__(self, master, presentation_id):
        super().__init__(master)
        
        # Configure window
        self.configure(fg_color="#ebeaf2")  # Base color
        self.resizable(True, True)
        self.state('zoomed')
        ctk.set_appearance_mode("dark")
        self.title("ClassZero Kaari")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Database configuration
        self.db_config = {
            'host': host_server,
            'database': 'ClassZero',
            'user': 'admin',
            'password': 'admin@2911',
            'port': postgre_port
        }
        
        # Redis configuration
        self.redis_config = {
            'host': host_server,
            'port': redis_port,
            'decode_responses': True
        }
        
        self.db_manager = DatabaseManager(self.db_config)
        self.redis_client = redis.Redis(**self.redis_config)
        
        # Application state
        self.user_id = master.user_id
        self.presentation_id = presentation_id
        self.slides = []
        self.current_slide = None
        self.slide_cards = {}  # Map slide_id to SlideCard widgets
        self.monitoring_slides = {}  # Track slides being monitored
        
        self.setup_ui()
        self.initialize_presentation(presentation_id)
    
    def setup_ui(self):
        """Setup the main UI with modern styling"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left panel - Slides frame
        self.slides_frame = ctk.CTkFrame(self, width=300, fg_color="#1a191f", corner_radius=10)  # Secondary color
        self.slides_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=15)
        self.slides_frame.grid_propagate(False)
        
        # Setup slides panel
        self.setup_slides_panel()
        
        # Right panel - Slide editor frame
        self.editor_frame = ctk.CTkFrame(self, fg_color="#ebeaf2", corner_radius=10)  # Base color
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 15), pady=15)
        
        # Setup editor panel
        self.setup_editor_panel()
        
        # Bottom control panel
        self.control_frame = ctk.CTkFrame(self, height=120, fg_color="#1a191f", corner_radius=10)  # Secondary color
        self.control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))
        
        # Setup control panel
        self.setup_control_panel()
    
    def setup_slides_panel(self):
        """Setup the left slides panel with modern styling"""
        # Title
        slides_label = ctk.CTkLabel(
            self.slides_frame,
            text="Your Slides",
            font=ctk.CTkFont(size=20, weight="bold", family="Inter"),
            text_color="#ebeaf2"  # Base color for text
        )
        slides_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Add slide button
        add_btn = ctk.CTkButton(
            self.slides_frame,
            text="New Slide",
            command=self.add_slide,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=40
        )
        add_btn.pack(pady=10, padx=20, fill="x")
        
        # Scrollable frame for slides
        self.slides_scroll = ctk.CTkScrollableFrame(
            self.slides_frame,
            fg_color="#1a191f",  # Secondary color
            corner_radius=0
        )
        self.slides_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def setup_editor_panel(self):
        """Setup the right editor panel with modern styling"""
        # Configure grid for editor
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(0, weight=1)
        
        # Main content area
        content_frame = ctk.CTkFrame(self.editor_frame, fg_color="#ebeaf2", corner_radius=8)  # Base color
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Video player / main slide area
        self.video_player = VideoPlayer(content_frame)  # Secondary color
        self.video_player.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Slide details panel (right side)
        self.details_frame = ctk.CTkFrame(self.editor_frame, width=300, fg_color="#1a191f", corner_radius=10)  # Secondary color
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.details_frame.grid_propagate(False)
        
        # Setup details panel
        self.setup_details_panel()
    
    def setup_details_panel(self):
        """Setup the slide details panel with modern styling"""
        details_label = ctk.CTkLabel(
            self.details_frame,
            text="Slide Properties",
            font=ctk.CTkFont(size=18, weight="bold", family="Inter"),
            text_color="#ebeaf2"  # Base color for text
        )
        details_label.pack(pady=(20, 15), padx=20, anchor="w")
        
        # Slide type
        self.type_label = ctk.CTkLabel(
            self.details_frame,
            text="Type:",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            text_color="#ebeaf2"  # Base color for text
        )
        self.type_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.type_value = ctk.CTkLabel(
            self.details_frame,
            text="None",
            font=ctk.CTkFont(size=14, family="Inter"),
            text_color="#db2859"  # Accent color
        )
        self.type_value.pack(anchor="w", padx=30, pady=(0, 15))
        
        # Slide position
        self.position_label = ctk.CTkLabel(
            self.details_frame,
            text="Position:",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            text_color="#ebeaf2"  # Base color for text
        )
        self.position_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.position_value = ctk.CTkLabel(
            self.details_frame,
            text="None",
            font=ctk.CTkFont(size=14, family="Inter"),
            text_color="#db2859"  # Accent color
        )
        self.position_value.pack(anchor="w", padx=30, pady=(0, 15))
        
        # Slide JSON data
        self.json_label = ctk.CTkLabel(
            self.details_frame,
            text="JSON Data:",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            text_color="#ebeaf2"  # Base color for text
        )
        self.json_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.json_text = ctk.CTkTextbox(
            self.details_frame,
            height=250,
            fg_color="#ebeaf2",  # Base color
            text_color="#1a191f",  # Secondary color
            font=ctk.CTkFont(size=12, family="Inter"),
            corner_radius=8
        )
        self.json_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def setup_control_panel(self):
        """Setup the bottom control panel with modern styling"""
        # Configure grid
        self.control_frame.grid_columnconfigure(0, weight=1)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.control_frame, fg_color="#1a191f", corner_radius=0)  # Secondary color
        input_frame.pack(fill="x", padx=15, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Query input with send button
        query_frame = ctk.CTkFrame(input_frame, fg_color="#1a191f")  # Secondary color
        query_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        query_frame.grid_columnconfigure(0, weight=1)
        
        self.query_entry = ctk.CTkEntry(
            query_frame,
            placeholder_text="Enter your query...",
            font=ctk.CTkFont(size=14, family="Inter"),
            fg_color="#ebeaf2",  # Base color
            text_color="#1a191f",  # Secondary color
            corner_radius=8,
            height=40
        )
        self.query_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        
        send_btn = ctk.CTkButton(
            query_frame,
            text="Send",
            width=80,
            command=self.process_query,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=40
        )
        send_btn.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        # Control buttons
        buttons_frame = ctk.CTkFrame(input_frame, fg_color="#1a191f")  # Secondary color
        buttons_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        # First row of buttons
        btn_frame1 = ctk.CTkFrame(buttons_frame, fg_color="#1a191f")
        btn_frame1.pack(fill="x", padx=5, pady=2)
        
        render_slide_btn = ctk.CTkButton(
            btn_frame1,
            text="Render Slide",
            command=self.render_current_slide,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        render_slide_btn.pack(side="left", padx=5)
        
        download_pdf_btn = ctk.CTkButton(
            btn_frame1,
            text="Download PDF",
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        download_pdf_btn.pack(side="left", padx=5)
        
        img_btn = ctk.CTkButton(
            btn_frame1,
            text="Download Image",
            command=self.download_image,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        img_btn.pack(side="left", padx=5)
        
        video_btn = ctk.CTkButton(
            btn_frame1,
            text="Download Video",
            command=self.download_video,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        video_btn.pack(side="left", padx=5)
        
        # Second row of buttons
        btn_frame2 = ctk.CTkFrame(buttons_frame, fg_color="#1a191f")  # Secondary color
        btn_frame2.pack(fill="x", padx=5, pady=2)
        
        render_all_btn = ctk.CTkButton(
            btn_frame2,
            text="Render All Slides",
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        render_all_btn.pack(side="left", padx=5)
        
        present_btn = ctk.CTkButton(
            btn_frame2,
            text="Present",
            command=self.start_presentation,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        present_btn.pack(side="left", padx=5)
        
        load_video_btn = ctk.CTkButton(
            btn_frame2,
            text="Load Local Video",
            command=self.load_local_video,
            fg_color="#db2859",  # Accent color
            hover_color="#b52047",
            font=ctk.CTkFont(size=14, weight="bold", family="Inter"),
            corner_radius=8,
            height=36
        )
        load_video_btn.pack(side="left", padx=5)
    
    def initialize_presentation(self, presentation_id):
        """Initialize presentation with given ID"""
        self.presentation_id = presentation_id
        self.load_slides()
    
    def load_slides(self):
        """Load slides from database"""
        if not self.presentation_id:
            return
        
        self.slides = self.db_manager.fetch_slides(self.presentation_id)
        self.refresh_slides_panel()
    
    def refresh_slides_panel(self):
        """Refresh the slides panel with current slides"""
        # Clear existing slides
        for widget in self.slides_scroll.winfo_children():
            widget.destroy()
        self.slide_cards.clear()
        
        # Add slide cards
        for slide in self.slides:
            slide_card = SlideCard(self.slides_scroll, slide, self.select_slide)
            slide_card.pack(fill="x", pady=2)
            self.slide_cards[slide['slide_id']] = slide_card
    
    def select_slide(self, slide_data):
        """Select and display slide"""
        self.current_slide = slide_data
        self.update_details_panel()
        
        # Load video if available
        video_link = slide_data.get('render_video_link')
        if video_link:
            self.video_player.load_video_from_url(video_link)
    
    def update_details_panel(self):
        """Update the slide details panel"""
        if not self.current_slide:
            return
        
        self.type_value.configure(text=self.current_slide.get('slide_type', 'Unknown'))
        self.position_value.configure(text=str(self.current_slide.get('slide_pos', 0)))
        
        # Display JSON data
        slide_data = self.current_slide.get('slide_data', {})
        if isinstance(slide_data, str):
            json_str = slide_data
        else:
            json_str = json.dumps(slide_data, indent=2)
        
        self.json_text.delete("1.0", "end")
        self.json_text.insert("1.0", json_str)
    
    def add_slide(self):
        """Add a new slide"""
        # Fetch slide types from database
        slide_types = self.db_manager.fetch_slide_types()
        if not slide_types:
            slide_types = ["text", "image", "video", "chart"]  # Default types
        
        # Show dialog
        dialog = NewSlideDialog(self, slide_types, self.create_new_slide)
    
    def create_new_slide(self, slide_info):
        """Create a new slide with AI processing"""
        if not self.presentation_id:
            messagebox.showwarning("No Presentation", "Please initialize a presentation first.")
            return
        
        # Initial slide data
        slide_data = {
            "query": slide_info['query'],
            "status": "processing"
        }
        
        # Get next position
        next_position = len(self.slides) + 1
        
        # Create slide in database
        new_slide = self.db_manager.create_slide(
            self.presentation_id,
            slide_info['slide_type'],
            slide_data,
            next_position
        )
        
        if new_slide:
            # Add to slides list and refresh UI
            self.slides.append(new_slide)
            self.refresh_slides_panel()
            
            # Send Redis message for AI processing
            self.send_slide_request(new_slide, slide_info['query'])
            
            # Start monitoring this slide
            self.start_slide_monitoring(new_slide['slide_id'])
            
            messagebox.showinfo("Success", "Slide created! AI processing started...")
        else:
            messagebox.showerror("Error", "Failed to create slide.")
    
    def send_slide_request(self, slide, query):
        """Send slide processing request via Redis"""
        try:
            message = {
                "user_id": self.user_id,
                "presentation_id": str(self.presentation_id),
                "slide_id": str(slide['slide_id']),
                "type": slide['slide_type'],
                "query": query
            }
            
            self.redis_client.publish('kaari:request:in', json.dumps(message))
            print(f"Sent slide request: {message}")
            
        except Exception as e:
            messagebox.showerror("Redis Error", f"Failed to send slide request: {str(e)}")
    
    def send_render_request(self, slide):
        """Send slide render request via Redis"""
        try:
            # Get current slide data
            slide_data = slide.get('slide_data', {})
            if isinstance(slide_data, str):
                try:
                    slide_data = json.loads(slide_data)
                except:
                    slide_data = {}
            
            message = {
                "user_id": self.user_id,
                "presentation_id": str(self.presentation_id),
                "slide_id": str(slide['slide_id']),
                "type": slide['slide_type'],
                "data": slide_data
            }
            
            self.redis_client.publish('kaari:json:in', json.dumps(message))
            print(f"Sent render request: {message}")
            
        except Exception as e:
            messagebox.showerror("Redis Error", f"Failed to send render request: {str(e)}")
    
    def start_slide_monitoring(self, slide_id):
        """Start monitoring a slide for updates using after method"""
        if slide_id not in self.monitoring_slides:
            current_slide = self.db_manager.fetch_slide_by_id(slide_id)
            if current_slide:
                self.monitoring_slides[slide_id] = {
                    'last_data': current_slide.get('slide_data'),
                    'last_video_link': current_slide.get('render_video_link'),
                    'last_img_link': current_slide.get('render_img_link'),
                    'overlay': LoadingOverlay(self, "Processing Slide..."),
                    'is_monitoring': True
                }
                # Schedule the first check
                self.after(2000, self.check_slide_updates, slide_id)
    
    def check_slide_updates(self, slide_id):
        """Check for slide updates and schedule next check if necessary"""
        if slide_id not in self.monitoring_slides or not self.monitoring_slides[slide_id]['is_monitoring']:
            return
        
        slide = self.db_manager.fetch_slide_by_id(slide_id)
        if not slide:
            print(f"Could not fetch slide {slide_id}")
            # Schedule next check
            self.after(2000, self.check_slide_updates, slide_id)
            return
        
        monitor_data = self.monitoring_slides[slide_id]
        
        current_data = slide.get('slide_data')
        current_video = slide.get('render_video_link')
        current_img = slide.get('render_img_link')
        
        changes = []
        
        # Check data changes
        last_data = monitor_data['last_data']
        if current_data != last_data:
            if (last_data in [None, '{}', {}] and current_data not in [None, '{}', {}]):
                changes.append("Data processed")
            elif (current_data not in [None, '{}', {}] and last_data not in [None, '{}', {}]):
                changes.append("Data updated")
            monitor_data['last_data'] = current_data
        
        # Check video link changes
        if current_video != monitor_data['last_video_link'] and current_video is not None:
            changes.append("Video rendered")
            monitor_data['last_video_link'] = current_video
        
        # Check image link changes
        if current_img != monitor_data['last_img_link'] and current_img is not None:
            changes.append("Image rendered")
            monitor_data['last_img_link'] = current_img
        
        if changes:
            self.update_slide_progress(slide_id, slide, changes)
        
        # Check if processing is complete
        if (current_data not in [None, '{}', {}] and 
            current_video is not None and 
            current_img is not None):
            self.complete_slide_processing(slide_id, slide)
        else:
            # Schedule next check
            self.after(2000, self.check_slide_updates, slide_id)
    
    def update_slide_progress(self, slide_id, slide, changes):
        """Update slide progress in UI"""
        try:
            monitor_data = self.monitoring_slides.get(slide_id)
            if monitor_data and monitor_data['overlay']:
                status = "Processing..."
                details = " | ".join(changes)
                monitor_data['overlay'].update_status(status, details)
            
            # Update slide card
            if slide_id in self.slide_cards:
                self.slide_cards[slide_id].update_slide_data(slide)
            
            # Update slides list
            for i, s in enumerate(self.slides):
                if s['slide_id'] == slide_id:
                    self.slides[i] = slide
                    break
            
            # Update current slide if it's the one being monitored
            if self.current_slide and self.current_slide['slide_id'] == slide_id:
                self.current_slide = slide
                self.update_details_panel()
                
        except Exception as e:
            print(f"Error updating slide progress: {e}")
    
    def complete_slide_processing(self, slide_id, slide):
        """Complete slide processing"""
        try:
            monitor_data = self.monitoring_slides.get(slide_id)
            if monitor_data:
                # Stop monitoring
                monitor_data['is_monitoring'] = False
                if monitor_data['overlay']:
                    try:
                        monitor_data['overlay'].close_overlay()
                    except Exception as e:
                        print(f"Error closing overlay: {e}")
                # Clean up monitoring data
                del self.monitoring_slides[slide_id]
            
            # Update slide card
            if slide_id in self.slide_cards:
                self.slide_cards[slide_id].update_slide_data(slide)
            
            # Update slides list
            for i, s in enumerate(self.slides):
                if s['slide_id'] == slide_id:
                    self.slides[i] = slide
                    break
            
            # Update current slide if it's the one being processed
            if self.current_slide and self.current_slide['slide_id'] == slide_id:
                self.current_slide = slide
                self.update_details_panel()
                
                # Auto-load video if available
                video_link = slide.get('render_video_link')
                if video_link:
                    try:
                        self.video_player.load_video_from_url(video_link)
                    except Exception as e:
                        print(f"Error loading video: {e}")
            
            messagebox.showinfo("Success", "Slide processing completed!")
            
        except Exception as e:
            print(f"Error completing slide processing: {e}")
    
    def render_current_slide(self):
        """Render the current slide"""
        if not self.current_slide:
            messagebox.showwarning("No Slide Selected", "Please select a slide to render.")
            return
        
        slide_id = self.current_slide['slide_id']
        
        # If already monitoring, stop previous monitoring
        if slide_id in self.monitoring_slides:
            self.monitoring_slides[slide_id]['is_monitoring'] = False
            if self.monitoring_slides[slide_id]['overlay']:
                try:
                    self.monitoring_slides[slide_id]['overlay'].close_overlay()
                except:
                    pass
        
        # Reset render links
        self.db_manager.reset_render_links(slide_id)
        
        # Send render request
        self.send_render_request(self.current_slide)
        
        # Start fresh monitoring
        self.start_slide_monitoring(slide_id)
    
    def process_query(self):
        """Process query from input field"""
        query = self.query_entry.get().strip()
        if not query:
            return
        
        if not self.current_slide:
            messagebox.showwarning("No Slide Selected", "Please select a slide to update.")
            return
        
        slide_id = self.current_slide['slide_id']
        
        # If already monitoring, stop previous monitoring
        if slide_id in self.monitoring_slides:
            self.monitoring_slides[slide_id]['is_monitoring'] = False
            if self.monitoring_slides[slide_id]['overlay']:
                try:
                    self.monitoring_slides[slide_id]['overlay'].close_overlay()
                except:
                    pass
        
        # Reset render links
        self.db_manager.reset_render_links(slide_id)
        
        # Update current slide with new query
        current_data = self.current_slide.get('slide_data', {})
        if isinstance(current_data, str):
            try:
                current_data = json.loads(current_data)
            except:
                current_data = {}
        
        current_data['query'] = query
        current_data['status'] = 'processing'
        
        # Update slide in database
        if self.db_manager.update_slide(slide_id, current_data):
            # Send Redis message for processing
            self.send_slide_request(self.current_slide, query)
            
            # Start monitoring with fresh baseline
            self.start_slide_monitoring(slide_id)
            
            self.query_entry.delete(0, "end")
            messagebox.showinfo("Query Processing", "Query sent for AI processing...")
        else:
            messagebox.showerror("Error", "Failed to update slide.")
    
    def download_file(self, url, filename):
        """Download file from URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Get file extension from URL or content type
            parsed_url = urlparse(url)
            if not os.path.splitext(filename)[1]:
                content_type = response.headers.get('content-type', '')
                if 'video' in content_type:
                    filename += '.mp4'
                elif 'image' in content_type:
                    filename += '.png'
            
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=os.path.splitext(filename)[1],
                initialname=filename,
                filetypes=[("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                messagebox.showinfo("Success", f"File downloaded successfully to:\n{file_path}")
                return True
            
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to download file: {str(e)}")
            return False
    
    def download_video(self):
        """Download video for current slide"""
        if not self.current_slide:
            messagebox.showwarning("No Slide Selected", "Please select a slide first.")
            return
        
        video_link = self.current_slide.get('render_video_link')
        if not video_link:
            messagebox.showwarning("No Video", "No video available for this slide.")
            return
        
        filename = f"slide_{self.current_slide['slide_id']}_video"
        self.download_file(video_link, filename)
    
    def download_image(self):
        """Download image for current slide"""
        if not self.current_slide:
            messagebox.showwarning("No Slide Selected", "Please select a slide first.")
            return
        
        img_link = self.current_slide.get('render_img_link')
        if not img_link:
            messagebox.showwarning("No Image", "No image available for this slide.")
            return
        
        filename = f"slide_{self.current_slide['slide_id']}_image"
        self.download_file(img_link, filename)
    
    def load_local_video(self):
        """Load video file from local system"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv")]
        )
        
        if file_path:
            self.video_player.load_video(file_path)
    def start_presentation(self):
        """Start presentation mode"""
        if not self.slides:
            messagebox.showwarning("No Slides", "Please create some slides first.")
            return
        
        # Filter slides that have rendered images
        ready_slides = [slide for slide in self.slides if slide.get('render_video_link')]
        
        if not ready_slides:
            messagebox.showwarning("No Ready Slides", "Please render some slides first.")
            return
        
        # Sort slides by position
        ready_slides.sort(key=lambda x: x.get('slide_pos', 0))
        
        # Open presentation mode
        PresentationMode(self, ready_slides)

    def on_close(self):
        self.destroy()         # Destroys the EditorApp window
