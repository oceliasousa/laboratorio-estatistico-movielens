"""Gera o PDF de envio da Sistematização.

Sem os dois links externos, o arquivo recebe o prefixo PREVIA e não deve ser
enviado. Quando ambos forem informados, o nome final exigido é usado.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


RAIZ = Path(__file__).resolve().parents[1]
PASTA_SAIDA = RAIZ / "output" / "pdf"
NOME_FINAL = "SISTEMATIZACAO_MEC_OceliaAssisDeSousa.pdf"
NOME_PREVIA = "PREVIA_SISTEMATIZACAO_MEC_OceliaAssisDeSousa.pdf"
URL_DADOS = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera o PDF acadêmico de entrega.")
    parser.add_argument("--repositorio", default="", help="URL pública do GitHub/GitLab")
    parser.add_argument("--video", default="", help="URL pública ou não listada do vídeo")
    return parser.parse_args()


def rodape(canvas, documento) -> None:
    canvas.saveState()
    largura, _ = A4
    canvas.setStrokeColor(colors.HexColor("#DCE6F2"))
    canvas.line(1.8 * cm, 1.45 * cm, largura - 1.8 * cm, 1.45 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52657A"))
    canvas.drawString(1.8 * cm, 1.05 * cm, "Océlia Assis de Sousa - RA/DRT 72650579")
    canvas.drawRightString(largura - 1.8 * cm, 1.05 * cm, f"Página {documento.page}")
    canvas.restoreState()


def link_paragrafo(rotulo: str, url: str, estilo: ParagraphStyle) -> Paragraph:
    if url:
        valor = f'<link href="{url}" color="#1769E0"><u>{url}</u></link>'
    else:
        valor = "Não informado - esta prévia ainda não está pronta para envio."
    return Paragraph(f"<b>{rotulo}:</b> {valor}", estilo)


def gerar(repositorio: str, video: str) -> Path:
    completo = bool(repositorio.strip() and video.strip())
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_SAIDA / (NOME_FINAL if completo else NOME_PREVIA)

    estilos_base = getSampleStyleSheet()
    titulo = ParagraphStyle(
        "Titulo",
        parent=estilos_base["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        textColor=colors.HexColor("#192A56"),
        alignment=TA_CENTER,
        spaceAfter=18,
    )
    secao = ParagraphStyle(
        "Secao",
        parent=estilos_base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#263C87"),
        spaceBefore=10,
        spaceAfter=8,
    )
    corpo = ParagraphStyle(
        "Corpo",
        parent=estilos_base["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#24364B"),
        spaceAfter=7,
    )
    aviso = ParagraphStyle(
        "Aviso",
        parent=corpo,
        textColor=colors.HexColor("#8A4B00"),
        backColor=colors.HexColor("#FFF3D6"),
        borderColor=colors.HexColor("#F0BE62"),
        borderWidth=1,
        borderPadding=9,
        spaceBefore=8,
    )

    documento = BaseDocTemplate(
        str(caminho),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.8 * cm,
        title="Sistematização - Laboratório Estatístico MovieLens",
        author="Océlia Assis de Sousa",
    )
    frame = Frame(
        documento.leftMargin,
        documento.bottomMargin,
        documento.width,
        documento.height,
        id="conteudo",
    )
    documento.addPageTemplates([PageTemplate(id="padrao", frames=[frame], onPage=rodape)])

    historia = [
        Spacer(1, 0.7 * cm),
        Paragraph("Sistematização - Matemática e Estatística para Computação", titulo),
        Paragraph("Laboratório Estatístico Interativo - MovieLens", secao),
        Spacer(1, 0.25 * cm),
    ]
    identificacao = Table(
        [
            ["Autora", "Océlia Assis de Sousa"],
            ["RA/DRT", "72650579"],
            ["Modalidade", "Trabalho individual"],
            ["Projeto", "Laboratório Estatístico Interativo - MovieLens"],
        ],
        colWidths=[4 * cm, 12.2 * cm],
    )
    identificacao.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#24364B")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10.5),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#B8C8DC")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    historia.extend(
        [
            identificacao,
            Spacer(1, 0.45 * cm),
            Paragraph("Links obrigatórios", secao),
            link_paragrafo("Dados crus", URL_DADOS, corpo),
            link_paragrafo("Solução pública", repositorio.strip(), corpo),
            link_paragrafo("Vídeo de demonstração", video.strip(), corpo),
        ]
    )
    if not completo:
        historia.append(
            Paragraph(
                "PRÉVIA: o repositório público e o vídeo ainda precisam ser informados. "
                "Não envie este arquivo enquanto essa mensagem estiver presente.",
                aviso,
            )
        )

    historia.extend(
        [
            Spacer(1, 0.5 * cm),
            Paragraph("Conteúdo do repositório", secao),
            Paragraph(
                "O repositório contém o código-fonte da aplicação Streamlit, o núcleo "
                "estatístico próprio, testes automatizados, dados crus, instruções de "
                "execução, relatório acadêmico e roteiro do vídeo.",
                corpo,
            ),
            PageBreak(),
            Paragraph("Resumo executivo", titulo),
            Paragraph("Dataset escolhido", secao),
            Paragraph(
                "O projeto utiliza o MovieLens Latest Small, conjunto público do GroupLens. "
                "A unidade de análise é uma avaliação de filme. Após a preparação "
                "reprodutível, a base reúne 100.836 avaliações, 9.742 filmes, 11 colunas, "
                "quatro variáveis categóricas e sete colunas numéricas. Para as análises "
                "estatísticas são usadas quatro grandezas numéricas válidas, além das "
                "variáveis categóricas derivadas.",
                corpo,
            ),
            Paragraph("Módulos implementados", secao),
            Paragraph(
                "O laboratório possui núcleo estatístico implementado sem funções prontas "
                "para média, mediana, moda, amplitude, variâncias, desvios padrão, "
                "percentis, quartis, coeficiente de variação, covariância, correlação de "
                "Pearson e regressão linear. A interface oferece estatística descritiva, "
                "frequências, histogramas, boxplots, outliers pelo IQR, simulações da Lei "
                "dos Grandes Números e do Teorema Central do Limite, ajustes Normal, "
                "Exponencial e Uniforme, regressão com R² e predição interativa. As funções "
                "foram comparadas com NumPy e SciPy em 12 testes automatizados aprovados.",
                corpo,
            ),
            Paragraph("Três descobertas principais", secao),
            Paragraph(
                "<b>1.</b> As avaliações se concentram acima do ponto médio: a nota média "
                "é 3,5016 e a mediana é 3,5 em uma escala de 0,5 a 5.",
                corpo,
            ),
            Paragraph(
                "<b>2.</b> Ação possui o maior volume de avaliações quando o primeiro gênero "
                "é adotado como gênero principal: são 30.635 avaliações, seguida por "
                "Comédia, com 25.217.",
                corpo,
            ),
            Paragraph(
                "<b>3.</b> Ano de lançamento e nota individual apresentam correlação linear "
                "muito fraca (r = -0,0840). Portanto, o ano isoladamente explica muito "
                "pouco da avaliação atribuída pelo usuário.",
                corpo,
            ),
            Paragraph("Limitação interpretativa", secao),
            Paragraph(
                "Os resultados descrevem a amostra MovieLens. Correlação não implica "
                "causalidade, e os participantes da plataforma não representam toda a "
                "população de espectadores.",
                corpo,
            ),
        ]
    )
    documento.build(historia)
    return caminho


def main() -> None:
    args = argumentos()
    caminho = gerar(args.repositorio, args.video)
    print(caminho)


if __name__ == "__main__":
    main()

