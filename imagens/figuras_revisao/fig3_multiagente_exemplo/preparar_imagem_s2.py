"""Preparo de imagem (Figura 3) - recorta o painel S2 do composto real e
grava um PNG isolado, para ser embutido como nó de imagem no fluxograma
Graphviz `fig3_multiagente_exemplo.dot` (via atributo `image=`).

Este script NÃO compõe a figura final (isso é feito pelo Graphviz, para
um layout mais fluido e menos "embolado" que uma grade matplotlib com
setas cruzando texto). Ele só lê o composto real já enviado aos modelos
e recorta o painel S2, sem reconstrução a partir de pixels/máscaras
cruas (não disponíveis nesta máquina - ver nota de seleção de caso em
`fig3_multiagente_exemplo.dot`).

Mesma lesão da Figura 2: ISIC_0027950 / HAM_0000193, condição S2.
"""

from pathlib import Path

import numpy as np
from PIL import Image

# parents[5] a partir deste arquivo = C:\Projetos (ancestral comum dos dois repositórios)
CAMINHO_COMPOSTO_REAL = (
    Path(__file__).resolve().parents[4]
    / "IFES"
    / "mestrado_ifes"
    / "experiments"
    / "multiagent"
    / "s0_s1_s2_images"
    / "examples"
    / "ISIC_0027950_s0_s1_s2_example.png"
)
# Fallback absoluto: C:\Projetos\IFES\mestrado_ifes\experiments\multiagent\s0_s1_s2_images\examples\ISIC_0027950_s0_s1_s2_example.png

SAIDA_PNG = Path(__file__).resolve().parent / "fig3_s2_panel_real.png"

# Fração do topo do painel ocupada pela legenda antiga ("S2 -- ISIC_xxx")
# já embutida no composto original - ajustável aqui caso o corte não
# remova a legenda por completo na prática (não confirmado visualmente
# nesta sessão - ver pendência no README).
FRACAO_TOPO_LEGENDA_ANTIGA = 0.055


def extrair_painel_s2(caminho_png: Path) -> Image.Image:
    img = Image.open(caminho_png).convert("RGB")
    largura, altura = img.size
    arr = np.asarray(img)
    media_coluna = arr.mean(axis=(0, 2))
    quase_branco = media_coluna > 250

    def gutter_mais_proximo(alvo_x):
        candidatos = np.where(quase_branco)[0]
        if candidatos.size == 0:
            return alvo_x
        return candidatos[np.argmin(np.abs(candidatos - alvo_x))]

    corte2 = gutter_mais_proximo(2 * largura / 3)
    painel_s2 = img.crop((corte2, 0, largura, altura))
    w, h = painel_s2.size
    topo = int(h * FRACAO_TOPO_LEGENDA_ANTIGA)
    return painel_s2.crop((0, topo, w, h))


def main():
    if not CAMINHO_COMPOSTO_REAL.exists():
        raise FileNotFoundError(
            f"Artefato real não encontrado em: {CAMINHO_COMPOSTO_REAL}\n"
            "Ajuste CAMINHO_COMPOSTO_REAL para o caminho absoluto documentado no topo deste arquivo."
        )
    painel = extrair_painel_s2(CAMINHO_COMPOSTO_REAL)
    painel.save(SAIDA_PNG)
    print(f"Painel S2 isolado salvo em: {SAIDA_PNG} ({painel.size[0]}x{painel.size[1]} px)")


if __name__ == "__main__":
    main()
