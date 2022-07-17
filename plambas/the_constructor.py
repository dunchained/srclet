# Sprema podatke za računa i provodi račun, glavni algoritm računa!

import pandas
from the_morty_no_001 import the_black_reading_the_morty
from the_morty_no_43_23 import the_morty_the_conditioner
from the_morty_no_442 import the_morty_the_complex_calculator

# From project_opened_calc.py:
methods_list = ['method1', 'method2', 'method3']

# Common:
params_list = params_list = ['param1', 'param2', 'param3']
params_data = [[1, 2, 3],[1, 2, 3],[1, 2, 3]]
dataFrameZaCalc = pandas.DataFrame(data=params_data, columns=params_list)

for method in methods_list:
    # Svi podaci za račun iz Black Morty:
    the_black_reading_the_morty(method_name=method)

    # Kalkulacija kompleksnih parametara:
    complex_params_list = ['c_param1', 'c_param2']
    #complex_params_list = []
    complex_params_formulas = ['c1_formula.txt', 'c2_formula.txt']
    if not complex_params_list:
        print('The Morty The Complex Calculator nema posla ovdje.')
    else:
        # Poziv na:
        the_morty_the_complex_calculator(
            dataFrameZaCalc=dataFrameZaCalc,
            complex_params_formulas=complex_params_formulas,
            complex_params_list=complex_params_list,
            params_list=params_list)
        # Za sada dummy code:
        

# učitaš je kao varijablu iz prethodnog prozora
method_formula = 'formula.txt'


#complex_params_list = []

#if not complex_params_list:
    #print('nema kompleksnih parametara')
    # print zamijeni sa log consolom
 #   pass
#else:
 #   dataFrameToAdd = pandas.DataFrame()
  #  for complex_params_formula in complex_params_formulas:
        # šalješ theConstructoru, complex_parmeters_calculator, vrati pandas DataFrame koji kasnije dodaješ
        #complex_data = complex_params_calculator(dataFrame=dataFrame, )
        #print(complex_params_formula)
   #     dummy_complex_parameters_data = [[6, 6, 6],[0, 0, 0]]
    #    dummy_complex_parameters_dataFrame = pandas.DataFrame(dummy_complex_parameters_data, complex_params_list)
    #print(dummy_complex_parameters_dataFrame.T)
    # zasad je append ovdje, treba ga premjestiti
    #dummy_complex_parameters_dataFrame = dummy_complex_parameters_dataFrame.T

    #dataFrameToAdd = pandas.concat([dataFrameToAdd, dummy_complex_parameters_dataFrame])
    #print(dataFrameToAdd)
    #dataFrameZaCalc = pandas.concat([dataFrameZaCalc, dataFrameToAdd], axis=1, join='inner')
    #for parameter in complex_params_list:
     #   params_list.append(parameter)
#print('dataFrame nakon provjere na complexn parametre:')
#print(dataFrame)
#print('lista_parametara nakon provjere na complexne parametre:')
#print(params_list)

# dever s uslovima 
conditions_dic = {
    'uslov1': 'param1 < param2: c_param1 = c_param1 - 1',
    'uslov2': 'param1 > param2: c_param2 = c_param2 + 1'
}

for key, condition in conditions_dic.items():
    #print(key, ' : ', condition)
    #print(condition.split(':'))
    condition_to_pass = condition.split(':')[0]
    new_formula = condition.split(':')[1]
    #print(condition_to_pass)
    #print(new_formula)
    #dataFrame = conditions_data_transformation(dataFrame=dataFrame, condition=condition_to_pass, new_formula=new_formula)
    #print(condition)
#print('dataFrame nakon uslova:')
#print(dataFrame)


#if 
#function = 'k'

#method_list = ['method1', 'method2']

#for method in method_list:
 #   print(method)
  #  fcn = bob_the_builder(formula=formula, function_definition=function)
   # print(fcn(9))