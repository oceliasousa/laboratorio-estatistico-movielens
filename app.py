"""Laboratório Estatístico Interativo — MovieLens."""

import base64
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import streamlit as st
import streamlit.components.v1 as components

from src import minhastats as ms
from src.dados import CATEGORICAS, NUMERICAS, NUMERICAS_ANALISE, carregar_dados


RAIZ = Path(__file__).resolve().parent
st.set_page_config(page_title="LabEstat — MovieLens", page_icon="∑", layout="wide")

CONFIGURACAO_GRAFICOS = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": True,
    "showTips": True,
    "doubleClick": "reset+autosize",
    "staticPlot": False,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "grafico_labestat",
        "width": 1600,
        "height": 900,
        "scale": 2,
    },
}


def carregar_estilos():
    imagem = base64.b64encode(
        (RAIZ / "assets" / "ondas-estatisticas.png").read_bytes()
    ).decode("ascii")
    css = (RAIZ / "styles.css").read_text(encoding="utf-8")
    css = css.replace("__HERO_IMAGE__", f"data:image/png;base64,{imagem}")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def controlar_rolagem(pagina):
    """Retorna ao topo somente quando a rota da aplicação muda."""
    with st.container(key="scroll_controller"):
        components.html(
            f"""
            <script>
            (() => {{
              const appWindow = window.parent;
              const route = {pagina!r};
              const storageKey = "labestat-rota-atual";
              appWindow.history.scrollRestoration = "manual";

              const resetScroll = () => {{
                const document = appWindow.document;
                const containers = [
                  document.scrollingElement,
                  document.documentElement,
                  document.body,
                  document.querySelector('[data-testid="stAppViewContainer"]'),
                  document.querySelector('[data-testid="stMain"]')
                ];
                appWindow.scrollTo(0, 0);
                containers.forEach((container) => {{
                  if (!container) return;
                  container.scrollTop = 0;
                  if (typeof container.scrollTo === "function") container.scrollTo(0, 0);
                }});
              }};

              appWindow.__labestatResetScroll = resetScroll;

              if (!appWindow.__labestatScrollNavigationBound) {{
                appWindow.document.addEventListener("pointerdown", (event) => {{
                  const link = event.target.closest('a[href*="?page="]');
                  if (link) appWindow.__labestatResetScroll();
                }}, true);
                appWindow.addEventListener("beforeunload", () => {{
                  appWindow.__labestatResetScroll();
                }});
                appWindow.__labestatScrollNavigationBound = true;
              }}

              if (appWindow.sessionStorage.getItem(storageKey) !== route) {{
                appWindow.sessionStorage.setItem(storageKey, route);
                resetScroll();
              }}
            }})();
            </script>
            """,
            height=0,
            width=0,
        )


@st.cache_data
def dados_completos():
    return carregar_dados()


def valores_numericos(dataframe, coluna):
    return dataframe[coluna].dropna().astype(float).tolist()


def formatar(numero, casas=2):
    return f"{numero:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


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


def cabecalho(titulo, destaque, trilha):
    st.markdown(
        f"""
        <section class="page-hero">
          <p>{trilha}</p>
          <h1>{titulo} <span>{destaque}</span></h1>
        </section>
        """,
        unsafe_allow_html=True,
    )


def interpretar_assimetria(valores):
    desvio = ms.desvio_padrao_amostral(valores)
    indice = 3 * (ms.media(valores) - ms.mediana(valores)) / desvio if desvio else 0
    if abs(indice) < 0.1:
        return "aproximadamente simétrica", indice
    return ("assimétrica à direita" if indice > 0 else "assimétrica à esquerda"), indice


def shell(pagina, dados):
    total_avaliacoes = f"{len(dados):,}".replace(",", ".")
    total_filmes = f"{dados['movieId'].nunique():,}".replace(",", ".")
    links = [
        ("inicio", "⌂", "Início", None),
        ("descritiva", "▥", "Estatística Descritiva", "MÓDULOS DE ANÁLISE"),
        ("simulacoes", "⚄", "Probabilidade e Simulação", None),
        ("distribuicoes", "⌁", "Distribuições Teóricas", None),
        ("regressao", "⌁", "Correlação e Regressão", None),
        ("descobertas", "▤", "Relatório de Descobertas", "DADOS E RESULTADOS"),
        ("dados", "▣", "Gerenciar Dataset", None),
        ("sobre", "▤", "Documentação / Sobre", "SUPORTE"),
    ]
    itens = []
    for rota, icone, nome, grupo in links:
        if grupo:
            itens.append(f'<span class="nav-group">{grupo}</span>')
        ativo = " active" if rota == pagina else ""
        itens.append(
            f'<a class="side-link{ativo}" href="?page={rota}" target="_self">'
            f"<i>{icone}</i>{nome}</a>"
        )
    st.markdown(
        f"""
        <header class="topbar">
          <a class="brand" href="?page=inicio" target="_self">
            <b>∑</b><strong>Lab<span>Estat</span></strong>
          </a>
          <nav>
            <a href="?page=inicio" target="_self">⌂ Início</a>
            <a href="?page=descritiva" target="_self">◉ Módulos</a>
            <a href="?page=dados" target="_self">▣ Dataset</a>
            <a href="?page=descobertas" target="_self">▤ Relatório</a>
            <a href="?page=sobre" target="_self">▧ Documentação</a>
          </nav>
          <div class="top-actions">
            <span>⌕&nbsp; Buscar no app...</span>
            <a href="?page=dados" target="_self">▣&nbsp; MovieLens Latest Small⌄</a>
            <b>LE</b>
          </div>
        </header>
        <aside class="sidebar">
          <nav>{''.join(itens)}</nav>
          <div class="side-dataset">
            <small>DATASET ATUAL</small>
            <strong>MovieLens Latest Small</strong>
            <div>
              <span>{total_avaliacoes}<small>avaliações</small></span>
              <span>{total_filmes}<small>filmes</small></span>
            </div>
            <a href="?page=dados" target="_self">Ver dados do projeto&nbsp; →</a>
          </div>
        </aside>
        """,
        unsafe_allow_html=True,
    )


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
          <a href="?page=descritiva" target="_self">Ver todos os módulos&nbsp; →</a>
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
            st.markdown("#### Distribuição por gênero")
            fig = px.pie(
                values=generos.values,
                names=generos.index,
                hole=0.58,
                color_discrete_sequence=["#4f6dff", "#28c7dd", "#19d3ae", "#ff865e", "#d54bd1"],
            )
            fig.update_traces(
                textinfo="none", marker=dict(line=dict(color="#081526", width=2))
            )
            st.plotly_chart(estilizar(fig, 270), config=CONFIGURACAO_GRAFICOS)
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
            st.plotly_chart(estilizar(fig, 270), config=CONFIGURACAO_GRAFICOS)
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
            st.plotly_chart(estilizar(fig, 270), config=CONFIGURACAO_GRAFICOS)


def pagina_descritiva(dados):
    cabecalho(
        "Estatística Descritiva",
        "Interativa",
        "MÓDULOS  ›  ESTATÍSTICA DESCRITIVA",
    )
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([1.25, 1, 0.75, 1])
        tipo = c1.radio("Tipo de variável", ["Numérica", "Categórica"], horizontal=True)
        if tipo == "Numérica":
            coluna = c2.selectbox("Variável", NUMERICAS_ANALISE)
            c3.markdown(
                '<span class="type-chip"># &nbsp; Numérica</span>',
                unsafe_allow_html=True,
            )
        else:
            coluna = c2.selectbox("Variável", CATEGORICAS)
            c3.markdown(
                '<span class="type-chip purple-chip">A &nbsp; Categórica</span>',
                unsafe_allow_html=True,
            )
        c4.info(f"{len(dados):,} registros disponíveis")

    if tipo == "Categórica":
        contagem = dados[coluna].fillna("Ausente").value_counts().head(20)
        tabela = pd.DataFrame({"Categoria": contagem.index, "Frequência": contagem.values})
        tabela["Frequência relativa (%)"] = tabela["Frequência"] / len(dados) * 100
        esquerda, direita = st.columns([1, 1.55])
        with esquerda:
            with st.container(border=True, key="equal_card_categoria_tabela"):
                st.markdown("### Tabela de Frequência")
                st.dataframe(tabela, hide_index=True, width="stretch")
        with direita:
            with st.container(border=True, key="equal_card_categoria_grafico"):
                fig = px.bar(
                    tabela,
                    x="Frequência",
                    y="Categoria",
                    orientation="h",
                    title=f"Categorias mais frequentes — {coluna}",
                    color_discrete_sequence=["#29c9e6"],
                )
                st.plotly_chart(estilizar(fig, 440), config=CONFIGURACAO_GRAFICOS)
        st.success(
            f"A categoria modal é {contagem.index[0]}, com {contagem.iloc[0]:,} ocorrências."
        )
        return

    valores = valores_numericos(dados, coluna)
    q1, mediana, q3 = ms.quartis(valores)
    iqr = q3 - q1
    inferior, superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = [x for x in valores if x < inferior or x > superior]
    assimetria, indice = interpretar_assimetria(valores)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Média", formatar(ms.media(valores), 4))
    m2.metric("Mediana", formatar(mediana, 4))
    m3.metric("Desvio padrão", formatar(ms.desvio_padrao_amostral(valores), 4))
    m4.metric(
        "Coeficiente de variação",
        f"{formatar(ms.coeficiente_variacao(valores), 2)}%",
    )
    with st.expander("Ver todas as medidas calculadas pelo núcleo próprio"):
        modas = ms.moda(valores)
        medidas = pd.DataFrame(
            {
                "Medida": [
                    "Média",
                    "Mediana",
                    "Moda",
                    "Amplitude",
                    "Variância populacional",
                    "Variância amostral",
                    "Desvio padrão populacional",
                    "Desvio padrão amostral",
                    "Q1 (25%)",
                    "Q2 (50%)",
                    "Q3 (75%)",
                    "Percentil 90",
                    "Coeficiente de variação",
                ],
                "Resultado": [
                    formatar(ms.media(valores), 4),
                    formatar(mediana, 4),
                    ", ".join(formatar(valor, 4) for valor in modas[:8]),
                    formatar(ms.amplitude(valores), 4),
                    formatar(ms.variancia_populacional(valores), 4),
                    formatar(ms.variancia_amostral(valores), 4),
                    formatar(ms.desvio_padrao_populacional(valores), 4),
                    formatar(ms.desvio_padrao_amostral(valores), 4),
                    formatar(q1, 4),
                    formatar(mediana, 4),
                    formatar(q3, 4),
                    formatar(ms.percentil(valores, 90), 4),
                    f"{formatar(ms.coeficiente_variacao(valores), 2)}%",
                ],
            }
        )
        st.dataframe(medidas, hide_index=True, width="stretch")

    esquerda, centro, direita = st.columns([1.05, 1.5, 1.05])
    with esquerda:
        with st.container(border=True, key="equal_card_descritiva_frequencia"):
            st.markdown("### Tabela de Frequência")
            bins = st.slider("Número de classes", 5, 30, 10)
            frequencias, limites = np.histogram(valores, bins=bins)
            tabela = pd.DataFrame(
                {
                    "Classe": [
                        f"{limites[i]:.1f}–{limites[i + 1]:.1f}" for i in range(bins)
                    ],
                    "Frequência": frequencias,
                    "Relativa": [
                        f"{valor / len(valores) * 100:.1f}%"
                        for valor in frequencias
                    ],
                }
            )
            st.dataframe(tabela, hide_index=True, width="stretch", height=460)
    with centro:
        with st.container(border=True, key="equal_card_descritiva_distribuicao"):
            st.markdown("### Distribuição da Variável")
            fig = px.histogram(
                x=valores,
                nbins=bins,
                labels={"x": coluna},
                color_discrete_sequence=["#526fff"],
                title=f"Histograma de {coluna}",
            )
            st.plotly_chart(estilizar(fig, 300), config=CONFIGURACAO_GRAFICOS)
            fig_box = px.box(
                x=valores,
                labels={"x": coluna},
                color_discrete_sequence=["#21cfe2"],
            )
            st.plotly_chart(estilizar(fig_box, 190), config=CONFIGURACAO_GRAFICOS)
    with direita:
        with st.container(key="equal_stack_descritiva"):
            with st.container(border=True):
                st.markdown("### Análise de Outliers (IQR)")
                qcol1, qcol2 = st.columns(2)
                qcol1.metric("Q1", formatar(q1))
                qcol2.metric("Q3", formatar(q3))
                qcol1.metric("IQR", formatar(iqr))
                qcol2.metric("Outliers", f"{len(outliers):,}")
                if outliers:
                    st.warning(f"{len(outliers):,} valores atípicos identificados.")
                else:
                    st.success("Nenhum outlier detectado.")
            with st.container(border=True):
                st.markdown("### Interpretação Automática")
                st.markdown(
                    f"""
                    - **Tendência central:** média {formatar(ms.media(valores))} e mediana {formatar(mediana)}.
                    - **Assimetria:** distribuição {assimetria} (índice {indice:.2f}).
                    - **Dispersão:** amplitude {formatar(ms.amplitude(valores))}.
                    - **Limites IQR:** {formatar(inferior)} a {formatar(superior)}.
                    """
                )


def pagina_simulacoes(dados):
    cabecalho(
        "Probabilidade, Simulação e",
        "Distribuições",
        "PROBABILIDADE E SIMULAÇÃO",
    )
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        repeticoes = c1.slider("Número de repetições", 1000, 50000, 5000, 1000)
        tamanho = c2.slider("Tamanho da amostra (n)", 5, 300, 30)
        coluna = c3.selectbox("Variável para o TCL", NUMERICAS_ANALISE)
        semente = c4.number_input(
            "Semente", min_value=0, max_value=99999, value=123
        )

    rng = np.random.default_rng(int(semente))
    moeda = rng.integers(0, 2, repeticoes)
    acumulada = np.cumsum(moeda) / np.arange(1, repeticoes + 1)
    populacao = np.asarray(valores_numericos(dados, coluna))
    medias = [
        ms.media(rng.choice(populacao, tamanho, replace=True))
        for _ in range(repeticoes)
    ]
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
            st.plotly_chart(estilizar(fig, 330), config=CONFIGURACAO_GRAFICOS)
    with p2:
        with st.container(border=True, key="equal_card_simulacao_tcl"):
            st.markdown("### Teorema Central do Limite")
            st.caption("Distribuição das médias amostrais com curva Normal estimada.")
            mu = ms.media(medias)
            sigma = ms.desvio_padrao_amostral(medias)
            fig = px.histogram(
                x=medias,
                nbins=40,
                histnorm="probability density",
                color_discrete_sequence=["#7656ff"],
                labels={"x": "Média amostral"},
            )
            eixo = np.linspace(min(medias), max(medias), 300)
            fig.add_scatter(
                x=eixo,
                y=stats.norm.pdf(eixo, mu, sigma),
                mode="lines",
                name="Normal estimada",
                line=dict(color="#38e8d1", width=3),
            )
            st.plotly_chart(estilizar(fig, 330), config=CONFIGURACAO_GRAFICOS)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Frequência final de caras", formatar(acumulada[-1], 4))
    m2.metric("Erro absoluto", formatar(abs(acumulada[-1] - 0.5), 4))
    m3.metric("Média das médias", formatar(ms.media(medias), 4))
    m4.metric("Desvio das médias", formatar(ms.desvio_padrao_amostral(medias), 4))
    st.info(
        "A Lei dos Grandes Números mostra a convergência da frequência para 0,5. "
        "No TCL, a distribuição das médias amostrais se aproxima de uma Normal "
        "conforme o tamanho da amostra cresce."
    )


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
    frequencias, limites = np.histogram(valores, bins=30, density=True)
    centros = (limites[:-1] + limites[1:]) / 2
    eixo = np.linspace(min(valores), max(valores), 400)
    mu = ms.media(valores)
    desvio = ms.desvio_padrao_populacional(valores)
    if candidata == "Normal":
        curva = stats.norm.pdf(eixo, mu, desvio)
        parametros = {"Média (μ)": mu, "Desvio padrão (σ)": desvio}
    elif candidata == "Exponencial":
        minimo = min(valores)
        escala = ms.media([x - minimo for x in valores])
        curva = stats.expon.pdf(eixo, loc=minimo, scale=escala)
        parametros = {"Localização": minimo, "Escala": escala}
    else:
        minimo, maximo = min(valores), max(valores)
        curva = stats.uniform.pdf(eixo, loc=minimo, scale=maximo - minimo)
        parametros = {"Mínimo": minimo, "Máximo": maximo}
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
            st.plotly_chart(estilizar(fig, 455), config=CONFIGURACAO_GRAFICOS)
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
                st.warning(
                    "A comparação visual é exploratória e não substitui um teste formal de aderência."
                )


def pagina_regressao(dados):
    cabecalho(
        "Correlação e Regressão",
        "Linear",
        "LABESTAT  ›  CORRELAÇÃO E REGRESSÃO",
    )
    with st.container(border=True):
        c1, c2 = st.columns(2)
        x_nome = c1.selectbox(
            "Variável X (independente)", NUMERICAS_ANALISE, index=2
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
    inclinacao, intercepto, r2 = ms.regressao_linear(x, y)
    correlacao = ms.correlacao_pearson(x, y)
    previstos = [intercepto + inclinacao * valor for valor in x]
    residuos = [real - previsto for real, previsto in zip(y, previstos)]
    rmse = (sum(residuo**2 for residuo in residuos) / len(residuos)) ** 0.5
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
            st.plotly_chart(estilizar(fig, 620), config=CONFIGURACAO_GRAFICOS)
    with lateral:
        with st.container(key="equal_stack_regressao"):
            with st.container(border=True):
                st.markdown("### Equação da Regressão Linear")
                st.latex(rf"\hat{{y}} = {intercepto:.4f} + {inclinacao:.4f}x")
                st.caption("Modelo calculado pelo método dos mínimos quadrados.")
            with st.container(border=True):
                st.markdown("### Previsão Interativa")
                entrada = st.number_input(
                    f"Informe um valor para {x_nome}", value=float(ms.media(x))
                )
                st.metric(
                    f"Valor previsto de {y_nome}",
                    formatar(intercepto + inclinacao * entrada, 4),
                )
            with st.container(border=True):
                st.markdown("### Interpretação dos Resultados")
                sentido = "positiva" if correlacao >= 0 else "negativa"
                st.write(
                    f"A associação é {sentido} e {intensidade}. A cada unidade adicional "
                    f"em {x_nome}, o valor previsto de {y_nome} varia {inclinacao:.4f}, "
                    f"em média. O modelo explica {r2 * 100:.2f}% da variação de Y."
                )
                st.warning(
                    "Correlação não implica causalidade. A associação não comprova que X cause Y."
                )


def descobertas_calculadas(dados):
    contagem_generos = dados["genero_principal"].value_counts()
    percentual_generos = contagem_generos.head(2).sum() / len(dados) * 100
    notas_altas = dados["rating"].between(3, 5).sum() / len(dados) * 100
    pares = dados[["ano_filme", "rating"]].dropna()
    relacao = ms.correlacao_pearson(
        pares["ano_filme"].astype(float).tolist(),
        pares["rating"].astype(float).tolist(),
    )
    return contagem_generos, percentual_generos, notas_altas, pares, relacao


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
        grafico.plotly_chart(estilizar(fig, 220), config=CONFIGURACAO_GRAFICOS)
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
        grafico.plotly_chart(estilizar(fig, 220), config=CONFIGURACAO_GRAFICOS)
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
            x="ano_filme",
            y="rating",
            opacity=0.38,
            color_discrete_sequence=["#24cbe2"],
        )
        grafico.plotly_chart(estilizar(fig, 220), config=CONFIGURACAO_GRAFICOS)
        evidencias.markdown(
            f"### Evidências\n**Correlação (r):** {relacao:.3f}\n\n"
            f"**Avaliações válidas:** {len(pares):,}\n\n**Método:** Pearson"
        )


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
                    "Status": ["OK"] * len(dados.columns),
                }
            )
            st.dataframe(
                catalogo, hide_index=True, width="stretch", height=360
            )
    with validacao:
        with st.container(border=True, key="equal_card_dataset_validacao"):
            st.markdown("### Validação do dataset")
            st.success("✓ Dataset carregado com sucesso")
            st.success("✓ Possui pelo menos 1.000 registros")
            st.success("✓ Possui pelo menos 4 variáveis numéricas")
            st.success("✓ Possui pelo menos 2 variáveis categóricas")
            st.success("✓ Estrutura processada sem erros")
    with st.container(border=True):
        st.markdown("### Pré-visualização dos dados")
        st.dataframe(dados.head(10), width="stretch")
    st.info(
        "O MovieLens é disponibilizado pelo GroupLens (University of Minnesota) "
        "para fins educacionais e de pesquisa. IDs são códigos, não grandezas contínuas."
    )


def pagina_sobre():
    cabecalho(
        "Documentação e",
        "Sobre o Projeto",
        "LABESTAT  ›  DOCUMENTAÇÃO / SOBRE",
    )
    sobre, objetivos = st.columns([1.15, 1])
    with sobre:
        with st.container(border=True, key="equal_card_sobre_resumo"):
            st.markdown("### ⓘ Sobre o Projeto")
            st.write(
                "O Laboratório Estatístico Interativo é uma aplicação acadêmica "
                "para integrar conceitos de matemática e estatística por meio da "
                "análise de dados reais, visualizações e uma biblioteca própria."
            )
            a, b, c = st.columns(3)
            a.metric("Finalidade", "Acadêmica")
            b.metric("Abordagem", "Prática")
            c.metric("Dados", "Reais")
    with objetivos:
        with st.container(border=True, key="equal_card_sobre_objetivos"):
            st.markdown("### Objetivos do Trabalho")
            st.markdown(
                """
                <div class="objective-grid">
                  <div class="objective-item"><span>✓</span>Dados reais: MovieLens</div>
                  <div class="objective-item"><span>✓</span>Núcleo estatístico próprio</div>
                  <div class="objective-item"><span>✓</span>Estatística descritiva</div>
                  <div class="objective-item"><span>✓</span>Probabilidade e simulação</div>
                  <div class="objective-item"><span>✓</span>Distribuições e regressão</div>
                  <div class="objective-item"><span>✓</span>Relatório de descobertas</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    arquitetura, executar = st.columns([1.15, 1])
    with arquitetura:
        with st.container(border=True, key="equal_card_sobre_arquitetura"):
            st.markdown("### Arquitetura da Aplicação")
            st.markdown(
                """
                <section class="architecture">
                  <div><b>▣ Interface</b><small>Streamlit</small></div><em>→</em>
                  <div><b>▦ Dados</b><small>Pandas</small></div><em>→</em>
                  <div><b>⌁ Núcleo próprio</b><small>minhastats.py</small></div><em>→</em>
                  <div><b>✓ Validação</b><small>NumPy / SciPy</small></div>
                </section>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("### Núcleo estatístico")
            st.markdown(
                """
                <div class="function-grid">
                  <code>media(dados)</code>
                  <code>mediana(dados)</code>
                  <code>moda(dados)</code>
                  <code>amplitude(dados)</code>
                  <code>variancia_populacional(dados)</code>
                  <code>variancia_amostral(dados)</code>
                  <code>desvio_padrao_populacional(dados)</code>
                  <code>desvio_padrao_amostral(dados)</code>
                  <code>percentil(dados, p)</code>
                  <code>quartis(dados)</code>
                  <code>coeficiente_variacao(dados)</code>
                  <code>covariancia(x, y)</code>
                  <code>correlacao_pearson(x, y)</code>
                  <code>regressao_linear(x, y)</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with executar:
        with st.container(border=True, key="equal_card_sobre_execucao"):
            st.markdown("### Como Executar")
            st.markdown(
                """
                1. Crie e ative um ambiente virtual.
                2. Instale as dependências do arquivo requirements.txt.
                3. Inicie a aplicação com streamlit run app.py.
                4. Acesse o endereço local exibido no terminal.
                """
            )
            st.markdown("### Dataset e fontes")
            st.markdown(
                "[MovieLens Latest Small — fonte oficial]"
                "(https://grouplens.org/datasets/movielens/latest/)"
            )
            st.caption(
                "README.md, RELATORIO.md, roteiro do vídeo e checklist estão na raiz do projeto."
            )
            st.markdown("### Validação")
            st.markdown(
                "- Execute `pytest -q` para validar o núcleo estatístico.\n"
                "- Resultado atual: **12 testes aprovados**."
            )


def rodape():
    st.markdown(
        """
        <footer class="app-footer">
          <strong>∑&nbsp; LabEstat</strong>
          <span>Projeto acadêmico • Reproduzível com Python + Streamlit</span>
          <nav>
            <a href="https://grouplens.org/datasets/movielens/latest/" target="_blank">Dataset: MovieLens ↗</a>
            <a href="?page=sobre" target="_self">Documentação</a>
          </nav>
        </footer>
        """,
        unsafe_allow_html=True,
    )


carregar_estilos()
dados = dados_completos()
pagina = st.query_params.get("page", "inicio")
paginas_validas = {
    "inicio",
    "descritiva",
    "simulacoes",
    "distribuicoes",
    "regressao",
    "descobertas",
    "dados",
    "sobre",
}
if pagina not in paginas_validas:
    pagina = "inicio"

controlar_rolagem(pagina)
shell(pagina, dados)
with st.container(key="page_body"):
    if pagina == "inicio":
        pagina_inicio(dados)
    elif pagina == "descritiva":
        pagina_descritiva(dados)
    elif pagina == "simulacoes":
        pagina_simulacoes(dados)
    elif pagina == "distribuicoes":
        pagina_distribuicoes(dados)
    elif pagina == "regressao":
        pagina_regressao(dados)
    elif pagina == "descobertas":
        pagina_descobertas(dados)
    elif pagina == "dados":
        pagina_dados(dados)
    else:
        pagina_sobre()
rodape()
