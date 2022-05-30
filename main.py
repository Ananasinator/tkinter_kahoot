# import requests
# import urllib.request, json
#
# r = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean')
# data = r.json()
# for i in range(len(data['results'])):
#     print(data['results'][i]['correct_answer'])
#
# print(data['results'][1])

def a(x):
    x += 1
    return x


def b(x):
    x *= 2
    return x


def c():
    global x
    return x * 10


x = 2
print(a(x))
print(b(x))
print(x)
