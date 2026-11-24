"""Figura 3 -- Exemplo real das entradas e saidas do sistema multiagente.

Reaproveita a mesma lesao da Figura 2 (ISIC_0027950 / HAM_0000193),
condicao S2, e um registro real de execucao (modelo gemini-3.1-flash-lite,
lido de experiments/multiagent/full_scale_matrix/gemini-3.1-flash-lite/
call_log_main.jsonl nesta sessao de preparacao). Os textos completos de
origem, sem nenhum corte, estao em fig3_textos_completos.md -- este
script so grava excertos (marcados com "(...)") dos mesmos textos, nunca
reescritos ou corrigidos.

Escolha do modelo: Gemini e o primeiro modelo multiagente, na ordem
deterministica ja documentada no protocolo para desempate
(CNN -> Gemini -> GPT -> Qwen3-VL -> MedGemma, usada em
docs/reconstruction/34_consolidated_dissertation_status_report.md,
Analise 6) -- escolhido pela ordem, nao pelo resultado.

RESSALVA DE FIDELIDADE (nao escondida, repetida aqui e na figura): o
texto bruto do sumarizador termina com a linha literal
"decisao_final: indeterminado", mas os campos estruturados do mesmo
registro (classified_status_v2="negativo", decision_status="field_absent",
decisao_final=null) nao capturaram esse valor. Ver fig3_textos_completos.md,
secao "Ressalva de fidelidade", para a leitura completa apoiada em
docs/reconstruction/22_final_answer_extraction_preprocessing.md.
"""

from pathlib import Path
import sys

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _estilo_comum import (  # noqa: E402
    aplicar_estilo_comum,
    COR_TEXTO,
    COR_BORDA_PAINEL,
    COR_FUNDO_PAINEL,
    COR_DESTAQUE_SUAVE,
    COR_ALERTA_SUAVE,
    TAMANHO_FONTE_BASE,
    TAMANHO_FONTE_TITULO,
    TAMANHO_FONTE_NOTA,
    LARGURA_MAX_POL,
)

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
# Fallback absoluto: C:\Projetos\IFES\mestrado_ifes\experiments\multiagent\s0_s1_s2_images\examples\ISIC_0027950_s0_s1_s2_example.png

LESION_ID = "HAM_0000193"
IMAGE_ID = "ISIC_0027950"
MODELO = "gemini-3.1-flash-lite"
CONDICAO = "s2"

FRACAO_TOPO_LEGENDA_ANTIGA = 0.055

SAIDA_DIR = Path(__file__).resolve().parent
SAIDA_PDF = SAIDA_DIR / "fig3_multiagente_exemplo.pdf"
SAIDA_PNG = SAIDA_DIR / "fig3_multiagente_exemplo.png"

# Excertos truncados (ver fig3_textos_completos.md para o texto integral
# de cada um -- nenhuma palavra foi alterada, so cortada com "(...)").
EXCERTO_ABCD = (
    "assimetria='1 - ...assimetria em apenas um dos eixos...' "
    "bordas='6 - ...bem delimitadas em seis dos oito quadrantes...' "
    "cor='3 - três cores distintas...' estruturas='2 - duas estruturas principais...' "
    "explicacao='(1*1,3)+(6*0,1)+(3*0,5)+(2*0,5) = 4,4 < 4,75 -> benigna' (...)"
)
EXCERTO_MENZIES = (
    "positivas: todos os 7 critérios = '0. Ausente.' (...) "
    "negativas: simetria='1. padrão...relativamente simétrico.', "
    "cor_unica='0. múltiplas tonalidades...' "
    "explicacao='...ausência de todas as características positivas indica "
    "...uma lesão de natureza benigna.' (...)"
)
EXCERTO_SPCL = (
    "padrao_de_pigmentacao_atipico='Sim (...) (2 pontos)' "
    "vasos_atipicos='Sim, ...vasos lineares e arboriformes irregulares... (2 pontos)' "
    "hiperpigmentacao_localizada='Sim (...) (1 ponto)' (...) "
    "explicacao='...totalizando 5 pontos na checklist de sete pontos. "
    "...pontuação total igual ou superior a 3 indica uma lesão que requer "
    "avaliação clínica especializada.'"
)
EXCERTO_SUMARIZADOR = (
    "\"(...) Existe um conflito claro: enquanto os métodos baseados em "
    "'regras de ouro' (ABCD/Menzies) não atingem o limiar de malignidade "
    "(...), o SPCL detecta características morfológicas (vasos e "
    "pigmentação focal) que são clinicamente relevantes. (...) "
    "Conclusão: (...) a lesão apresenta características que impedem uma "
    "classificação definitiva como benigna apenas com base em algoritmos "
    "automatizados. (...) a evidência é insuficiente para uma "
    "classificação binária segura neste momento.\"\n\n"
    "decisao_final: indeterminado"
)

NOTA_FIDELIDADE = (
    "Ressalva de fidelidade: o texto bruto termina em \"decisao_final: indeterminado\", "
    "mas os campos estruturados do mesmo registro (classified_status_v2=\"negativo\", "
    "decision_status=\"field_absent\", decisao_final=null) não capturaram esse valor "
    "— mecanismo de extração já documentado em docs/reconstruction/"
    "22_final_answer_extraction_preprocessing.md (ver fig3_textos_completos.md)."
)


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


def caixa_texto(eixo, titulo, texto, cor_borda=COR_BORDA_PAINEL, destaque=False):
    eixo.set_xticks([])
    eixo.set_yticks([])
    for lado in eixo.spines.values():
        lado.set_color(cor_borda)
        lado.set_linewidth(1.4 if destaque else 0.8)
    eixo.set_facecolor(COR_FUNDO_PAINEL)
    eixo.set_title(titulo, fontsize=TAMANHO_FONTE_BASE, color=COR_TEXTO, loc="left", fontweight="bold")
    eixo.text(
        0.03, 0.95, texto, transform=eixo.transAxes, fontsize=TAMANHO_FONTE_NOTA,
        color=COR_TEXTO, va="top", ha="left", wrap=True,
    )


def montar_figura():
    aplicar_estilo_comum()

    if not CAMINHO_COMPOSTO_REAL.exists():
        raise FileNotFoundError(
            f"Artefato real nao encontrado em: {CAMINHO_COMPOSTO_REAL}\n"
            "Ajuste CAMINHO_COMPOSTO_REAL para o caminho absoluto documentado no topo deste arquivo."
        )

    painel_s2 = extrair_painel_s2(CAMINHO_COMPOSTO_REAL)

    fig = plt.figure(figsize=(LARGURA_MAX_POL, LARGURA_MAX_POL * 1.15))
    fig.suptitle(
        "Exemplo real de entradas e saída do sistema multiagente (condição S2)",
        fontsize=TAMANHO_FONTE_TITULO, color=COR_TEXTO,
    )

    grade = fig.add_gridspec(
        3, 3,
        height_ratios=[1.1, 0.85, 1.25],
        width_ratios=[1, 1, 1],
        left=0.04, right=0.97, top=0.90, bottom=0.10, hspace=0.55, wspace=0.12,
    )

    eixo_imagem = fig.add_subplot(grade[0, 0])
    eixo_imagem.imshow(np.asarray(painel_s2))
    eixo_imagem.set_title(f"Imagem S2\n{IMAGE_ID}", fontsize=TAMANHO_FONTE_BASE, color=COR_TEXTO)
    eixo_imagem.set_xticks([])
    eixo_imagem.set_yticks([])
    for lado in eixo_imagem.spines.values():
        lado.set_color(COR_BORDA_PAINEL)

    eixo_abcd = fig.add_subplot(grade[1, 0])
    caixa_texto(eixo_abcd, "Parecer ABCD", EXCERTO_ABCD)

    eixo_menzies = fig.add_subplot(grade[1, 1])
    caixa_texto(eixo_menzies, "Parecer Menzies", EXCERTO_MENZIES)

    eixo_spcl = fig.add_subplot(grade[1, 2])
    caixa_texto(eixo_spcl, "Parecer Seven-Point Checklist", EXCERTO_SPCL)

    eixo_sumario = fig.add_subplot(grade[2, :])
    caixa_texto(
        eixo_sumario,
        "Agente sumarizador -- recebe a imagem e os 3 pareceres acima",
        EXCERTO_SUMARIZADOR,
        cor_borda=COR_DESTAQUE_SUAVE,
        destaque=True,
    )
    eixo_sumario.text(
        0.03, 0.08, NOTA_FIDELIDADE, transform=eixo_sumario.transAxes,
        fontsize=TAMANHO_FONTE_NOTA - 0.5, color=COR_ALERTA_SUAVE, va="bottom", ha="left", wrap=True,
        style="italic",
    )

    # Setas: imagem -> sumarizador; cada parecer -> sumarizador
    # (desenhadas em coordenadas de figura para atravessar eixos distintos)
    def seta(origem_eixo, destino_eixo):
        p1 = origem_eixo.get_position()
        p2 = destino_eixo.get_position()
        origem_xy = ((p1.x0 + p1.x1) / 2, p1.y0)
        destino_xy = ((p2.x0 + p2.x1) / 2, p2.y1)
        arrow = FancyArrowPatch(
            origem_xy, destino_xy, transform=fig.transFigure,
            arrowstyle="-|>", mutation_scale=10, color=COR_DESTAQUE_SUAVE, linewidth=1.1,
        )
        fig.add_artist(arrow)

    seta(eixo_imagem, eixo_sumario)
    seta(eixo_abcd, eixo_sumario)
    seta(eixo_menzies, eixo_sumario)
    seta(eixo_spcl, eixo_sumario)

    legenda = (
        f"Modelo: {MODELO} | Condição: {CONDICAO.upper()} | Lesão: {LESION_ID} (imagem {IMAGE_ID}) | "
        "call_status=\"ok\" nos 4 registros (ABCD, Menzies, SPCL, sumarizador), mesma janela de ~11 s "
        "(2026-11-16, 22:41:25–22:41:36 UTC). Execução real registrada, não demonstração sintética. "
        "O diagnóstico do sistema não constitui confirmação clínica."
    )
    fig.text(0.5, 0.015, legenda, ha="center", va="bottom", fontsize=TAMANHO_FONTE_NOTA, color=COR_TEXTO, wrap=True)

    fig.savefig(SAIDA_PDF)
    fig.savefig(SAIDA_PNG, dpi=300)


if __name__ == "__main__":
    montar_figura()
