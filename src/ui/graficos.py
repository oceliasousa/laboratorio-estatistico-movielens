"""Graficos do laboratório estatístico."""


import streamlit as st
from src.config import CONFIGURACAO_GRAFICOS


def estilizar(figura, altura=300):
    titulo = figura.layout.title.text if figura.layout.title else ""
    titulo = titulo if isinstance(titulo, str) else ""
    figura.update_layout(
        height=altura,
        margin=dict(l=20, r=18, t=42, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(4,14,28,.35)",
        font=dict(color="#a9bad0", size=11),
        title=dict(text=titulo, font=dict(color="#f4f7fb", size=14)),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#0c1c32", font_color="#ffffff"),
        dragmode="zoom",
        uirevision=True,
    )
    if not titulo:
        figura.update_layout(title_text="", margin=dict(l=20, r=18, t=18, b=24))
    figura.update_xaxes(
        gridcolor="rgba(115,148,187,.12)",
        zerolinecolor="rgba(115,148,187,.16)",
    )
    figura.update_yaxes(
        gridcolor="rgba(115,148,187,.12)",
        zerolinecolor="rgba(115,148,187,.16)",
    )
    return figura


def exibir_grafico(figura, *, container=None, config=None):
    """Centraliza configuração e informa ao carregamento quantos gráficos esperar."""
    st.session_state['_graficos_esperados'] = st.session_state.get('_graficos_esperados', 0) + 1
    destino = st if container is None else container
    destino.plotly_chart(figura, config=config or CONFIGURACAO_GRAFICOS)
