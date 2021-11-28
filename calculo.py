from typing import Union, List
from functools import partial
from math import *


def somar_vetores_iguais(vetor1, vetor2):
    if len(vetor1) != len(vetor2):
        return None

    return [a + b for (a, b) in zip(vetor1, vetor2)]

def multiplicar_matriz_vetor(matriz, vetor):
    return [sum([im * iv for im, iv in zip(linha, vetor)]) for linha in matriz]


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


def integral(expressao, a, b, dx=0.0001):
    """
    Realiza a aproximação de uma integral, dada uma expressão com variável "x" e um intervalo a < b

    :param expressao: uma string de expressão contendo variável x
    :param a: o valor inteiro de início do intervalo da integral
    :param b: o valor inteiro do fim do intervalo da integral
    :param dx: um valor mínimo de delta x simular seu limite tendendo a zero
    :return: o valor da integral na expressão e parâmetros especificados
    """
    if a >= b:
        return None

    n = int((b - a) / dx)
    return sum([funcao(expressao, x * dx) for x in range(n)]) * dx
