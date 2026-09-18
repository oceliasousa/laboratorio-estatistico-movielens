"""Sobre do laboratório estatístico."""

import streamlit as st
from src.ui.layout import cabecalho


def pagina_sobre(dados=None):
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
                  <code>moda_categorica(dados)</code>
                  <code>frequencias_categoricas(dados)</code>
                  <code>frequencias_relativas(contagens)</code>
                  <code>frequencias_acumuladas(contagens)</code>
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
                "- Moda categórica: todos os empates são preservados. Ausentes entram no total como categoria separada.\n"
                "- Consulte `docs/VALIDACAO.md` para o resultado registrado da validação."
            )
            from src.config import RAIZ
            for nome in ("README.md", "RELATORIO.md", "CHECKLIST_ENTREGA.md"):
                st.download_button(f"Baixar {nome}", (RAIZ / nome).read_text(encoding="utf-8"),
                                   file_name=nome, mime="text/markdown")
