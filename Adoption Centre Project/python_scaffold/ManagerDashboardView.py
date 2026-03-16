from tkinter import *
from tkinter import ttk
from python_scaffold.Utils import Utils, full_width_button, styled_treeview
from python_scaffold.UserListView import UserListView
from python_scaffold.AddAnimalView import AddAnimalView
from python_scaffold.ErrorView import ErrorView
from python_scaffold.model.exception.InvalidOperationException import InvalidOperationException
#fixed the imports

class ManagerDashboardView:
    def __init__(self, adoption_centre):
        self.adoption_centre = adoption_centre
        self.current_filter = "all"

        self.root = Utils.top_level("Manager Dashboard")

    
        banner_frame = Utils.frame(self.root)
        banner_frame.pack(fill=X)
        Utils.image(banner_frame, "python_scaffold/image/cat_banner.jpg").pack(fill=X)
        Utils.separator(self.root).pack(fill=X)

        
        dashboard_frame = Utils.frame(self.root)
        dashboard_frame.pack(fill=X, pady=(12, 0))
        Utils.label(dashboard_frame, "Manager Dashboard").pack()
        Utils.separator(self.root).pack(fill=X)
        Utils.frame(self.root).pack(fill=X, pady=(6, 0))

        
        filter_frame = Utils.frame(self.root)
        filter_frame.pack(fill=X)
        self.all_button = Utils.filter_button(filter_frame, "All", lambda: self.filter_animals("all"))
        self.all_button.pack(side=LEFT, expand=True, fill=X)
        self.cat_button = Utils.filter_button(filter_frame, "Cat", lambda: self.filter_animals("Cat"))
        self.cat_button.pack(side=LEFT, expand=True, fill=X)
        self.dog_button = Utils.filter_button(filter_frame, "Dog", lambda: self.filter_animals("Dog"))
        self.dog_button.pack(side=LEFT, expand=True, fill=X)
        self.rabbit_button = Utils.filter_button(filter_frame, "Rabbit", lambda: self.filter_animals("Rabbit"))
        self.rabbit_button.pack(side=LEFT, expand=True, fill=X)

        
        animal_frame = Utils.frame(self.root)
        animal_frame.pack(fill=BOTH, expand=True)
        columns = ["Name", "Type", "Age", "Adoption Status"]
        self.animal_tree = styled_treeview(animal_frame, columns)
        scrollbar = ttk.Scrollbar(animal_frame, orient=VERTICAL, command=self.animal_tree.yview)
        self.animal_tree.configure(yscrollcommand=scrollbar.set)
        self.animal_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.animal_tree.bind("<<TreeviewSelect>>", self.on_animal_selected)
        self.populate_animal_table()

        
        button_frame = Utils.frame(self.root)
        button_frame.pack(fill=X, pady=(8, 10))
        self.user_list_button = full_width_button(button_frame, "User List", self.open_user_list)
        self.user_list_button.pack(side=LEFT, expand=True, fill=X)
        self.add_button = full_width_button(button_frame, "Add", self.add_animal)
        self.add_button.pack(side=LEFT, expand=True, fill=X)
        self.remove_button = full_width_button(button_frame, "Remove", self.remove_animal)
        self.remove_button.pack(side=LEFT, expand=True, fill=X)
        self.remove_button.set_disabled(True)
        self.close_button = full_width_button(button_frame, "Close", self.close)
        self.close_button.pack(side=LEFT, expand=True, fill=X)

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def populate_animal_table(self):
        for item in self.animal_tree.get_children():
            self.animal_tree.delete(item)
        animals = self.adoption_centre.animals.get_animals_by_filter(self.current_filter)
        for animal in animals:
            animal_type = type(animal).__name__
            adoption_status = "Adopted" if animal.is_already_adopted() else "Available"
            self.animal_tree.insert("", END, values=[animal.get_name(), animal_type, animal.age, adoption_status])

    def on_animal_selected(self, event):
        if self.animal_tree.selection():
            self.remove_button.set_disabled(False)
        else:
            self.remove_button.set_disabled(True)

    def filter_animals(self, filter_type):
        self.current_filter = filter_type
        self.populate_animal_table()
        self.remove_button.set_disabled(True)

    def open_user_list(self):
        UserListView(self.adoption_centre)

    def add_animal(self):
        AddAnimalView(self.adoption_centre, self.populate_animal_table)

    def remove_animal(self):
        if not self.animal_tree.selection():
            return
        selected_item = self.animal_tree.selection()[0]
        values = self.animal_tree.item(selected_item, "values")
        animal_name = values[0]
        animal = self.adoption_centre.animals.animal(animal_name)
        if animal:
            if animal.is_already_adopted():
                ErrorView("InvalidOperationException", f"{animal_name} is already adopted")
            else:
                self.adoption_centre.animals.remove(animal)
                self.populate_animal_table()
                self.remove_button.set_disabled(True)

    def close(self):
        self.root.destroy()
        import sys
        sys.exit(0)
