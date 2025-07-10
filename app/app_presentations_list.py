import customtkinter as ctk
import psycopg2
import datetime
import random
import string
from app_editor import EditorApp

from HostPortMapping import *

class Card(ctk.CTkFrame):
    def __init__(self, master, presentation_id):
        super().__init__(
            master,
            corner_radius=12,
            fg_color="#ebeaf2",  # Base color
            border_width=2,
            border_color="#db2859",  # Accent color
            cursor="hand2",
            height=180
        )
        self.presentation_id = presentation_id
        # fetch presentation details from database
        try:
            conn = psycopg2.connect(
                dbname="ClassZero",
                user="admin",
                password="admin@2911",
                host=host_server,
                port=postgre_port
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT presentation_name, creation_date "
                "FROM presentations WHERE presentation_id = %s",
                (presentation_id,)
            )
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                pres_name, creation_date = row
            else:
                pres_name, creation_date = ("Unknown", None)
        except Exception:
            pres_name, creation_date = ("Error loading", None)

        # create widgets with icons and modern styling
        # Title with icon
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Presentation icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="📊",
            font=ctk.CTkFont(family="Inter", size=18),
            width=30,
            text_color="#1a191f"  # Secondary color
        )
        icon_label.grid(row=0, column=0, sticky="w", padx=(0, 8))
        
        self.presentation_name = ctk.CTkLabel(
            title_frame,
            text=pres_name,
            font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
            text_color="#1a191f",  # Secondary color
            anchor="w"
        )
        self.presentation_name.grid(row=0, column=1, sticky="ew")
        
        # Info section with icons
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Slides count with icon
        slides_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        slides_frame.grid(row=0, column=0, sticky="w")
        
        slides_icon = ctk.CTkLabel(
            slides_frame,
            text="📑",
            font=ctk.CTkFont(family="Inter", size=14),
            width=20,
            text_color="#1a191f"  # Secondary color
        )
        slides_icon.grid(row=0, column=0, sticky="w")
        
        # self.slide_count_label = ctk.CTkLabel(
        #     slides_frame,
        #     font=ctk.CTkFont(family="Inter", size=14, weight="normal"),
        #     text_color="#1a191f"  # Secondary color
        # )
        # self.slide_count_label.grid(row=0, column=1, sticky="w", padx=(5, 0))
        
        # Date with icon
        date_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        date_frame.grid(row=0, column=1, sticky="e")
        
        date_icon = ctk.CTkLabel(
            date_frame,
            text="📅",
            font=ctk.CTkFont(family="Inter", size=14),
            width=20,
            text_color="#1a191f"  # Secondary color
        )
        date_icon.grid(row=0, column=1, sticky="e")
        
        # Fix potential None error with creation_date
        if creation_date:
            date_str = creation_date.strftime("%m/%d/%y")
        else:
            date_str = "N/A"
            
        self.creation_date_label = ctk.CTkLabel(
            date_frame,
            text=date_str,
            font=ctk.CTkFont(family="Inter", size=14, weight="normal"),
            text_color="#1a191f"  # Secondary color
        )
        self.creation_date_label.grid(row=0, column=1, sticky="e", padx=(5, 0))
        
        # Subtle divider line
        divider = ctk.CTkFrame(self, height=1, fg_color="#db2859")  # Accent color
        divider.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 0))
        
        # Status indicator
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=(8, 15))
        
        status_dot = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#db2859",  # Accent color
            width=20
        )
        status_dot.grid(row=0, column=0, sticky="w")
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to present",
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#1a191f"  # Secondary color
        )
        status_label.grid(row=0, column=1, sticky="w", padx=(5, 0))

        # layout with better spacing
        self.grid_columnconfigure(0, weight=1)

        # bind click events after widgets are created
        self._bind_click_events()
        
        # hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _bind_click_events(self):
        """Bind click events to the frame and all its children recursively"""
        def _on_click(event):
            toplevel = self.winfo_toplevel()
            if hasattr(toplevel, '_open_presentation'):
                toplevel._open_presentation(self)

        # bind to frame
        self.bind("<Button-1>", _on_click)
        
        # recursively bind to all children and their children
        def bind_recursive(widget):
            widget.bind("<Button-1>", _on_click)
            for child in widget.winfo_children():
                bind_recursive(child)
        
        bind_recursive(self)
    
    def _on_enter(self, event):
        """Mouse enter hover effect with smooth transition"""
        self.configure(
            fg_color="#ffffff", 
            border_color="#b21f47"  # Darker accent for hover
        )
    
    def _on_leave(self, event):
        """Mouse leave hover effect"""
        self.configure(
            fg_color="#ebeaf2",  # Base color
            border_color="#db2859"  # Accent color
        )

class PresentationsListApp(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#ebeaf2")  # Base color

        # --- Validate session token ---
        try:
            conn = psycopg2.connect(
                dbname="ClassZero",
                user="admin",
                password="admin@2911",
                host=host_server,
                port=postgre_port
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT token FROM users WHERE user_id = %s",
                (master.user_id,)
            )
            row = cur.fetchone()
            cur.close()
            conn.close()
            if not row or row[0] != master.token:
                # Invalidate UI and ask for re-login
                for child in self.winfo_children():
                    child.destroy()
                ctk.CTkLabel(
                    self,
                    text="Session invalid.\nPlease close and login again.",
                    font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
                    text_color="#db2859"  # Accent color
                ).pack(expand=True, pady=50)
                return
        except Exception:
            for child in self.winfo_children():
                child.destroy()
            ctk.CTkLabel(
                self,
                text="Error validating session.\nPlease close and login again.",
                font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
                text_color="#db2859"  # Accent color
            ).pack(expand=True, pady=50)
            return

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("ClassZero Kaari")
        self.state('zoomed')
        self.resizable(True, True)
        self.token = master.token
        self.user_id = master.user_id

        # --- Header with logo ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(
            header_frame,
            text="Your Presentations",
            font=ctk.CTkFont(family="Inter", size=28, weight="bold"),
            text_color="#1a191f"  # Secondary color
        ).pack(side="left")

        # --- Scrollable card container ---
        container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            width=1000,
            height=700
            
        )
        container._scrollbar.configure(
            fg_color="#db2859",
            button_hover_color="#1a191f"
        )
        container.pack(expand=True, fill="both", padx=30, pady=20)

        self._build_cards(container, getattr(master, "presentations", []))

    def _build_cards(self, parent, *_args, columns=3):
        # 1) fetch all presentation_ids for this user
        try:
            conn = psycopg2.connect(
                dbname="ClassZero",
                user="admin",
                password="admin@2911",
                host=host_server,
                port=postgre_port
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT presentation_id FROM presentations WHERE user_id = %s",
                (self.master.user_id,)
            )
            pres_ids = [r[0] for r in cur.fetchall()]
            cur.close()
            conn.close()
        except Exception:
            pres_ids = []
        
        # 2) build one Card per presentation_id, then a "+ New" card
        padx = pady = 20
        for idx, pres_id in enumerate(pres_ids+[None]):
            row, col = divmod(idx, columns)
            if pres_id is not None:
                # real presentation card
                card = Card(parent, pres_id)
            else:
                # "+ New" as a big plus button with modern styling
                card = ctk.CTkButton(
                    parent,
                    text="+ New",
                    font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
                    corner_radius=12,
                    fg_color="#ebeaf2",  # Base color
                    border_width=2,
                    border_color="#db2859",  # Accent color
                    text_color="#1a191f",  # Secondary color
                    hover_color="#ffffff",  # White for hover
                    cursor="hand2",
                    height=180,
                    command=self._create_new_presentation
                )

            card.grid(row=row, column=col, padx=padx, pady=pady)
            card.grid_propagate(False)

    def _open_presentation(self, pres):
        self.withdraw()
        editor = EditorApp(self, pres.presentation_id)
        while editor.winfo_exists():
            self.update()
            self.after(100) 
        self.destroy()

    def _create_new_presentation(self):
        """Create a new presentation with user input dialog"""
        # Create overlay dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create New Presentation")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#ebeaf2")  # Base color
        
        # Center the dialog on parent window
        dialog.transient(self)
        dialog.grab_set()
        
        # Position dialog in center of parent
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")
        
        # Dialog content
        title_label = ctk.CTkLabel(
            dialog,
            text="Create New Presentation",
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="#1a191f"  # Secondary color
        )
        title_label.pack(pady=(30, 10))
        
        # Input field
        name_label = ctk.CTkLabel(
            dialog,
            text="Presentation Name:",
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#1a191f"  # Secondary color
        )
        name_label.pack(pady=(10, 5))
        
        name_entry = ctk.CTkEntry(
            dialog,
            width=300,
            height=40,
            font=ctk.CTkFont(family="Inter", size=14),
            fg_color="#ffffff",
            border_color="#db2859",  # Accent color
            text_color="#1a191f"  # Secondary color
        )
        name_entry.pack(pady=(0, 20))
        name_entry.focus()
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        def create_presentation():
            """Create the presentation and open editor"""
            pres_name = name_entry.get().strip()
            if not pres_name:
                # Show error if name is empty
                error_label = ctk.CTkLabel(
                    dialog,
                    text="Please enter a presentation name!",
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#db2859"  # Accent color for error
                )
                error_label.pack(pady=(0, 10))
                return
            
            try:
                # Connect to database
                conn = psycopg2.connect(
                    dbname="ClassZero",
                    user="admin",
                    password="admin@2911",
                    host=host_server,
                    port=postgre_port
                )
                cur = conn.cursor()
                
                # Generate unique presentation ID
                code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                
                # Insert new presentation
                cur.execute(
                    """INSERT INTO presentations 
                    (presentation_id, user_id, presentation_name) 
                    VALUES (%s, %s, %s)""",
                    (code, self.user_id, pres_name)
                )
                
                conn.commit()
                cur.close()
                conn.close()
                
                # Close dialog
                dialog.destroy()
                
                # Open the new presentation in editor
                self.withdraw()
                editor = EditorApp(self, code)
                
            except Exception as e:
                # Show error message
                error_label = ctk.CTkLabel(
                    dialog,
                    text=f"Error creating presentation: {str(e)}",
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#db2859"  # Accent color for error
                )
                error_label.pack(pady=(0, 10))
                print(f"Database error: {e}")
        
        def cancel_creation():
            """Cancel and close dialog"""
            dialog.destroy()
        
        # Bind Enter key to create presentation
        dialog.bind('<Return>', lambda event: create_presentation())
        
        # Create button
        create_btn = ctk.CTkButton(
            button_frame,
            text="Create",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            fg_color="#db2859",  # Accent color
            hover_color="#b21f47",  # Darker accent for hover
            text_color="#ffffff",
            width=100,
            height=35,
            command=create_presentation
        )
        create_btn.pack(side="left", padx=(0, 10))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(family="Inter", size=14),
            fg_color="#ffffff",
            hover_color="#f0f0f0",
            text_color="#1a191f",  # Secondary color
            border_width=2,
            border_color="#db2859",  # Accent color
            width=100,
            height=35,
            command=cancel_creation
        )
        cancel_btn.pack(side="left")