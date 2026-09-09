"""Inicio do laboratório estatístico."""

import pandas as pd
import plotly.express as px
import streamlit as st
from src import minhastats as ms
from src.dados import CATEGORICAS, NUMERICAS
from src.ui.graficos import estilizar, exibir_grafico


def pagina_inicio(dados):
    st.markdown(
        """
        <section class="home-hero">
          <h1>Laboratório Estatístico <span>Interativo</span></h1>
          <section class="hero-actions">
            <a class="primary" href="?page=descritiva" target="_self">Explorar Módulos&nbsp; →</a>
            <a href="?page=dados" target="_self">▣&nbsp; Ver Dataset</a>
          </section>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <section class="metric-grid">
          <article><i class="green">▱</i><div><small>Registros</small><strong>{len(dados):,}</strong><span>linhas no dataset</span></div></article>
          <article><i class="purple">▦</i><div><small>Variáveis</small><strong>{len(dados.columns)}</strong><span>colunas de dados</span></div></article>
          <article><i class="blue">◇</i><div><small>Categóricas</small><strong>{len(CATEGORICAS)}</strong><span>variáveis categóricas</span></div></article>
          <article><i class="amber">#</i><div><small>Numéricas</small><strong>{len(NUMERICAS)}</strong><span>variáveis numéricas</span></div></article>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="section-heading">
          <div><h2>Módulos do Laboratório</h2><p>Escolha um módulo para começar sua análise.</p></div>
          <a href="?page=descritiva" target="_self">Análise descritiva&nbsp; →</a>
        </div>
        <section class="module-grid">
          <a href="?page=descritiva" target="_self"><i class="blue">▥</i><div><strong>Estatística Descritiva</strong><small>Frequências, medidas centrais, dispersão e detecção de outliers.</small></div><b>›</b></a>
          <a href="?page=simulacoes" target="_self"><i class="purple">⚄</i><div><strong>Probabilidade e Simulação</strong><small>Lei dos Grandes Números e Teorema Central do Limite.</small></div><b>›</b></a>
          <a href="?page=distribuicoes" target="_self"><i class="blue">⌁</i><div><strong>Distribuições Teóricas</strong><small>Comparação com Normal, Exponencial e Uniforme.</small></div><b>›</b></a>
          <a href="?page=regressao" target="_self"><i class="purple">⌁</i><div><strong>Correlação e Regressão</strong><small>Pearson, mínimos quadrados e predição interativa.</small></div><b>›</b></a>
          <a href="?page=descobertas" target="_self"><i class="green">▤</i><div><strong>Relatório de Descobertas</strong><small>Síntese das análises, evidências e conclusões obtidas.</small></div><b>›</b></a>
          <a href="?page=sobre" target="_self"><i class="blue">ⓘ</i><div><strong>Sobre o Projeto</strong><small>Objetivos, dataset, metodologia e referências.</small></div><b>›</b></a>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-heading compact"><div><h2>Visão Geral do Dataset</h2>'
        '<p>Análises rápidas para entender a estrutura dos dados MovieLens.</p></div></div>',
        unsafe_allow_html=True,
    )
    p1, p2, p3 = st.columns(3)
    generos = dados["genero_principal"].value_counts().head(5)
    with p1:
        with st.container(border=True, key="equal_card_home_generos"):
            st.markdown("#### Distribuição entre os 5 gêneros mais avaliados")
            fig = px.pie(
                values=generos.values,
                names=generos.index,
                hole=0.58,
                color_discrete_sequence=["#4f6dff", "#28c7dd", "#19d3ae", "#ff865e", "#d54bd1"],
            )
            fig.update_traces(
                textinfo="none", marker=dict(line=dict(color="#081526", width=2))
            )
            exibir_grafico(estilizar(fig, 270))
    with p2:
        with st.container(border=True, key="equal_card_home_avaliacoes"):
            st.markdown("#### Distribuição das avaliações")
            fig = px.histogram(
                dados,
                x="rating",
                nbins=10,
                color_discrete_sequence=["#7c3aed"],
                labels={"rating": "Avaliação"},
            )
            exibir_grafico(estilizar(fig, 270))
    with p3:
        with st.container(border=True, key="equal_card_home_medias"):
            st.markdown("#### Avaliação média por gênero")
            medias = pd.DataFrame(
                {
                    "Gênero": list(generos.index),
                    "Média": [
                        ms.media(
                            dados.loc[
                                dados["genero_principal"] == genero, "rating"
                            ].tolist()
                        )
                        for genero in generos.index
                    ],
                }
            ).sort_values("Média")
            fig = px.bar(
                medias,
                x="Média",
                y="Gênero",
                orientation="h",
                text_auto=".2f",
                color="Gênero",
                color_discrete_sequence=["#ff5f75", "#ff9f43", "#8b5cf6", "#23c8d9", "#3498ff"],
            )
            fig.update_layout(showlegend=False)
            exibir_grafico(estilizar(fig, 270))
