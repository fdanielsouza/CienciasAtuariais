from math import sqrt, pi, exp, erf
from calculo import integral_aproximada

def fatorial(x):
    return x * fatorial(x - 1) if x > 1 else 1

def combinacao(n, k):
    return fatorial(n) / fatorial(k) / fatorial(n - k)

def fdp_bernoulli(x, p):
    return p ** x * (1 - p) ** (1 - x) if x in [0, 1] else 0

def fdp_binomial(n, k, p):
    return combinacao(n, k) * p ** k * (1 - p) ** (n - k)

def fdp_geometrica(k, p):
    """
    Dá a probabilidade de ocorrer um sucesso após "k - 1" tentativas

    :param k: o número de tentativas que serão realizadas
    :param p: a probabilidade de sucesso
    :return: o valor da probabilidade
    """
    return (1 - p) ** k - 1 * p

def fdp_hipergeometrica(n, g1, k):
    """
    Dada uma população com dois grupos ("g1" e "g2"), calcula a probabilidade de se retirar "k" objetos de "g1" da população
    geral, com testes de Bernoulli que alteram a probabilidade a cada retirada.

    :param n: população total
    :param g1: total do primeiro grupo
    :param k: quantos objetos de "g1" quer retirar de "n"
    :return: a probabilidade da função
    """
    return combinacao(g1, k) * combinacao(n - g1, n - g1 - k) / combinacao(n, n - g1) if g1 <= n else 0


def fdp_poisson(x, la):
    """
    Dá a probabilidade de ocorrerem "x" eventos em um determinado intervalo (de tempo ou espaço), dado que em média esse
    evento ocorre "la" vezes.

    :param x: o número de vezes que ocorrerá o evento
    :param la: valor de lambda, ou a média de vezes em que o evento costuma acontecer
    :return: a probabilidade de o evento ocorrer x vezes
    """
    return exp(-la) * la ** x / fatorial(x)

def fdp_exponencial(t, la):
    """
    A probabilidade de decorrer t períodos entre um evento e outro descritos pela dstribuição poisson.

    :param t: o tempo em que se quer saber se ocorrerá um evento
    :param la: valor de lambda, ou a média de vezes em que o evento costuma acontecer
    :return: a probabilidade de o evento ocorrer dentro do tempo t
    """
    return la * exp(-la * t)

def uniforme(x):
    return 1 if x and x <= 1 else 0

def fda_uniforme(x):
    if x < 0:
        return 0
    elif x < 1:
        return x
    else:
        return 1

def fdp_normal(x, mu=0, si=1):
    return (1 / (si * sqrt(2 * pi))) * exp(-1/2 * ((x - mu) / si) ** 2)

def fda_normal(x, mu=0, si=1):
    return (1 + erf((x - mu) / (sqrt(2) * si))) / 2

def fda_inversa_normal(p, mu=0, si=1, tolerancia=0.000001):
    if mu != 0 or si != 1:
        return mu + si * fda_inversa_normal(p, tolerancia=tolerancia)

    z_min, p_min = -10, 0
    z_max, p_max = 10, 1
    while z_max - z_min > tolerancia:
        z_med = (z_max + z_min) / 2
        p_med = fda_normal(z_med)
        if p_med < p:
            z_min, p_min = z_med, p_med
        elif p_med > p:
            z_max, p_max = z_med, p_med
        else:
            break

    return z_med


