"""Figura 2 -- Uma lesao nas condicoes S0, S1 e S2 (variantes paralelas, nao sequencia).

Le o artefato composto real (ja enviado aos modelos) e re-rotula/recompoe
em 3 paineis lado a lado com a identidade visual deste conjunto de
figuras. Nao reconstroi a partir de pixels/mascaras cruas (nao
disponiveis nesta maquina) -- so recorta e rotula o composto real.

--------------------------------------------------------------------
SELECAO DO CASO -- documentada aqui propositalmente, nao e um dado
escondido no README. Regra pedida pelo pesquisador: "primeiro caso, na
ordem do manifesto complementar de 300 lesoes, com os artefatos
necessarios e mascara predita nao vazia".

Leitura estrita por ordem de linha do manifesto
(experiments/multiagent/local_300_s2_subset/local_300_s2_subset_manifest.csv)
aponta para a 1a linha, HAM_0000019 / ISIC_0025396. Essa lesao tem
status_s2 = "disponivel" no manifesto de preparacao
(experiments/multiagent/s0_s1_s2_preparation_manifest.csv) -- ou seja,
o pipeline que gerou as imagens a considerou disponivel -- mas os
arquivos de pixel reais (path_s0/path_s1/path_s2) estao registrados
como caminhos absolutos de outra maquina (Mac) e NAO existem nesta
maquina/sessao. As imagens cruas do HAM10000 e as mascaras de
referencia tambem nao estao acessiveis aqui (o caminho documentado em
D:/Andrey/Mestrado/dataverse_files/... nao resolve neste ambiente).

So existem, localmente, 5 composicoes de exemplo ja renderizadas em
experiments/multiagent/s0_s1_s2_images/examples/:
  ISIC_0024579, ISIC_0027950, ISIC_0030114 (uma das 6 lesoes com
  mascara S2 vazia -- excluida por regra), ISIC_0031922, ISIC_0032854.
Dessas 5, SO ISIC_0027950 (HAM_0000193) tambem pertence ao manifesto
complementar de 300 lesoes (linha 13, ou seja, a 12a linha de dados).
As outras 4 nao pertencem a esse subconjunto de 300.

DECISAO (documentada, nao silenciosa): usar ISIC_0027950 / HAM_0000193
-- e o primeiro caso, na ordem do manifesto complementar, para o qual os
artefatos reais estao de fato recuperaveis neste ambiente de trabalho,
com mascara S2 nao vazia. Isto e um desvio assumido da leitura estrita
"linha 1 do manifesto" por indisponibilidade de arquivo nesta maquina,
nao por estetica do contorno ou por acerto diagnostico -- dx=akiec
(nao-melanoma) desta lesao nao influenciou a escolha.
--------------------------------------------------------------------
"""

from pathlib import Path

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _estilo_comum import (  # noqa: E402
    aplicar_estilo_comum,
    COR_TEXTO,
    COR_BORDA_PAINEL,
    COR_ALERTA_SUAVE,
    TAMANHO_FONTE_BASE,
    TAMANHO_FONTE_TITULO,
    TAMANHO_FONTE_NOTA,
    LARGURA_MAX_POL,
)

# Caminho relativo assumindo o layout de pastas-irmas documentado:
# C:\Projetos\Mestrado\Dissertacao  e  C:\Projetos\IFES\mestrado_ifes
# parents[5] a partir deste arquivo = C:\Projetos (ancestral comum dos dois repositorios)
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
# Fallback absoluto documentado (caso o layout de pastas-irmas mude):
# C:\Projetos\IFES\mestrado_ifes\experiments\multiagent\s0_s1_s2_images\examples\ISIC_0027950_s0_s1_s2_example.png

LESION_ID = "HAM_0000193"
IMAGE_ID = "ISIC_0027950"
DX = "akiec"  # nao-melanoma

SAIDA_DIR = Path(__file__).resolve().parent
SAIDA_PDF = SAIDA_DIR / "fig2_s0_s1_s2.pdf"
SAIDA_PNG = SAIDA_DIR / "fig2_s0_s1_s2.png"

# Fracao do topo de cada painel ocupada pela legenda antiga ("S0 -- ISIC_xxx")
# ja embutida no composto original -- removida para dar lugar aos nossos
# proprios rotulos. Ajustavel aqui caso a legenda antiga nao seja
# totalmente removida na pratica (nao foi possivel confirmar visualmente
# nesta sessao sem executar o script -- ver pendencia no README).
FRACAO_TOPO_LEGENDA_ANTIGA = 0.055


def dividir_em_3_paineis(caminho_png: Path):
    """Abre o composto real e divide em 3 paineis (S0, S1, S2) por largura.

    Le as dimensoes reais do arquivo (nao assume nenhum valor fixo) e
    detecta as duas faixas de "gutter" (colunas quase brancas) proximas
    de 1/3 e 2/3 da largura para posicionar o corte, em vez de dividir
    cegamente em terços iguais -- robusto a pequenas assimetrias no
    composto original.
    """
    img = Image.open(caminho_png).convert("RGB")
    largura, altura = img.size
    arr = np.asarray(img)

    media_coluna = arr.mean(axis=(0, 2))  # brilho medio por coluna
    quase_branco = media_coluna > 250

    def gutter_mais_proximo(alvo_x):
        candidatos = np.where(quase_branco)[0]
        if candidatos.size == 0:
            return alvo_x
        return candidatos[np.argmin(np.abs(candidatos - alvo_x))]

    corte1 = gutter_mais_proximo(largura / 3)
    corte2 = gutter_mais_proximo(2 * largura / 3)

    painel_s0 = img.crop((0, 0, corte1, altura))
    painel_s1 = img.crop((corte1, 0, corte2, altura))
    painel_s2 = img.crop((corte2, 0, largura, altura))

    # Remove a faixa superior com a legenda antiga embutida ("S0 -- id").
    paineis_recortados = []
    for painel in (painel_s0, painel_s1, painel_s2):
        w, h = painel.size
        topo = int(h * FRACAO_TOPO_LEGENDA_ANTIGA)
        paineis_recortados.append(painel.crop((0, topo, w, h)))

    return paineis_recortados


def montar_figura():
    aplicar_estilo_comum()

    if not CAMINHO_COMPOSTO_REAL.exists():
        raise FileNotFoundError(
            f"Artefato real nao encontrado em: {CAMINHO_COMPOSTO_REAL}\n"
            "Confira o layout de pastas-irmas Dissertacao/mestrado_ifes, "
            "ou ajuste CAMINHO_COMPOSTO_REAL para o caminho absoluto documentado no topo deste arquivo."
        )

    s0, s1, s2 = dividir_em_3_paineis(CAMINHO_COMPOSTO_REAL)

    fig, eixos = plt.subplots(1, 3, figsize=(LARGURA_MAX_POL, LARGURA_MAX_POL / 3 + 0.9))
    fig.suptitle(
        "Mesma lesão, três apresentações",
        fontsize=TAMANHO_FONTE_TITULO,
        color=COR_TEXTO,
    )

    rotulos = [
        ("S0 - imagem original", s0),
        ("S1 - contorno de referência", s1),
        ("S2 - contorno predito\npelo segmentador", s2),
    ]

    for eixo, (rotulo, painel) in zip(eixos, rotulos):
        eixo.imshow(np.asarray(painel))
        eixo.set_title(rotulo, fontsize=TAMANHO_FONTE_BASE, color=COR_TEXTO)
        eixo.set_xticks([])
        eixo.set_yticks([])
        for lado in eixo.spines.values():
            lado.set_color(COR_BORDA_PAINEL)

    nota = (
        f"Lesão {LESION_ID} (imagem {IMAGE_ID}, dx={DX}, não-melanoma). "
    )
    fig.text(0.5, 0.2, nota, ha="center", va="bottom", fontsize=TAMANHO_FONTE_NOTA, color=COR_ALERTA_SUAVE, wrap=True)

    fig.subplots_adjust(left=0.03, right=0.97, top=0.80, bottom=0.22, wspace=0.08)

    fig.savefig(SAIDA_PDF)
    fig.savefig(SAIDA_PNG, dpi=300)


if __name__ == "__main__":
    montar_figura()
