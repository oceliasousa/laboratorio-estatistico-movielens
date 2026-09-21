"""Contratos de entrada e validação independente do núcleo próprio."""

import statistics
import numpy as np
import pytest
from scipy import stats
from src import minhastats as ms

TOL = {"rel": 1e-10, "abs": 1e-12}


@pytest.mark.parametrize("dados", [[7], [1, 2, 3], [-5, -4, -3, -1], [8]*6,
                                  np.random.default_rng(5).normal(size=500).tolist()])
def test_referencias_em_varios_conjuntos(dados):
    assert ms.media(dados) == pytest.approx(np.mean(dados), **TOL)
    assert ms.mediana(dados) == pytest.approx(np.median(dados), **TOL)
    assert ms.moda(dados) == sorted(statistics.multimode(dados))
    assert ms.amplitude(dados) == pytest.approx(np.ptp(dados), **TOL)
    assert ms.variancia_populacional(dados) == pytest.approx(np.var(dados), **TOL)
    assert ms.desvio_padrao_populacional(dados) == pytest.approx(np.std(dados), **TOL)
    assert ms.quartis(iter(dados)) == pytest.approx(np.percentile(dados, [25, 50, 75]), **TOL)
    if len(dados) > 1:
        assert ms.variancia_amostral(dados) == pytest.approx(np.var(dados, ddof=1), **TOL)
        assert ms.desvio_padrao_amostral(dados) == pytest.approx(np.std(dados, ddof=1), **TOL)
    if np.mean(dados) != 0:
        assert ms.coeficiente_variacao(iter(dados), amostral=False) == pytest.approx(
            abs(stats.variation(dados)) * 100, **TOL)


@pytest.mark.parametrize("funcao", [ms.media, ms.mediana, ms.moda, ms.amplitude,
    ms.variancia_populacional, ms.variancia_amostral, ms.desvio_padrao_populacional,
    ms.desvio_padrao_amostral, ms.quartis, ms.coeficiente_variacao])
@pytest.mark.parametrize("dados", [[], [1, float('nan')], [1, float('inf')], [float('-inf')]])
def test_recusa_vazios_e_nao_finitos(funcao, dados):
    with pytest.raises(ValueError):
        funcao(dados)


def test_covariancia_populacional_e_amostral():
    x, y = [1, 4, 8, 9], [7, 6, 3, -2]
    for amostral in (False, True):
        assert ms.covariancia(iter(x), iter(y), amostral) == pytest.approx(
            np.cov(x, y, ddof=int(amostral))[0, 1], **TOL)
    assert ms.correlacao_pearson(x, y) == pytest.approx(stats.pearsonr(x, y).statistic, **TOL)


def test_erros_em_pares_e_tipos():
    with pytest.raises(TypeError):
        ms.media([1, '2'])
    with pytest.raises(ValueError):
        ms.covariancia([1, 2], [1])
    with pytest.raises(ValueError):
        ms.coeficiente_variacao([-1, 1])
    for x, y in [([1, 1], [1, 2]), ([1, 2], [3, 3])]:
        with pytest.raises(ValueError):
            ms.regressao_linear(x, y)


def test_regressao_negativa_e_predicao():
    x, y = [1, 2, 5, 8], [8, 6, 0, -6]
    b, a, r2 = ms.regressao_linear(iter(x), iter(y))
    referencia = stats.linregress(x, y)
    assert (b, a, r2) == pytest.approx((referencia.slope, referencia.intercept, referencia.rvalue**2), **TOL)
    assert a + b * 3 == pytest.approx(4)


def test_cv_avisa_cancelamento_sem_confundir_escala_pequena():
    with pytest.warns(RuntimeWarning, match='próxima de zero'):
        assert ms.coeficiente_variacao([-1, 1 + 1e-12]) > 1e12
    # Mudar a unidade de medida não deve tornar o CV instável.
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        assert ms.coeficiente_variacao([1e-14, 2e-14, 3e-14]) == pytest.approx(50)
