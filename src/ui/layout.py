"""Layout do laboratório estatístico."""

import base64
import streamlit as st
from src.config import RAIZ


def carregar_estilos():
    imagem = base64.b64encode(
        (RAIZ / "assets" / "ondas-estatisticas.png").read_bytes()
    ).decode("ascii")
    css = (RAIZ / "styles.css").read_text(encoding="utf-8")
    css = css.replace("__HERO_IMAGE__", f"data:image/png;base64,{imagem}")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


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


def shell(pagina, dados):
    total_avaliacoes = f"{len(dados):,}".replace(",", ".")
    total_filmes = f"{dados['movieId'].nunique():,}".replace(",", ".")
    modulo_ativo = pagina in {"descritiva", "simulacoes", "distribuicoes", "regressao"}
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
            <a class="{'active' if pagina == 'inicio' else ''}" href="?page=inicio" target="_self">⌂ Início</a>
            <a class="{'active' if modulo_ativo else ''}" href="?page=descritiva" target="_self">◉ Módulos</a>
            <a class="{'active' if pagina == 'dados' else ''}" href="?page=dados" target="_self">▣ Dataset</a>
            <a class="{'active' if pagina == 'descobertas' else ''}" href="?page=descobertas" target="_self">▤ Relatório</a>
            <a class="{'active' if pagina == 'sobre' else ''}" href="?page=sobre" target="_self">▧ Documentação</a>
          </nav>
          <div class="top-actions">
            <a href="?page=sobre" target="_self">Ajuda</a>
            <a href="?page=dados" target="_self">▣&nbsp; MovieLens Latest Small⌄</a>
          </div>
        </header>
        <details class="mobile-nav"><summary>Navegar pelas páginas</summary><nav>{''.join(itens)}</nav></details>
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


def rodape():
    with st.container(key="page_footer"):
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
