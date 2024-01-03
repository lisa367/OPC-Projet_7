import sys
import csv

BUDGET_MAX = 500 or sys.arg[2]
file_to_import = sys.argv[1]

raw_data = []
shares = []
prices = []
profits = []



def clean_data(string):
    splitted_str = string.split(";")
    sliced_list = splitted_str[:3]
    """ 
    sliced_list[1] = int(sliced_list[1].replace(",", "."))
    sliced_list[2] = round(float(sliced_list[2].replace(",", ".")), 1)
    """
    sliced_list[1] = int(float(sliced_list[1]))
    sliced_list[2] = float(sliced_list[2])
    return sliced_list
    

def import_data(file):
    with open(file, newline="") as file:
        dataset = csv.reader(file, delimiter=" ", quotechar="|")
        for row in list(dataset)[1:]:
            new_row = clean_data(row[0])
            data = tuple(new_row)
            raw_data.append(data)
            if data[1] > 0:
                shares.append(data[0])
                prices.append(data[1])
                profits.append(data[2])

    return raw_data


def optimized_algorithm(n):
    matrix = [[0 for j in range(BUDGET_MAX+1)] for i in range(n+1)]

    for i in range(n+1):
        for j in range(BUDGET_MAX+1):
            if i == 0 or j == 0:
                continue
            elif prices[i-1] <= j :
                matrix[i][j] = max(profits[i-1] + matrix[i-1][j-prices[i-1]], matrix[i-1][j])
                # Arg1 = profit of share[i] + profit of element at position in the row above at column [current buget - current price] (j-prices(i))
                # Arg2 = the data in row above in the matrix ([i-1]), on the same column j
                # selects the max value between Arg1 and Arg2
            else:
                matrix[i][j] = matrix[i-1][j]
        #print(matrix[i])

    estimated_cost = 0.0
    best_portfolio = []
    i = n
    j = BUDGET_MAX
    while (i > 0 and j > 0):
        """ #print(i, j)
        #print(shares) """
        if matrix[i][j] == matrix[i-1][j-prices[i-1]] + profits[i-1]:
            best_portfolio.append(shares[i-1])
            estimated_cost += prices[i-1]
            j -= prices[i-1]
        i -= 1

    max_profit_within_budget = matrix[-1][-1]

    return max_profit_within_budget, best_portfolio, estimated_cost



if __name__ == "__main__":
    import_data(file_to_import)    
    best_profit, best_portfolio, estimated_cost = optimized_algorithm(n=len(shares))
    print(f"Best portfolio : {best_portfolio}")
    print(f"Estimated cost : {estimated_cost}")
    print(f"Best profit : {best_profit}")
