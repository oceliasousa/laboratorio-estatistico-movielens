"""Testes de integração: rotas e estados interativos após a refatoração."""
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

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
    app.run().radio[0].set_value('Categórica').run()
    assert not app.exception
    assert app.dataframe[0].value['Frequência'].sum() == 100836


def test_regressao_mesma_variavel():
    app = AppTest.from_file(APP)
    app.query_params['page'] = 'regressao'
    app.run().selectbox[0].set_value('rating').run()
    assert not app.exception
    assert 'diferentes' in app.error[0].value
