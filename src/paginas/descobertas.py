"""Descobertas do laboratório estatístico."""

import plotly.express as px
import streamlit as st
from src import minhastats as ms
from src.analises import descobertas_calculadas
from src.ui.layout import cabecalho
from src.ui.graficos import estilizar, exibir_grafico


def pagina_descobertas(dados):
    cabecalho(
        "Relatório de",
        "Descobertas",
        "LABESTAT  ›  RELATÓRIO DE DESCOBERTAS",
    )
    generos, percentual, notas_altas, pares, relacao = descobertas_calculadas(dados)
    m1, m2, m3 = st.columns(3)
    m1.metric("Gêneros mais avaliados", "Ação e Comédia", f"{percentual:.1f}%")
    m2.metric("Avaliações entre 3 e 5", f"{notas_altas:.1f}%")
    m3.metric("Relação ano × nota", f"r = {relacao:.3f}")

    with st.container(border=True):
        texto, grafico, evidencias = st.columns([1.25, 1.2, 0.75])
        texto.markdown(
            "## <span class='number-badge'>1</span> Ação e Comédia lideram em volume",
            unsafe_allow_html=True,
        )
        texto.write(
            f"Os dois gêneros representam {percentual:.1f}% das avaliações. "
            "Isso evidencia maior presença desses tipos de filme no conjunto analisado."
        )
        top5 = generos.head(5).sort_values()
        fig = px.bar(
            x=top5.values,
            y=top5.index,
            orientation="h",
            color_discrete_sequence=["#586cff"],
        )
        exibir_grafico(estilizar(fig, 220), container=grafico)
        evidencias.markdown(
            f"### Evidências\n**Total:** {len(dados):,}\n\n"
            f"**Ação + Comédia:** {percentual:.1f}%\n\n"
            f"**Gêneros:** {dados['genero_principal'].nunique()}"
        )

    with st.container(border=True):
        texto, grafico, evidencias = st.columns([1.25, 1.2, 0.75])
        texto.markdown(
            "## <span class='number-badge purple-number'>2</span> "
            "Avaliações se concentram entre 3 e 5",
            unsafe_allow_html=True,
        )
        texto.write(
            f"{notas_altas:.1f}% das avaliações estão na faixa de 3 a 5 estrelas, "
            "indicando predominância de avaliações médias e altas."
        )
        fig = px.histogram(
            dados,
            x="rating",
            nbins=10,
            color_discrete_sequence=["#8a42f4"],
        )
        exibir_grafico(estilizar(fig, 220), container=grafico)
        evidencias.markdown(
            f"### Evidências\n**Média:** {ms.media(dados['rating'].tolist()):.2f}"
            f"\n\n**Mediana:** {ms.mediana(dados['rating'].tolist()):.2f}"
            f"\n\n**Na faixa:** {notas_altas:.1f}%"
        )

    with st.container(border=True):
        texto, grafico, evidencias = st.columns([1.25, 1.2, 0.75])
        texto.markdown(
            "## <span class='number-badge green-number'>3</span> "
            "Ano e nota individual têm relação muito fraca",
            unsafe_allow_html=True,
        )
        texto.write(
            f"A correlação de Pearson é {relacao:.3f}. O ano de lançamento, "
            "isoladamente, explica muito pouco da nota atribuída pelos usuários."
        )
        amostra = pares.sample(min(5000, len(pares)), random_state=42)
        fig = px.scatter(
            amostra,
            render_mode="svg",
            x="ano_filme",
            y="rating",
            opacity=0.38,
            color_discrete_sequence=["#24cbe2"],
        )
        exibir_grafico(estilizar(fig, 220), container=grafico)
        evidencias.markdown(
            f"### Evidências\n**Correlação (r):** {relacao:.3f}\n\n"
            f"**Avaliações válidas:** {len(pares):,}\n\n**Método:** Pearson"
        )
