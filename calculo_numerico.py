from typing import Union, List
import pandas as pd
from functools import partial


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


def funcao(expressao: str, x: Union[int, float]) -> Union[int, float]:
    """
    Avalia uma função contendo a variável x

    :param expressao: um texto contendo uma expressão matemática contendo a variável x
    :param x: valor em que a variável x será avaliada
    :return: o resultado da função, ou um valor de y
    """
    return eval(expressao)


def quociente_diferencial(expressao: str, x: Union[int, float], dx: float) -> Union[int, float]:
    """
    Deriva uma determinada função contendo a variável x por aproximação utilizando um número dx preferencialmente pequeno

    :param expressao: um texto contendo uma expressão matemática contendo a variável x
    :param x: um valor de "x" a ser avaliado na função
    :param dx: um valor muito pequeno que deve simular o limite de delta_x -> 0
    :return: o valor aproximado da inclinação da reta tangente em x, f(x)
    """
    f = partial(funcao, expressao)
    return (f(x + dx) - f(x)) / dx


def derivar_em_intervalo(expressao: str, a: int, b: int, dx: Union[int, float]) -> Union[List[int], List[float]]:
    """
    Deriva determinada função matemática para cada valor de x em um intervalo de números inteiros

    :param expressao: um texto contendo uma expressão matemática contendo a variável x
    :param a: o valor inteiro inicial do intervalo de avaliação das derivadas
    :param b: o valor inteiro final do intervalo de avaliação das derivadas
    :param dx: um valor muito pequeno que deve simular o limite de delta_x -> 0
    :return: o valor aproximado da reta tangente em x, f(x) para cada x no intervalo especificado
    """
    x = range(a, b)
    return [quociente_diferencial(expressao, xi, dx) for xi in x]


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


#print(metodo_bisseccao("x ** 3 - x - 1", -3, 2, 20))
#print(metodo_newton_raphson("x ** 2", 1, 0.000001, 0.00001, 20))
#print(metodo_secantes("x ** 2", 1, 3, 0.00001, 20))




