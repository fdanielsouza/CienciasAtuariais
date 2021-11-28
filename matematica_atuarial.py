def converter_taxa_juros(i, p):
    return (1 + i) ** p - 1


print(converter_taxa_juros(0.05, 1/6))