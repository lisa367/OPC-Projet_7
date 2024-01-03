import sys
import csv
import pandas as pd
from itertools import combinations
from operator import itemgetter

BUDGET_MAX = 500 or sys.arg[2]

file_to_import = sys.argv[1]
raw_data = []
raw_dict = {}


def clean_data(string):
    splitted_str = string.split(";")
    sliced_list = splitted_str[:3]
    sliced_list[1] = int(float(sliced_list[1]))
    sliced_list[2] = float(sliced_list[2])
    return sliced_list
    

# Import et calcul des benefices
def import_data(file):
    #raw_data = []
    #raw_dict = {}
    with open(file, newline="") as file:
        dataset = csv.reader(file, delimiter=" ", quotechar="|")
        # print(list(dataset))
        for row in list(dataset)[1:]:
            new_row = clean_data(row[0])
            # print(new_row)
            data = tuple(new_row)
            raw_data.append(data)
            raw_dict[data[0]] = {
                "price": data[1],
                "profit": data[2],
            }

    return raw_data

# Filtrer les combinaisons dont le prix est inferieur ou egal a 500 euros
def price_within_budget(combination):
    combination_profits = [raw_dict[share]["price"] for share in list(combination)]
    total_profit = sum(combination_profits)
    return total_profit <= BUDGET_MAX


# Determiner toutes les combinaisons possibles
def all_possible_combinations(shares_list):
    all_shares_names = [share[0] for share in shares_list]
    # print("Shares names : ", all_shares_names)
    combinations_full_data = []
    # for i in range(2, 3):
    for i in range(1, len(shares_list)):
        combinations_list = list(combinations(all_shares_names, i))
        #print(f"\nCOMB {i} : \n",combinations_list)
        for combination in combinations_list:
            within_budget = price_within_budget(combination)
            if within_budget:
                #print("Combination : \n", combination)
                total_price = sum([raw_dict[share]["price"] for share in combination])
                total_profit = sum([raw_dict[share]["profit"] for share in combination])
                combinations_full_data.append((combination, total_price, total_profit))

    # print("All combinations : ", combinations_full_data)

    return combinations_full_data


# Ordonner les combinaisons selon leur rendement, puis selon leur prix
def sort_combinations(combinations_list):
    """ # combination = (shares, prix, profit)
    # combinations_list = list of all combinations --> [(), (), (), ...] """
    sort_by_profit = sorted(combinations_list, key=itemgetter(2))
    #print(sort_by_profit)
    # sort_by_price = sorted(sort_by_profit, key=itemgetter(1), reverse=True)
    return sort_by_profit


if __name__ == "__main__":
    raw_shares_data = import_data(file_to_import)
    all_portfolios_within_budget = all_possible_combinations(raw_shares_data)
    sorted_portfolios = sort_combinations(all_portfolios_within_budget)
    print(sorted_portfolios[-1])
    # Returns (('Action-4', 'Action-5', 'Action-6', 'Action-8', 'Action-10', 'Action-11', 'Action-13', 'Action-16', 'Action-17', 'Action-19', 'Action-20'), 500, 598.8000000000001)

