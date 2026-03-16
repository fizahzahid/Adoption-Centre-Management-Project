from tkinter import *
from python_scaffold.Utils import Utils
from python_scaffold.DetailsView import DetailsView
from python_scaffold.ErrorView import ErrorView
from python_scaffold.model.exception.InvalidOperationException import InvalidOperationException

class CustomerDashboardView:
    def __init__(self, adoption_centre):
        self.adoption_centre = adoption_centre
        self.user = adoption_centre.logged_in_user

        
        self.PURPLE = Utils.purple
        self.LIGHT_PURPLE = "#e2d6f7"

        
        self.details_view = None

        
        self.root = Utils.top_level("Customer Dashboard")

        
        logo_frame = Utils.frame(self.root)
        logo_frame.pack(fill=X)
        Utils.image(logo_frame, "python_scaffold/image/cat_banner.jpg").pack(fill=X)

       
        Utils.separator(self.root).pack(fill=X)

        
        welcome_frame = Utils.frame(self.root)
        welcome_frame.pack(fill=X, pady=10)
        welcome_label = Label(welcome_frame, text=f"Welcome {self.user.get_first_name()}",
                              font="Helvetica 12", fg=Utils.purple)
        welcome_label.pack()

        
        Utils.separator(self.root).pack(fill=X)

        
        spacer = Frame(self.root, height=30)
        spacer.pack()

        
        Utils.separator(self.root).pack(fill=X)

       
        animals_label_frame = Utils.frame(self.root)
        animals_label_frame.pack(fill=X)
        animals_label = Label(animals_label_frame, text="Animals", font="Helvetica 12 bold")
        animals_label.pack()

        
        Utils.separator(self.root).pack(fill=X)

        
        listbox_frame = Utils.frame(self.root)
        listbox_frame.pack(fill=BOTH, expand=True)

       
        center_frame = Frame(listbox_frame)
        center_frame.pack(expand=True)

        
        self.animal_listbox = Listbox(center_frame, height=15,
                                      font="Helvetica 10",
                                      highlightthickness=0,  
                                      borderwidth=0,         
                                      justify=CENTER,        
                                      width=90)              
        self.animal_listbox.pack(fill=BOTH, expand=True)
        self.animal_listbox.bind("<<ListboxSelect>>", self.on_animal_selected)

        
        self.populate_animal_list()

        
        button_frame = Frame(self.root, bg=Utils.purple)
        button_frame.pack(fill=X, side=BOTTOM)

        
        my_details_button = Button(button_frame, text="My Details", command=self.open_details,
                                   bg=Utils.purple, fg="white", font="Arial 11 bold",
                                   relief=FLAT, padx=10, pady=5,
                                   activebackground=Utils.purple, activeforeground="white")
        my_details_button.pack(side=LEFT, fill=X, expand=True)

        
        self.adopt_button = Button(button_frame, text="Adopt", command=self.adopt_animal,
                                   bg=self.LIGHT_PURPLE, fg="white", font="Arial 11 bold",
                                   relief=FLAT, padx=10, pady=5, state=DISABLED,
                                   activebackground=Utils.purple, activeforeground="white",
                                   disabledforeground="white")
        self.adopt_button.pack(side=LEFT, fill=X, expand=True)

        
        close_button = Button(button_frame, text="Close", command=self.close,
                              bg=Utils.purple, fg="white", font="Arial 11 bold",
                              relief=FLAT, padx=10, pady=5,
                              activebackground=Utils.purple, activeforeground="white")
        close_button.pack(side=LEFT, fill=X, expand=True)

        
        self.root.update_idletasks()
        width = 550 
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def set_adopt_button_state(self, enabled):
        if enabled:
            self.adopt_button.config(state=NORMAL, bg=self.PURPLE, fg="white")
        else:
            self.adopt_button.config(state=DISABLED, bg=self.LIGHT_PURPLE, fg="white", disabledforeground="white")

    def populate_animal_list(self):
        self.animal_listbox.delete(0, END)
        self.adoptable_animals = self.adoption_centre.get_adoptable_animals()
        for animal in self.adoptable_animals:
            self.animal_listbox.insert(END, f"{animal.get_name()} (Age: {animal.age})")

    def on_animal_selected(self, event):
        if self.animal_listbox.curselection():
            self.set_adopt_button_state(True)
        else:
            self.set_adopt_button_state(False)

    def open_details(self):
        
        if self.details_view is None or not self.details_view.is_open:
            self.details_view = DetailsView(self.adoption_centre)
        else:
            
            self.details_view.root.lift()

    def adopt_animal(self):
        if not self.animal_listbox.curselection():
            return

        selected_index = self.animal_listbox.curselection()[0]
        animal = self.adoptable_animals[selected_index]

        try:
            if self.user.can_adopt(animal):
                animal.adopt()
                self.user.get_adopted_animals().add(animal)
                self.populate_animal_list()
                self.set_adopt_button_state(False)
                
                if self.details_view is not None and self.details_view.is_open:
                    self.details_view.populate_adopted_animals()
            else:
                animal_type = type(animal).__name__
                ErrorView("InvalidOperationException", f"Cannot adopt {animal.get_name()}, adoption limit for {animal_type} reached")
        except Exception as e:
            ErrorView("Error", str(e))

    def close(self):
        self.root.destroy()




