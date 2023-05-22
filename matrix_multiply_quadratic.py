from decimal import Decimal, getcontext
import math
from random import randint

def matrix_multiply_positive_integer(A, B):
    assert len(A) == len(B), "Matrices must have the same length"
    N = len(A)
    assert all(len(A[i]) == len(B[i]) for i in range(N)), "Matrices must have the same dimensions"
    
    maxi = 0
    for i in range(N):
        for j in range(N):
            maxi = max(maxi, A[i][j], B[i][j])
    
    M = math.ceil(math.log10(maxi))
    P = math.ceil(math.log10((10**(2*M)-1)*N))
    
    C = [0 for i in range(N)]
    D = [0 for i in range(N)]
    E = [[0 for i in range(N)] for j in range(N)]
    
    # Set the precision to the required number of digits
    # Note that we need extra precision due to the multiplication step
    getcontext().prec = 10 ** P - 1
    
    # Convert A and B to decimals
    A_dec = [[Decimal(str(A[i][j])) for j in range(N)] for i in range(N)]
    B_dec = [[Decimal(str(B[i][j])) for j in range(N)] for i in range(N)]
    
    for i in range(N):
        for j in range(N):
            C[i] = C[i] * (10**P) + A_dec[i][j] * (10**M)
    
    for j in range(N):
        for i in range(N):
            D[j] = D[j] * (10**P) + B_dec[N-1-i][j] * (10**M)
    
    for i in range(N):
        for j in range(N):
            E[i][j] = int((C[i] * D[j]) // (10**(P*(N-1)+2*M))) % (10**P)
    
    return E

def matrix_multiply_general_integer(A, B):
    N = len(A)
    A1 = [[0 for _ in range(N)] for _ in range(N)]
    A2 = [[0 for _ in range(N)] for _ in range(N)]
    B1 = [[0 for _ in range(N)] for _ in range(N)]
    B2 = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] >= 0:
                A1[i][j] = A[i][j]
                A2[i][j] = 0
            else:
                A1[i][j] = 0
                A2[i][j] = -A[i][j]
            if B[i][j] >= 0:
                B1[i][j] = B[i][j]
                B2[i][j] = 0
            else:
                B1[i][j] = 0
                B2[i][j] = -B[i][j]
    C1 = matrix_multiply_positive_integer(A1, B1)
    C2 = matrix_multiply_positive_integer(A1, B2)
    C3 = matrix_multiply_positive_integer(A2, B1)
    C4 = matrix_multiply_positive_integer(A2, B2)
    C = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            C[i][j] = C1[i][j] - C2[i][j] - C3[i][j] + C4[i][j]
    return C

def number_of_decimal_digits(x):
    decimal_places = 0
    if '.' in str(x):
        decimal_places = len(str(x).split('.')[1])
    return decimal_places

def matrix_multiply_float_point(A, B):
    N = len(A)
    R1, R2 = 0, 0
    A1 = [[0 for _ in range(N)] for _ in range(N)]
    B1 = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if R1 < number_of_decimal_digits(A[i][j]):
                R1 = number_of_decimal_digits(A[i][j])
            if R2 < number_of_decimal_digits(B[i][j]):
                R2 = number_of_decimal_digits(B[i][j])
    for i in range(N):
        for j in range(N):
            A1[i][j] = A[i][j] * 10 ** R1
            B1[i][j] = B[i][j] * 10 ** R2
    C = matrix_multiply_general_integer(A1, B1)
    for i in range(N):
        for j in range(N):
            C[i][j] = C[i][j] / 10 ** (R1 + R2)
    return C

def matrix_multiply_complex_number(A, B):
    N = len(A)
    def Real(x: list[list[complex]]):
        return [[z.real for z in row] for row in x]
    def Imag(x: list[list[complex]]):
        return [[z.imag for z in row] for row in x]
    Ar = Real(A)
    Ai = Imag(A)
    Br = Real(B)
    Bi = Imag(B)
    C1 = matrix_multiply_float_point(Ar, Br)
    C2 = matrix_multiply_float_point(Ar, Bi)
    C3 = matrix_multiply_float_point(Ai, Br)
    C4 = matrix_multiply_float_point(Ai, Bi)
    C = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            C[i][j] = complex(C1[i][j] - C4[i][j], C2[i][j] + C3[i][j])
    return C

def my_matrix_multiply(A, B):
    if isinstance(A[0][0], int) and A[0][0] >= 0:
        return matrix_multiply_positive_integer(A, B)
    elif isinstance(A[0][0], int):
        return matrix_multiply_general_integer(A, B)
    elif isinstance(A[0][0], float):
        return matrix_multiply_float_point(A, B)
    elif isinstance(A[0][0], complex):
        return matrix_multiply_complex_number(A, B)
    else:
        return None

def ijk_method(A,B): # for verification
    flag = True
    flag = flag and (len(A) == len(B))
    if not flag: return None
    N = len(A)
    for i in range(N): flag = flag and (len(A[i])==len(B[i]))
    if not flag: return None
    C = [ [ 0 for j in range(N) ] for i in range(N) ]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] = C[i][j] + A[i][k]*B[k][j]
    return C

if __name__ == "__main__":
    N = 20
    A = [ [ randint(1,150) for j in range(N) ] for i in range(N) ]
    B = [ [ randint(1,150) for j in range(N) ] for i in range(N) ]
    C1 = my_matrix_multiply(A,B)
    C2 = ijk_method(A,B)
    flag = True
    for i in range(N):
        for j in range(N): flag = flag and C1[i][j] == C2[i][j]
    if flag:
        print('Input size: ', N)
        print('Input matrix A')
        for i in range(N):
            for j in range(N):
                print(A[i][j], end=' ')
            print()
        print('Input matrix B')
        for i in range(N):
            for j in range(N):
                print(B[i][j], end=' ')
            print()
        print('Output matrix C1')
        for i in range(N):
            for j in range(N):
                print(C1[i][j], end=' ')
            print()
    else:
        print('Debug needed')