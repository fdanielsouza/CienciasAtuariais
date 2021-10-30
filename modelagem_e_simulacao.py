from math import sqrt


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


print(gerar_sequencia_congruente(1000, 900, 10000))
