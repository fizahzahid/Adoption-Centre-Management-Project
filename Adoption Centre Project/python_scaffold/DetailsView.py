from tkinter import *
from python_scaffold.Utils import Utils, full_width_button

class DetailsView:
    def __init__(self, adoption_centre):
        self.adoption_centre = adoption_centre
        self.user = adoption_centre.logged_in_user

        self.root = Utils.top_level("My Details")
        self.is_open = True

        
        banner_frame = Utils.frame(self.root)
        banner_frame.pack(fill=X)
        Utils.image(banner_frame, "python_scaffold/image/cat_banner.jpg").pack(fill=X)

        
        name_frame = Utils.frame(self.root)
        name_frame.pack(fill=X, pady=10)
        name_label = Utils.label(name_frame, self.user.get_name())
        name_label.pack()

        Utils.separator(self.root).pack(fill=X)

        
        adopted_frame = Utils.frame(self.root)
        adopted_frame.pack(fill=X, pady=10)

       
        adopted_label = Label(adopted_frame, text="Adopted Animals:", font="Helvetica 12 bold", fg=Utils.purple)
        adopted_label.pack(pady=(0, 4))

        
        self.adopted_listbox = Listbox(
            adopted_frame,
            height=10,
            font="Helvetica 10",
            highlightthickness=0,
            borderwidth=0,
            justify=CENTER,
            width=50
        )
        self.adopted_listbox.pack(fill=BOTH, expand=True)

        self.populate_adopted_animals()

        
        button_frame = Utils.frame(self.root)
        button_frame.pack(fill=X, pady=10)
        close_button = full_width_button(button_frame, "Close", self.close)
        close_button.pack(fill=X)

        
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def populate_adopted_animals(self):
        self.adopted_listbox.delete(0, END)
        adopted_animals = self.user.get_adopted_animals().get_animals()
        for animal in adopted_animals:
            self.adopted_listbox.insert(END, f"{animal.get_name()} (Age: {animal.age})")

    def close(self):
        self.is_open = False
        self.root.destroy()


