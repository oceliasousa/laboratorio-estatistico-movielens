"""Dados do laboratório estatístico."""

import pandas as pd
import streamlit as st
from src.dados import CATEGORICAS, NUMERICAS
from src.dados import validar_estrutura
from src.ui.layout import cabecalho


def pagina_dados(dados):
    cabecalho(
        "Gerenciar",
        "Dataset",
        "LABESTAT  ›  GERENCIAR DATASET",
    )
    st.markdown(
        f"""
        <section class="metric-grid dataset-metrics">
          <article><i class="green">▱</i><div><small>Dataset atual</small><strong class="dataset-name">MovieLens Latest Small</strong><span>Fonte: GroupLens</span></div></article>
          <article><i class="green">▱</i><div><small>Registros</small><strong>{len(dados):,}</strong><span>linhas</span></div></article>
          <article><i class="purple">▦</i><div><small>Variáveis</small><strong>{len(dados.columns)}</strong><span>colunas</span></div></article>
          <article><i class="blue">◇</i><div><small>Categóricas</small><strong>{len(CATEGORICAS)}</strong><span>variáveis</span></div></article>
          <article><i class="amber">#</i><div><small>Numéricas</small><strong>{len(NUMERICAS)}</strong><span>variáveis</span></div></article>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.download_button(
        "↓ Exportar amostra CSV",
        dados.head(5000).to_csv(index=False),
        "amostra_movielens.csv",
        width="stretch",
    )
    principal, validacao = st.columns([1.75, 1])
    with principal:
        with st.container(border=True, key="equal_card_dataset_colunas"):
            st.markdown("### Visão geral das colunas")
            catalogo = pd.DataFrame(
                {
                    "#": range(1, len(dados.columns) + 1),
                    "Nome da coluna": dados.columns,
                    "Tipo de dado": [
                        "Numérica" if coluna in NUMERICAS else "Categórica"
                        for coluna in dados.columns
                    ],
                    "Valores ausentes": [
                        int(dados[coluna].isna().sum()) for coluna in dados.columns
                    ],
                    "Valores únicos": [
                        int(dados[coluna].nunique()) for coluna in dados.columns
                    ],
                    "Status": ["Com ausentes" if dados[c].isna().any() else "Completa" for c in dados.columns],
                }
            )
            st.dataframe(
                catalogo, hide_index=True, width="stretch", height=360
            )
    with validacao:
        with st.container(border=True, key="equal_card_dataset_validacao"):
            st.markdown("### Validação do dataset")
            for descricao, passou in validar_estrutura(dados).items():
                (st.success if passou else st.error)(descricao)
    with st.container(border=True):
        st.markdown("### Pré-visualização dos dados")
        st.dataframe(dados.head(10), width="stretch")
    st.info(
        "O MovieLens é disponibilizado pelo GroupLens (University of Minnesota) "
        "para fins educacionais e de pesquisa. IDs são códigos, não grandezas contínuas."
    )
