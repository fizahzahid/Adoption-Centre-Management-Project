

from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

#You will never have to manually call this
class ObservableButton(Button):
    def __init__(self, root, text, callback, main_color, hover_color):
        Button.__init__(self, root, text=text, command=callback, background=main_color, padx=0, relief=FLAT,
                   font="Arial 11 bold", foreground="white")
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_exit)
        self.main_color = main_color
        self.hover_color = hover_color

    def on_hover(self, event):
        self["background"] = self.hover_color

    def on_exit(self, event):
        self["background"] = self.main_color

class Utils:
    purple = "#be8fff"
    width = 550
    image_height = 250

    @staticmethod
    def disable():
        pass

    @staticmethod
    def root():
        window = Tk()
        window.resizable(False, False)
        window.title("Login")
        return window


    #Some operating systems struggle to automatically stretch the window
    #If needed, pass in a manual height and uncomment line 46
    @staticmethod
    def top_level(title_, height=0):
        tl = Toplevel()
        tl.resizable(False, False)
        tl.title(title_)
        # tl.geometry(f"{Utils.width}x{height}")
        return tl

    @staticmethod
    def button(root, text_, callback=None):
        return ObservableButton(root, text_, callback, Utils.purple, "#aa82ff")

    @staticmethod
    def filter_button(root, text_, callback=None):
        return ObservableButton(root, text_, callback, "#444444", "#333333")

    @staticmethod
    def frame(root):
        return Frame(root, width=Utils.width)

    @staticmethod
    def separator(root):
        return ttk.Separator(root, orient='horizontal')

    @staticmethod
    def label(root, text_):
        return Label(root, text=text_, font="Helvetica 12 bold", foreground=Utils.purple)

    @staticmethod
    def image(root, path):
        image_ = ImageTk.PhotoImage(Image.open(path).resize((Utils.width, Utils.image_height)))
        lbl = Label(root, image=image_)
        lbl.photo = image_
        return lbl

    @staticmethod
    def treeview(root, columns, multi=False):
        tree = ttk.Treeview(root, show="headings", height=12, columns=columns, selectmode="extended" if multi else "browse")
        for column in tree["columns"]:
            tree.column(column, anchor=CENTER, width=int(Utils.width/len(columns)), stretch=NO)
        for i in range(len(columns)):
            tree.heading(i, text=columns[i])
        tree.bind("<Motion>", 'break')
        return tree
    
    @staticmethod
    def colored_button_frame(root):
        """Creates a frame with purple background for buttons"""
        return Frame(root, width=Utils.width, bg=Utils.purple)
        
    @staticmethod
    def full_width_button(frame, text_, callback=None):
        """Creates a button that fills its container frame"""
        btn = Button(frame, text=text_, command=callback, 
                    bg=Utils.purple, fg="white", font="Arial 11 bold",
                    relief=FLAT, padx=10, pady=5)
        return btn
    

    @staticmethod
    def focused_entry(root):
        entry = Entry(root, highlightthickness=1, relief=FLAT)
        entry.config(highlightbackground="SystemButtonFace", highlightcolor="#4287f5")
        return entry
    

from tkinter import Button
from tkinter import ttk

class FullWidthButton(Button):
    def __init__(self, root, text, callback=None, bg=None, disabled_bg=None):
        super().__init__(root, text=text, command=callback, font="Arial 11 bold", relief="flat", padx=10, pady=5)
        self.default_bg = bg if bg else Utils.purple
        self.disabled_bg = disabled_bg if disabled_bg else "#e2d6f7"
        self.configure(bg=self.default_bg, fg="white", activeforeground="white", activebackground=self.default_bg)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self._hover = False

    def _on_hover(self, event):
        if self['state'] != 'disabled':
            self.configure(bg="#aa82ff")

    def _on_leave(self, event):
        if self['state'] != 'disabled':
            self.configure(bg=self.default_bg)

    def set_disabled(self, disabled=True):
        if disabled:
            self.configure(state="disabled", bg=self.disabled_bg, fg="white", disabledforeground="white")
        else:
            self.configure(state="normal", bg=self.default_bg, fg="white")

def full_width_button(root, text, callback=None):
    btn = FullWidthButton(root, text, callback)
    return btn

def styled_treeview(root, columns, multi=False):
    tree = ttk.Treeview(root, show="headings", height=12, columns=columns, selectmode="extended" if multi else "browse")
    style = ttk.Style(root)
    style.theme_use('default')
    style.configure("Custom.Treeview.Heading",
                    font=("Helvetica", 11, "bold"),
                    foreground=Utils.purple,
                    background="#f2f2f2",   
                    anchor="center")
    style.configure("Custom.Treeview",
                    font=("Helvetica", 11),
                    rowheight=25,
                    fieldbackground="white",
                    background="white")
    tree.configure(style="Custom.Treeview")
    for column in columns:
        tree.column(column, anchor="center", width=int(Utils.width/len(columns)), stretch=False)
        tree.heading(column, text=column, anchor="center", command=lambda: None)
    return tree
