"""Testes de integração: rotas e estados interativos após a refatoração."""
from pathlib import Path
import json
from unittest.mock import patch
import pytest
from streamlit.testing.v1 import AppTest
from src import minhastats as ms

APP = Path(__file__).resolve().parents[1] / 'app.py'


@pytest.mark.parametrize('pagina', ['inicio', 'descritiva', 'simulacoes', 'distribuicoes',
                                   'regressao', 'descobertas', 'dados', 'sobre', 'inexistente'])
def test_paginas(pagina):
    app = AppTest.from_file(APP)
    app.query_params['page'] = pagina
    app.run(timeout=45)
    assert not app.exception
    assert not app.error


def test_descritiva_categorica():
    app = AppTest.from_file(APP)
    app.query_params['page'] = 'descritiva'
    app.run()
    with patch.object(ms, 'frequencias_categoricas', wraps=ms.frequencias_categoricas) as contagem, \
         patch.object(ms, 'moda_categorica', wraps=ms.moda_categorica) as moda:
        app.radio[0].set_value('Categórica').run()
        assert contagem.called
        assert moda.called
    assert not app.exception
    assert app.dataframe[0].value['Frequência'].sum() == 100836
    assert 'Action' in app.success[0].value
    assert app.dataframe[0].value['Frequência relativa (%)'].sum() == pytest.approx(100)


def _tela_categorica(valores):
    import pandas as pd
    from src.dados import CATEGORICAS, NUMERICAS_ANALISE
    from src.paginas.descritiva import pagina_descritiva

    dados = pd.DataFrame({coluna: valores for coluna in CATEGORICAS})
    for coluna in NUMERICAS_ANALISE:
        dados[coluna] = range(1, len(valores) + 1)
    pagina_descritiva(dados)


@pytest.mark.parametrize('valores,modais,mensagem', [
    (['A', 'B', 'A', 'B', 'C'], {'A', 'B'}, '2 categorias modais'),
    (['A', 'B', 'C'], {'A', 'B', 'C'}, 'mesma frequência'),
    ([None, None, 'Ausente', 'A'], {'Ausente (valor faltante)'}, 'Categoria modal'),
])
def test_tela_categorica_empates_e_ausentes(valores, modais, mensagem):
    app = AppTest.from_function(_tela_categorica, args=(valores,))
    app.run().radio[0].set_value('Categórica').run()
    assert not app.exception
    tabela = app.dataframe[0].value
    assert set(tabela.loc[tabela['Modal'], 'Categoria']) == modais
    assert tabela['Frequência'].sum() == len(valores)
    assert tabela['Frequência relativa (%)'].sum() == pytest.approx(100)
    assert any(mensagem in aviso.value for aviso in [*app.info, *app.success])


@pytest.mark.parametrize('pagina', ['inicio', 'descritiva', 'descobertas', 'simulacoes', 'distribuicoes'])
def test_graficos_recebem_contagens_sem_agregadores_prontos(pagina):
    # Falha se uma tela voltar a delegar contagens ao Pandas ou ao Plotly.
    import pandas as pd
    import plotly.express as px

    app = AppTest.from_file(APP)
    app.query_params['page'] = pagina
    with patch.object(pd.Series, 'value_counts', side_effect=AssertionError('Use o núcleo próprio')), \
         patch.object(px, 'histogram', side_effect=AssertionError('Envie contagens próprias')):
        app.run(timeout=45)
    assert not app.exception
    assert not app.error
    graficos = app.get('plotly_chart')
    assert graficos
    for grafico in graficos:
        assert all(serie['type'] != 'histogram' for serie in json.loads(grafico.proto.spec)['data'])
    if pagina in ('inicio', 'descobertas'):
        from src.analises import tabela_frequencias
        from src.dados import carregar_dados

        barras = json.loads(graficos[1].proto.spec)['data'][0]
        assert barras['y'] == tabela_frequencias(carregar_dados()['rating'], 10).contagens
        assert sum(barras['y']) == 100836


def test_regressao_mesma_variavel():
    app = AppTest.from_file(APP)
    app.query_params['page'] = 'regressao'
    app.run().selectbox[0].set_value('rating').run()
    assert not app.exception
    assert 'diferentes' in app.error[0].value


def test_descritiva_sturges_e_tcl_amostra_pequena():
    app = AppTest.from_file(APP)
    app.query_params['page'] = 'descritiva'
    app.run(timeout=45)
    assert app.slider[0].value == 18
    assert len(app.dataframe[-1].value) == 18
    assert app.dataframe[-1].value['Frequência'].sum() == 100836
    app.query_params['page'] = 'simulacoes'
    app.run(timeout=45).slider[1].set_value(2).run(timeout=45)
    assert not app.error
    assert not app.exception
