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


def determinante_2x2(matriz):
    return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]


def expansao_laplace(matriz):
    coeficientes = list()
    determinantes = list()

    def coeficientes_e_submatrizes(matriz, linhas_removidas=0):
        if len(matriz) > 2:
            coefs_linha = matriz[0]
            coefs_linha = [v * (-1) ** i for i, v in enumerate(coefs_linha)]
            coeficientes.append(coefs_linha)
            del matriz[0]

            for i, c in enumerate(coefs_linha):
                mt = transpor_matriz(matriz)
                del mt[i]
                mt = transpor_matriz(mt)

                if len(mt) == 2:
                    det = determinante_2x2(mt)
                    determinantes.append(det)

                coeficientes_e_submatrizes(mt, linhas_removidas + 1)

    coeficientes_e_submatrizes(matriz)
    tamanho_maior_coef = max([len(c) for c in coeficientes])

    for t in range(3, tamanho_maior_coef + 1):
        coefs_superiores = [c for c in coeficientes if len(c) == t]
        multiplicadores = sum([v for v in coefs_superiores], [])
        determinantes = list(transformar_vetor_em_matriz(
            [mlt * (sum(det) if isinstance(det, list) else det) for mlt, det in zip(multiplicadores, determinantes)], len(coefs_superiores[0])
        ))

    return sum(sum(determinantes, []))


def matriz_adjunta(matriz):
    adjunta = [[j for j in i] for i in matriz]

    for i in range(len(matriz[0])):
        for j in range(len(matriz)):
            mt = transpor_matriz(matriz)
            del mt[j]
            mt = transpor_matriz(mt)
            del mt[i]
            det_mt = expansao_laplace(mt) if len(mt) > 2 else determinante_2x2(mt) if len(mt) == 2 else sum(sum(mt, []))
            cofator = (-1) ** (i + j) * det_mt
            adjunta[i][j] = cofator

    return adjunta


def matriz_inversa(matriz):
    t = transpor_matriz(matriz)
    det = expansao_laplace(t) if len(t) > 2 else determinante_2x2(t)
    adj = matriz_adjunta(transpor_matriz(matriz))
    return [[j / det for j in i] for i in adj]




m = [
    [4, 5, -3, 0, 3, 3],
    [2, -1, 3, 1, 2, -2],
    [1, -3, 2, 1, 4, 5],
    [1, 2, -2, 5, 3, -5],
    [2, 4, -1, 1, -2, -4],
    [-2, -1, 1, 1, 7, 1]
]

#m = [[4, 3, 2], [4, 5, 6], [7, 9, 8]]
#m = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]


#m = [[-2, 1], [0, 0]]
print(matriz_inversa(m))

