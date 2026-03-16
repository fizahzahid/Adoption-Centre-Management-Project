from tkinter import *
from python_scaffold.Utils import Utils, full_width_button

class UserListView:
    def __init__(self, adoption_centre):
        self.adoption_centre = adoption_centre

        self.root = Utils.top_level("User List")
        self.root.resizable(False, False)

        # Set window size to match Utils.width and a reasonable height
        window_width = Utils.width
        window_height = 700  # or any height that looks good
        x = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Banner image
        banner_frame = Utils.frame(self.root)
        banner_frame.pack(fill=X)
        Utils.image(banner_frame, "python_scaffold/image/cat_banner.jpg").pack(fill=X)

        # Separator after banner
        Utils.separator(self.root).pack(fill=X)

        # Header
        header_frame = Utils.frame(self.root)
        header_frame.pack(fill=X, pady=10)
        Utils.label(header_frame, "User List").pack()

        Utils.separator(self.root).pack(fill=X)

        # User list section
        users_frame = Utils.frame(self.root)
        users_frame.pack(fill=BOTH, expand=True, pady=10)

        # Column heading for users
        users_heading = Label(users_frame, text="Users", font=("Helvetica", 11, "bold"), fg=Utils.purple)
        users_heading.pack(pady=(0, 4))

        # Centered Listbox for users
        self.users_listbox = Listbox(
            users_frame,
            height=15,
            width=0,  # Let it expand
            font=("Helvetica", 12),
            justify="center",  # Center text
            activestyle="none",
            borderwidth=0,
            highlightthickness=0,
            selectbackground="#e2d6f7",
            selectforeground="black"
        )
        self.users_listbox.pack(fill=BOTH, expand=True, padx=30)

        # Populate user list
        self.populate_user_list()

        # Full-width Close button
        button_frame = Utils.frame(self.root)
        button_frame.pack(fill=X, pady=10)
        close_button = full_width_button(button_frame, "Close", self.close)
        close_button.pack(fill=X)

        self.root.grab_set()  # Make this window modal
        self.root.wait_window()

    def populate_user_list(self):
        self.users_listbox.delete(0, END)
        users = self.adoption_centre.get_users().get_users()
        for user in users:
            self.users_listbox.insert(END, str(user))

    def close(self):
        self.root.destroy()


