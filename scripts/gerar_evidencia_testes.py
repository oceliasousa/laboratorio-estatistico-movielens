"""Executa o pytest e registra o resultado em uma imagem para o relatório."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "docs" / "images" / "testes-pytest.png"


def fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    candidatos = [
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/SFNSMonoBold.ttf" if negrito else "",
        "/System/Library/Fonts/Menlo.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for caminho in candidatos:
        if caminho and Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    return ImageFont.load_default()


def quebrar_texto(texto: str, largura: int = 102) -> list[str]:
    linhas: list[str] = []
    for linha in texto.splitlines() or [""]:
        if not linha:
            linhas.append("")
            continue
        while len(linha) > largura:
            corte = linha.rfind(" ", 0, largura)
            corte = corte if corte > 0 else largura
            linhas.append(linha[:corte])
            linha = linha[corte:].lstrip()
        linhas.append(linha)
    return linhas


def main() -> int:
    processo = subprocess.run(
        [sys.executable, "-m", "pytest", "-rA"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        check=False,
    )
    saida_completa = (processo.stdout + processo.stderr).strip()
    linhas_saida = saida_completa.splitlines()
    if len(linhas_saida) > 2:
        saida_terminal = "\n".join([linhas_saida[0], linhas_saida[-1]])
    else:
        saida_terminal = saida_completa
    status = "TESTES APROVADOS" if processo.returncode == 0 else "TESTES COM FALHA"

    largura, altura = 1600, 900
    imagem = Image.new("RGB", (largura, altura), "#050d1a")
    desenho = ImageDraw.Draw(imagem)
    desenho.rounded_rectangle(
        (70, 70, largura - 70, altura - 70),
        radius=24,
        fill="#081729",
        outline="#1e4264",
        width=3,
    )
    desenho.rectangle((70, 70, largura - 70, 156), fill="#0d2239")
    desenho.ellipse((100, 101, 124, 125), fill="#ff5f57")
    desenho.ellipse((138, 101, 162, 125), fill="#febc2e")
    desenho.ellipse((176, 101, 200, 125), fill="#28c840")

    titulo = fonte(34, True)
    corpo = fonte(25)
    pequeno = fonte(21)
    desenho.text((235, 92), "LabEstat - validação automatizada", font=titulo, fill="#eef7ff")
    desenho.text((110, 198), "$ python -m pytest -rA", font=corpo, fill="#35e7d0")

    y = 255
    for linha in quebrar_texto(saida_terminal):
        desenho.text((110, y), linha, font=corpo, fill="#d5e5f7")
        y += 39

    cor_status = "#35e7a4" if processo.returncode == 0 else "#ff6b6b"
    desenho.rounded_rectangle((110, 665, 570, 742), radius=14, fill="#0b3040")
    desenho.text((140, 684), status, font=titulo, fill=cor_status)
    momento = datetime.now().astimezone().strftime("Executado em %d/%m/%Y às %H:%M:%S %Z")
    desenho.text((110, 785), momento, font=pequeno, fill="#8ca8c4")
    desenho.text(
        (largura - 540, 785),
        "Tolerância: rel=1e-10 | abs=1e-12",
        font=pequeno,
        fill="#8ca8c4",
    )

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    imagem.save(SAIDA, optimize=True)
    print(f"Evidência salva em: {SAIDA}")
    return processo.returncode


if __name__ == "__main__":
    raise SystemExit(main())
