import customtkinter as ctk
from app_login import LoginApp
from app_presentations_list import PresentationsListApp

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.token = None
        self.user_id = None

        # hide the main window
        self.withdraw()
        # self.update()
        # instantiate the login window
        self.login_app = LoginApp(self)
        # keep the main loop running until the login window is closed
        while self.login_app.winfo_exists():
            self.update()
            self.after(100)
        if self.token is None:
            self.destroy()
            return
        self.presentations_list_app = PresentationsListApp(self)
        while self.presentations_list_app.winfo_exists():
            self.update()
            self.after(100)
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()