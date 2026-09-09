"""Ponto de entrada: configura, carrega os dados e encaminha a página."""

import streamlit as st
from src.dados import carregar_dados, assinatura_dados
from src.rotas import PAGINAS
from src.ui.layout import carregar_estilos, shell, rodape
from src.ui.carregamento import controlar_rolagem, iniciar_carregamento, finalizar_carregamento


@st.cache_data(show_spinner=False)
def dados_completos(assinatura):
    """A assinatura participa da chave do cache do Streamlit."""
    return carregar_dados()


def main():
    st.set_page_config(page_title="LabEstat — MovieLens", page_icon="∑", layout="wide")
    carregar_estilos()
    pagina = st.query_params.get("page", "inicio")
    if pagina not in PAGINAS:
        pagina = "inicio"
    st.session_state['_graficos_esperados'] = 0
    controlar_rolagem(pagina)
    iniciar_carregamento(pagina)
    try:
        dados = dados_completos(assinatura_dados())
        shell(pagina, dados)
        with st.container(key="page_body"):
            PAGINAS[pagina](dados)
    except (OSError, ValueError) as erro:
        st.error(f"Não foi possível concluir a análise: {erro}")
    finally:
        rodape()
        finalizar_carregamento()


if __name__ == "__main__":
    main()
