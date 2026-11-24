"""Identidade visual compartilhada das figuras de revisao (Acoes de figuras, 2026-11-20).

Importado por fig2_s0_s1_s2.py e fig3_multiagente_exemplo.py (figuras
compostas com matplotlib). Os arquivos .dot (fig1 e fig4) nao podem
importar Python; a mesma paleta/tipografia esta documentada em
README.md para ser replicada manualmente nos atributos DOT.

Este modulo so define constantes e aplica rcParams -- nao executa nada
por si so, nao faz I/O, nao depende de nenhum dado do projeto.
"""

import matplotlib as mpl

# Paleta discreta (nao saturada), com contraste suficiente em fundo
# branco. O vermelho do contorno (255,0,0) NAO faz parte desta paleta:
# e mantido exatamente como no artefato real (ver docs/reconstruction/
# 19_s0_s1_s2_preparation.md paragrafo sobre draw_contour), nao e uma
# escolha de identidade visual.
COR_TEXTO = "#2B2B2B"
COR_FUNDO_PAINEL = "#F7F6F4"
COR_BORDA_PAINEL = "#8C8C8C"
COR_DESTAQUE_SUAVE = "#4C6B8A"       # azul acinzentado discreto (links/arrows)
COR_ALERTA_SUAVE = "#8A5A3A"         # marrom/terracota discreto (notas de ressalva/fidelidade)
COR_CONTORNO_REAL = (255 / 255, 0, 0)  # vermelho puro do artefato real -- nao mexer

FONTE_FAMILIA = "DejaVu Sans"  # disponivel por padrao no matplotlib, sem dependencia extra
TAMANHO_FONTE_BASE = 9
TAMANHO_FONTE_TITULO = 11
TAMANHO_FONTE_NOTA = 7.5

LARGURA_MAX_POL = 15.5 / 2.54  # 15,5 cm == largura maxima de pagina assumida, em polegadas


def aplicar_estilo_comum():
    """Aplica rcParams compartilhados. Chamar uma vez no topo de cada script de figura."""
    mpl.rcParams.update(
        {
            "font.family": FONTE_FAMILIA,
            "font.size": TAMANHO_FONTE_BASE,
            "text.color": COR_TEXTO,
            "axes.edgecolor": COR_BORDA_PAINEL,
            "axes.labelcolor": COR_TEXTO,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.dpi": 300,
            "pdf.fonttype": 42,  # fontes como texto selecionavel no PDF, nao como curvas
            "ps.fonttype": 42,
        }
    )
