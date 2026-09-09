"""Núcleo estatístico educacional implementado sem funções estatísticas prontas.

As funções aceitam qualquer iterável numérico finito. Percentis usam interpolação
linear, equivalente ao método ``linear`` padrão do NumPy. Variâncias adotam
denominador N (população) ou N-1 (amostra).
"""

from math import fsum, isfinite, sqrt
from numbers import Real


def _valores(dados):
    valores = list(dados)
    if not valores:
        raise ValueError("A amostra não pode ser vazia.")
    if any(not isinstance(x, Real) for x in valores):
        raise TypeError("Todos os valores devem ser numéricos.")
    valores = [float(x) for x in valores]
    if not all(isfinite(x) for x in valores):
        raise ValueError("Os valores devem ser finitos (sem NaN ou infinito).")
    return valores


def media(dados):
    valores = _valores(dados)
    return fsum(valores) / len(valores)


def mediana(dados):
    valores = sorted(_valores(dados))
    n = len(valores)
    meio = n // 2
    return valores[meio] if n % 2 else (valores[meio - 1] + valores[meio]) / 2


def moda(dados):
    """Retorna uma lista com todas as modas, em ordem crescente."""
    valores = _valores(dados)
    contagens = {}
    for valor in valores:
        contagens[valor] = contagens.get(valor, 0) + 1
    maior = max(contagens.values())
    return sorted(valor for valor, quantidade in contagens.items() if quantidade == maior)


def amplitude(dados):
    valores = _valores(dados)
    return max(valores) - min(valores)


def variancia_populacional(dados):
    valores = _valores(dados)
    centro = media(valores)
    return sum((x - centro) ** 2 for x in valores) / len(valores)


def variancia_amostral(dados):
    valores = _valores(dados)
    if len(valores) < 2:
        raise ValueError("A variância amostral exige ao menos dois valores.")
    centro = media(valores)
    return sum((x - centro) ** 2 for x in valores) / (len(valores) - 1)


def desvio_padrao_populacional(dados):
    return sqrt(variancia_populacional(dados))


def desvio_padrao_amostral(dados):
    return sqrt(variancia_amostral(dados))


def percentil(dados, p):
    """Percentil por interpolação linear; ``p`` deve estar entre 0 e 100."""
    if not 0 <= p <= 100:
        raise ValueError("O percentil deve estar entre 0 e 100.")
    valores = sorted(_valores(dados))
    posicao = (len(valores) - 1) * p / 100
    inferior = int(posicao)
    superior = min(inferior + 1, len(valores) - 1)
    fracao = posicao - inferior
    return valores[inferior] + fracao * (valores[superior] - valores[inferior])


def quartis(dados):
    valores = _valores(dados)
    return tuple(percentil(valores, p) for p in (25, 50, 75))


def coeficiente_variacao(dados, amostral=True):
    valores = _valores(dados)
    centro = media(valores)
    if centro == 0:
        raise ValueError("O coeficiente de variação não é definido para média zero.")
    desvio = desvio_padrao_amostral(valores) if amostral else desvio_padrao_populacional(valores)
    return desvio / abs(centro) * 100


def _pares(x, y):
    valores_x, valores_y = _valores(x), _valores(y)
    if len(valores_x) != len(valores_y):
        raise ValueError("As variáveis devem possuir o mesmo número de observações.")
    return valores_x, valores_y


def covariancia(x, y, amostral=True):
    valores_x, valores_y = _pares(x, y)
    n = len(valores_x)
    if amostral and n < 2:
        raise ValueError("A covariância amostral exige ao menos dois pares.")
    mx, my = media(valores_x), media(valores_y)
    return sum((a - mx) * (b - my) for a, b in zip(valores_x, valores_y)) / (n - int(amostral))


def correlacao_pearson(x, y):
    valores_x, valores_y = _pares(x, y)
    sx, sy = desvio_padrao_amostral(valores_x), desvio_padrao_amostral(valores_y)
    if sx == 0 or sy == 0:
        raise ValueError("A correlação não é definida para variável constante.")
    return covariancia(valores_x, valores_y, amostral=True) / (sx * sy)


def regressao_linear(x, y):
    """Retorna inclinação, intercepto e R² por mínimos quadrados."""
    valores_x, valores_y = _pares(x, y)
    mx, my = media(valores_x), media(valores_y)
    soma_xx = sum((a - mx) ** 2 for a in valores_x)
    if soma_xx == 0:
        raise ValueError("A regressão exige variação em X.")
    inclinacao = sum((a - mx) * (b - my) for a, b in zip(valores_x, valores_y)) / soma_xx
    intercepto = my - inclinacao * mx
    previstos = [intercepto + inclinacao * a for a in valores_x]
    sq_total = sum((b - my) ** 2 for b in valores_y)
    sq_residuos = sum((b - previsto) ** 2 for b, previsto in zip(valores_y, previstos))
    # Sem variação em Y, não há uma proporção de variância a explicar.
    if sq_total == 0:
        raise ValueError("R² não é definido para variável Y constante.")
    r2 = 1 - sq_residuos / sq_total
    return inclinacao, intercepto, r2
