# -*- coding: utf-8 -*-
"""
Autor: Piotr Palczewski

Program oceniający wydajnosc pracy reaktora chemicznego biorący pod uwage podstawowe parametry:
cisnienie, temperatury oraz stezenia substratow reakcji.

"""

import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

"""Dane wejsciowe programu - wybrane randomowo"""
pressure_val = 1050
temperature_val = 500
concentration_val = 9

"""Skala badanych danych wejsciowch"""
pressure = ctrl.Antecedent(np.arange(1013,1114,1), 'pressure')
temperature = ctrl.Antecedent(np.arange(373,674,1),'temperature')
concentration = ctrl.Antecedent(np.arange(0,11), 'concentration')

performance = ctrl.Consequent(np.arange(0,101,1), 'performance')

"""Klasyfikacja (przynależnosc) danych do klas"""
pressure['low'] = fuzzy.trimf(pressure.universe, [1013, 1013, 1063])
pressure['optimal'] = fuzzy.trimf(pressure.universe, [1013, 1063, 1113])
pressure['high'] = fuzzy.trimf(pressure.universe, [1063, 1113, 1113])

temperature['vlow'] = fuzzy.trimf(temperature.universe, [373, 373, 473])
temperature['low'] = fuzzy.trimf(temperature.universe, [373, 473, 523])
temperature['optimal'] = fuzzy.trimf(temperature.universe, [473, 523, 573])
temperature['high'] = fuzzy.trimf(temperature.universe, [523, 573, 673])
temperature['vhigh'] = fuzzy.trimf(temperature.universe, [573, 673, 673])

concentration['low'] = fuzzy.trimf(concentration.universe, [0, 0, 5])
concentration['mid'] = fuzzy.trimf(concentration.universe, [2, 5, 7])
concentration['high'] = fuzzy.trimf(concentration.universe, [5, 10, 10])

performance['vlow'] = fuzzy.trimf(performance.universe, [0, 0, 40])
performance['low'] = fuzzy.trimf(performance.universe, [30, 50, 70])
performance['avarage'] = fuzzy.trimf(performance.universe, [50, 60, 70])
performance['above-avrage'] = fuzzy.trimf(performance.universe, [60, 70, 80])
performance['optimal'] = fuzzy.trimf(performance.universe, [70, 100, 100])

"""Zasady logiki rozmytej programu"""
rule_1 = ctrl.Rule(pressure['low'] | temperature['vlow'] | concentration['low'], performance['vlow'])
rule_2 = ctrl.Rule(pressure['low'] | temperature['low'] | concentration['low'], performance['low'])
rule_3 = ctrl.Rule(pressure['optimal'] | temperature['optimal'] | concentration['low'], performance['avarage'])
rule_4 = ctrl.Rule(pressure['optimal'] | temperature['optimal'] | concentration['mid'], performance['above-avrage'])
rule_5 = ctrl.Rule(pressure['optimal'] | temperature['optimal'] | concentration['high'], performance['optimal'])
rule_6 = ctrl.Rule(pressure['high'] | temperature['vhigh'] | concentration['low'], performance['vlow'])
rule_7 = ctrl.Rule(pressure['high'] | temperature['high'] | concentration['low'], performance['low'])
rule_8 = ctrl.Rule(pressure['high'] | temperature['high'] | concentration['mid'], performance['avarage'])

"""Zbiór regół jako system - agregacja"""
performance_ctrl = ctrl.ControlSystem([rule_1, rule_2, rule_3, rule_4, rule_5, rule_6, rule_7, rule_8])
performance = ctrl.ControlSystemSimulation(performance_ctrl)

performance.input['pressure'] = pressure_val
performance.input['temperature'] = temperature_val
performance.input['concentration'] = concentration_val

performance.compute()

"""Wyswietlenie wyniku"""
print("Wydajnosc wynosi obecnie: " + str(int(performance.output['performance'])))
