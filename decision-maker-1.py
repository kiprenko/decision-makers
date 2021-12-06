import csv
import sys
import numpy as np

PROBABILITY_KEY = 'olasilik'
def get_strategies(data):
    return {key: value for key, value in data.items() if key != PROBABILITY_KEY}

def run_app(data_file_name):
    esas_criterions = {
        1: gelir_esasli,
        2: maliyet_esasli,
    }
    with open(data_file_name, newline='') as csv_file:
        data = {entry[0]: entry[1:] for entry in list(csv.reader(csv_file))}


    esas_option = input('Secenekler:\n'
                        '    1. Gelir esaslı\n'
                        '    2. Maliyet esaslı\n'
                        'Uygun olan seçenek: '
                        )
    try:
        esas_criterions[int(esas_option)](data)
    except KeyError and ValueError:
        print('Gecersiz secenek degeri girildi. Cikiliyor...')




def gelir_esasli(data):

    available_criterions = {
        1: iyimserlik_kriteri,
        2: kötümserlik_kriteri,
        3: hurwitz_kriteri,
        4: savage_kriteri,
        5: laplace_kriteri
    }


    menu_option = input('Secenekler:\n'
                        '    1. İyimserlik kriteri\n'
                        '    2. Kötümserlik kriteri\n'
                        '    3. Hurwitz kriteri\n'
                        '    4. Savage kriteri\n'
                        '    5. Laplace kriteri\n'
                        'Uygun olan seçenek: ')
    try:
        available_criterions[int(menu_option)](data)
    except KeyError and ValueError:
        print('Gecersiz secenek degeri girildi. Cikiliyor...')

def maliyet_esasli(data):

    available_criterions = {
        1: iyimserlik_kriteri_maliyet,
        2: kötümserlik_kriteri_maliyet,
        #3: hurwitz_kriteri_maliyet,
        #4: savage_kriteri_maliyet,
        5: laplace_kriteri_maliyet
    }

    menu_option = input('Secenekler:\n'
                        '    1. İyimserlik kriteri\n'
                        '    2. Kötümserlik kriteri\n'
                        '    5. Laplace kriteri\n'
                        'Uygun olan seçenek: ')
    try:
        available_criterions[int(menu_option)](data)
    except KeyError and ValueError:
        print('Gecersiz secenek degeri girildi. Cikiliyor...')


def iyimserlik_kriteri(data):
    max_val = get_maxs(data)
    maximax = max(max_val.values())
    answer = [k for k, v in max_val.items() if v == maximax]
    print(f'İyimserlik kriterine göre, optimal strateji {answer}')

def iyimserlik_kriteri_maliyet(data):
    min_val = get_mins(data)
    minimin = min(min_val.values())
    answer = [k for k, v in min_val.items() if v == minimin]
    print(f'İyimserlik kriterine göre, optimal strateji {answer}')

def kötümserlik_kriteri(data):
    min_val = get_mins(data)
    minimax = max(min_val.values())
    answer = [k for k, v in min_val.items() if v == minimax]
    print(f'Kötümserlik kriterine göre, optimal strateji {answer}')

def kötümserlik_kriteri_maliyet(data):
    max_val = get_maxs(data)
    maximin = min(max_val.values())
    answer = [k for k, v in max_val.items() if v == maximin]
    print(f'Kötümserlik kriterine göre, optimal strateji {answer}')

def hurwitz_kriteri(data):
    try:
        optimism_value = float(input('λ Degeri girin, 0 ≤ λ ≤ 1: '))
        if optimism_value > 1 or optimism_value < 0:
            raise ValueError
    except ValueError:
        print('Yanlış λ belirlendi. Cikiliyor')
        sys.exit()

    max_vals = get_maxs(data)
    min_vals = get_mins(data)
    hurwitz_values = {}
    n = 1 - optimism_value
    for s_name, max_val in max_vals.items():
        hurwitz_values[s_name] = int(max_val) * optimism_value + n * int(min_vals[s_name])
    max_hurwitz_value = max(hurwitz_values.values())
    answer = [k for k, v in hurwitz_values.items() if v == max_hurwitz_value]
    print(f'Hurwitz kriterine göre, optimal strateji {answer}')


def savage_kriteri(data):
    max_profits = []
    for i in range(len(next(iter(data.values())))):
        max_profits.append(max([value[i] for value in data.values()]))
    regret_matrix = {}
    for s_name, env_values in data.items():
        regret_matrix[s_name] = [int(max_profits[i]) - int(env_values[i]) for i in range(len(env_values))]
    max_regrets = {}
    for s_name, regrets in regret_matrix.items():
        max_regrets[s_name] = max(regrets)
    minimal_max_regret = min(max_regrets.values())
    answer = [k for k, v in max_regrets.items() if v == minimal_max_regret]
    print(f'Savage kriterine göre, optimal strateji {answer}')

def laplace_kriteri(strategies):
    count_of_env_states = len(next(iter(strategies.values())))
    strat_weights = {}
    for strat_name, values in strategies.items():
        strat_weights[strat_name] = sum([int(value) for value in values]) / count_of_env_states
    print_results(strat_weights, 'Laplace')

def laplace_kriteri_maliyet(strategies, probabilities):
    count_of_env_states = len(next(iter(strategies.values())))
    strat_weights = {}
    for strat_name, values in strategies.items():
        strat_weights[strat_name] = sum([int(value) for value in values]) / count_of_env_states
    print_results_maliyet(strat_weights, 'Laplace')

def prettify(iterable):
    import json
    return json.dumps(iterable, indent=4)

def print_results(strat_weights, strat_name):
    print('Strategies weights:\n', prettify(strat_weights))
    max_weight = max(strat_weights.values())
    answer = [k for k, v in strat_weights.items() if v == max_weight]
    print(f'The biggest weight {max_weight} has strategy(-ies) {answer}')
    print(f'According to {strat_name} criterion, the optimal strategy is {answer}')

def print_results_maliyet(strat_weights, strat_name):
    print('Strategies weights:\n', prettify(strat_weights))
    min_weight = min(strat_weights.values())
    answer = [k for k, v in strat_weights.items() if v == min_weight]
    print(f'The biggest weight {min_weight} has strategy(-ies) {answer}')
    print(f'According to {strat_name} criterion, the optimal strategy is {answer}')


def get_mins(data):
    return {s_name: min({int(item) for item in env_values}) for s_name, env_values in data.items()}


def get_maxs(data):
    return {s_name: max({int(item) for item in env_values}) for s_name, env_values in data.items()}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Dosya adını girmelisiniz!')
        sys.exit()
    run_app(sys.argv[1])
