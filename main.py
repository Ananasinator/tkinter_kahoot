g_age = 18


class Human:
    def method(self, age):
        global g_age
        g_age = age

    def __init__(self, age, height, weight):
        self.age = self.method(age)
        self.height = height
        self.weight = weight


peter = Human(21, 180, 75)

print(g_age)
