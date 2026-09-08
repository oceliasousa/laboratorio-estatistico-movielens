import numpy as np
import pytest
from scipy import stats

from src import minhastats as ms


DADOS = [1.2, 2.5, 2.5, 4.1, 8.0, -1.3]
X = [1, 2, 3, 4, 5, 6]
Y = [2.1, 3.9, 6.2, 7.8, 10.1, 12.2]
TOL = {"rel": 1e-10, "abs": 1e-12}


def aprox(valor):
    return pytest.approx(valor, **TOL)


def test_tendencia_central_e_amplitude():
    assert ms.media(DADOS) == aprox(np.mean(DADOS))
    assert ms.mediana(DADOS) == aprox(np.median(DADOS))
    assert ms.moda(DADOS) == [float(stats.mode(DADOS, keepdims=False).mode)]
    assert ms.amplitude(DADOS) == aprox(np.ptp(DADOS))


def test_variancias_e_desvios():
    assert ms.variancia_populacional(DADOS) == aprox(np.var(DADOS, ddof=0))
    assert ms.variancia_amostral(DADOS) == aprox(np.var(DADOS, ddof=1))
    assert ms.desvio_padrao_populacional(DADOS) == aprox(np.std(DADOS, ddof=0))
    assert ms.desvio_padrao_amostral(DADOS) == aprox(np.std(DADOS, ddof=1))


@pytest.mark.parametrize("p", [0, 10, 25, 50, 75, 90, 100])
def test_percentis(p):
    assert ms.percentil(DADOS, p) == aprox(np.percentile(DADOS, p))


def test_quartis_cv_covariancia_correlacao():
    assert ms.quartis(DADOS) == aprox(np.percentile(DADOS, [25, 50, 75]))
    assert ms.coeficiente_variacao(DADOS) == aprox(stats.variation(DADOS, ddof=1) * 100)
    assert ms.covariancia(X, Y) == aprox(np.cov(X, Y, ddof=1)[0, 1])
    assert ms.correlacao_pearson(X, Y) == aprox(np.corrcoef(X, Y)[0, 1])


def test_regressao_linear():
    referencia = stats.linregress(X, Y)
    a, b, r2 = ms.regressao_linear(X, Y)
    assert a == aprox(referencia.slope)
    assert b == aprox(referencia.intercept)
    assert r2 == aprox(referencia.rvalue ** 2)


def test_erros_documentados():
    with pytest.raises(ValueError):
        ms.media([])
    with pytest.raises(ValueError):
        ms.variancia_amostral([1])
    with pytest.raises(ValueError):
        ms.percentil(DADOS, 101)
    with pytest.raises(ValueError):
        ms.correlacao_pearson([1, 1], [2, 3])
