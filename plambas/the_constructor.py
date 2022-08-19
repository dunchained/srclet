# Sprema podatke za računa i provodi račun, glavni algoritm računa!

import pandas
#from the_morty_no_001 import the_black_reading_the_morty
#from the_morty_no_43_23 import the_morty_the_conditioner
#from the_morty_no_442 import the_morty_the_complex_calculator

# From project_opened_calc.py:
methods_list = ['method1', 'method2', 'method3']

# Common:
params_list = ['param1', 'param2', 'param3']
params_data = [[1, 2, 3, 4],[1, 2, 3, 4],[1, 2, 3, 4]]
dataFrameZaCalc = pandas.DataFrame(data=params_data, columns=params_list)

for method in methods_list:
    # Kalkulacija uslova i to, učito ih crni Morty.
    conditions_dict = {
        'uslov1': 'param1 < param2: param1 = param1 - 1',
        'uslov2': 'param1 > param2: param2 = param2 + 1',
        'uslov3': 'param1 == param2: param2 = param2 + 1'
    }

    if not conditions_dict:
        print('The Morty The Conditioner nema posla ovdje.')

    else:
        for key, condition in conditions_dict.items():
            condition_to_pass = condition.split(':')[0]
            new_formula = condition.split(':')[1]
            print('Kondicionalna!')