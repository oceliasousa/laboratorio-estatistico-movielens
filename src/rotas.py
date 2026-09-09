"""Registro único das páginas disponíveis."""

from src.paginas.inicio import pagina_inicio
from src.paginas.descritiva import pagina_descritiva
from src.paginas.simulacoes import pagina_simulacoes
from src.paginas.distribuicoes import pagina_distribuicoes
from src.paginas.regressao import pagina_regressao
from src.paginas.descobertas import pagina_descobertas
from src.paginas.dados import pagina_dados
from src.paginas.sobre import pagina_sobre

PAGINAS = {
    "inicio": pagina_inicio,
    "descritiva": pagina_descritiva,
    "simulacoes": pagina_simulacoes,
    "distribuicoes": pagina_distribuicoes,
    "regressao": pagina_regressao,
    "descobertas": pagina_descobertas,
    "dados": pagina_dados,
    "sobre": pagina_sobre,
}
