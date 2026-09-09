"""Carga e preparação reprodutível dos dados MovieLens."""

from pathlib import Path
import re
import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]


def preparar_dados(avaliacoes, filmes):
    """Une as tabelas sem perder avaliações silenciosamente."""
    for tabela, exigidas in [(avaliacoes, {"userId", "movieId", "rating", "timestamp"}),
                             (filmes, {"movieId", "title", "genres"})]:
        faltantes = exigidas.difference(tabela.columns)
        if faltantes:
            raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(faltantes))}")
    if avaliacoes.empty or not avaliacoes["rating"].between(0.5, 5).all():
        raise ValueError("As avaliações devem existir e estar entre 0,5 e 5.")
    dados = avaliacoes.merge(filmes, on="movieId", how="left", validate="many_to_one", indicator=True)
    if not dados["_merge"].eq("both").all():
        raise ValueError("Há avaliações de filmes ausentes no catálogo.")
    dados = dados.drop(columns="_merge")
    dados["ano_filme"] = dados["title"].str.extract(r"\((\d{4})\)\s*$", expand=False)
    dados["ano_filme"] = pd.to_numeric(dados["ano_filme"], errors="coerce")
    dados["ano_avaliacao"] = pd.to_datetime(dados["timestamp"], unit="s", utc=True).dt.year
    dados["genero_principal"] = dados["genres"].str.split("|").str[0]
    dados["quantidade_generos"] = dados["genres"].str.count(re.escape("|")) + 1
    # O marcador de ausência não é um gênero. Zero significa nenhum gênero listado.
    sem_generos = dados["genres"].isna() | dados["genres"].eq("(no genres listed)")
    dados.loc[sem_generos, "quantidade_generos"] = 0
    dados["faixa_avaliacao"] = pd.cut(
        dados["rating"], bins=[0, 2, 3.5, 5], labels=["Baixa", "Média", "Alta"], include_lowest=True
    ).astype(str)
    return dados


def carregar_dados(pasta=None):
    pasta = RAIZ / "data" if pasta is None else Path(pasta)
    return preparar_dados(pd.read_csv(pasta / "ratings.csv"), pd.read_csv(pasta / "movies.csv"))


def assinatura_dados():
    """Invalida o cache quando mudam os CSVs ou a regra de preparação."""
    arquivos = [RAIZ / "data/ratings.csv", RAIZ / "data/movies.csv", Path(__file__)]
    return tuple((arquivo.stat().st_mtime_ns, arquivo.stat().st_size) for arquivo in arquivos)


def validar_estrutura(dados):
    """Resultados calculados; IDs não contam como grandezas de análise."""
    return {
        "Dataset carregado": not dados.empty,
        "Pelo menos 1.000 registros": len(dados) >= 1000,
        "Pelo menos 4 variáveis numéricas de análise": sum(
            c in dados and pd.api.types.is_numeric_dtype(dados[c]) for c in NUMERICAS_ANALISE
        ) >= 4,
        "Pelo menos 2 variáveis categóricas": sum(c in dados for c in CATEGORICAS) >= 2,
        "Notas válidas na escala 0,5 a 5": "rating" in dados and dados["rating"].between(0.5, 5).all(),
    }


NUMERICAS = ["rating", "timestamp", "ano_filme", "ano_avaliacao", "quantidade_generos", "userId", "movieId"]
NUMERICAS_ANALISE = ["rating", "ano_filme", "ano_avaliacao", "quantidade_generos"]
CATEGORICAS = ["genero_principal", "faixa_avaliacao", "title", "genres"]
