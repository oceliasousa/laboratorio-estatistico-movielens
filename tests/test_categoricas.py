"""Contagens exatas; proporções com tolerância relativa 1e-10 e absoluta 1e-12."""

import statistics

import numpy as np
import pandas as pd
import pytest

from src import minhastats as ms
from src.analises import tabela_categorica


TOL = {"rel": 1e-10, "abs": 1e-12}


@pytest.mark.parametrize(
    "dados",
    [
        ["Action", "Drama", "Action", "Comedy", "Action"],
        ["Drama", "Action", "Drama", "Action", "Comedy"],
        ["terceira", "primeira", "segunda"],
        ["única"],
        ["Ação", "Comédia", "Ação", "日本語", "🎬", "日本語"],
        [None, float("nan"), "Ausente", "Drama", np.float64("nan")],
        [None, None],
        [1, "1", 1, 2.5, "Ação", 2.5],
    ],
)
@pytest.mark.parametrize("usar_iterador", [False, True])
def test_contagens_e_modas_contra_referencias(dados, usar_iterador):
    # A referência adota a mesma convenção documentada: todos os ausentes
    # representam uma categoria, que participa do denominador.
    normalizados = [None if pd.isna(valor) else valor for valor in dados]
    referencia = pd.Series(normalizados, dtype=object).value_counts(dropna=False)
    entrada = iter(dados) if usar_iterador else dados
    contagens = ms.frequencias_categoricas(entrada)
    assert contagens == referencia.to_dict()
    assert sum(contagens.values()) == len(dados)
    assert list(contagens.values()) == sorted(contagens.values(), reverse=True)
    entrada = iter(dados) if usar_iterador else dados
    assert ms.moda_categorica(entrada) == statistics.multimode(normalizados)
    proporcoes = ms.frequencias_relativas(contagens.values())
    referencia_relativa = pd.Series(normalizados, dtype=object).value_counts(
        dropna=False, normalize=True
    ).to_dict()
    assert proporcoes == pytest.approx(
        [referencia_relativa[categoria] for categoria in contagens], **TOL
    )
    assert sum(proporcoes) == pytest.approx(1.0, **TOL)


def test_empates_preservam_primeira_ocorrencia():
    dados = ["z", "b", "a", "b", "a", "z", "restante"]
    assert list(ms.frequencias_categoricas(dados)) == ["z", "b", "a", "restante"]
    assert ms.moda_categorica(dados) == ["z", "b", "a"]


def test_rotulo_literal_ausente_nao_e_confundido_com_ausencia():
    dados = ["Ausente", "Ausente", None, np.nan]
    assert ms.frequencias_categoricas(dados) == {"Ausente": 2, None: 2}
    assert ms.moda_categorica(dados) == ["Ausente", None]


def test_categorias_hashable_nao_precisam_ser_textos():
    dados = [("Ação", 2001), ("Drama", 2002), ("Ação", 2001)]
    assert ms.frequencias_categoricas(dados) == {
        ("Ação", 2001): 2, ("Drama", 2002): 1
    }
    assert ms.moda_categorica(dados) == [("Ação", 2001)]


@pytest.mark.parametrize("funcao", [ms.frequencias_categoricas, ms.moda_categorica])
def test_categoricas_recusam_iterador_vazio(funcao):
    with pytest.raises(ValueError, match="vazia"):
        funcao(iter([]))


@pytest.mark.parametrize("funcao", [ms.frequencias_categoricas, ms.moda_categorica])
@pytest.mark.parametrize("infinito", [float("inf"), float("-inf")])
def test_categoricas_recusam_infinito(funcao, infinito):
    with pytest.raises(ValueError, match="infinitas"):
        funcao(["Ação", infinito])


@pytest.mark.parametrize("funcao", [ms.frequencias_categoricas, ms.moda_categorica])
@pytest.mark.parametrize("categoria", [["lista"], {"chave": "valor"}, {"conjunto"}])
def test_categoricas_recusam_valores_nao_hashable(funcao, categoria):
    with pytest.raises(TypeError, match="hashable"):
        funcao([categoria])


@pytest.mark.parametrize("contagens", [[1], [0, 2, 5, 0, 3], [4, 4, 4], [2, 1000, 7]])
def test_relativas_e_acumuladas_aceitam_iteradores(contagens):
    referencia = np.asarray(contagens, dtype=np.int64)
    assert ms.frequencias_relativas(iter(contagens)) == pytest.approx(
        referencia / referencia.sum(), **TOL
    )
    assert ms.frequencias_acumuladas(iter(contagens)) == np.cumsum(referencia).tolist()
    # Contagens NumPy também são inteiros válidos.
    assert ms.frequencias_acumuladas(referencia) == np.cumsum(referencia).tolist()


@pytest.mark.parametrize("funcao", [ms.frequencias_relativas, ms.frequencias_acumuladas])
@pytest.mark.parametrize(
    "contagens",
    [[], [-1, 2], [1.0, 2], [1, "2"], [None], [float("nan")], [float("inf")]],
)
def test_recusa_contagens_invalidas(funcao, contagens):
    with pytest.raises(ValueError, match="inteiras"):
        funcao(iter(contagens))


def test_total_zero_tem_acumuladas_mas_nao_proporcoes():
    assert ms.frequencias_acumuladas([0, 0, 0]) == [0, 0, 0]
    with pytest.raises(ValueError, match="positivo"):
        ms.frequencias_relativas([0, 0, 0])


@pytest.mark.parametrize(
    "dados",
    [
        ["Ação", "Drama", "Ação", "Drama", "Comédia"],
        ["A", "B", "C"],
        [pd.NA, pd.NaT, None, float("nan"), "Ausente"],
        [pd.NA, pd.NaT, None, float("nan")],
        [
            "Ausente", "Ausente (valor faltante)", "Ausente (valor faltante) *",
            pd.NA, pd.NaT, None, float("nan"),
        ],
    ],
)
def test_tabela_categorica_contra_referencias(dados):
    tabela = tabela_categorica(iter(dados))
    normalizados = [None if pd.isna(valor) else valor for valor in dados]
    referencia = pd.Series(normalizados, dtype=object).value_counts(dropna=False)
    referencia_moda = statistics.multimode(normalizados)
    # Reproduz apenas a regra de apresentação; valores estatísticos esperados
    # vêm das bibliotecas de referência, nunca do núcleo testado.
    rotulo = "Ausente (valor faltante)"
    while rotulo in normalizados:
        rotulo += " *"
    esperadas = {
        rotulo if categoria is None else categoria: quantidade
        for categoria, quantidade in referencia.items()
    }
    assert tabela["Categoria"].is_unique
    assert tabela.set_index("Categoria")["Frequência"].to_dict() == esperadas
    assert tabela["Frequência"].sum() == len(dados)
    assert tabela["Frequência relativa (%)"].tolist() == pytest.approx(
        [100 * esperadas[categoria] / len(dados) for categoria in tabela["Categoria"]],
        **TOL,
    )
    assert tabela["Frequência relativa (%)"].sum() == pytest.approx(100.0, **TOL)
    modas_exibidas = tabela.loc[tabela["Modal"], "Categoria"].tolist()
    assert modas_exibidas == [
        rotulo if categoria is None else categoria for categoria in referencia_moda
    ]


def test_tabela_categorica_recusa_entrada_vazia():
    with pytest.raises(ValueError, match="vazia"):
        tabela_categorica([])
