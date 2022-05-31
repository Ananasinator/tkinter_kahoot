import tkinter as tk
import winsound
import requests

index, counter = 0, 0
r = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean')
data = r.json()
for i in range(len(data['results'])):
    if "&quot;" in str(data['results'][i]['question']):
        data['results'][i]['question'] = str(data['results'][i]['question']).replace("&quot;", "")
question_label = tk.Label(tk.Tk().withdraw())
counter_label = tk.Label(tk.Tk().withdraw())


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
        quit_btn = tk.Button(self, text="Quit", command=lambda: exit())
        start_btn.pack()
        pref_btn.pack()
        quit_btn.pack()


class Game(tk.Frame):
    cc = 1000

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        mainmenu_btn = tk.Button(self, text="Go to the main menu",
                                 command=lambda: controller.show_frame("MainMenu"))
        mainmenu_btn.pack(anchor="n")

        start_btn = tk.Button(self, text="Start",
                              command=lambda: [self.updateQuestion(), start_btn.pack_forget()])
        start_btn.pack(anchor="n")
        global question_label
        question_label = tk.Label(self, textvariable=self.updateQuestion())
        question_label.pack(side="top", fill="x", pady=10)

        truefalse_frame = tk.Frame(self)
        true_btn = tk.Button(truefalse_frame, text="True",
                             command=lambda val=True: self.onClickHandler(val))
        true_btn.pack(side="left")
        false_btn = tk.Button(truefalse_frame, text="False",
                              command=lambda val=False: self.onClickHandler(val))
        false_btn.pack()
        truefalse_frame.pack()

        global counter_label
        counter_label = tk.Label(self, textvariable=self.updateCounter())
        counter_label.pack()

    def updateQuestion(self):
        global index, question_label
        question_label['text'] = str(data['results'][index]['question'])

    def updateCounter(self):
        global counter, counter_label
        counter_label['text'] = int(counter)

    def onClickHandler(self, val):
        global index, data, counter
        try:
            if val == bool(data['results'][index]['correct_answer']):
                counter += 1
                self.updateCounter()
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

            else:
                winsound.MessageBeep(winsound.MB_ICONHAND)
            index += 1
            self.updateQuestion()
        except IndexError:
            question_label['text'] = str(f"You scored {counter} points!")


class Preferences(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PreferenceScreen")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the MainMenu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.pack()


def center_window(width, height):
    # get screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    app.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == "__main__":
    app = Kahoot()
    center_window(800, 800)
    # app.geometry("800x800")
    app.mainloop()
