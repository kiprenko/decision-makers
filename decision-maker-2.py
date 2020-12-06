import csv
import json
import sys

PROBABILITY_KEY = 'probability'


def get_strategies(data):
    return {key: value for key, value in data.items() if key != PROBABILITY_KEY}


def run_app(data_file_name):
    available_criterions = {1: bayes_criterion,
                            2: bernoulli_laplace_criterion,
                            3: hodge_lehmann_criterion,
                            4: germeier_criterion}
    with open(data_file_name, newline='') as csv_file:
        data = {entry[0]: entry[1:] for entry in list(csv.reader(csv_file))}
        probabilities = data[PROBABILITY_KEY]
        strategies = get_strategies(data)
    print('Data loaded:\n', prettify(data))
    menu_option = input('Available options:\n'
                        '    1. Bayes criterion\n'
                        '    2. Bernoulli-Laplace criterion\n'
                        '    3. Hodge-Lehmann criterion\n'
                        '    4. Germeier criterion\n'
                        'Choose the number of option: ')
    try:
        available_criterions[int(menu_option)](strategies, probabilities)
    except KeyError or ValueError:
        print('Invalid menu value provided. Exiting.')


def bayes_criterion(strategies, probabilities):
    strat_weights = {}
    for strat_name, values in strategies.items():
        strat_weights[strat_name] = sum([float(probabilities[i]) * int(values[i]) for i in range(len(probabilities))])
    print_results(strat_weights, 'Bayes')


def bernoulli_laplace_criterion(strategies, probabilities):
    count_of_env_states = len(next(iter(strategies.values())))
    strat_weights = {}
    for strat_name, values in strategies.items():
        strat_weights[strat_name] = sum([int(value) for value in values]) / count_of_env_states
    print_results(strat_weights, 'Bernoulli-Laplace')


def hodge_lehmann_criterion(strategies, probabilities):
    try:
        confidence_degree = float(input('Write your λ, 0 ≤ λ ≤ 1: '))
        if confidence_degree > 1 or confidence_degree < 0:
            raise ValueError
    except ValueError:
        print('Incorrect λ specified. Exiting')
        sys.exit()
    strat_weights = {}
    k = 1 - confidence_degree
    for strat_name, values in strategies.items():
        weight_by_bayes = sum([float(probabilities[i]) * int(values[i]) for i in range(len(probabilities))])
        weight_by_wald = min([int(value) for value in values])
        strat_weights[strat_name] = confidence_degree * weight_by_bayes + k * weight_by_wald
    print_results(strat_weights, 'Hodge-Lehmann')


def germeier_criterion(strategies, probabilities):
    strat_weights = {}
    for strat_name, values in strategies.items():
        strat_weights[strat_name] = min([float(probabilities[i]) * int(values[i]) for i in range(len(probabilities))])
    print_results(strat_weights, 'Germeier')


def print_results(strat_weights, strat_name):
    print('Strategies weights:\n', prettify(strat_weights))
    max_weight = max(strat_weights.values())
    answer = [k for k, v in strat_weights.items() if v == max_weight]
    print(f'The biggest weight {max_weight} has strategy(-ies) {answer}')
    print(f'According to {strat_name} criterion, the optimal strategy is {answer}')


def prettify(iterable):
    return json.dumps(iterable, indent=4)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('You have not specified the file name!')
        sys.exit()
    run_app(sys.argv[1])
