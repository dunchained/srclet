# zaprima dataFrame i uslove, riješi uslove i vrati dataFrame
# poziva ga the_constructor
from math import *
from numpy import append

import pandas

condition = 'var.param1 <= var.param2'
condition_if_true = 'i_var.param3 = i_var.param1 + i_var.param2 + i_var.param2'
condition_if_false = 'var.param3 = var.param1 - var.param2'
condition_parameters = ['param1', 'param2']
condition_params_data = [[3, 2],[3, 2],[1, 2]]
conditionsDataFrame = pandas.DataFrame(data=condition_params_data, columns=condition_parameters)

params_list = ['param1', 'param2', 'param3']
params_data = [[2, 2, 3],[2, 2, 3],[1, 2, 3]]
dataFrame = pandas.DataFrame(data=params_data, columns=params_list)

def the_morty_the_conditioner(condition, condition_parameters, conditionsDataFrame, dataFrame, condition_if_true, condition_if_false):
    #print(conditionsDataFrame)
    for row in range(conditionsDataFrame.shape[0]):
        function_parameters = []
        for column in range(conditionsDataFrame.shape[1]):
            cell_value = conditionsDataFrame.iloc[row, column]
            data = str(cell_value)
            addition_to_list = conditionsDataFrame.columns[column] + ' = ' + data
            function_parameters.append(addition_to_list)
        
        parameter_keys = []
        parameter_values = []
        
        for parameter in function_parameters:
            parameter_key = parameter.split(' = ')[0]
            parameter_value = float(parameter.split(' = ')[1])
            parameter_keys.append(parameter_key)
            parameter_values.append(parameter_value)
        
        parameter_dict = dict(zip(parameter_keys, parameter_values))
        var = pandas.Series(parameter_dict)

        if eval(condition):
            #print(condition_if_true)
            kolona_za_mijenjati = condition_if_true.split(' = ')[0]
            #print(kolona_za_mijenjati)
            promjena = condition_if_true.split(' = ')[1]
            added_rezultat = []
            for row_if_true in range(dataFrame.shape[0]):
                if_true_function_parameters = []
                irgat_parametri = ''
                for column_if_true in range(dataFrame.shape[1]):
                    cell_value_if_true = dataFrame.iloc[row_if_true, column_if_true]
                    data_if_true = str(cell_value_if_true)
                    addition_to_list_if_true = dataFrame.columns[column_if_true] + ' = ' + data_if_true
                    if_true_function_parameters.append(addition_to_list_if_true)

                parameter_keys_if_true = []
                parameter_values_if_true = []
            
                for parameter_if_true in if_true_function_parameters:
                    parameter_key_if_true = parameter_if_true.split(' = ')[0]
                    parameter_value_if_true = float(parameter_if_true.split(' = ')[1])
                    parameter_keys_if_true.append(parameter_key_if_true)
                    parameter_values_if_true.append(parameter_value_if_true)
                
                parameter_dict_if_true = dict(zip(parameter_keys_if_true, parameter_values_if_true))
                i_var = pandas.Series(parameter_dict_if_true)
                rezultat = eval(promjena)
                added_rezultat.append(rezultat)
            lisanaka = []
            kolona_izmijenjena = kolona_za_mijenjati.split('.')[1]
            dataFrame_if_true = pandas.DataFrame(data=added_rezultat, columns=[kolona_izmijenjena])
            #print(dataFrame_if_true)
        else:
            print(condition_if_false)
            #kolona_za_mijenjati = condition_if_false.split(' = ')[0]
            #promjena = condition_if_false.split(' = ')[1]
    #print('ulazni dataframe')
    #print(kolona_izmijenjena)
    dataFrame.drop(columns=kolona_izmijenjena, inplace=True, axis=1)
    dataFrame = pandas.concat([dataFrame, dataFrame_if_true], axis=1, join='inner')
    #print(dataFrame)
    return dataFrame
            
data = the_morty_the_conditioner(
    condition=condition,
    condition_if_true=condition_if_true,
    condition_if_false=condition_if_false, 
    condition_parameters=condition_parameters, 
    conditionsDataFrame=conditionsDataFrame,
    dataFrame = dataFrame)
print(data)
