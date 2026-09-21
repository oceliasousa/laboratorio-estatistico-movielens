"""Núcleo estatístico educacional implementado sem funções estatísticas prontas.

As medidas numéricas aceitam qualquer iterável numérico finito. Percentis usam interpolação
linear, equivalente ao método ``linear`` padrão do NumPy. Variâncias adotam
denominador N (população) ou N-1 (amostra). Contagens e modas categóricas
aceitam categorias hashable; None e NaN formam uma categoria ausente única.
"""

from math import fsum, isfinite, isnan, sqrt
from numbers import Integral, Real
import warnings


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


def frequencias_categoricas(dados):
    """Contagem própria, decrescente; empates preservam a primeira ocorrência.

    Ausentes (None/NaN) são contados sob a chave None e entram no total.
    Marcadores de bibliotecas, como pd.NA/NaT, devem ser normalizados para
    None na preparação. Rótulos literais como "Ausente" não são ausentes.
    Não utiliza Counter, value_counts ou funções estatísticas prontas.
    """
    contagens = {}
    for categoria in dados:
        if isinstance(categoria, Real):
            if isnan(categoria):
                categoria = None
            elif not isfinite(categoria):
                raise ValueError("Categorias numéricas não podem ser infinitas.")
        try:
            contagens[categoria] = contagens.get(categoria, 0) + 1
        except TypeError as erro:
            raise TypeError("Cada categoria deve ser hashable (ex.: texto ou número).") from erro
    if not contagens:
        raise ValueError("A amostra não pode ser vazia.")
    return dict(sorted(contagens.items(), key=lambda item: -item[1]))


def moda_categorica(dados):
    """Todas as categorias de frequência máxima, na ordem de ocorrência.

    Segue a convenção de multimode: se todas empatam, retorna todas.
    """
    contagens = frequencias_categoricas(dados)
    maior = max(contagens.values())
    return [categoria for categoria, quantidade in contagens.items() if quantidade == maior]


def _contagens(valores):
    contagens = list(valores)
    if not contagens or any(not isinstance(n, Integral) or n < 0 for n in contagens):
        raise ValueError("Informe contagens inteiras não negativas em uma lista não vazia.")
    return contagens


def frequencias_relativas(contagens):
    """Proporções n_i / N, entre 0 e 1, na mesma ordem das contagens."""
    contagens = _contagens(contagens)
    total = sum(contagens)
    if total == 0:
        raise ValueError("A frequência relativa exige total positivo.")
    return [quantidade / total for quantidade in contagens]


def frequencias_acumuladas(contagens):
    """Somas parciais próprias; úteis para classes numéricas ordenadas."""
    acumuladas = []
    total = 0
    for quantidade in _contagens(contagens):
        total += quantidade
        acumuladas.append(total)
    return acumuladas


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
    """CV não negativo; avisa se |média| <= 1e-10 vezes a maior magnitude."""
    valores = _valores(dados)
    centro = media(valores)
    if centro == 0:
        raise ValueError("O coeficiente de variação não é definido para média zero.")
    if abs(centro) <= 1e-10 * max(abs(x) for x in valores):
        warnings.warn("Média próxima de zero em relação aos dados: CV instável.",
                      RuntimeWarning, stacklevel=2)
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
