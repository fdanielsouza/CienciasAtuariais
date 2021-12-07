def transformar_vetor_em_matriz(vetor, linhas):
    for i in range(0, len(vetor), linhas):
        yield vetor[i:i + linhas]


def transpor_matriz(matriz):
    return list(map(list, zip(*matriz)))


def multiplicar_matrizes(matriz1, matriz2):
    m2_transposta = transpor_matriz(matriz2)
    res = [[sum([a * b for a, b in zip(lin, col)]) for col in m2_transposta] for lin in matriz1]
    res = list(transformar_vetor_em_matriz(res, len(matriz1)))[0]
    return res


def processo_de_markov(matriz, n):
    estacionaria = matriz
    for _ in range(n - 1):
        matriz = multiplicar_matrizes(matriz, estacionaria)

    return matriz


def matriz_limite(matriz, tolerancia=0.00001):
    n = 1
    while True:
        matriz = processo_de_markov(matriz, n + 1)

        for i in range(len(matriz) - 1):
            teste_limite = all([abs(a - b) < tolerancia for a, b in zip(matriz[i], matriz[i + 1])])

        if teste_limite:
            print('Limite da matriz de transição encontrada na iteração:', n)
            break

        n += 1
    return matriz


m = [
    [0.25, 0.25, 0.5],
    [0.5, 0.5, 0],
    [0, 0.25, 0.75]
]

m = [
    [1/2, 1/2],
    [1/4, 3/4]
]

print(matriz_limite(m))

