from tkinter import *
from python_scaffold.Utils import Utils
from python_scaffold.ErrorView import ErrorView
from python_scaffold.CustomerDashboardView import CustomerDashboardView
from python_scaffold.ManagerDashboardView import ManagerDashboardView
from python_scaffold.model.exception.UnauthorizedAccessException import UnauthorizedAccessException
from python_scaffold.model.exception.InvalidOperationException import InvalidOperationException

#colours for my buttons and select thing
DISABLED_PURPLE = "#e8d9ff"  
FOCUS_BLUE = "#4287f5"       
DISABLED_BG = "#e0e0e0"      
DISABLED_FG = "#888888"      

class LoginView:
    def __init__(self, adoption_centre):
        self.adoption_centre = adoption_centre
        self.root = Utils.root()
        
        
        logo_frame = Utils.frame(self.root)
        logo_frame.pack(fill=X)
        Utils.image(logo_frame, "python_scaffold/image/cat_banner.jpg").pack(fill=X)

        
        Utils.separator(self.root).pack(fill=X, pady=5)
        
        
        login_label_frame = Utils.frame(self.root)
        login_label_frame.pack(fill=X, pady=10)
        Utils.label(login_label_frame, "Login").pack()
        
        
        Utils.separator(self.root).pack(fill=X, pady=5)
        
        
        form_frame = Utils.frame(self.root)
        form_frame.pack(fill=BOTH, expand=True, pady=(10, 10))
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=0)
        form_frame.grid_columnconfigure(2, weight=1)
        
        entry_width = 25
        
        
        username_label = Label(form_frame, text="Username:", fg=Utils.purple, anchor=E)
        username_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky=E)
        self.username_entry = Entry(form_frame, width=entry_width, relief=FLAT, highlightthickness=2)
        self.username_entry.grid(row=0, column=1, pady=10, sticky=W)
        self.username_entry.bind("<KeyRelease>", self.on_entry_change)
        self.username_entry.bind("<FocusIn>", lambda e: self.set_entry_focus(self.username_entry, True))
        self.username_entry.bind("<FocusOut>", lambda e: self.set_entry_focus(self.username_entry, False))
        
        
        email_label = Label(form_frame, text="Email:", fg=Utils.purple, anchor=E)
        email_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky=E)
        self.email_entry = Entry(form_frame, width=entry_width, relief=FLAT, highlightthickness=2)
        self.email_entry.grid(row=1, column=1, pady=10, sticky=W)
        self.email_entry.bind("<KeyRelease>", self.on_entry_change)
        self.email_entry.bind("<FocusIn>", lambda e: self.set_entry_focus(self.email_entry, True))
        self.email_entry.bind("<FocusOut>", lambda e: self.set_entry_focus(self.email_entry, False))

        Utils.separator(self.root).pack(fill=X)

        # Manager ID field
        manager_label = Label(form_frame, text="Manager ID:", fg=Utils.purple, anchor=E)
        manager_label.grid(row=3, column=0, padx=(0, 10), pady=10, sticky=E)
        self.manager_id_entry = Entry(form_frame, width=entry_width, relief=FLAT, highlightthickness=2)
        self.manager_id_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.manager_id_entry.bind("<KeyRelease>", self.on_entry_change)
        self.manager_id_entry.bind("<FocusIn>", lambda e: self.set_entry_focus(self.manager_id_entry, True))
        self.manager_id_entry.bind("<FocusOut>", lambda e: self.set_entry_focus(self.manager_id_entry, False))
        
        # Buttons
        button_frame = Frame(self.root, width=Utils.width, bg="#be8fff")
        button_frame.pack(fill=X, side=BOTTOM)
        self.login_button = Button(button_frame, text="Login", command=self.login, 
                                  bg=Utils.purple, fg="white", font="Arial 11 bold",
                                  relief=FLAT, width=25, padx=10, pady=5, activebackground=Utils.purple)
        self.login_button.pack(side=LEFT, fill=X, expand=True)
        self.set_button_disabled(self.login_button)
        
        exit_button = Button(button_frame, text="Exit", command=self.exit_application,
                            bg=Utils.purple, fg="white", font="Arial 11 bold", 
                            relief=FLAT, width=25, padx=10, pady=5)
        exit_button.pack(side=RIGHT, fill=X, expand=True)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Set this window as the master window for the application
        self.root.mainloop()

    def set_entry_focus(self, entry, focused):
        if focused:
            entry.config(highlightbackground=FOCUS_BLUE, highlightcolor=FOCUS_BLUE)
        else:
            entry.config(highlightbackground="lightgrey", highlightcolor="lightgrey")

    def set_button_disabled(self, button):
        button.config(state=DISABLED, bg=DISABLED_PURPLE, fg="white", activebackground=DISABLED_PURPLE, disabledforeground="white")
        
    def set_button_enabled(self, button):
        button.config(state=NORMAL, bg=Utils.purple, fg="white", activebackground=Utils.purple)

    def set_entry_state(self, entry, state):
        """Set entry state and background for visual feedback."""
        if state == NORMAL:
            entry.config(state=NORMAL, disabledbackground="white", disabledforeground="black", bg="white", fg="black")
        else:
            entry.config(state=DISABLED, disabledbackground=DISABLED_BG, disabledforeground=DISABLED_FG, bg=DISABLED_BG, fg=DISABLED_FG)

    def on_entry_change(self, event=None):
        customer_fields_filled = bool(self.username_entry.get()) and bool(self.email_entry.get())
        manager_field_filled = bool(self.manager_id_entry.get())
        # If manager ID has content, disable customer fields
        if manager_field_filled:
            self.set_entry_state(self.username_entry, DISABLED)
            self.set_entry_state(self.email_entry, DISABLED)
            self.set_entry_state(self.manager_id_entry, NORMAL)
            self.set_button_enabled(self.login_button)
        # If either username or email has content, disable manager field
        elif self.username_entry.get() or self.email_entry.get():
            self.set_entry_state(self.username_entry, NORMAL)
            self.set_entry_state(self.email_entry, NORMAL)
            self.set_entry_state(self.manager_id_entry, DISABLED)
            if customer_fields_filled:
                self.set_button_enabled(self.login_button)
            else:
                self.set_button_disabled(self.login_button)
        # If nothing entered, enable all fields
        else:
            self.set_entry_state(self.username_entry, NORMAL)
            self.set_entry_state(self.email_entry, NORMAL)
            self.set_entry_state(self.manager_id_entry, NORMAL)
            self.set_button_disabled(self.login_button)
    
    def login(self):
        if self.manager_id_entry.get():
            try:
                try:
                    manager_id = int(self.manager_id_entry.get()) 
                except ValueError:
                    ErrorView("InvalidOperationException", "Id must be an integer")
                    return
                manager = self.adoption_centre.get_users().validate_manager(str(manager_id))
                if manager:
                    self.adoption_centre.logged_in_user = manager
                    # Important: Withdraw the current window before opening new one
                    self.root.withdraw()
                    dashboard = ManagerDashboardView(self.adoption_centre)
                    # After dashboard is closed, quit the application
                    self.root.quit()
            except UnauthorizedAccessException as e:
                ErrorView("UnauthorizedAccessException", str(e))
            except InvalidOperationException as e:
                ErrorView("InvalidOperationException", str(e))
        elif self.username_entry.get() and self.email_entry.get():
            try:
                user = self.adoption_centre.get_users().validate_customer(
                    self.username_entry.get(), self.email_entry.get())
                if user:
                    self.adoption_centre.logged_in_user = user
                    # Important: Withdraw the current window before opening new one
                    self.root.withdraw()
                    dashboard = CustomerDashboardView(self.adoption_centre)
                    # After dashboard is closed, quit the application
                    self.root.quit()
                else:
                    ErrorView("UnauthorizedAccessException", "Invalid customer credentials")
            except Exception as e:
                ErrorView("UnauthorizedAccessException", "Invalid customer credentials")
    
    def exit_application(self):
        self.root.quit()
        self.root.destroy()


