from typing import Union, List
from scipy.stats import f
from math import log
import estatistica_basica as eb
from distribuicoes import fda_f


def inclinacao_reta(
        variavelx: Union[List[int], List[float]], variavely: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função para calcular a inclinação da reta em uma regressão linear

    :param variavelx: lista de valores numéricos para a variável explicativa
    :param variavely: lista de valores numéricos para a variável dependente
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o valor do fator de inclinação da reta, ou a variação de y explicado por x
    """
    if not len(variavelx) or not len(variavely) or not len(variavelx) == len(variavely):
        return None

    cov = eb.covariancia(variavelx, variavely, lista_amostral)
    var = eb.variancia(variavelx, lista_amostral)
    resultado = cov / var
    return resultado


def intercepto_reta(
        variavelx: Union[List[int], List[float]], variavely: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função para calcular o intercepto da reta de regressão

    :param variavelx: lista de valores numéricos para a variável explicativa
    :param variavely: lista de valores numéricos para a variável dependente
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o valor do intercepto da reta, ou o valor de y quando x = 0
    """
    if not len(variavelx) or not len(variavely) or not len(variavelx) == len(variavely):
        return None

    media_x = eb.media(variavelx)
    media_y = eb.media(variavely)
    inclinacao = inclinacao_reta(variavelx, variavely, lista_amostral)
    resultado = media_y - (inclinacao * media_x)
    return resultado


def y_estimados(
        variavelx: Union[List[int], List[float]], intercepto: Union[int, float], inclinacao: Union[int, float]
) -> Union[List[int], List[float]]:
    """
    Função que calcula o valor de Y explicado para cada valor de X em uma lista, baseado na função de regressão linear

    :param variavelx: uma lista apenas numérica contendo os valores da variável explicativa
    :param intercepto: valor em que a reta de regressão linear atravessa o eixo y no ponto onde x = 0
    :param inclinacao: fator de ajuste de y para cada valor de x
    :return: uma lista numérica contendo os valores de y estimados para cada valor x na lista de entrada
    """
    if not len(variavelx):
        return None

    resultado = [intercepto + (inclinacao * item) for item in variavelx]
    return resultado


def soma_quadrados_residuos(
        variavelx: Union[List[int], List[float]], variavely: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função que calcula a soma dos quadrados dos resíduos dos valores y estimados em relação aos valores y reais

    :param variavelx: lista contendo apenas valores numéricos da variável explicativa
    :param variavely: lista contendo apenas valores numéricos da variável dependente
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o valor da soma dos quadrados de cada valor y menos o valor de y estimado para seu x correspondente
    """
    if not len(variavelx) or not len(variavely) or not len(variavelx) == len(variavely):
        return None

    intercepto = intercepto_reta(variavelx, variavely, lista_amostral)
    inclinacao = inclinacao_reta(variavelx, variavely, lista_amostral)
    lista_ychapeu = y_estimados(variavelx, intercepto=intercepto, inclinacao=inclinacao)

    if not len(lista_ychapeu) or not len(lista_ychapeu) == len(variavely):
        return None

    quadrados_residuos_estimacao = [(y - y_chapeu) ** 2 for (y, y_chapeu) in zip(variavely, lista_ychapeu)]
    resultado = sum(quadrados_residuos_estimacao)
    return resultado


def soma_quadrados_explicados(
        variavelx: Union[List[int], List[float]], variavely: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função que calcula a soma dos quadrados dos desvios dos valores y estimados em relação a média de y

    :param variavelx: lista contendo apenas valores numéricos da variável explicativa
    :param variavely: lista contendo apenas valores numéricos da variável dependente
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o valor da soma dos quadrados de cada valor y menos a média da variável y
    """
    if not len(variavelx) or not len(variavely) or not len(variavelx) == len(variavely):
        return None

    intercepto = intercepto_reta(variavelx, variavely, lista_amostral)
    inclinacao = inclinacao_reta(variavelx, variavely, lista_amostral)
    lista_ychapeu = y_estimados(variavelx, intercepto=intercepto, inclinacao=inclinacao)
    media_y = eb.media(variavely)

    if not len(lista_ychapeu):
        return None

    quadrados_desvios_explicacao = [(y_chapeu - media_y) ** 2 for y_chapeu in lista_ychapeu]
    resultado = sum(quadrados_desvios_explicacao)
    return resultado


def coef_determinacao(
        variavelx: Union[List[int], List[float]], variavely: Union[List[int], List[float]], lista_amostral: bool = True
) -> Union[int, float]:
    """
    Função que retorna o coeficiente de determinação do modelo com base na soma dos quadrados explicados e a soma dos quadrados totais

    :param variavelx: lista contendo apenas valores numéricos da variável explicativa
    :param variavely: lista contendo apenas valores numéricos da variável dependente
    :param lista_amostral: valor booleano indicando se a variância é amostral (True) ou populacional (False)
    :return: o valor do coeficiente de determinação
    """
    if not len(variavelx) or not len(variavely) or not len(variavelx) == len(variavely):
        return None

    sqe = soma_quadrados_explicados(variavelx, variavely, lista_amostral)
    sqt = sum(eb.quadrados_totais(variavely))
    resultado = sqe / sqt
    return resultado


def media_dos_quadrados(soma_dos_quadrados: Union[int, float], graus_liberdade: int) -> Union[int, float]:
    """
    Função para calcular a média dos quadrados de determinada soma, com base em n graus de liberdade

    :param soma_dos_quadrados: valor total da soma dos quadrados
    :param graus_liberdade: número de graus de liberdade
    :return:
    """
    if graus_liberdade == 0:
        return None

    resultado = soma_dos_quadrados / graus_liberdade
    return resultado


def estatistica_f(media_quadrados_explicados: Union[int, float], media_quadrados_residuos: Union[int, float]) -> Union[int, float]:
    """
    Função para retornar o valor da estatística F

    :param media_quadrados_explicados: valor da média dos quadrados explicados
    :param media_quadrados_residuos: valor da média dos quadrados dos resíduos
    :return: o valor da estatística F
    """
    if media_quadrados_residuos == 0:
        return None

    resultado = media_quadrados_explicados / media_quadrados_residuos
    return resultado


def p_value_estatistica_f(
        estatistica_f: Union[int, float], grau_liberdade_numerador: int, grau_liberdade_denominador: int
) -> Union[int, float]:
    """
    Função para trazer o valor-p da estatística F para ANOVA

    :param estatistica_f: valor da estatística F computada
    :param grau_liberdade_numerador: graus de liberdade da soma dos quadrados explicados
    :param grau_liberdade_denominador: graus de liberdade da soma dos quadrados dos resíduos
    :return: o valor-p da estatística F
    """
    resultado = 1 - fda_f(estatistica_f, grau_liberdade_numerador, grau_liberdade_denominador)
    return resultado


x = [14.83, 13.54, 12.74, 13.04, 12.73, 13.40, 13.46, 13.96, 14.67, 15.32, 16.33]
y = [1242.5, 1247.4, 1262.1, 1292.3, 1357.9, 1402.5, 1443.3, 1464.7, 1519.2, 1539.9, 1569.4]
x = [log(x_i) for x_i in x]
y = [log(y_i) for y_i in y]



print(f.cdf(12, 3, 9))



