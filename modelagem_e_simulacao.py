import numpy as np
from math import sqrt, log
from distribuicoes import fda_inversa_qui2


def eh_num_primo(n):
    return n > 1 and all(n % i for i in range(2, n))


def linear_congruente(x, a, c, m):
    return (a * x + c) % m


def menor_primo(n):
    z = sqrt(10 * n)
    de_1_a_z = range(1, int(z))
    primos_intervalo = [eh_num_primo(i) for i in de_1_a_z]
    return max([i for (i, filtro) in zip(range(1, int(z)), primos_intervalo) if filtro])


def gerar_sequencia_congruente(n, c, sem):
    m = menor_primo(n) ** 2
    a = menor_primo(n) + 1
    res = [linear_congruente(sem, a, c, m)]
    for k in range(1, n):
        res.append(linear_congruente(res[k-1], a, c, m))

    return [i / m for i in res]


def teste_unif_qui_quadrado(n, gl, val_obs, a):
    val_esp = [n / (gl + 1) for _ in range(n)]
    qui2_calc = sum((val_obs - val_esp) ** 2 / val_esp)
    qui2_tab = fda_inversa_qui2(a, gl)
    teste_h0 = qui2_calc < qui2_tab

    return "Aceitar h0" if teste_h0 else "Rejeitar h0"


def modelo_seguros_gompertz(n, idade, benef, juros, B=0.0000429, c=1.1070839):
    v = 1/ (1 + juros)
    seq_uniforme = gerar_sequencia_congruente(n, 800, np.random.randint(low=1, high=9999))
    modelo = [log(1 - (log(c) * log(u) / B / c ** idade)) / log(c) for u in seq_uniforme]
    perda = [0 if t > n else benef * v ** t for t in modelo]
    return modelo, perda


m, p = modelo_seguros_gompertz(10000, idade=70, benef=200, juros=0.03)
print(m)