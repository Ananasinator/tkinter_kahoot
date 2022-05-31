import tkinter as tk
import winsound
import requests

index, counter = int(), int()
r = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean')
data = r.json()
for i in range(len(data['results'])):
    if "&quot;" in str(data['results'][i]['question']):
        data['results'][i]['question'] = str(data['results'][i]['question']).replace("&quot;", "")


# question_text = ''


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
        for frame in (MainMenu, Game, Preferences, TheEnd):
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
    q_var =
    def display_question(self, number):
        global data
        current_question = data['results'][number]['question']
        return current_question

    def start_game_btn(self):
        global index
        self.display_question(index, )

    def btn_onclick_handler(self, val):
        global index, counter
        if index <= 8:
            if val == bool(data['results'][index]['correct_answer']):
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                counter += 1
                print(counter)
            else:
                winsound.MessageBeep(winsound.MB_ICONHAND)
                print(counter)
            index += 1
            self.display_question(index)
        else:
            print(counter, "The End")
            self.controller.show_frame("TheEnd")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        mainmenu_btn = tk.Button(self, text="Go to the main menu",
                                 command=lambda: controller.show_frame("MainMenu"))
        mainmenu_btn.pack(anchor="n")

        start_btn = tk.Button(self, text="Start",
                              command=lambda: [self.start_game_btn(), start_btn.pack_forget()])
        start_btn.pack(anchor="n")

        q_var = tk.Variable()
        question_label = tk.Label(self, textvariable=self.display_question(index))
        question_label.pack(side="top", fill="x", pady=10)

        truefalse_frame = tk.Frame(self)
        true_btn = tk.Button(truefalse_frame, text="True",
                             command=lambda val=True: self.btn_onclick_handler(val))
        true_btn.pack(side="left")
        false_btn = tk.Button(truefalse_frame, text="False",
                              command=lambda val=False: self.btn_onclick_handler(val))
        false_btn.pack()
        truefalse_frame.pack()


class TheEnd(tk.Frame):
    def __init__(self, parent, controller):
        global counter
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text=f"You scored {counter} points!")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the Main Menu",
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
