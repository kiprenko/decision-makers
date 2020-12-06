import csv
import sys


def run_app(data_file_name):
    available_strategies = {1: wald_criterion,
                  2: optimism_criterion,
                  3: pessimism_criterion,
                  4: hurwitz_criterion,
                  5: savage_criterion}
    with open(data_file_name, newline='') as csv_file:
        data = {entry[0]: entry[1:] for entry in list(csv.reader(csv_file))}
    menu_option = input('Available options:\n'
                        '    1. Wald criterion\n'
                        '    2. optimism criterion\n'
                        '    3. pessimism criterion\n'
                        '    4. Hurwitz criterion\n'
                        '    5. Savage criterion\n'
                        'Choose the number of option: ')
    try:
        available_strategies[int(menu_option)](data)
    except KeyError and ValueError:
        print('Invalid menu value provided. Exiting.')


def wald_criterion(data):
    min_val = get_mins(data)
    maximin = max(min_val.values())
    answer = [k for k, v in min_val.items() if v == maximin]
    print(f'According to Wald\'s criterion, the optimal strategy is {answer}')


def optimism_criterion(data):
    max_val = get_maxs(data)
    maximax = max(max_val.values())
    answer = [k for k, v in max_val.items() if v == maximax]
    print(f'According to optimism criterion, the optimal strategy is {answer}')


def pessimism_criterion(data):
    min_val = get_mins(data)
    minimin = min(min_val.values())
    answer = [k for k, v in min_val.items() if v == minimin]
    print(f'According to pessimism criterion, the optimal strategy is {answer}')


def hurwitz_criterion(data):
    try:
        optimism_value = float(input('Write your λ, 0 ≤ λ ≤ 1: '))
        if optimism_value > 1 or optimism_value < 0:
            raise ValueError
    except ValueError:
        print('Incorrect λ specified. Exiting')
        sys.exit()

    max_vals = get_maxs(data)
    min_vals = get_mins(data)
    hurwitz_values = {}
    n = 1 - optimism_value
    for s_name, max_val in max_vals.items():
        hurwitz_values[s_name] = int(max_val) * optimism_value + n * int(min_vals[s_name])
    max_hurwitz_value = max(hurwitz_values.values())
    answer = [k for k, v in hurwitz_values.items() if v == max_hurwitz_value]
    print(f'According to Hurwitz criterion, the optimal strategy is {answer}')


def savage_criterion(data):
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
    print(f'According to Savage criterion, the optimal strategy is {answer}')


def get_mins(data):
    return {s_name: min(env_values) for s_name, env_values in data.items()}


def get_maxs(data):
    return {s_name: max(env_values) for s_name, env_values in data.items()}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('You have not specified the file name!')
        sys.exit()
    run_app(sys.argv[1])
