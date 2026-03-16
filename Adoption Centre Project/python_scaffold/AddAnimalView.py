from tkinter import *
from tkinter import ttk
from python_scaffold.Utils import Utils, full_width_button
from python_scaffold.ErrorView import ErrorView
from python_scaffold.model.Animal import Cat, Dog, Rabbit

class AddAnimalView:
    def __init__(self, adoption_centre, refresh_callback):
        self.adoption_centre = adoption_centre
        self.refresh_callback = refresh_callback

        self.root = Utils.top_level("Add Animal")

       
        banner_frame = Utils.frame(self.root)
        banner_frame.pack(fill=X)
        Utils.image(banner_frame, "python_scaffold/image/cat_banner.jpg").pack(fill=X)

       
        Utils.separator(self.root).pack(fill=X)

       
        header_frame = Utils.frame(self.root)
        header_frame.pack(fill=X, pady=10)
        Utils.label(header_frame, "Add Animal").pack()
        Utils.separator(self.root).pack(fill=X)

        
        form_frame = Frame(self.root, width=320, height=120)
        form_frame.pack(anchor="center", pady=20)
        form_frame.pack_propagate(False)

        
        style = ttk.Style(self.root)
        style.theme_use('default')
        style.map('Custom.TCombobox',
          fieldbackground=[('readonly', 'white')],
          bordercolor=[('focus', '#4287f5'), ('!focus', '#cccccc')],
          lightcolor=[('focus', '#4287f5'), ('!focus', '#cccccc')],
          darkcolor=[('focus', '#4287f5'), ('!focus', '#cccccc')])
        style.configure('Custom.TCombobox',
                selectbackground='white',
                selectforeground='black',   
                foreground='black',         
                fieldbackground='white',
                borderwidth=2,
                relief='flat')


       
        type_label = Label(form_frame, text="Type:", fg=Utils.purple, font="Helvetica 11 bold")
        type_label.grid(row=0, column=0, sticky=E, padx=(0, 10), pady=6)
        self.animal_type = StringVar()
        self.animal_type.set("Cat")
        self.type_dropdown = ttk.Combobox(form_frame, textvariable=self.animal_type,
                                          values=["Cat", "Dog", "Rabbit"],
                                          width=8, state="readonly", style="Custom.TCombobox")
        self.type_dropdown.grid(row=0, column=1, sticky=W, pady=6)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.on_field_change)
        self.type_dropdown.bind("<FocusIn>", lambda e: style.configure('Custom.TCombobox', bordercolor='#4287f5', lightcolor='#4287f5', darkcolor='#4287f5'))
        self.type_dropdown.bind("<FocusOut>", lambda e: style.configure('Custom.TCombobox', bordercolor='#cccccc', lightcolor='#cccccc', darkcolor='#cccccc'))

        
        name_label = Label(form_frame, text="Name:", fg=Utils.purple, font="Helvetica 11 bold")
        name_label.grid(row=1, column=0, sticky=E, padx=(0, 10), pady=6)
        self.name_entry = Entry(form_frame, width=18, relief=FLAT, highlightthickness=2, highlightbackground="#cccccc", highlightcolor="#4287f5")
        self.name_entry.grid(row=1, column=1, sticky=W, pady=6)
        self.name_entry.bind("<KeyRelease>", self.on_field_change)
        self.name_entry.bind("<FocusIn>", lambda e: self.name_entry.config(highlightbackground="#4287f5"))
        self.name_entry.bind("<FocusOut>", lambda e: self.name_entry.config(highlightbackground="#cccccc"))

        
        age_label = Label(form_frame, text="Age:", fg=Utils.purple, font="Helvetica 11 bold")
        age_label.grid(row=2, column=0, sticky=E, padx=(0, 10), pady=6)
        self.age_entry = Entry(form_frame, width=18, relief=FLAT, highlightthickness=2, highlightbackground="#cccccc", highlightcolor="#4287f5")
        self.age_entry.grid(row=2, column=1, sticky=W, pady=6)
        self.age_entry.bind("<KeyRelease>", self.on_field_change)
        self.age_entry.bind("<FocusIn>", lambda e: self.age_entry.config(highlightbackground="#4287f5"))
        self.age_entry.bind("<FocusOut>", lambda e: self.age_entry.config(highlightbackground="#cccccc"))

        
        button_frame = Utils.frame(self.root)
        button_frame.pack(fill=X, pady=10)
        self.add_button = full_width_button(button_frame, "Add", self.add_animal)
        self.add_button.pack(side=LEFT, expand=True, fill=X)
        self.add_button.set_disabled(True)
        close_button = full_width_button(button_frame, "Close", self.close)
        close_button.pack(side=LEFT, expand=True, fill=X)

        
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.root.grab_set()  
        self.root.wait_window()

    def on_field_change(self, event=None):
        if self.animal_type.get() and self.name_entry.get() and self.age_entry.get():
            self.add_button.set_disabled(False)
        else:
            self.add_button.set_disabled(True)

    def add_animal(self):
        animal_type = self.animal_type.get()
        name = self.name_entry.get()
        age_str = self.age_entry.get()
        for animal in self.adoption_centre.animals.get_animals():
            if animal.get_name() == name:
                ErrorView("InvalidOperationException", f"{name} already exists in the adoption centre")
                return
        try:
            age = int(age_str)
        except ValueError:
            ErrorView("InvalidOperationException", f"Age must be an integer")
            return
        if animal_type == "Cat":
            new_animal = Cat(name, age)
        elif animal_type == "Dog":
            new_animal = Dog(name, age)
        elif animal_type == "Rabbit":
            new_animal = Rabbit(name, age)
        self.adoption_centre.animals.add(new_animal)
        self.refresh_callback()
        self.close()

    def close(self):
        self.root.destroy()
