"""Distribuicoes do laboratório estatístico."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from src.dados import NUMERICAS_ANALISE
from src.analises import valores_numericos
from src.analises import ajustar_distribuicao, tabela_frequencias
from src.ui.formatacao import formatar
from src.ui.layout import cabecalho
from src.ui.graficos import estilizar, exibir_grafico


def pagina_distribuicoes(dados):
    cabecalho(
        "Distribuições",
        "Teóricas",
        "MÓDULOS  ›  DISTRIBUIÇÕES TEÓRICAS",
    )
    with st.container(border=True):
        c1, c2 = st.columns(2)
        coluna = c1.selectbox("Variável", NUMERICAS_ANALISE)
        candidata = c2.selectbox(
            "Distribuição candidata", ["Normal", "Exponencial", "Uniforme"]
        )
    valores = valores_numericos(dados, coluna)
    histograma = tabela_frequencias(valores, 30)
    frequencias, limites = histograma.densidades, histograma.limites
    centros = histograma.centros
    eixo = np.linspace(min(valores), max(valores), 400)
    curva, parametros = ajustar_distribuicao(valores, candidata, eixo)
    grafico, resumo = st.columns([2.2, 1])
    with grafico:
        with st.container(border=True, key="equal_card_distribuicoes_grafico"):
            st.markdown(f"### Histograma com ajuste da {candidata}")
            fig = go.Figure()
            fig.add_bar(
                x=centros,
                y=frequencias,
                width=np.diff(limites),
                name="Dados observados",
                marker_color="#7248ef",
                opacity=0.82,
            )
            fig.add_scatter(
                x=eixo,
                y=curva,
                mode="lines",
                name=candidata,
                line=dict(color="#3be1d2", width=3),
            )
            fig.update_layout(
                xaxis_title=coluna, yaxis_title="Densidade", bargap=0.03
            )
            exibir_grafico(estilizar(fig, 455))
    with resumo:
        with st.container(key="equal_stack_distribuicoes"):
            with st.container(border=True):
                st.markdown("### Parâmetros estimados")
                for nome, valor in parametros.items():
                    st.metric(nome, formatar(valor, 4))
            with st.container(border=True):
                st.markdown("### Interpretação")
                st.write(
                    "A qualidade do ajuste pode ser observada pela proximidade entre a "
                    "curva e as barras. Diferenças sistemáticas indicam que a candidata "
                    "não descreve completamente os dados."
                )
                if coluna == "rating":
                    leituras = {
                        "Normal": "Nas notas, a Normal acompanha o centro em torno de 3,5, "
                                  "mas não representa os saltos de 0,5 estrela e atribui probabilidade "
                                  "fora da escala de 0,5 a 5. Compare principalmente as extremidades.",
                        "Exponencial": "A Exponencial deslocada atinge o pico na menor nota (0,5) "
                                       "e decresce. Isso contrasta com a concentração observada entre "
                                       "3 e 5 estrelas, indicando uma candidata pouco adequada às notas.",
                        "Uniforme": "A Uniforme atribui a mesma densidade a toda a escala. "
                                    "As barras das notas mostram concentração entre 3 e 5 estrelas, "
                                    "que a curva plana não consegue reproduzir.",
                    }
                    st.info(leituras[candidata])
                st.warning(
                    "A comparação visual é exploratória e não substitui um teste formal de aderência."
                )
                st.caption("As variáveis disponíveis são discretas ou discretizadas. "
                           "Curvas contínuas são aproximações didáticas; não descrevem "
                           "exatamente as notas ou os anos. A Exponencial usa deslocamento "
                           "pelo mínimo observado, não um tempo de espera comprovado.")
