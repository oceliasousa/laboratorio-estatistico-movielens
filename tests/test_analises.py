import numpy as np
import pytest
from scipy import stats
from src.analises import tabela_frequencias, resumo_iqr, ajustar_distribuicao, simular
from src.dados import carregar_dados, preparar_dados, validar_estrutura
from src import minhastats as ms


@pytest.mark.parametrize("valores", [[0, 1, 2, 3, 4], [1]*10, [0.5, 1, 2.5, 5]*10])
def test_histograma_e_densidade(valores):
    tabela = tabela_frequencias(valores, 5)
    referencia, _ = np.histogram(valores, bins=tabela.limites)
    assert tabela.contagens == referencia.tolist()
    assert sum(tabela.contagens) == len(valores)
    assert sum(d*l for d, l in zip(tabela.densidades, tabela.larguras)) == pytest.approx(1)


def test_iqr_compartilhado_com_boxplot():
    valores = [1, 2, 3, 4, 5, 6, 100]
    resumo = resumo_iqr(valores)
    assert (resumo['q1'], resumo['mediana'], resumo['q3']) == pytest.approx(np.percentile(valores, [25, 50, 75]))
    assert resumo['outliers'] == [100]
    assert resumo['bigode_superior'] == 6


@pytest.mark.parametrize("nome", ['Normal', 'Exponencial', 'Uniforme'])
def test_densidades_proprias(nome):
    valores = [1, 2, 4, 8]
    eixo = np.linspace(-1, 10, 100)
    curva, _ = ajustar_distribuicao(valores, nome, eixo)
    referencias = {
        'Normal': stats.norm.pdf(eixo, np.mean(valores), np.std(valores)),
        'Exponencial': stats.expon.pdf(eixo, loc=1, scale=np.mean(valores)-1),
        'Uniforme': stats.uniform.pdf(eixo, loc=1, scale=7),
    }
    assert curva == pytest.approx(referencias[nome], rel=1e-10, abs=1e-12)


def test_simulacao_reproduzivel():
    args = ([0, 1, 2, 3], 1500, 30, 42)
    frequencias, medias = simular(*args)
    assert (frequencias, medias) == simular(*args)
    assert len(medias) == 1500
    assert abs(frequencias[-1] - 0.5) < 0.05
    assert abs(ms.media(medias) - 1.5) < 0.05
    assert all(0 <= f <= 1 for f in frequencias)


def test_dataset_real_e_validacao():
    dados = carregar_dados()
    assert dados.shape == (100836, 11)
    assert dados.movieId.nunique() == 9724
    assert dados.ano_filme.isna().sum() == 18
    assert dados.loc[dados.genres == '(no genres listed)', 'quantidade_generos'].eq(0).all()
    assert dados.quantidade_generos.eq(0).sum() == 47
    assert all(validar_estrutura(dados).values())
    assert not all(validar_estrutura(dados.head(3)).values())
    assert not validar_estrutura(dados.drop(columns='ano_filme'))['Pelo menos 4 variáveis numéricas de análise']
    assert ms.correlacao_pearson(dados.dropna().ano_filme, dados.dropna().rating) == pytest.approx(-0.084, abs=0.0001)


def test_merge_recusa_perda_de_avaliacoes():
    dados = carregar_dados().head(3)
    with pytest.raises(ValueError, match='ausentes no catálogo'):
        preparar_dados(dados[['userId', 'movieId', 'rating', 'timestamp']],
                       dados[['movieId', 'title', 'genres']].iloc[:1])
