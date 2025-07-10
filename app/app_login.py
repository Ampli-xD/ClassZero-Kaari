import customtkinter as ctk
import tkinter as tk
import psycopg2
import hashlib
import datetime
import random
import secrets
from HostPortMapping import *

class LoginApp(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.conn = psycopg2.connect(
            dbname="ClassZero",
            user="admin",
            password="admin@2911",
            host = host_server,
            port= postgre_port
        )

        # Fixed size
        self.resizable(False, False)
        width, height = 500, 400
        self.geometry(f"{width}x{height}")
        self.title("ClassZero Authentication")

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.stage = 1
        self.setup_ui()

    def setup_ui(self):
        """Initialize and configure all UI elements with modern styling"""
        # Configure window background
        self.configure(fg_color="#ebeaf2")  # Base color

        # Welcome label (replacing title)
        self.title_label = ctk.CTkLabel(
            self, 
            text="Welcome back!", 
            font=ctk.CTkFont(family="Inter", size=30, weight="bold"),
            text_color="#1a191f"  # Secondary color
        )
        self.title_label.pack(pady=(50, 20))

        # Prompt label
        self.prompt = ctk.CTkLabel(
            self, 
            text="Enter your UserId:", 
            font=ctk.CTkFont(family="Inter", size=18),
            text_color="#1a191f"  # Secondary color
        )
        self.prompt.pack(pady=(40, 5))

        # Entry field with modern styling
        self.entry = ctk.CTkEntry(
            self, 
            width=350, 
            height=40,
            corner_radius=10,
            fg_color="#ffffff",
            text_color="#1a191f",  # Secondary color
            border_color="#db2859",  # Accent color
            border_width=2,
            font=ctk.CTkFont(family="Inter", size=18),
            show=""
        )
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda event: self.on_button_click())

        # Error label
        self.error_label = ctk.CTkLabel(
            self, 
            text="", 
            text_color="#db2859",  # Accent color for visibility
            font=ctk.CTkFont(family="Inter", size=14)
        )
        self.error_label.pack(pady=(5, 10))

        # Loading label
        self.loading_label = ctk.CTkLabel(
            self, 
            text="Loading...", 
            font=ctk.CTkFont(family="Inter", size=16),
            text_color="#1a191f"  # Secondary color
        )

        # Button with modern styling
        self.button = ctk.CTkButton(
            self, 
            text="Hop In", 
            command=self.on_button_click, 
            font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
            fg_color="#db2859",  # Accent color
            hover_color="#b21f47",  # Darker accent for hover
            text_color="#ebeaf2",  # Base color for text
            corner_radius=10,
            height=40
        )
        self.button.pack(pady=(0, 30))

    def on_button_click(self):
        """Handle button click events"""
        self.error_label.configure(text="")
        
        text = self.entry.get().strip()
        if not text:
            self.error_label.configure(text="Please enter a value.")
            return

        self.button.configure(state="disabled")
        self.loading_label.pack(pady=(10, 0))
        
        if self.stage == 1:
            self.verify_user(text)
        else:
            self.verify_password(text)

    def verify_user(self, user_id):
        """Verify user ID and prepare for password stage"""
        self.loading_label.pack_forget()

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT passwrod_hash, title, last_name FROM users WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
            cur.close()

            if row is None:
                self.error_label.configure(text="Invalid UserId")
                self.button.configure(state="normal")
                return

            self.stored_hash, title, last_name = row
            self.user_id = user_id
            
            greeting = self.create_personalized_greeting(title, last_name)
            self.title_label.configure(text=greeting)
            
            self.transition_to_password_stage()
            
        except psycopg2.Error as e:
            self.error_label.configure(text="Database error occurred")
            self.button.configure(state="normal")
            print(f"Database error: {e}")

    def create_personalized_greeting(self, title, last_name):
        """Create a personalized greeting based on time and randomness"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greet_word = "Good Morning"
        elif hour < 17:
            greet_word = "Good Afternoon"
        else:
            greet_word = "Good Evening"

        quirky_greetings = ["Ahoy", "Salutations", "Greetings", "Bonjour"]
        if random.random() < 0.2:
            greet_word = random.choice(quirky_greetings)

        return f"{greet_word} {title} {last_name.capitalize()}"

    def transition_to_password_stage(self):
        """Transition UI from user ID stage to password stage"""
        self.stage = 2
        self.prompt.configure(text="Password:")
        self.entry.delete(0, tk.END)
        self.entry.configure(show="*")
        self.entry.focus()  # Focus on entry field
        self.button.configure(text="Login", state="normal")

    def verify_password(self, password):
        """Verify password and complete login"""
        self.loading_label.pack_forget()

        try:
            hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
            
            if hashed != self.stored_hash:
                self.error_label.configure(text="Invalid Password")
                self.button.configure(state="normal")
                return

            self.login_successful()
            
        except Exception as e:
            self.error_label.configure(text="Authentication error occurred")
            self.button.configure(state="normal")
            print(f"Authentication error: {e}")

    def login_successful(self):
        """Handle successful login"""
        self.prompt.pack_forget()
        self.entry.pack_forget()
        self.button.pack_forget()      

        self.error_label.configure(text="Login successful!", text_color="green")
        cur = self.conn.cursor()
        new_token = secrets.token_hex(32)
        cur.execute(
            "UPDATE users SET token = %s WHERE user_id = %s",
            (new_token, self.user_id)
        )
        self.conn.commit()
        self.master.token = new_token
        self.master.user_id = self.user_id
        cur.close()
        self.destroy()

    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()