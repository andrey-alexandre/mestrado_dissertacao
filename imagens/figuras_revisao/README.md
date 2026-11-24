# Figuras de revisão — fontes e geração

Entrega de **fontes editáveis** para 4 figuras novas, propostas pelo
pesquisador. Nada aqui foi executado, renderizado ou inspecionado
visualmente nesta tarefa — só os textos/código foram escritos. O
pesquisador deve rodar os comandos abaixo e inspecionar o resultado
antes de qualquer validação. Nenhum arquivo `.tex`, `.bib` ou figura
antiga (`imagens/Ch2`, `imagens/Ch3`, `imagens/Ch4`) foi tocado.

## Identidade visual comum

- `_estilo_comum.py`: paleta discreta, fonte legível, tamanhos e
  `rcParams` compartilhados pelos scripts Python (fig2 e fig3).
- Paleta: cinza-texto `#2B2B2B`, fundo de painel `#F7F6F4`, borda
  `#8C8C8C`, azul-acinzentado de destaque/setas `#4C6B8A`, terracota de
  nota/ressalva `#8A5A3A`. O vermelho puro do contorno (`255,0,0`) é
  mantido como está porque é o artefato real (parâmetro documentado de
  `draw_contour`), não uma escolha de identidade visual.
- Os arquivos `.dot` (figuras 1 e 4) não importam Python — replicam a
  mesma paleta manualmente nos atributos `color`/`fillcolor`/`fontcolor`,
  documentado nos comentários de cada `.dot`.
- Nenhuma figura depende só de cor para distinguir categorias: setas de
  reaproveitamento (fig. 1) usam traço tracejado além da cor; painéis
  (fig. 2/3) têm rótulo textual completo, não só cor de fundo.
- Largura assumida: ≤ 15,5 cm (compatível com largura de página A4 do
  modelo).

## Dependências

- Python 3.10+ com `matplotlib`, `numpy`, `Pillow` (`pip install matplotlib numpy pillow`).
- Graphviz (`dot`) instalado e no PATH — testado mentalmente contra a
  sintaxe do `dot` padrão (engine `dot`, não `neato`/`fdp`); confirmar a
  versão instalada ao renderizar.

## Comandos de geração (a rodar pelo pesquisador — nada disto foi executado aqui)

```bash
cd imagens/figuras_revisao

# Figura 1
dot -Tpdf fig1_desenho_experimental/fig1_desenho_experimental.dot -o fig1_desenho_experimental/fig1_desenho_experimental.pdf
dot -Tpng -Gdpi=300 fig1_desenho_experimental/fig1_desenho_experimental.dot -o fig1_desenho_experimental/fig1_desenho_experimental.png

# Figura 2
python fig2_s0_s1_s2/fig2_s0_s1_s2.py

# Figura 3 (duas etapas: 1. recorta a imagem real; 2. renderiza o fluxo)
cd fig3_multiagente_exemplo
python preparar_imagem_s2.py
dot -Tpdf fig3_multiagente_exemplo.dot -o fig3_multiagente_exemplo.pdf
dot -Tpng -Gdpi=300 fig3_multiagente_exemplo.dot -o fig3_multiagente_exemplo.png
cd ..

# Figura 4
dot -Tpdf fig4_cenario_uso/fig4_cenario_uso.dot -o fig4_cenario_uso/fig4_cenario_uso.pdf
dot -Tpng -Gdpi=300 fig4_cenario_uso/fig4_cenario_uso.dot -o fig4_cenario_uso/fig4_cenario_uso.png
```

Os scripts Python (fig2, e o preparo de imagem da fig3) já escrevem seus
arquivos diretamente (sem comando extra) na própria pasta da figura.
**Importante para a Figura 3**: rode `dot` a partir de dentro da pasta
`fig3_multiagente_exemplo/` (como acima) para que o atributo `image=` do
`.dot` encontre `fig3_s2_panel_real.png` pelo caminho relativo — e rode
`preparar_imagem_s2.py` antes, senão esse PNG não existe ainda.

## Arquivos de saída esperados

| Figura | PDF | PNG | Outros |
|---|---|---|---|
| 1 | `fig1_desenho_experimental/fig1_desenho_experimental.pdf` | `fig1_desenho_experimental/fig1_desenho_experimental.png` | — |
| 2 | `fig2_s0_s1_s2/fig2_s0_s1_s2.pdf` | `fig2_s0_s1_s2/fig2_s0_s1_s2.png` | — |
| 3 | `fig3_multiagente_exemplo/fig3_multiagente_exemplo.pdf` | `fig3_multiagente_exemplo/fig3_multiagente_exemplo.png` | `fig3_multiagente_exemplo/fig3_s2_panel_real.png` (gerado por `preparar_imagem_s2.py`, insumo do `.dot`, não é a figura final) |
| 4 | `fig4_cenario_uso/fig4_cenario_uso.pdf` | `fig4_cenario_uso/fig4_cenario_uso.png` | — |

## Legendas propostas e posicionamento sugerido (proposta, inserção real fica para ação textual separada)

**Figura 1** — proposta de legenda: *"Visão geral do desenho
experimental: preparação independente da segmentação (ISIC2018 Task 1),
da CNN (BCN20000) e do sistema multiagente, e sua articulação apenas na
etapa de avaliação sobre as 3.000 lesões congeladas do HAM10000 e o
subconjunto complementar de 300 lesões."* Posição sugerida: substituta
futura de `fig:estrutura_geral` em `tex/materiaisMetodos.tex`, Seção
"Estrutura Geral da Pesquisa" (inserção em ação separada, não nesta).

**Figura 2** — proposta de legenda: *"Mesma lesão (HAM\_0000193, imagem
ISIC\_0027950, dx=akiec) nas três condições visuais do protocolo: S0
(imagem original), S1 (contorno da máscara de referência, uso
experimental) e S2 (contorno da máscara predita pelo segmentador). As
três são variantes paralelas da mesma imagem, não uma sequência de
processamento."* Posição sugerida: Seção de Segmentação ou Seção
"Avaliação Experimental" de `tex/materiaisMetodos.tex` (onde S0/S1/S2 são
definidas).

**Figura 3** — proposta de legenda: *"Exemplo real de execução do
sistema multiagente (modelo gemini-3.1-flash-lite, condição S2, lesão
HAM\_0000193/ISIC\_0027950): saída JSON real dos três pareceres (ABCD,
Menzies, Seven-Point Checklist) e a síntese produzida pelo agente
sumarizador a partir da imagem e dos três pareceres. Campos e excertos
reais (truncados com reticências onde indicado), com ressalva de
fidelidade sobre a extração automática da decisão final (ver texto)."*
Posição sugerida: Seção "Integração Multiagente e Consolidação
Diagnóstica" de `tex/materiaisMetodos.tex`, ou abertura do capítulo de
Resultados/Discussão qualitativa.

**Figura 4** — proposta de legenda: *"Cenário de uso proposto para o
sistema multiagente (condição S2), não validado com profissionais em
consulta: o médico fornece a imagem, o sistema apresenta o contorno
predito e os pareceres estruturados, e o médico interpreta a decisão,
a justificativa e eventuais limitações (incluindo indeterminação) na
condução clínica."* Posição sugerida: Conclusão ou Discussão (trabalhos
futuros/aplicação proposta), não na Metodologia — é um cenário
conceitual, não parte do desenho experimental.

## Registro de fontes e regras de seleção (figuras 2 e 3)

### Figura 2 — desvio assumido na seleção do caso

Regra pedida: *primeiro caso, na ordem do manifesto complementar de 300
lesões, com os artefatos necessários e máscara predita não vazia.*

- Pela ordem estrita de linha do manifesto
  (`experiments/multiagent/local_300_s2_subset/local_300_s2_subset_manifest.csv`),
  a 1ª linha é `HAM_0000019`/`ISIC_0025396`, com `status_s2=disponivel`
  no manifesto de preparação
  (`experiments/multiagent/s0_s1_s2_preparation_manifest.csv`) — ou
  seja, a máscara S2 não é vazia, segundo o pipeline original.
- Porém os arquivos de pixel dessa lesão
  (`experiments/multiagent/s0_s1_s2_images/{s0,s1,s2}/ISIC_0025396_s{0,1,2}.png`)
  **não existem nesta máquina/sessão** — os caminhos gravados no
  manifesto são absolutos de outra máquina (Mac), e
  `docs/reconstruction/19_s0_s1_s2_preparation.md` já registra que os
  PNGs individuais de S2 "ainda não foram copiados para este
  repositório/máquina". As imagens brutas do HAM10000 e as máscaras de
  referência também não estão acessíveis aqui (caminho documentado em
  `D:/Andrey/Mestrado/dataverse_files/...` não resolve neste ambiente).
- Só existem localmente 5 composições de exemplo já renderizadas, em
  `experiments/multiagent/s0_s1_s2_images/examples/`: `ISIC_0024579`,
  `ISIC_0027950`, `ISIC_0030114` (uma das 6 lesões com máscara S2 vazia
  — excluída por regra), `ISIC_0031922`, `ISIC_0032854`. Checado nesta
  sessão: só `ISIC_0027950` (`HAM_0000193`) pertence também ao manifesto
  complementar de 300 lesões (linha 13, ou seja, a 12ª linha de dados);
  as outras 3 não pertencem a esse subconjunto.
- **Decisão (desvio assumido, não silencioso):** usar `ISIC_0027950` /
  `HAM_0000193` — o primeiro caso da ordem do manifesto complementar
  para o qual os artefatos reais estão de fato recuperáveis neste
  ambiente de trabalho, com máscara S2 não vazia. Não foi escolhido por
  estética do contorno nem por acerto diagnóstico (`dx=akiec`,
  não-melanoma, não influenciou a escolha). Esta mesma justificativa
  está no cabeçalho de `fig2_s0_s1_s2.py` e repetida na nota da própria
  figura.
- Artefato reaproveitado (não reconstruído): o composto PNG real já
  enviado aos modelos,
  `experiments/multiagent/s0_s1_s2_images/examples/ISIC_0027950_s0_s1_s2_example.png`,
  gerado pela função documentada `draw_contour` (cor `(255,0,0)`,
  espessura 3px, `cv2.RETR_EXTERNAL`+`cv2.CHAIN_APPROX_SIMPLE`, sem
  anti-aliasing — `docs/reconstruction/19_s0_s1_s2_preparation.md` §3).
  O script só recorta e re-rotula essa imagem; não há reconstrução a
  partir de pixels/máscaras cruas.

### Figura 3 — registro de origem e ressalva de fidelidade

- Reaproveita a mesma lesão da Figura 2 (`ISIC_0027950`/`HAM_0000193`),
  condição S2.
- Modelo escolhido: `gemini-3.1-flash-lite` — primeiro modelo
  multiagente na ordem determinística já documentada no protocolo para
  desempate (CNN → Gemini → GPT → Qwen3-VL → MedGemma, usada em
  `docs/reconstruction/34_consolidated_dissertation_status_report.md`,
  Análise 6) — escolhido pela ordem, não pelo resultado.
- Fonte: `experiments/multiagent/full_scale_matrix/gemini-3.1-flash-lite/call_log_main.jsonl`,
  4 registros (`diagnostic_abcd`, `diagnostic_menzies`,
  `diagnostic_spcl`, `summary`) com `lesion_id`/`image_id`/`model_name`/
  `condition` idênticos, `call_status: "ok"` nos 4, timestamps
  consecutivos entre `2026-11-16T22:41:25` e `2026-11-16T22:41:36` UTC
  (identificados nesta sessão nas linhas 36–39; identificação
  definitiva é pelos campos, não pelo número de linha, caso o arquivo
  cresça por append).
- Texto completo de cada parecer e da síntese, sem nenhum corte, está
  em `fig3_multiagente_exemplo/fig3_textos_completos.md`. A figura só
  mostra excertos marcados com `(...)`; nenhuma palavra foi reescrita.
- **Ressalva de fidelidade (destacada na própria figura, não só na
  legenda):** o texto bruto do sumarizador termina com a linha literal
  `decisao_final: indeterminado`, mas os campos estruturados do mesmo
  registro são `classified_status_v2="negativo"`,
  `decision_status="field_absent"`, `decisao_final=null` (campo
  parseado) — o extrator automático não capturou esse valor. A leitura
  mais plausível, apoiada em
  `docs/reconstruction/22_final_answer_extraction_preprocessing.md`
  (que documenta, para outros casos reais da mesma família de
  extrator, um mecanismo de "última ocorrência de vocabulário fechado
  vence", mesmo dentro de frases que descrevem divergência e não um
  veredito), é que a palavra "benigna" na frase de conclusão ("...como
  benigna...") foi capturada antes da linha final com o rótulo
  "indeterminado" (fora do vocabulário fechado buscado). Isto é
  reportado como leitura plausível apoiada em documentação existente,
  **não como reexecução confirmada do extrator sobre este registro
  específico**. Os valores brutos (`negativo`/`field_absent`) não foram
  alterados nem corrigidos nesta tarefa.

## Revisão pós-entrega (2026-11-20, pelo coordenador)

Após sua conferência visual, dois ajustes foram pedidos e aplicados:

1. **Acentuação**: os arquivos `.dot` (figuras 1 e 4) haviam sido escritos
   sem acentos (ASCII puro, por cautela de codificação do subagente) —
   todos os rótulos renderizados foram reescritos com acentuação correta
   em português. Os scripts Python (figuras 2 e 3) já usavam acentos
   corretamente.
2. **Travessão duplo (`--`)**: trocado por hífen simples (`-`) em todos os
   textos renderizados (títulos, rótulos de nó, legendas) nas quatro
   figuras. Ocorrências de `--` só em comentários de código (divisórias
   `/* --- */`) foram deixadas como estão, por não aparecerem na figura
   renderizada.
3. **Figura 3 redesenhada**: a primeira versão (grade matplotlib 3x3 com
   texto denso e setas cruzando entre eixos) foi reportada como "muito
   embolada". Substituída por um fluxo Graphviz horizontal
   (esquerda→direita, no estilo de figuras de pipeline de extração por
   LLM): imagem S2 real → 3 pareceres em paralelo → sumarizador → nota de
   ressalva de fidelidade à parte (ligação tracejada, fora do fluxo
   principal) → nota de rastreabilidade no rodapé. O script Python antigo
   (`fig3_multiagente_exemplo.py`) foi removido; a extração da imagem real
   do composto agora é um passo separado e mínimo
   (`preparar_imagem_s2.py`, só recorte de imagem, sem composição de
   figura), e o Graphviz (`fig3_multiagente_exemplo.dot`) embute esse PNG
   via atributo `image=`. Os textos/excertos e a ressalva de fidelidade em
   si não mudaram de conteúdo — só o layout.
4. **Pendência nova por causa do redesenho**: a proporção real (largura
   x altura) do recorte do painel S2 não foi conferida nesta sessão (nada
   foi executado); o `.dot` assume um nó quase-quadrado
   (`width=1.9; height=1.9`, polegadas). Se o recorte real for bem mais
   largo que alto (ou vice-versa), ajustar esses dois valores em
   `fig3_multiagente_exemplo.dot` após rodar `preparar_imagem_s2.py` e
   observar as dimensões reais impressas pelo script.
5. **Segunda revisão da Figura 3 (ainda neste dia)**: os três pareceres
   (ABCD, Menzies, SPCL) deixaram de ser uma frase corrida resumindo a
   conclusão e passaram a ser blocos JSON reais — chaves e valores
   literais dos campos de `raw_response_text` de cada agente (fonte
   monoespaçada, uma linha por campo), não mais uma paráfrase da ideia
   geral. Os nomes de campo (`assimetria`, `bordas`, `cor`, `estruturas`,
   `explicacao` no ABCD; `positivas`/`negativas` aninhados e `explicacao`
   no Menzies; os 7 critérios + `explicacao` no SPCL) são os nomes reais
   do schema, lidos do log, não inventados. Valores longos (sobretudo
   `explicacao`) continuam truncados com `(...)`, nunca reescritos —
   texto integral inalterado em `fig3_textos_completos.md`. O agente
   sumarizador permanece como texto real (não JSON), pois seu registro de
   log real não é JSON estruturado nesta execução (é texto narrativo com
   a linha final `decisao_final: indeterminado` — ver ressalva de
   fidelidade já documentada). Não renderizado/conferido visualmente
   nesta sessão.
6. **Terceira revisão da Figura 3 (ainda neste dia)**: o item 5 acima foi
   corrigido — o sumarizador também passou a ser um bloco JSON. O
   registro de log real desse papel é, de fato, uma lista Python contendo
   um dicionário (`[{'type': 'text', 'text': ..., 'extras': {'signature':
   ...}}]`) — o formato de *content block* bruto devolvido pelo provedor,
   não uma invenção deste script. O campo `"text"` (truncado com `(...)`)
   usa o mesmo excerto já citado antes; `extras.signature` é mostrado como
   `"(opaco, omitido)"`, por ser telemetria/assinatura do provedor, não
   conteúdo de raciocínio (mesma observação já registrada em
   `fig3_textos_completos.md`). A ressalva de fidelidade sobre
   `decisao_final` continua igual, ligada a esse novo bloco JSON. Também
   removi o nó de legenda da imagem que ficava ao lado dela (alongando a
   figura) — a identificação da imagem (`ISIC_0027950`/`HAM_0000193`) foi
   incorporada à nota de rastreabilidade, agora no mesmo rank/coluna da
   caixa do sumarizador, no rodapé logo abaixo dela. Não
   renderizado/conferido visualmente nesta sessão.

## Pendências concretas (não resolvidas, não inventadas)

1. **Remoção da legenda antiga embutida no composto (figuras 2 e 3):**
   o script usa uma fração fixa do topo do painel
   (`FRACAO_TOPO_LEGENDA_ANTIGA = 0.055`) para cortar a legenda
   "S0 -- ISIC\_0027950" etc. já embutida no PNG original. Isso não foi
   confirmado visualmente nesta sessão (nenhuma execução foi feita) —
   o pesquisador deve conferir, ao rodar o script, se o corte remove a
   legenda antiga por completo sem cortar parte da imagem da lesão; se
   não, ajustar essa constante.
2. **Detecção de gutter por brilho de coluna:** o corte horizontal dos
   3 painéis do composto (figuras 2 e 3) usa detecção de colunas quase
   brancas (`média > 250`) próximas de 1/3 e 2/3 da largura. Não foi
   testado em execução real; se o composto tiver textura de fundo não
   totalmente branca no gutter, o corte pode cair ligeiramente
   deslocado — conferir visualmente após renderizar.
3. **Fonte "Helvetica" nos arquivos `.dot`:** assume-se que o Graphviz
   local tenha uma fonte compatível com o nome `Helvetica` (fallback
   comum do Graphviz para uma sans-serif do sistema). Se o resultado
   renderizado usar uma fonte visualmente destoante do `DejaVu Sans`
   das figuras matplotlib, trocar `fontname` nos `.dot` para
   `"DejaVu Sans"` (mesma família usada em `_estilo_comum.py`) para
   manter a identidade visual verdadeiramente unificada entre `.dot` e
   `.py`.
4. **Figura 1 não foi comparada lado a lado com a imagem antiga**
   (`imagens/Ch3/eraser_diagram.png`) além da leitura textual já feita
   em ação anterior — o pesquisador deve conferir se o novo diagrama
   cobre tudo que considera essencial antes de autorizar a troca futura
   de `fig:estrutura_geral`.
5. **Ressalva de fidelidade da Figura 3 (seção acima)** é uma leitura
   plausível, não uma confirmação de causa — mantida como ressalva
   explícita na própria figura e não como fato resolvido.
6. Nenhum arquivo foi executado nesta tarefa: PDFs/PNGs listados acima
   ainda não existem até o pesquisador rodar os comandos. "Entregue" =
   fontes escritas; não = renderizado/validado.
