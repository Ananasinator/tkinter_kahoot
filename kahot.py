import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import winsound
import requests

'''
--------------------------------
KAHOOT (kahot) TKINTER PROGRAM
Author: ROMANOVA Anastasiia 
--------------------------------

This program is a parody of a popular game Kahoot. The point of the game is answer correctly on the given question
by pressing "true" of "false" button to gain points. 1 right answer = 1 point, 1 false answer = 0 points.

--------------------------------
'''

# global variables which are used in Game class to change questions
index, counter = 0, 0

# get questions data from open database in json format
r = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean')
data = r.json()
# parse json file and check for visual mistakes which occur because of wrong text encoding
for i in range(len(data['results'])):
    if "&quot;" in str(data['results'][i]['question']):
        data['results'][i]['question'] = str(data['results'][i]['question']).replace("&quot;", "")
# "global labels", aka labels which are initialised here to be used later to update the game score and questions
question_label = tk.Label(tk.Tk().withdraw())
counter_label = tk.Label(tk.Tk().withdraw())


# root class
class Kahoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # create a container which stores all the other classes
        # other classes are inheriting from tk.Frame so they are frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (MainMenu, Game, Preferences):
            page_name = frame.__name__
            frame = frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # here is a call of a method which raises frames when using them is needed
        # basically changing the screen content
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        # show a frame using given page (frame) name
        frame = self.frames[page_name]
        frame.tkraise()


# main menu frame class
class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        app_name = tk.Label(self, text="Kah(o)t")
        app_description = tk.Label(self, text="CE (Computer Expert) Edition")
        app_name.pack(side="top", fill="x", pady=10)
        app_description.pack(side="top", fill="x", pady=10)

        start_btn = tk.Button(self, text="Start",
                              command=lambda: controller.show_frame("Game"))
        pref_btn = tk.Button(self, text="Preferences",
                             command=lambda: controller.show_frame("Preferences"))
        quit_btn = tk.Button(self, text="Quit", command=lambda: exit())
        start_btn.pack()
        pref_btn.pack()
        quit_btn.pack()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # we need to restart the game after user quits to main menu so we call restart_game method
        mainmenu_btn = tk.Button(self, text="Go to the main menu",
                                 command=lambda: [restart_game(), controller.show_frame("MainMenu")])
        mainmenu_btn.pack(anchor="n")

        start_btn = tk.Button(self, text="Start",
                              command=lambda: [self.updateQuestion(), start_btn.pack_forget()])
        start_btn.pack(anchor="n")

        # making this value global was to give a possibility to update question's contests using updateQuestion() method
        # otherwise it would've been imposibble to dynamically update it
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

        # it's the same as with the question_label
        global counter_label
        counter_label = tk.Label(self, textvariable=self.updateCounter())
        counter_label.pack()

    def updateQuestion(self):
        # update value of question_label using index
        global index, question_label
        question_label['text'] = str(data['results'][index]['question'])

    def updateCounter(self):
        # update value of counter_label using counter
        global counter, counter_label
        counter_label['text'] = int(counter)

    def onClickHandler(self, val):
        # when a button is pressed, this method is called
        global index, data, counter
        # the try/except structure is used because when data['results][index] is out of range, we need
        # to catch IndexOutOfBounds exception and use it as an indicator that game is finished
        try:
            # if the value which a button has (given by lambda) is the same as the correct answer in the json file,
            # we assume that user pushed the right button and proceed with adding 1 point to the score (counter),
            # dynamically update counter using updateCounter() and play a sound which indicates right answer
            if val == bool(data['results'][index]['correct_answer']):
                counter += 1
                self.updateCounter()
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            # else we do nothing and play another sound which would indicate wrong answeer
            else:
                winsound.MessageBeep(winsound.MB_ICONHAND)
            index += 1
            self.updateQuestion()
        # when we are out of questions, IndexError occurs, and then the game is finished so we display a final screen
        # and a number of points that user had scored
        except IndexError:
            question_label['text'] = str(f"You scored {counter} points!")


# settings frame class
class Preferences(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        mainmenu_btn = tk.Button(self, text="Go to the MainMenu",
                                 command=lambda: controller.show_frame("MainMenu"))
        mainmenu_btn.pack()

        label = tk.Label(self, text="Preferences")
        label.pack(side="top", fill="x", pady=10)

        setting_frame = tk.Frame(self)
        res_label = tk.Label(setting_frame, text="Resolution: ")
        # creating a combobox for user to choose resolutions from
        resolutions = ttk.Combobox(setting_frame)
        resolutions['values'] = ("800x600", "1366x768", "1920x1080")
        resolutions.current()
        # binding a click in combobox with resize_window_callback to change window size when the option is chosen
        resolutions.bind("<<ComboboxSelected>>", resize_window_callback)
        res_label.pack(side="left")
        resolutions.pack()
        setting_frame.pack()


def resize_window_callback(event):
    # getting a callback of an event, which is a click in the combobox and extracting the string from the chosen
    # option, then splitting it to put as an arguments for center_window
    vals = event.widget.get().split("x")
    center_window(int(vals[0]), int(vals[1]))


def center_window(width, height):
    # getting screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # calculating position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    app.geometry('%dx%d+%d+%d' % (width, height, x, y))


def restart_game():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def on_closing():
    # creating message dialogue whenever user presses cross in windows interface in the upper right corner
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        exit()


# start application
if __name__ == "__main__":
    app = Kahoot()
    center_window(800, 600)
    winsound.PlaySound("play.wav", winsound.SND_ASYNC)
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
