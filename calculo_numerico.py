from typing import Union, List, Tuple
import pandas as pd
import re
from calculo import somar_vetores_iguais, multiplicar_matriz_vetor, funcao, quociente_diferencial, derivar_em_intervalo


def metodo_bisseccao(
        expressao: str, a_inicial: Union[int, float], b_inicial: Union[int, float], max_iteracoes: int = 10
) -> pd.DataFrame:
    """
    Função que utiliza o método de bissecção para obter um número aproximado da raíz da função entre dois intervalos

    :param expressao: uma string com a expressão a ser avaliada contendo uma variável x
    :param a_inicial: um valor inicial para o ponto mínimo do intervalo
    :param b_inicial: um valor inicial para o ponto máximo do intervalo
    :param max_iteracoes: o número máximo de interações, com o valor padrão 10
    :return: um DataFrame contendo os resultados das interações
    """
    if a_inicial >= b_inicial:
        print("O valor de a_inicial deve ser inferior ao de b_inicial")
        return None

    resultado = pd.DataFrame()
    a = a_inicial
    b = b_inicial

    for i in range(1, max_iteracoes + 1):
        x = a
        fa = eval(expressao)
        x = b
        fb = eval(expressao)

        if fa * fb > 0:
            print("Não é possível encontrar a raíz da função no intervalo especificado através do método de bissecção")
            return None

        xn = (a + b) / 2
        x = xn
        fxn = eval(expressao)
        comp_a_xn = fa * fxn < 0
        comp_b_xn = fb * fxn < 0
        linha = {"iteração": i, "a": a, "xn": xn, "b": b, "f(a)": fa, "f(xn)": fxn, "f(b)": fb}
        resultado = resultado.append(linha, ignore_index=True)

        if not (comp_a_xn or comp_b_xn) and fxn != 0:
            print("Não existe raíz da função no intervalo especificado")
            return resultado

        if comp_a_xn: b = (b + a) / 2
        if comp_b_xn: a = (b + a) / 2
    print("O valor de x mais róximo da raíz no intervalo", a_inicial, "e", b_inicial, "é:", resultado.loc[max_iteracoes - 1, "xn"], "com f(x)", resultado.loc[max_iteracoes - 1, "f(xn)"])
    return resultado


def encontra_trocas_sinal(valores: List[Union[int, float]]) -> List[Tuple[Union[int, float]]]:
    """
    Encontra os pares de valores onde ocorrem mudanças de sinal entre eles em uma lista numérica

    :param valores: uma lista de valores numéricos
    :return: uma lista de tuplas contendo os intervalos onde há mudança de sinal
    """
    resultado = list()

    for i, y in enumerate(valores):
        y_anterior = valores[i - 1]
        if i and y_anterior * y < 0:
            resultado.append((y_anterior, y))

    return resultado


def metodo_newton_raphson(
        expressao: str, x0: Union[int, float], dx: float, erro_limite: float = 0.0001, max_iteracoes: int = 5
) -> pd.DataFrame:
    """
    Função que utiliza o método de Newton-Raphson para obter um número aproximado da raíz da função a partir de um x inicial

    :param expressao: uma string com a expressão a ser avaliada contendo uma variável x
    :param x0: um valor inicial de x para avaliação da função
    :param dx: um valor muito pequeno que deve simular o limite de delta_x -> 0
    :param erro_limite: um valor limite de desvio entre 0 e o valor de f(xk), com valor padrão 0.0001
    :param max_iteracoes: o número máximo de interações, com o valor padrão 5
    :return: um DataFrame contendo os resultados das interações
    """
    resultado = pd.DataFrame()
    xk = x0

    for i in range(1, max_iteracoes + 1):
        fxk = funcao(expressao, xk)
        dxk = quociente_diferencial(expressao, xk, dx)
        linha = {"iteração": i, "xk": xk, "f(xk)": fxk, "f'(xk)": dxk}
        resultado = resultado.append(linha, ignore_index=True)

        if fxk < erro_limite:
            print("O valor de f(x)", fxk, "inferior ao limite de erro foi encontrado no x", xk, ", na iteração", i)
            erro_limite = 0

        xk = xk - (fxk / dxk)


    if erro_limite != 0: print("Não foi encontrado f(xk) inferior ao limite de erro estabelecido")
    return resultado


def metodo_secantes(
    expressao: str, x0: Union[int, float], x1: Union[int, float], erro_limite: float = 0.0001, max_iteracoes: int = 5
) -> pd.DataFrame:
    """
    Função que utiliza o método das secantes para obter um número aproximado da raíz da função a partir de dois x iniciais

    :param expressao: uma string com a expressão a ser avaliada contendo uma variável x
    :param x0: um valor inicial de x0 para avaliação da função
    :param x1: um valor inicial de x1 para avaliação da função
    :param erro_limite: um valor limite de desvio entre 0 e o valor de f(xk), com valor padrão 0.0001
    :param max_iteracoes: o número máximo de interações, com o valor padrão 5
    :return: um DataFrame contendo os resultados das interações
    """
    resultado = pd.DataFrame()
    xk_2a = x0
    xk_1a = x1
    resultado = resultado.append({"iteração": 0, "x": xk_2a, "f(x)": funcao(expressao, xk_2a)}, ignore_index=True)

    for i in range(1, max_iteracoes + 1):
        fxk_2a = funcao(expressao, xk_2a)
        fxk_1a = funcao(expressao, xk_1a)
        linha = {"iteração": i, "x": xk_1a, "f(x)": fxk_1a}
        resultado = resultado.append(linha, ignore_index=True)

        if fxk_1a < erro_limite:
            print("O valor de f(x)", fxk_1a, "inferior ao limite de erro foi encontrado no x", xk_1a, ", na iteração", i)
            erro_limite = 0

        xk = (xk_2a * fxk_1a - xk_1a * fxk_2a) / (fxk_1a - fxk_2a)
        xk_2a = xk_1a
        xk_1a = xk


    if erro_limite != 0: print("Não foi encontrado f(xk) inferior ao limite de erro estabelecido")
    return resultado

    return resultado


def metodo_gauss_seidel(sistema: List[str], max_iteracoes: int = 10) -> List[float]:
    """
    Este método aproxima a solução de um sistema linear de forma iterativa. Caso alguma variável possua coeficiente 0,
    ele deve ser colocado (exemplo: "0x"), já o coeficiente 1 pode ser omitido. As variáveis podem ter quaisquer
    letras, mas não podem usar números (use "a", "b", "c" ao invés de "x1", "x2", "x3"). Sem suporte a exponenciação ou
    funções complexas.

    :param sistema: uma lista de equações escritas em formato de texto
    :param max_iteracoes: o máximo de vezes que o algorítmo deverá iterar
    :return: um vetor com os valores aproximados aos termos independentes
    """
    matriz = list()
    vetor_independente = list()
    vetor_iterativo = [0 for _ in sistema]

    for i, eq in enumerate(sistema):
        t_independente = re.findall("=?[\-0-9]+$", eq)[0]
        termos = list(filter(None, re.split("[\+\-\s]", re.sub("=.?[\-0-9]+$", "", eq))))
        coeficientes = [re.sub("[a-zA-Z]", "", t) for t in termos]
        coeficientes = ["1" if not len(c) else c for c in coeficientes]

        sinais = re.findall("[\+\-]", eq)
        if len(sinais) < len(coeficientes):
            sinais.insert(i, "-")

        coeficiente_divisao = sinais[i] + coeficientes[i]
        del coeficientes[i]
        del sinais[i]
        sinais = ["-" if s == "+" else "+" for s in sinais]

        vetor_coeficientes = [float(s + c) / float(coeficiente_divisao) for (s, c) in zip(sinais, coeficientes)]
        vetor_coeficientes.insert(i, 0)
        matriz.append(vetor_coeficientes)
        vetor_independente.append(float(t_independente) / float(coeficiente_divisao))

    for i in range(max_iteracoes):
        vetor_iterativo_anterior = vetor_iterativo
        vetor_iterativo = somar_vetores_iguais(multiplicar_matriz_vetor(matriz, vetor_iterativo), vetor_independente)
        erro = max([abs(b - a) for (a, b) in zip(vetor_iterativo_anterior, vetor_iterativo)])

    return vetor_iterativo


print(metodo_gauss_seidel(["10a + 2b + 3c = 7", "a + 5b + c = 8", "2a +3b +10c = 6"]))








