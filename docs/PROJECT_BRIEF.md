# Brief do projeto

## Objetivo

Entregar um projeto Power BI editável (PBIP) que permita analisar os indicadores de qualidade de uma usina sucroenergética sem esconder as limitações da base de origem.

O projeto tem quatro compromissos, nesta ordem:

1. Integridade dos dados e leitura correta da unidade de cada indicador.
2. Modelo dimensional e medidas que não inventem agregação.
3. Relatório com densidade analítica e leitura rápida.
4. Rastreabilidade do que foi feito, com testes executáveis.

## O que existe hoje

- Planilha `data/Base_Usina_PowerBI_Final_v4.xlsx` com 6 abas, 19.532 medições e 23 indicadores.
- Projeto PBIP `dashboard_cana.pbip` com modelo semântico em TMDL e relatório.
- Seis páginas definidas, um tema visual próprio e 55 medidas.
- Duas suites de teste executáveis, com 78 verificações no total.

## Escopo funcional

| Página | Pergunta que responde |
| --- | --- |
| Visão geral | Qual é a cobertura da base e como o indicador selecionado se comporta no tempo? |
| Evolução | Como o indicador muda no tempo e como o período atual se compara ao anterior? |
| Fontes | As frentes de colheita se comportam de forma diferente para o mesmo indicador? |
| Indicadores | Qual é o contrato do indicador (unidade, agregação, status) e como os valores se distribuem? |
| Qualidade | O que está pendente, onde há lacuna de calendário e quais registros foram preservados? |
| Detalhes | Qual é o registro exato, seu valor original e a regra de transformação aplicada? |

## Decisões de escopo que mudam o desenho

**Safra e ano não viram filtro.** A base tem um único valor de safra (`2026/2027`) e um único ano (`2026`). Um seletor de valor único não filtra nada, então a safra aparece como texto no cabeçalho.

**Frentes e laboratório não se comparam.** As 7 frentes medem 11 indicadores de cana; o laboratório mede 12 indicadores de processo. Não existe um único indicador medido pelos dois grupos, e a janela do laboratório é menor (abril a novembro contra o ano inteiro).

**Nenhum indicador é o protagonista industrial.** A base não tem volume de cana, produção, produtividade nem meta. O destaque da Visão geral é a cobertura da base, com exploração por indicador.

**Ponderação por TC está bloqueada.** Dez indicadores recomendam média ponderada por TC, e TC não tem unidade nem regra confirmadas. O modelo não calcula média ponderada. Onde a tela precisa de um valor, ele aparece como média aritmética declarada não ponderada.

## Fora de escopo

- Metas, limites aceitáveis, faixas de qualidade e classificação de desempenho: a fonte não define nenhum.
- Mapas, medidores e gráficos de pizza.
- Previsão ou linha de tendência apresentada como resultado.
- Publicação no Power BI Service. O projeto é local.

## Critério de conclusão

O projeto está concluído quando abre no Desktop, o modelo atualiza, as seis páginas têm visuais conforme a especificação e os testes passam. O estado de cada item está registrado em [TEST_PLAN.md](TEST_PLAN.md).
