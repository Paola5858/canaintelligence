# Digest real da base — Base_Usina_PowerBI_Final_v4.xlsx

> Gerado por inspeção direta da planilha. Todos os números abaixo foram contados no arquivo, não estimados.

## Contagens confirmadas (Fato_Medicoes, formato longo)

- 19.532 registros / 1 linha = 1 medição
- 23 indicadores (23 códigos distintos, todos presentes em Dim_Indicador — zero órfãos)
- 8 fontes: 7 frentes de colheita + Laboratorio
- 2 grupos de fonte: "Frente de colheita" (9.932 reg) e "Laboratorio" (9.600 reg)
- 274 dias com dado, entre 2026-01-04 e 2026-12-11
- Calendário: 365 dias (2026-01-01 a 2026-12-31). 68 dias sem nenhuma medição dentro da janela
- Safra: **apenas 1 valor** ("2026/2027"). Ano: **apenas 1 valor** (2026) → filtro de safra/ano não tem o que filtrar
- Status: Validado 16.823 | Normalizado 1.806 | Pendente 903
- 1.585 linhas com ajuste de escala (PC e ArCana): 1.445 divisões por 10.000 e 140 por 1.000
- 135 cópias exatas preservadas (marcadas, não removidas)
- 903 registros pendentes = 4,62% da base; 1 indicador pendente de 23

## Cobertura por fonte (assimetria que impede comparação entre grupos)

| Fonte | Grupo | Registros | Dias | Indicadores | Janela |
|---|---|---|---|---|---|
| FRENTE 11 | Frente de colheita | 1.496 | 159 | 11 | 06/01 a 11/12 |
| FRENTE 12 | Frente de colheita | 1.496 | 152 | 11 | 06/01 a 11/12 |
| FRENTE 13 | Frente de colheita | 1.396 | 150 | 11 | 04/01 a 11/12 |
| FRENTE 14 | Frente de colheita | 1.386 | 149 | 11 | 04/01 a 11/12 |
| FRENTE 23 | Frente de colheita | 1.386 | 147 | 11 | 05/01 a 11/12 |
| FRENTE 31 | Frente de colheita | 1.386 | 145 | 11 | 04/01 a 11/12 |
| FRENTE 41 | Frente de colheita | 1.386 | 149 | 11 | 04/01 a 11/12 |
| Laboratorio | Laboratorio | 9.600 | 236 | 12 | 01/04 a 30/11 |

As 7 frentes medem os mesmos 11 indicadores de cana. O Laboratório mede 12 indicadores de processo que nenhuma frente mede. Não existe indicador medido pelos dois.

## Catálogo de indicadores (código, unidade, agregação recomendada na fonte, status)

Frentes de colheita:
- ATR — kg/t — média ponderada por TC — Validado — valores 104,0 a 131,3; média 117,23
- PC — % — média ponderada por TC — Normalizado — 10,32 a 13,21; média 11,74
- ArCana (AR) — % — média ponderada por TC — Normalizado — 0,53 a 0,67; média 0,60
- Pol — % — média ponderada por TC — Validado — 12,22 a 15,63; média 13,97
- Pureza — % — média ponderada por TC — Validado — 83,2 a 87,8; média 85,39
- Brix — % — média ponderada por TC — Validado — 14,57 a 17,93; média 16,35
- Fibra — % — média ponderada por TC — Validado — 11,70 a 13,49; média 12,44
- Umidade Cana (UMIDADE_CANA) — % — média ponderada por TC — Validado — 78,91 a 82,41; média 80,54
- IMP Min (IMP_MIN) — % — média ponderada por TC — Validado — 0,00 a 2,60; média 1,34
- IMP Veg (IMP_VEG) — % — média ponderada por TC — Validado — 0,07 a 9,98; média 4,96
- TC — unidade **Desconhecida** — agregação **pendente** — **Pendente** — 148,07 a 779,82

Laboratório:
- Acidez Total — mg/L — média aritmética — Validado — 6,50 a 11,49
- AM / Açúcares Redutores — % — média aritmética — Validado — 0,65 a 0,90
- Amido — ppm — média aritmética — Validado — 130 a 250
- Cinzas Solúveis — % — média aritmética — Validado — 0,07 a 0,13
- Condutividade — µS/m — média aritmética — Validado — 15,02 a 114,98
- Cor ICUMSA — UI — média aritmética — Validado — 700 a 1.050
- CV (Coeficiente de Variação) — % — média aritmética — Validado — 29,02 a 48,97
- Dextrana — ppm — média aritmética — Validado — 20 a 65
- pH — pH — **média logarítmica / ponderada** (não somar, não média simples) — Validado — 6,8 a 7,7
- Resíduo Insolúvel (RI) — mg/L — média aritmética — Validado — 270 a 439
- Teor Alcoólico — ° INPM — média aritmética — Validado — 92,9 a 93,4
- Umidade Laboratório (UMIDADE_LAB) — **fração (0-1)** — média aritmética — Validado — 0,055 a 0,125

## Armadilhas de escala que a interface precisa deixar explícitas

- PC e ArCana: armazenados **já em escala percentual** (11,71 significa 11,71%). Formatar com `%` sem multiplicar por 100. 1.585 linhas passaram por divisão por 1.000 ou 10.000 na origem.
- UMIDADE_LAB: fração decimal 0-1 (0,09 = 9%). UMIDADE_CANA: percentual direto (80,54 = 80,54%). Nunca combinar as duas numa mesma média.
- TC: unidade desconhecida e sem regra de agregação. Não pode virar KPI, não é tonelagem, não alimenta média ponderada.
- ACIDEZ é mg/L; PH é pH (escala log); TEOR_ALCOOLICO é ° INPM. Nenhum deles aceita soma.
- Não existe ATR/produtividade/tonelagem de cana como volume: só o indicador ATR em kg/t por frente.

## Série mensal real (média, frentes de colheita)

| Mês | ATR kg/t | PC % | Pureza % | IMP Veg % | Umidade Cana % | Brix % | Pol % | Fibra % |
|---|---|---|---|---|---|---|---|---|
| 1 | 116,94 | 11,704 | 85,30 | 4,79 | 80,60 | 16,32 | 13,95 | 12,44 |
| 2 | 116,88 | 11,701 | 85,31 | 4,86 | 80,44 | 16,31 | 13,94 | 12,41 |
| 3 | 117,27 | 11,734 | 85,33 | 4,61 | 80,57 | 16,34 | 13,98 | 12,43 |
| 4 | 112,83 | 11,276 | 85,14 | 4,61 | 80,63 | 16,28 | 13,89 | 12,46 |
| 5 | 113,03 | 11,302 | 85,13 | 4,80 | 80,63 | 16,27 | 13,87 | 12,47 |
| 6 | 115,45 | 11,542 | 85,24 | 4,91 | 80,68 | 16,36 | 13,92 | 12,50 |
| 7 | 116,80 | 11,688 | 85,30 | 4,86 | 80,59 | 16,38 | 13,93 | 12,46 |
| 8 | 119,92 | 12,019 | 85,46 | 5,04 | 80,56 | 16,39 | 14,02 | 12,42 |
| 9 | 121,22 | 12,152 | 85,54 | 5,20 | 80,50 | 16,40 | 14,03 | 12,38 |
| 10 | 120,92 | 12,128 | 85,55 | 5,18 | 80,52 | 16,41 | 14,04 | 12,36 |
| 11 | 116,87 | 11,698 | 85,43 | 5,06 | 80,45 | 16,36 | 14,00 | 12,39 |
| 12 | 118,09 | 11,824 | 85,38 | 4,72 | 80,63 | 16,31 | 13,99 | 12,40 |

Cobertura por mês: jan-mar e dez têm 11 indicadores e ~8 dias cada; abr-nov têm 23 indicadores e ~30 dias cada. Qualquer gráfico mensal precisa deixar isso visível, senão jan-mar parecem "queda".

## ATR por frente (média e leituras)

FRENTE 11: 118,40 / 136 leituras · FRENTE 12: 114,03 / 136 · FRENTE 13: 117,59 / 127 · FRENTE 14: 118,17 / 126 · FRENTE 23: 117,77 / 126 · FRENTE 31: 117,75 / 126 · FRENTE 41: 117,07 / 126

Quantidade de leituras por frente é diferente (126 a 136). Diferença de média não prova desempenho melhor.

## Pendências registradas na fonte (4)

- P_PC_01 · PC · escalas heterogêneas (x1, x1000, x10000) no legado · Resolvida na Fato / Aberta no Legado
- P_AR_01 · ArCana · variação de escala na recepção de cana · Resolvida na Fato / Aberta no Legado
- P_TC_01 · TC · definição técnica e unidade não confirmadas · Aberta
- P_UMB_01 · Umidade · UMIDADE_LAB exibida como fração · Documentada / Pronto para PBI

## Resumo oficial da fonte

Status_Base: "Pronto para Power BI (com ressalva de formatação e pendência técnica em TC)"
Transformações PC/ArCana: 1.585 · Duplicidades preservadas: 135
