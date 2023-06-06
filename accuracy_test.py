from random import randint
import matplotlib.pyplot as plt
from time import time
from matrix_multiply_quadratic import my_matrix_multiply, ijk_method, matrix_multiply_positive_integer

def calc_accuracy(input: list[list[int]], target: list[list[int]]):
    output_list = []
    n = len(input)
    for i, j in zip(input, target):
        for x, y in zip(i, j):
            if x == y:
                output_list.append(1)
            else:
                output_list.append(1 - (abs(x - y) / (x+y)))
    return sum(output_list) / len(output_list)

if __name__ == "__main__":
    setparams = [2,132,8]
    actualTime = [k for k in range(setparams[0],setparams[1],setparams[2])]
    experiTime = [k for k in range(setparams[0],setparams[1],setparams[2])]
    experiAccuracy = [k for k in range(setparams[0],setparams[1],setparams[2])]
    xaxis = [k for k in range(setparams[0],setparams[1],setparams[2])]
    for k in range(len(xaxis)):
        n1 = xaxis[k]
        A = [[randint(5,10) for i in range(n1)] for j in range(n1)]
        B = [[randint(5,10) for i in range(n1)] for j in range(n1)]
        start = time()
        C1 = ijk_method(A, B)
        # print(C1)
        end = time()
        actualTime[k] = end - start
        start = time()
        C2 = my_matrix_multiply(A, B)
        # print(C2)
        end = time()
        experiTime[k] = end - start
        experiAccuracy[k] = calc_accuracy(C1, C2)
    fig, ax = plt.subplots()
    ax.plot(xaxis,actualTime,label='Schoolbook algo')
    ax.plot(xaxis,experiTime,label='My algo')
    ax.plot(xaxis,experiAccuracy,label='My algo accuracy')
    legend = ax.legend()
    plt.show()