from math import log


def converte_i_composto(i, proporcao):
    return (1 + i) ** proporcao - 1


def vf_composto(vp, i, n):
    return vp * (1 + i) ** n


def vp_composto(vf, i, n):
    return vf / (1 + i) ** n


def n_composto(vf, i):
    return log(vf) / log(1 + i)


def pmt_periodico(vf=None, vp=None, n, i, p=True):
    if p:
        if vp:
            return vp * ((1 + i ** n) * i) / ((1 + i) ** n - 1)
        else:
            return vf * i / ((1 + i) ** n - 1)
    else:
        if vp:
            return vp * ((1 + i) ** (n - 1) * i) / ((1 + i) ** n - 1)
        else:
            return vf * i / ((1 + i) ** n - 1) * 1 / (1 + i)


def vp_periodico(pmt, n, i, p=True):
    if p == True:
        return pmt * ((1 + i) ** n - 1) / i / (1 + i) ** n
    else:
        return pmt * ((1 + i) ** n - 1) / ((1 + i) ** (n - 1) * i)


def vf_periodico(pmt, n, i, p=True):
    if p == True:
        return pmt / i * ((1 + i) ** n - 1)
    else:
        return pmt * (1 + i) / i * ((1 + i) ** n - 1)


