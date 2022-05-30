# import requests
# import urllib.request, json
#
# r = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean')
# data = r.json()
#
#
# # print(r.text)
# for i in range(len(data['results'])):
#     if "&quot;" in str(data['results'][i]['question']):
#         data['results'][i]['question'] = str(data['results'][i]['question']).replace("&quot;", "")
#     print(data['results'][i]['question'])
#
# # print(data['results'][1])
#
# # def a(x):
# #     x += 1
# #     return x
# #
# #
# # def b(x):
# #     x *= 2
# #     return x
# #
# #
# # def c():
# #     global x
# #     return x * 10
# #
# #
# # x = 2
# # print(a(x))
# # print(b(x))
# # print(x)

a_global_var = "hello"

class A():
    def modify_global(self):
        global a_global_var
        a_global_var += " world"

A().modify_global()

print(a_global_var)