import tkinter as tk
import json

import requests


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

        def display_question(number):
            current_question = data['results'][number]['question']
            update_label(current_question)

        def update_label(txt):
            question_text.set(txt)

        def start_game_btn():
            display_question(0)

        def btn_onclick_handler(val):
            if val == bool(data['results'][index]['correct_answer']):
                return True
            return False

        def check():
            


        counter = int()
        index = 0

        self.controller = controller
        question_text = tk.StringVar()
        mainmenu_btn = tk.Button(self, text="Go to the main menu",
                                 command=lambda: controller.show_frame("MainMenu"))
        mainmenu_btn.pack(anchor="n")

        start_btn = tk.Button(self, text="Start",
                              command=lambda: [start_game_btn(), start_btn.pack_forget()])
        start_btn.pack(anchor="n")

        question_label = tk.Label(self, textvariable=question_text)
        question_label.pack(side="top", fill="x", pady=10)

        truefalse_frame = tk.Frame(self)
        true_btn = tk.Button(truefalse_frame, text="True",
                             command=lambda val=True: btn_onclick_handler())
        true_btn.pack(side="left")
        false_btn = tk.Button(truefalse_frame, text="False",
                              command=lambda val=False: btn_onclick_handler())
        false_btn.pack()
        truefalse_frame.pack()

        counter_label = tk.Label(self, text=counter)
        counter_label.pack(side="top")

        r = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean')
        data = r.json()


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
