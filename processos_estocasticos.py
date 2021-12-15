from math import exp
from algebra_linear import *



def processo_de_markov(matriz, n):
    estacionaria = matriz
    for _ in range(n - 1):
        matriz = multiplicar_matrizes(matriz, estacionaria)

    return matriz


def matriz_limite(matriz, tolerancia=0.00001):
    n = 0
    while True:
        matriz = processo_de_markov(matriz, n + 1)

        for i in range(len(matriz) - 1):
            teste_limite = all([abs(a - b) < tolerancia for a, b in zip(matriz[i], matriz[i + 1])])

        if teste_limite:
            print('Limite da matriz de transição encontrada na iteração:', n)
            break

        n += 1
    return matriz


def probabilidade_nasc_morte(par, dt=0.00001):
    return 1 - exp(-par * dt)

def probabilidade_nasc_morte(la, mu, n):
    return (1 - la / mu) * (la / mu) ** n

def definicao_sistema_nasc_morte(la, mu, c, k):
    return [(la, mu * (i if i <= c else c)) for i in range(k + 1)]


def matriz_nascimento_morte(la, mu, c, k):
    return [
        [
            - (la if i < k else 0) - (mu * min([i, c])) if i == j else la if i == j + 1 else (mu * min([j, c])) if i == j - 1 else 0
            for i in range(k + 1)
        ]
        for j in range(k + 1)
    ]

def modificar_matriz(matriz):
    modificada = transpor_matriz(matriz)
    modificada[len(modificada) - 1] = [1 for _ in modificada[len(modificada) - 1]]
    return modificada


#print(modificar_matriz(matriz_nascimento_morte(50, 30, 3, 5)))

m = [
    [0.25, 0.25, 0.5, ],
    [0.5, 0.5, 0],
    [0, 0.25, 0.75]
]

m = [[4, 5, -3, 0, 7], [2, -1, 3, 1, 3], [1, -3, 2, 1, 4], [1, 2, -2, 5, 2], [5, 3, 8, 3, 1]]

#m = [[4, 5, -3, 0], [2, -1, 3, 1], [1, -3, 2, 1], [1, 2, -2, 5]]

#m = [[4, 3, 2], [4, 5, 6], [7, 9, 8]]


print(m)
print(expansao_laplace(m))


