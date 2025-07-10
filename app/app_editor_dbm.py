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


class DatabaseManager:

    def __init__(self, connection_params):
        self.connection_params = connection_params
        
    def get_connection(self):
        """Create and return a database connection"""
        try:
            return psycopg2.connect(**self.connection_params)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None
    
    def fetch_slides(self, presentation_id):
        """Fetch all slides for a given presentation"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT slide_id, slide_pos, slide_type, slide_data, render_img_link, render_video_link 
                    FROM slides 
                    WHERE presentation_id = %s 
                    ORDER BY slide_pos
                """, (presentation_id,))
                return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch slides: {str(e)}")
            return []
        finally:
            conn.close()
    
    def fetch_slide_by_id(self, slide_id):
        """Fetch a specific slide by ID"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT slide_id, slide_pos, slide_type, slide_data, render_img_link, render_video_link 
                    FROM slides 
                    WHERE slide_id = %s
                """, (slide_id,))
                return cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch slide: {str(e)}")
            return None
        finally:
            conn.close()
    
    def fetch_slide_types(self):
        """Fetch all slide types from kaari_prompt_set table"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT DISTINCT type FROM kaari_prompt_set ORDER BY type")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch slide types: {str(e)}")
            return []
        finally:
            conn.close()
    
    def create_slide(self, presentation_id, slide_type, slide_data, slide_pos):
        """Create a new slide in the database"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO slides (presentation_id, slide_type, slide_data, slide_pos)
                    VALUES (%s, %s, %s, %s)
                    RETURNING slide_id, slide_pos, slide_type, slide_data, render_img_link, render_video_link
                """, (presentation_id, slide_type, json.dumps(slide_data), slide_pos))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to create slide: {str(e)}")
            return None
        finally:
            conn.close()
    
    def update_slide(self, slide_id, slide_data):
        """Update slide data"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE slides SET slide_data = %s WHERE slide_id = %s
                """, (json.dumps(slide_data), slide_id))
                conn.commit()
                return True
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update slide: {str(e)}")
            return False
        finally:
            conn.close()
    
    def reset_render_links(self, slide_id):
        """Reset render image and video links to null for a slide"""
        conn = self.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE slides SET render_img_link = NULL, render_video_link = NULL WHERE slide_id = %s
                """, (slide_id,))
                conn.commit()
                return True
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to reset render links: {str(e)}")
            return False
        finally:
            conn.close()
 