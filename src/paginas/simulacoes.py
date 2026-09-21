"""Simulacoes do laboratório estatístico."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src import minhastats as ms
from src.dados import NUMERICAS_ANALISE
from src.analises import valores_numericos
from src.analises import simular, densidade_normal, tabela_frequencias
from src.ui.formatacao import formatar
from src.ui.layout import cabecalho
from src.ui.graficos import estilizar, exibir_grafico

simular_cache = st.cache_data(show_spinner=False, max_entries=8)(simular)


def pagina_simulacoes(dados):
    cabecalho(
        "Probabilidade, Simulação e",
        "Distribuições",
        "PROBABILIDADE E SIMULAÇÃO",
    )
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        repeticoes = c1.slider("Número de repetições", 1000, 50000, 5000, 1000)
        tamanho = c2.slider("Tamanho da amostra (n)", 2, 300, 30)
        coluna = c3.selectbox("Variável para o TCL", NUMERICAS_ANALISE)
        semente = c4.number_input(
            "Semente", min_value=0, max_value=99999, value=123
        )

    populacao = valores_numericos(dados, coluna)
    acumulada, medias = simular_cache(populacao, repeticoes, tamanho, int(semente))
    passo = max(1, repeticoes // 2500)
    p1, p2 = st.columns(2)
    with p1:
        with st.container(border=True, key="equal_card_simulacao_lgn"):
            st.markdown("### Lei dos Grandes Números")
            st.caption("A frequência relativa converge para a probabilidade teórica.")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=np.arange(1, repeticoes + 1)[::passo],
                    y=acumulada[::passo],
                    name="Frequência de caras",
                    line=dict(color="#20cee2", width=2),
                )
            )
            fig.add_hline(
                y=0.5,
                line_dash="dash",
                line_color="#9a4dff",
                annotation_text="p = 0,5",
            )
            fig.update_layout(
                title="Convergência da frequência relativa",
                xaxis_title="Lançamentos",
                yaxis_title="Frequência acumulada",
            )
            exibir_grafico(estilizar(fig, 330))
    with p2:
        with st.container(border=True, key="equal_card_simulacao_tcl"):
            st.markdown("### Teorema Central do Limite")
            st.caption("Médias amostrais com referência Normal de média μ e desvio σ/√n.")
            mu = ms.media(populacao)
            sigma = ms.desvio_padrao_populacional(populacao) / tamanho ** 0.5
            classes = tabela_frequencias(medias, 40)
            fig = go.Figure(go.Bar(x=classes.centros, y=classes.densidades,
                                  width=classes.larguras, marker_color="#7656ff",
                                  name="Médias amostrais"))
            fig.update_layout(xaxis_title="Média amostral", yaxis_title="Densidade", bargap=0.03)
            eixo = np.linspace(min(medias), max(medias), 300)
            fig.add_scatter(
                x=eixo,
                y=densidade_normal(eixo, mu, sigma),
                mode="lines",
                name="Normal teórica do TCL",
                line=dict(color="#38e8d1", width=3),
            )
            exibir_grafico(estilizar(fig, 330))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Frequência final de caras", formatar(acumulada[-1], 4))
    m2.metric("Erro absoluto", formatar(abs(acumulada[-1] - 0.5), 4))
    m3.metric("Média das médias", formatar(ms.media(medias), 4))
    m4.metric("Desvio das médias", formatar(ms.desvio_padrao_amostral(medias), 4))
    st.info(
        "A Lei dos Grandes Números mostra a convergência da frequência para 0,5. "
        "No TCL, a distribuição das médias amostrais se aproxima de uma Normal "
        "conforme o tamanho da amostra cresce. Compare n = 2, 30 e 100 para ano_filme: "
        "as médias suavizam a assimetria presente na distribuição dos anos."
    )
