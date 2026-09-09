"""Regressao do laboratório estatístico."""

import plotly.express as px
import streamlit as st
from src import minhastats as ms
from src.analises import analisar_regressao
from src.dados import NUMERICAS_ANALISE
from src.ui.formatacao import formatar
from src.ui.layout import cabecalho
from src.ui.graficos import estilizar, exibir_grafico


def pagina_regressao(dados):
    cabecalho(
        "Correlação e Regressão",
        "Linear",
        "LABESTAT  ›  CORRELAÇÃO E REGRESSÃO",
    )
    with st.container(border=True):
        c1, c2 = st.columns(2)
        x_nome = c1.selectbox(
            "Variável X (independente)", NUMERICAS_ANALISE, index=1
        )
        y_nome = c2.selectbox(
            "Variável Y (dependente)", NUMERICAS_ANALISE, index=0
        )
    pares = dados[[x_nome, y_nome]].dropna()
    if x_nome == y_nome or pares[x_nome].nunique() < 2 or pares[y_nome].nunique() < 2:
        st.error("Escolha duas variáveis diferentes e não constantes.")
        return
    x = pares[x_nome].astype(float).tolist()
    y = pares[y_nome].astype(float).tolist()
    modelo = analisar_regressao(x, y)
    inclinacao, intercepto, r2 = modelo.inclinacao, modelo.intercepto, modelo.r2
    correlacao, rmse = modelo.correlacao, modelo.rmse
    intensidade = (
        "forte"
        if abs(correlacao) >= 0.7
        else "moderada"
        if abs(correlacao) >= 0.4
        else "fraca"
    )

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Correlação de Pearson", formatar(correlacao, 4))
    m2.metric("Inclinação (b)", formatar(inclinacao, 4))
    m3.metric("Intercepto (a)", formatar(intercepto, 4))
    m4.metric("R²", formatar(r2, 4))
    m5.metric("Erro residual (RMSE)", formatar(rmse, 4))

    principal, lateral = st.columns([1.55, 1])
    with principal:
        with st.container(border=True, key="equal_card_regressao_grafico"):
            st.markdown("### Dispersão e Regressão Linear")
            amostra = pares.sample(min(5000, len(pares)), random_state=42)
            minimo, maximo = min(x), max(x)
            fig = px.scatter(
                amostra,
                render_mode="svg",
                x=x_nome,
                y=y_nome,
                opacity=0.3,
                color_discrete_sequence=["#47a7ff"],
            )
            fig.add_scatter(
                x=[minimo, maximo],
                y=[
                    intercepto + inclinacao * minimo,
                    intercepto + inclinacao * maximo,
                ],
                mode="lines",
                name="Reta de regressão",
                line=dict(color="#9e55ff", width=4),
            )
            exibir_grafico(estilizar(fig, 620))
    with lateral:
        with st.container(key="equal_stack_regressao"):
            with st.container(border=True):
                st.markdown("### Equação da Regressão Linear")
                sinal = "+" if inclinacao >= 0 else "-"
                st.latex(rf"\hat{{y}} = {intercepto:.4f} {sinal} {abs(inclinacao):.4f}x")
                st.caption("Modelo calculado pelo método dos mínimos quadrados.")
            with st.container(border=True):
                st.markdown("### Previsão Interativa")
                entrada = st.number_input(
                    f"Informe um valor para {x_nome}", value=float(ms.media(x))
                )
                st.metric(
                    f"Valor previsto de {y_nome}",
                    formatar(modelo.prever(entrada), 4),
                )
                if entrada < min(x) or entrada > max(x):
                    st.warning("Predição fora da faixa observada em X: extrapolação.")
            with st.container(border=True):
                st.markdown("### Interpretação dos Resultados")
                sentido = "positiva" if correlacao >= 0 else "negativa"
                st.write(
                    f"A associação é {sentido} e {intensidade}. A cada unidade adicional "
                    f"em {x_nome}, o valor previsto de {y_nome} varia {inclinacao:.4f}, "
                    f"em média. O modelo explica {r2 * 100:.2f}% da variação de Y."
                )
                st.caption(f"O intercepto {formatar(intercepto, 4)} é a previsão para X = 0. "
                           "Esse valor pode não ter significado prático se zero estiver fora dos dados. "
                           "A reta usa todos os pares válidos; a dispersão mostra até 5.000 pontos.")
                st.warning(
                    "Correlação não implica causalidade. A associação não comprova que X cause Y."
                )
