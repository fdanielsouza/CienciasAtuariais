from math import sqrt
from distribuicoes import fdp_normal, fda_normal, fda_inversa_normal



def cria_intervalo_confianca(n, mu, si, a):
    z = abs(fda_inversa_normal(a/2))
    return mu - z * si / sqrt(n), mu + z * si / sqrt(n)


def probabilidade_intervalo_normal(a, b, mu=0, si=1):
    return fda_normal(b, mu, si) - fda_normal(a, mu, si)



