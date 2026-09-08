"""Carga e preparação reprodutível dos dados MovieLens."""

from pathlib import Path
import re
import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]


def carregar_dados():
    avaliacoes = pd.read_csv(RAIZ / "data" / "ratings.csv")
    filmes = pd.read_csv(RAIZ / "data" / "movies.csv")
    dados = avaliacoes.merge(filmes, on="movieId", validate="many_to_one")
    dados["ano_filme"] = dados["title"].str.extract(r"\((\d{4})\)\s*$", expand=False)
    dados["ano_filme"] = pd.to_numeric(dados["ano_filme"], errors="coerce")
    dados["ano_avaliacao"] = pd.to_datetime(dados["timestamp"], unit="s").dt.year
    dados["genero_principal"] = dados["genres"].str.split("|").str[0]
    dados["quantidade_generos"] = dados["genres"].str.count(re.escape("|")) + 1
    dados["faixa_avaliacao"] = pd.cut(
        dados["rating"], bins=[0, 2, 3.5, 5], labels=["Baixa", "Média", "Alta"], include_lowest=True
    ).astype(str)
    return dados


NUMERICAS = ["rating", "timestamp", "ano_filme", "ano_avaliacao", "quantidade_generos", "userId", "movieId"]
NUMERICAS_ANALISE = ["rating", "ano_filme", "ano_avaliacao", "quantidade_generos"]
CATEGORICAS = ["genero_principal", "faixa_avaliacao", "title", "genres"]
