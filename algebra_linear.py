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
                    det = mt[0][0] * mt[1][1] - mt[0][1] * mt[1][0]
                    determinantes.append(det)

                coeficientes_e_submatrizes(mt, linhas_removidas + 1)

    coeficientes_e_submatrizes(matriz)
    tamanhos_coeficientes = [len(c) for c in coeficientes]
    tamanho_maior_coef = max(tamanhos_coeficientes)

    for t in range(3, tamanho_maior_coef + 1):
        coefs_superiores = [c for c in coeficientes if len(c) == t]
        multiplicadores = sum([v for v in coefs_superiores], [])
        determinantes = list(transformar_vetor_em_matriz(
            [mlt * (sum(det) if isinstance(det, list) else det) for mlt, det in zip(multiplicadores, determinantes)], len(coefs_superiores[0])
        ))

    return sum(sum(determinantes, []))
