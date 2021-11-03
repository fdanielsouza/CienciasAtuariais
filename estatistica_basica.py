from typing import Union, List
from math import sqrt


def media(variavel: Union[List[int], List[float]]) -> Union[int, float]:
    """
    Função para encontrar a média dos valores de determinada lista

    :param variavel: uma lista contendo apenas valores numéricos
    :return: a média dos valores contidos na lista
    """
    if not len(variavel):
        return None

    resultado = sum(variavel) / len(variavel)
    return resultado


def quadrados_totais(variavel: Union[List[int], List[float]]) -> Union[List[int], List[float]]:
    """
    Função que retorna uma lista com o quadrado dos desvios de cada elemento de uma lista em relação a sua média

    :param variavel: uma lista contendo apenas valores numéricos
    :return: uma lista contendo o quadrado dos desvios de seus valores em relação a média
    """
    if not len(variavel):
        return None

    media_variavel = media(variavel)
    resultado = [(item - media_variavel) ** 2 for item in variavel]
    return resultado


def variancia(variavel: Union[List[int], List[float]], lista_amostral: bool = True) -> Union[int, float]:
    """
    Função para obter a variância dos valores de determinada lista

    :param variavel: uma lista contendo apenas valores numéricos
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: a variância dos valores contidos na lista em relação a sua própria média
    """
    if not len(variavel):
        return None

    soma_quadrados_totais = sum(quadrados_totais(variavel))
    resultado = soma_quadrados_totais / (len(variavel) - lista_amostral)
    return resultado


def desvio_padrao(variavel: Union[List[int], List[float]], lista_amostral: bool = True) -> Union[int, float]:
    """
    Função para trazer o desvio padrão dos valores de uma lista numérica

    :param variavel: uma lista contendo apenas valores numéricos
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o valor de desvio padrão dos valores da lista em relação a sua própria média
    """
    if not len(variavel):
        return None

    resultado = sqrt(variancia(variavel, lista_amostral))
    return resultado


def covariancia(
        variavel1: Union[List[int], List[float]], variavel2: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função para obter a covariância entre duas variáveis de mesmo número de observações

    :param variavel1: uma lista contendo apenas valores numéricos
    :param variavel2: uma lista contendo apenas valores numéricos
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: a covariância entre as duas listas
    """
    if not len(variavel1) or not len(variavel2) or not len(variavel1) == len(variavel2):
        return None

    media_v1 = media(variavel1)
    media_v2 = media(variavel2)
    produto_dos_desvios = [(item_v1 - media_v1) * (item_v2 - media_v2) for (item_v1, item_v2) in zip(variavel1, variavel2)]
    resultado = sum(produto_dos_desvios) / (len(variavel1) - lista_amostral)
    return resultado


def coef_correlacao(
        variavel1: Union[List[int], List[float]], variavel2: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função para trazer o coeficiente de correlação de Pearson em relação a duas variáveis

    :param variavel1: uma lista contendo apenas valores numéricos
    :param variavel2: uma lista contendo apenas valores numéricos
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o coeficiente de correlação entre as duas listas
    """
    if not len(variavel1) or not len(variavel2) or not len(variavel1) == len(variavel2):
        return None

    sigma1 = desvio_padrao(variavel1, lista_amostral)
    sigma2 = desvio_padrao(variavel2, lista_amostral)
    cov = covariancia(variavel1, variavel2, lista_amostral)
    resultado = cov / (sigma1 * sigma2)
    return resultado


x = [25, 20, 40, 45, 22, 63, 70, 60, 55, 50, 30]
y = [2000, 3500, 1000, 800, 3000, 1300, 1500, 1100, 950, 900, 1600]

print(variancia(x))
print(covariancia(x, y))
print(coef_correlacao(x, y))
print(sum(quadrados_totais(y)))