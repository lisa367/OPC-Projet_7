import sys
import csv
import pandas as pd

BUDGET_MAX = 500 or sys.arg[2]
file_to_import = sys.argv[1]

raw_data = []
shares = []
prices = []
profits = []


def clean_data1(string):
    splitted_str = string.split(";")
    #print(splitted_str)
    sliced_list = splitted_str[:3]
    #print(sliced_list)
    
    sliced_list[1] = int(sliced_list[1].replace(",", "."))
    sliced_list[2] = round(float(sliced_list[2].replace(",", ".")), 1)
   
    """ sliced_list[1] = int(float(sliced_list[1]))
    sliced_list[2] = float(sliced_list[2]) """
    return sliced_list


def clean_data2(string):
    splitted_str = string.split(",")
    #print(splitted_str)
    sliced_list = splitted_str[:3]
    #print(sliced_list)
    """ 
    sliced_list[1] = int(sliced_list[1].replace(",", "."))
    sliced_list[2] = round(float(sliced_list[2].replace(",", ".")), 1)
    """
    sliced_list[1] = int(float(sliced_list[1]))
    sliced_list[2] = float(sliced_list[2])
    return sliced_list
    

# Import et calcul des benefices
def import_data(file):
    with open(file, newline="") as file:
        dataset = csv.reader(file, delimiter=" ", quotechar="|")
        # print(list(dataset))
        for row in list(dataset)[1:]:
            new_row = clean_data1(row[0])
            # print(new_row)
            data = tuple(new_row)
            raw_data.append(data)
            shares.append(data[0])
            prices.append(data[1])
            profits.append(data[2])

    return raw_data

# import_data(file_to_import)

""" def output_best_portfolio(matrix, n, shares_list):
    best_portfolio = []
    i = n
    j = BUDGET_MAX
    while i > 0 and j > 0:
        if matrix[i][j] == matrix[i-1][j]:
            continue
        else :
            best_portfolio.append(shares_list[i-1])
            j -= prices[i]
        i -= 1
    return best_portfolio """


def knapsack_algorithm(n):
    matrix = [[0 for j in range(BUDGET_MAX+1)] for i in range(n+1)]
    print(len(matrix[0]),len(matrix))

    for i in range(n+1):
        for j in range(1,BUDGET_MAX+1):
            #print(i, j)
            if i == 0 or j == 0:
                matrix[i][j] = 0
            elif prices[i-1] <= j :
                matrix[i][j] = max(profits[i-1] + matrix[i-1][j-prices[i-1]], matrix[i-1][j])
                print(matrix[i][j])
                # Arg1 = profit of share[i] + profit of element at position in the row above at column [current buget - current price] (j-prices(i))
                # Arg2 = the data in row above in the matrix ([i-1]), on the same column j
                # selects the max value between Arg1 and Arg2
            else:
                matrix[i][j] = matrix[i-1][j]
        # print(len(matrix[i]))
        print(matrix[i])

    # max_profit_within_budget = matrix[n][BUDGET_MAX]

    # with preset zeros in the matrix
    # matrix = [[0 for j in range(BUDGET_MAX)] for i in range(n)]

    """ for i in range(1, n+1):
        for j in range(1, BUDGET_MAX+1):
            # print(f"Etape [{i}][{j}]")
            if prices[i-1] <= j :
                matrix[i][j] = max(profits[i-1] + matrix[i-1][j-prices[i]], matrix[i-1][j])
                #
            else:
                matrix[i][j] = matrix[i-1][j]
        print(matrix[i]) """
    
    best_portfolio = []
    i = n
    j = BUDGET_MAX
    while (i > 0 and j > 0):
        #print(i, j)
        #print(shares)
        if matrix[i][j] == matrix[i-1][j-prices[i-1]] + profits[i-1]:
            #print(i, j)
            best_portfolio.append(shares[i-1])
            #print(best_portfolio)
            j -= prices[i-1]
            #print(j)
        i -= 1
    print(f"Best portfolio : {best_portfolio}")
    """ while (i > 0 and j > 0):
        #print(i, j)
        #print(shares)
        if matrix[i][j] == matrix[i-1][j]:
            print("pass : ", i, j)
            continue
        else :
            print(i, j)
            best_portfolio.append(shares[i-1])
            print(best_portfolio)
            j -= prices[i-1]
            print(j)
        i -= 1 """


    max_profit_within_budget = matrix[-1][-1]
    #best_portfolio = output_best_portfolio(matrix=matrix, n=n, shares_list=shares)
    #print(best_portfolio)

    return max_profit_within_budget, best_portfolio



if __name__ == "__main__":
    import_data(file_to_import)
    #print(raw_data)
    #print(shares)
    #print(prices)
    #print(profits)
    print(len(shares))
    best_profit, best_portfolio = knapsack_algorithm(n=len(shares))
    print(f"Best portfolio : {best_portfolio}")
    print(f"Best profit : {best_profit}")
    # print(matrix)
    """ best_portfolio = output_best_portfolio()
    print(f"Best portfolio : {best_portfolio}") """


