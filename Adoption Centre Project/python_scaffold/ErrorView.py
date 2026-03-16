from tkinter import *
from python_scaffold.Utils import Utils, full_width_button

class ErrorView:
    def __init__(self, error_type, error_message):
        self.root = Utils.top_level("Error")
        self.root.configure(bg="#e6e6e6")

        
        banner_frame = Utils.frame(self.root)
        banner_frame.pack(fill=X)
        Utils.image(banner_frame, "python_scaffold/image/error_banner.jpg").pack(fill=X)

        
        error_type_frame = Frame(self.root, width=Utils.width, bg="#e6e6e6")
        error_type_frame.pack(fill=X, pady=(10, 0))
        error_label = Label(
            error_type_frame,
            text=error_type,
            fg="#ff0000",
            bg="#e6e6e6",
            font=("Arial", 12, "bold")
        )
        error_label.pack()

        
        Utils.separator(self.root).pack(fill=X, pady=(8, 0))

        
        error_message_frame = Frame(self.root, width=Utils.width, bg="#e6e6e6")
        error_message_frame.pack(fill=X, pady=(12, 0))
        message_label = Label(
            error_message_frame,
            text=error_message,
            fg=Utils.purple,
            bg="#e6e6e6",
            font=("Arial", 11, "bold")
        )
        message_label.pack()

        
        Frame(self.root, bg="#e6e6e6").pack(fill=BOTH, expand=True)

        
        button_frame = Frame(self.root, width=Utils.width, bg="#be8fff")
        button_frame.pack(fill=X, side=BOTTOM)
        close_button = Button(
            button_frame,
            text="Close",
            command=self.close,
            bg="#be8fff",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=FLAT,
            padx=10,
            pady=8,
            borderwidth=0,
            activebackground="#be8fff",
            activeforeground="white"
        )
        close_button.pack(fill=X, expand=True)

        
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.grab_set()
        self.root.wait_window()

    def close(self):
        self.root.destroy()
