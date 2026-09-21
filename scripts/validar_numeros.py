"""Reproduz a tabela numérica do relatório; bibliotecas só validam resultados."""

from pathlib import Path
import sys
import statistics

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy import stats
from src import minhastats as ms
from src.analises import ajustar_distribuicao, tabela_frequencias


def tabela_validacao():
    dados = [1.2, 2.5, 2.5, 4.1, 8.0, -1.3]
    x, y = [1, 2, 3, 4, 5, 6], [2.1, 3.9, 6.2, 7.8, 10.1, 12.2]
    linhas = ["| Função / resultado | Referência | Maior diferença absoluta | Tolerância |",
              "|---|---|---:|---|"]

    def comparar(nome, fonte, obtido, esperado, exato=False):
        diferencas = np.abs(np.asarray(obtido) - np.asarray(esperado))
        limite = 0 if exato else np.maximum(1e-12, 1e-10 * np.abs(esperado))
        if not np.all(diferencas <= limite):
            raise AssertionError(f"Validação falhou: {nome}")
        erro = float(np.max(diferencas))
        tolerancia = "Exata" if exato else "rel=1e-10; abs=1e-12"
        linhas.append(f"| {nome} | {fonte} | {erro:.3e} | {tolerancia} |")

    for nome, fonte, referencia in [
        ('media', 'NumPy.mean', np.mean(dados)),
        ('mediana', 'NumPy.median', np.median(dados)),
        ('amplitude', 'NumPy.ptp', np.ptp(dados)),
        ('variancia_populacional', 'NumPy.var(ddof=0)', np.var(dados)),
        ('variancia_amostral', 'NumPy.var(ddof=1)', np.var(dados, ddof=1)),
        ('desvio_padrao_populacional', 'NumPy.std(ddof=0)', np.std(dados)),
        ('desvio_padrao_amostral', 'NumPy.std(ddof=1)', np.std(dados, ddof=1)),
        ('coeficiente_variacao', 'SciPy.variation(ddof=1) × 100', stats.variation(dados, ddof=1)*100),
        ('quartis', 'NumPy.percentile(25,50,75)', np.percentile(dados, [25,50,75])),
    ]:
        comparar(nome, fonte, getattr(ms, nome)(dados), referencia)
    comparar('moda', 'statistics.multimode', ms.moda(dados), statistics.multimode(dados), True)
    percentis = [0, 10, 25, 50, 75, 90, 100]
    comparar('percentil', 'NumPy.percentile', [ms.percentil(dados, p) for p in percentis], np.percentile(dados, percentis))
    for amostral in (False, True):
        comparar(f'covariancia (amostral={amostral})', f'NumPy.cov(ddof={int(amostral)})',
                 ms.covariancia(x, y, amostral), np.cov(x, y, ddof=int(amostral))[0,1])
    comparar('correlacao_pearson', 'SciPy.pearsonr', ms.correlacao_pearson(x, y), stats.pearsonr(x, y).statistic)
    b, a, r2 = ms.regressao_linear(x, y)
    referencia = stats.linregress(x, y)
    comparar('regressao_linear: inclinação', 'SciPy.linregress.slope', b, referencia.slope)
    comparar('regressao_linear: intercepto', 'SciPy.linregress.intercept', a, referencia.intercept)
    comparar('regressao_linear: R²', 'SciPy.linregress.rvalue²', r2, referencia.rvalue**2)
    categorias = [1, 2, 2, 3, 3, 3]
    contagens = ms.frequencias_categoricas(categorias)
    comparar('frequencias_categoricas', 'NumPy.unique(return_counts)',
             [contagens[k] for k in sorted(contagens)], np.unique(categorias, return_counts=True)[1], True)
    comparar('moda_categorica', 'statistics.multimode', ms.moda_categorica(categorias), statistics.multimode(categorias), True)
    comparar('frequencias_relativas', 'NumPy: contagens / soma', ms.frequencias_relativas([1,2,3]), np.array([1,2,3])/6)
    comparar('frequencias_acumuladas', 'NumPy.cumsum', ms.frequencias_acumuladas([1,2,3]), np.cumsum([1,2,3]), True)
    hist = tabela_frequencias(dados, 5)
    comparar('tabela_frequencias', 'NumPy.histogram', hist.contagens, np.histogram(dados, bins=hist.limites)[0], True)
    comparar('densidades do histograma', 'NumPy.histogram(density=True)', hist.densidades,
             np.histogram(dados, bins=hist.limites, density=True)[0])
    eixo = np.linspace(-3, 10, 100)
    referencias = {
        'Normal': stats.norm.pdf(eixo, loc=np.mean(dados), scale=np.std(dados)),
        'Exponencial': stats.expon.pdf(eixo, loc=min(dados), scale=np.mean(dados)-min(dados)),
        'Uniforme': stats.uniform.pdf(eixo, loc=min(dados), scale=max(dados)-min(dados)),
    }
    for nome, valores in referencias.items():
        comparar(f'Densidade {nome}', f'SciPy: {nome}', ajustar_distribuicao(dados, nome, eixo)[0], valores)
    return '\n'.join(linhas)


if __name__ == '__main__':
    print(tabela_validacao())
