"""Formatacao do laboratório estatístico."""




def formatar(numero, casas=2):
    return f"{numero:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
