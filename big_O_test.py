import big_o
import functools
from matrix_multiply_quadratic_test import my_matrix_multiply, ijk_method, matrix_multiply_positive_integer
from random import randint

def samples(n):
    return ([[randint(5,10) for i in range(n)] for j in range(n)], [[randint(5,10) for i in range(n)] for j in range(n)])

def my_function_list(n: tuple):
    return my_matrix_multiply(n[0], n[1])

best, others = big_o.big_o(my_function_list, samples, min_n=10, max_n=128, n_measures=20)
print(best)