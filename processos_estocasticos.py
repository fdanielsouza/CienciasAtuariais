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


def probabilidades_nascimento_morte(matriz):
    modificada = transpor_matriz(matriz)
    modificada[len(modificada) - 1] = [1 for _ in modificada[len(modificada) - 1]]
    inversa = matriz_inversa(modificada)
    vetor_resultados_pi = [0 if i < len(inversa[0]) - 1 else 1 for i in range(len(inversa[0]))]
    vetor_probabilidade = multiplicar_matriz_vetor(inversa, vetor_resultados_pi)

    return vetor_probabilidade


def tempo_medio_atendimento(la, mu, c, k):
    matriz_nm = matriz_nascimento_morte(la, mu, c, k)
    vetor_probs = probabilidades_nascimento_morte(matriz_nm)
    soma_probs_estados = sum([i * v for i, v in enumerate(vetor_probs)])
    tma = soma_probs_estados / la / (1 - vetor_probs[k])
    return tma


def tempo_medio_espera(la, mu, c, k):
    matriz_nm = matriz_nascimento_morte(la, mu, c, k)
    vetor_probs = probabilidades_nascimento_morte(matriz_nm)
    probs_espera = [i * v for i, v in enumerate(vetor_probs) if c <= i < k]
    tme = sum([(i + 1) * (p / sum(probs_espera)) / c / mu for i, p in enumerate(probs_espera)])
    return tme



probs_sistema = probabilidades_nascimento_morte(matriz_nascimento_morte(50, 30, 3, 5))
print(tempo_medio_espera(100, 30, 3, 5) * 60 * 60)



