#import json

# a Python object (dict):
#x = {
#  "name": "John",
#  "age": 30,
#  "city": "New York"
#}

# convert into JSON:
#y = json.dumps(x)

# the result is a JSON string:
#print(y)
#print(y["age"])

import os

lista = os.listdir(os.getcwd() + '/projects/')

print(lista)

if 'projsekat' in lista:
  print('ima')
else:
  print('nema')