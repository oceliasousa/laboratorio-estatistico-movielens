"""Configuração compartilhada; caminhos independentes do diretório atual."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

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
