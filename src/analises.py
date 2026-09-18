"""Analises do laboratório estatístico."""

from src import minhastats as ms
from dataclasses import dataclass
from bisect import bisect_right
from math import exp, pi, sqrt

import numpy as np
import pandas as pd


def tabela_categorica(valores):
    """Prepara ausentes; contagem, proporções e modas vêm do núcleo próprio.

    O DataFrame só organiza os resultados para exibição. O marcador visual
    dos ausentes não colide com categorias literais já presentes.
    """
    categorias = [None if pd.isna(valor) else valor for valor in valores]
    contagens = ms.frequencias_categoricas(categorias)
    modas = set(ms.moda_categorica(categorias))
    rotulo_ausente = "Ausente (valor faltante)"
    while rotulo_ausente in contagens:
        rotulo_ausente += " *"
    return pd.DataFrame({
        "Categoria": [rotulo_ausente if c is None else c for c in contagens],
        "Frequência": list(contagens.values()),
        "Frequência relativa (%)": [100 * p for p in ms.frequencias_relativas(contagens.values())],
        "Modal": [c in modas for c in contagens],
    })


@dataclass(frozen=True)
class Frequencias:
    limites: list[float]
    contagens: list[int]

    @property
    def centros(self):
        return [(a + b) / 2 for a, b in zip(self.limites, self.limites[1:])]

    @property
    def larguras(self):
        return [b - a for a, b in zip(self.limites, self.limites[1:])]

    @property
    def densidades(self):
        total = sum(self.contagens)
        return [n / (total * largura) for n, largura in zip(self.contagens, self.larguras)]


def tabela_frequencias(valores, classes=10):
    """Classes [a,b), última fechada; contagem própria compartilhada pelo gráfico."""
    valores = ms._valores(valores)
    if not isinstance(classes, int) or classes < 1:
        raise ValueError("O número de classes deve ser um inteiro positivo.")
    minimo, maximo = min(valores), max(valores)
    if minimo == maximo:
        minimo, maximo = minimo - 0.5, maximo + 0.5
    passo = (maximo - minimo) / classes
    limites = [minimo + i * passo for i in range(classes)] + [maximo]
    contagens = [0] * classes
    # Busca binária respeita exatamente as bordas usadas para desenhar as barras.
    for valor in valores:
        indice = min(classes - 1, bisect_right(limites, valor) - 1)
        contagens[indice] += 1
    return Frequencias(limites, contagens)


def resumo_iqr(valores):
    valores = ms._valores(valores)
    q1, mediana, q3 = ms.quartis(valores)
    iqr = q3 - q1
    inferior, superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    internos = [v for v in valores if inferior <= v <= superior]
    return {
        "q1": q1, "mediana": mediana, "q3": q3, "iqr": iqr,
        "inferior": inferior, "superior": superior,
        "bigode_inferior": min(internos), "bigode_superior": max(internos),
        "outliers": [v for v in valores if v < inferior or v > superior],
    }


def densidade_normal(eixo, media, desvio):
    if desvio <= 0:
        raise ValueError("A Normal exige desvio padrão positivo.")
    return [exp(-0.5 * ((x - media) / desvio) ** 2) / (desvio * sqrt(2 * pi)) for x in eixo]


def ajustar_distribuicao(valores, candidata, eixo):
    valores = ms._valores(valores)
    minimo, maximo = min(valores), max(valores)
    if minimo == maximo:
        raise ValueError("O ajuste exige valores não constantes.")
    if candidata == "Normal":
        mu, desvio = ms.media(valores), ms.desvio_padrao_populacional(valores)
        return densidade_normal(eixo, mu, desvio), {"Média (μ)": mu, "Desvio padrão (σ)": desvio}
    if candidata == "Exponencial":
        escala = ms.media([x - minimo for x in valores])
        return [exp(-(x-minimo)/escala)/escala if x >= minimo else 0.0 for x in eixo], {"Localização": minimo, "Escala": escala}
    if candidata == "Uniforme":
        return [1/(maximo-minimo) if minimo <= x <= maximo else 0.0 for x in eixo], {"Mínimo": minimo, "Máximo": maximo}
    raise ValueError("Distribuição desconhecida.")


def simular(valores, repeticoes, tamanho, semente):
    """RNG reproduzível; todas as médias são calculadas pelo núcleo próprio."""
    populacao = ms._valores(valores)
    if repeticoes < 2 or tamanho < 1:
        raise ValueError("Use ao menos duas repetições e amostra não vazia.")
    rng = np.random.default_rng(semente)
    caras = 0
    frequencias = []
    for i, lancamento in enumerate(rng.integers(0, 2, repeticoes), 1):
        caras += int(lancamento)
        frequencias.append(caras / i)
    medias = [ms.media(rng.choice(populacao, tamanho, replace=True)) for _ in range(repeticoes)]
    return frequencias, medias


@dataclass(frozen=True)
class Regressao:
    inclinacao: float
    intercepto: float
    r2: float
    correlacao: float
    rmse: float

    def prever(self, x):
        return self.intercepto + self.inclinacao * x


def analisar_regressao(x, y):
    x, y = ms._pares(x, y)
    inclinacao, intercepto, r2 = ms.regressao_linear(x, y)
    residuos = [real - (intercepto + inclinacao * valor) for valor, real in zip(x, y)]
    return Regressao(inclinacao, intercepto, r2, ms.correlacao_pearson(x, y),
                     sqrt(ms.media([residuo**2 for residuo in residuos])))


def valores_numericos(dataframe, coluna):
    return dataframe[coluna].dropna().astype(float).tolist()


def interpretar_assimetria(valores):
    desvio = ms.desvio_padrao_amostral(valores)
    indice = 3 * (ms.media(valores) - ms.mediana(valores)) / desvio if desvio else 0
    if abs(indice) < 0.1:
        return "com baixo índice de assimetria de Pearson", indice
    return ("assimétrica à direita" if indice > 0 else "assimétrica à esquerda"), indice


def descobertas_calculadas(dados):
    tabela = tabela_categorica(dados["genero_principal"])
    contagem_generos = pd.Series(tabela["Frequência"].tolist(), index=tabela["Categoria"])
    # Os títulos desta descoberta se referem explicitamente a Ação e Comédia.
    percentual_generos = sum(contagem_generos.get(g, 0) for g in ("Action", "Comedy")) / len(dados) * 100
    faixas = ms.frequencias_categoricas(3 <= nota <= 5 for nota in dados["rating"])
    notas_altas = faixas.get(True, 0) / len(dados) * 100
    pares = dados[["ano_filme", "rating"]].dropna()
    relacao = ms.correlacao_pearson(
        pares["ano_filme"].astype(float).tolist(),
        pares["rating"].astype(float).tolist(),
    )
    return contagem_generos, percentual_generos, notas_altas, pares, relacao
