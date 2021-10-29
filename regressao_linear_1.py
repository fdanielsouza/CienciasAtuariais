from typing import Union, List
from math import sqrt
from scipy.stats import f


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

    cov = covariancia(variavelx, variavely, lista_amostral)
    var = variancia(variavelx, lista_amostral)
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

    media_x = media(variavelx)
    media_y = media(variavely)
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
    media_y = media(variavely)

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
    sqt = sum(quadrados_totais(variavely))
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
    resultado = 1 - f.cdf(estatistica_f, grau_liberdade_numerador, grau_liberdade_denominador)
    return resultado


x = [25, 20, 40, 45, 22, 63, 70, 60, 55, 50, 30]
y = [2000, 3500, 1000, 800, 3000, 1300, 1500, 1100, 950, 900, 1600]

print(variancia(x))
print(covariancia(x, y))
print(coef_correlacao(x, y))
print(inclinacao_reta(x, y))
print(intercepto_reta(x, y))
print(y_estimados(x, intercepto=intercepto_reta(x, y), inclinacao=inclinacao_reta(x, y)))
print(sum(quadrados_totais(y)))
print(soma_quadrados_residuos(x, y))
print(soma_quadrados_explicados(x, y))

"""
Atentar que o coef_determinacao pode ser feito usando somas de quadrados dos resíduos ou explicados / totais, 
ou simplesmente elevando o coeficiente de correlação ao quadrado, que é bem mais simples
"""
print(coef_determinacao(x, y))
print(coef_correlacao(x, y) ** 2)
print(estatistica_f(media_dos_quadrados(soma_quadrados_explicados(x, y), 1), media_dos_quadrados(soma_quadrados_residuos(x, y), len(x) - 2)))
print(1-p_value_estatistica_f(
    estatistica_f(
        media_dos_quadrados(soma_quadrados_explicados(x, y), 1),
        media_dos_quadrados(soma_quadrados_residuos(x, y), len(x) - 2)
    ), 1, 9)
)

print(estatistica_f(
        media_dos_quadrados(soma_quadrados_explicados(x, y), 1),
        media_dos_quadrados(soma_quadrados_residuos(x, y), len(x) - 2)
    ))

