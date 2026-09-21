"""Descritiva do laboratório estatístico."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src import minhastats as ms
from src.dados import CATEGORICAS, NUMERICAS_ANALISE
from src.analises import valores_numericos, interpretar_assimetria
from src.analises import tabela_frequencias, tabela_categorica, resumo_iqr, classes_sturges
from src.ui.formatacao import formatar
from src.ui.layout import cabecalho
from src.ui.graficos import estilizar, exibir_grafico


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
        tabela = tabela_categorica(dados[coluna])
        esquerda, direita = st.columns([1, 1.55])
        with esquerda:
            with st.container(border=True, key="equal_card_categoria_tabela"):
                st.markdown("### Tabela de Frequência")
                st.dataframe(tabela, hide_index=True, width="stretch")
        with direita:
            with st.container(border=True, key="equal_card_categoria_grafico"):
                fig = px.bar(
                    tabela.head(20),
                    x="Frequência",
                    y="Categoria",
                    orientation="h",
                    title=f"Categorias mais frequentes — {coluna}",
                    color_discrete_sequence=["#29c9e6"],
                )
                exibir_grafico(estilizar(fig, 440))
        modais = tabela.loc[tabela["Modal"]]
        maior = int(modais["Frequência"].iloc[0])
        if len(modais) == 1:
            st.success(f"Categoria modal: {modais['Categoria'].iloc[0]} — {maior:,} ocorrências.")
        elif len(modais) == len(tabela):
            st.info(f"Todas as {len(modais)} categorias têm a mesma frequência ({maior:,}). "
                    "Não há uma categoria modal única; todas estão marcadas na coluna Modal.")
        else:
            st.info(f"Há {len(modais)} categorias modais, com {maior:,} ocorrências cada. "
                    "Todas estão marcadas na coluna Modal da tabela.")
        st.caption("Contagens, proporções e modas calculadas pelo núcleo próprio. "
                   "A tabela inclui todas as categorias; o gráfico mostra até 20. "
                   "Valores ausentes entram no total como categoria separada.")
        return

    valores = valores_numericos(dados, coluna)
    resumo = resumo_iqr(valores)
    q1, mediana, q3 = resumo["q1"], resumo["mediana"], resumo["q3"]
    iqr, inferior, superior = resumo["iqr"], resumo["inferior"], resumo["superior"]
    outliers = resumo["outliers"]
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
            padrao = classes_sturges(len(valores))
            bins = st.slider("Número de classes", 1, max(30, padrao), padrao)
            st.caption(f"Regra de Sturges: {padrao} classes para {len(valores):,} valores válidos. Ajuste para comparar.")
            classes = tabela_frequencias(valores, bins)
            frequencias, limites = classes.contagens, classes.limites
            tabela = pd.DataFrame(
                {
                    "Classe": [
                        f"[{limites[i]:.4g}; {limites[i + 1]:.4g}{']' if i == bins-1 else ')'}" for i in range(bins)
                    ],
                    "Frequência": frequencias,
                    "Relativa": [
                        f"{proporcao * 100:.1f}%"
                        for proporcao in ms.frequencias_relativas(frequencias)
                    ],
                }
            )
            tabela["Acumulada"] = ms.frequencias_acumuladas(frequencias)
            st.dataframe(tabela, hide_index=True, width="stretch", height=460)
    with centro:
        with st.container(border=True, key="equal_card_descritiva_distribuicao"):
            st.markdown("### Distribuição da Variável")
            fig = go.Figure(go.Bar(x=classes.centros, y=frequencias,
                                  width=classes.larguras, marker_color="#526fff"))
            fig.update_layout(title=f"Histograma de {coluna}", xaxis_title=coluna,
                              yaxis_title="Frequência", bargap=0.03)
            exibir_grafico(estilizar(fig, 300))
            fig_box = go.Figure(go.Box(q1=[q1], median=[mediana], q3=[q3],
                lowerfence=[resumo["bigode_inferior"]], upperfence=[resumo["bigode_superior"]],
                orientation="h", marker_color="#21cfe2", name=coluna))
            if outliers:
                unicos = sorted(set(outliers))
                fig_box.add_scatter(x=unicos, y=[0]*len(unicos), mode="markers",
                                    name="Outliers", marker=dict(color="#21cfe2", size=4))
            fig_box.update_layout(showlegend=False, xaxis_title=coluna)
            exibir_grafico(estilizar(fig_box, 190))
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
    st.caption("A assimetria é estimada pelo índice 3 × (média − mediana) / desvio; "
               "valor próximo de zero não comprova simetria. CV de anos e escalas de notas "
               "é mostrado para fins didáticos: essas escalas não possuem zero absoluto.")
