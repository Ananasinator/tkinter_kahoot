g_age = 18


class Human:
    def method(self, age):
        global g_age
        g_age = age

    def __init__(self, age, height, weight):
        self.age = self.method(age)
        self.height = height
        self.weight = weight

        Animal.change_gb(self)


class Animal:
    def __init__(self, type):
        self.type = type

        # self.change_gb()

    def change_gb(self):
        global g_age
        g_age *= 100




peter = Human(21, 180, 75)
dog = Animal('dog')
# dog.change_gb()
print(g_age)

# def display_question(self, number):
#     global data
#     current_question = data['results'][number]['question']
#     return current_question
#
#
# def start_game_btn(self):
#     global index
#     self.display_question(index, )
#
#
# def btn_onclick_handler(self, val):
#     global index, counter
#     if index <= 8:
#         if val == bool(data['results'][index]['correct_answer']):
#             winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
#             counter += 1
#             print(counter)
#         else:
#             winsound.MessageBeep(winsound.MB_ICONHAND)
#             print(counter)
#         index += 1
#         self.display_question(index)
#     else:
#         print(counter, "The End")
#         self.controller.show_frame("TheEnd")
