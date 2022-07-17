# izdirlika one račune ispred, da li će ga zvati neko prije ili svaki put kad se računa, čuće se xD

import pandas

def the_morty_the_complex_calculator(dataFrameZaCalc, complex_params_formulas, complex_params_list, params_list):
    dataFrameToAdd = pandas.DataFrame()
    for complex_params_formula in complex_params_formulas:
        # šalješ theConstructoru, complex_parmeters_calculator, vrati pandas DataFrame koji kasnije dodaješ
        #complex_data = complex_params_calculator(dataFrame=dataFrame, )
        #print(complex_params_formula)
        dummy_complex_parameters_data = [[6, 6, 6],[0, 0, 0]]
        dummy_complex_parameters_dataFrame = pandas.DataFrame(dummy_complex_parameters_data, complex_params_list)
    #print(dummy_complex_parameters_dataFrame.T)
    # zasad je append ovdje, treba ga premjestiti
    dummy_complex_parameters_dataFrame = dummy_complex_parameters_dataFrame.T

    dataFrameToAdd = pandas.concat([dataFrameToAdd, dummy_complex_parameters_dataFrame])
    #print(dataFrameToAdd)
    dataFrameZaCalc = pandas.concat([dataFrameZaCalc, dataFrameToAdd], axis=1, join='inner')
    for parameter in complex_params_list:
        params_list.append(parameter)
    print('The Morty The Complex Calculator je odradio svoje.')
    print(dataFrameZaCalc)