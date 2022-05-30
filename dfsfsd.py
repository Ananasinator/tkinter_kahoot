import tkinter as tk


class Kahoot(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (MainMenu, Game, Preferences):
            page_name = frame.__name__
            frame = frame(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        app_name = tk.Label(self, text="Kahoot")
        app_name.pack(side="top", fill="x", pady=10)

        start_btn = tk.Button(self, text="Start",
                              command=lambda: controller.show_frame("Game"))
        pref_btn = tk.Button(self, text="Preferences",
                             command=lambda: controller.show_frame("Preferences"))
        quit_btn = tk.Button(self, text="Quit", command=lambda: quit())
        start_btn.pack()
        pref_btn.pack()
        quit_btn.pack()

    def quit(self):
        self.destroy()
        exit()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="GAMEEE")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the main menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()


class Preferences(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PreferenceScreen")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the MainMenu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()


if __name__ == "__main__":
    app = Kahoot()
    app.geometry("800x800")
    app.mainloop()
