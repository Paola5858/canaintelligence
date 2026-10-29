# Especificação dos visuais

Inventário de cada visual das seis páginas, com a pergunta que ele responde, os campos, as medidas, a posição em pixels e a regra de cor.

## Estado da implementação

| Página | Estado |
| --- | --- |
| Visão geral | **Implementada em JSON** e verificada no Desktop em 29/10/2026 |
| Evolução, Fontes, Indicadores, Qualidade, Detalhes | Sem visuais |

A página 1 foi gerada por `scripts/build_visuals_page1.py`, que escreve um `visual.json` por visual em `definition/pages/<pagina>/visuals/<id>/`. O schema usado é `visualContainer/1.4.0` e ele é aceito pelo Desktop.

O que está funcionando com dado real, confirmado na sessão do app:

- Cartões com 274, 23, 8 e 11/12/2026.
- Gráfico de linhas da Acidez Total plotando a série, com tooltip mostrando 9,58 mg/L em 05/07/2026.
- Barras horizontais de cobertura por fonte, com as 8 fontes.
- Segmentação de período em faixa de datas e duas segmentações em lista.
- Cabeçalho em caixa de texto com a marca e o nome da página.

### Limites encontrados ao escrever PBIR na mão

1. **Unidades de exibição não são configuráveis por JSON nesta versão.** Cinco variações foram testadas no cartão de `Registros Validados` (`labels.displayUnits`, `calloutValue.displayUnits`, `values.displayUnits`, com literais `1D`, `1L` e `'None'`) e nenhuma alterou o resultado: 16.823 continua aparecendo como "17 Mil". O mesmo vale para rótulo de dados do gráfico de barras, que mostra "1,5 Mil". Correção manual, uma vez por visual: Formatar visual, Valor da chamada, Unidades de exibição, Nenhuma.
2. **Segmentação em lista suspensa não fecha por JSON.** As propriedades `mode` nos objetos `data` e `general` não foram aplicadas; a segmentação renderiza como lista. Solução provisória: listas com altura suficiente para mostrar os itens. Ajuste fino no Desktop: Formatar visual, Configurações da segmentação, Estilo, Lista suspensa.
3. **O cartão moderno (`cardVisual`) não renderizou** com o mesmo binding que o cartão clássico aceita. Ficou no clássico.
4. **Aplicar formato por visual é pouco confiável.** Título e subtítulo funcionaram em `visualContainerObjects`; propriedades dentro de `objects` tiveram efeito inconsistente. Por isso o grosso do estilo vive no tema.

Conclusão do piloto: gerar visuais por JSON funciona e vale a pena para posição, campos e título, que é o que dá trabalho de refazer. Acabamento fino de formatação continua sendo trabalho de Desktop, e está listado como passo manual.

O passo a passo está em [RUNBOOK.md](RUNBOOK.md#montar-os-visuais).

Página de 1440 x 810 px. Todas as posições abaixo usam esse sistema.

## Mapa de páginas

```text
┌──────────────────────────────────────────────────────────────┐
│ cabeçalho 24,24 1392x48                                      │
├──────────────────────────────────────────────────────────────┤
│ navegação 24,80 1392x44                                      │
├──────────────────────────────────────────────────────────────┤
│ filtros 24,140 1392x64                                       │
├──────────────────────────────────────────────────────────────┤
│ conteúdo 24,220 até 734                                      │
├──────────────────────────────────────────────────────────────┤
│ rodapé 24,750 1392x36                                        │
└──────────────────────────────────────────────────────────────┘
```

## Convenções de interação

| Regra | Aplicação |
| --- | --- |
| Filtro de período | Sincronizado nas seis páginas, intervalo 01/01/2026 a 31/12/2026 |
| Slicer de Fonte | Sincronizado nas páginas Visão geral, Evolução, Fontes e Detalhes |
| Seletor de indicador | Sincronizado entre Visão geral, Evolução, Fontes e Indicadores |
| Drill-through | Qualquer visual com dados leva a Detalhes, filtrando Data, Fonte e Indicador |
| Drill-up | Desligado. Não existe hierarquia de data modelada além de ano, mês e dia |
| Interação entre visuais | Padrão de destaque. Nenhum visual é configurado como filtro, exceto a matriz de Fontes, que filtra a tabela da mesma página |

---

## Página 1: Visão geral

Pergunta da página: qual é a cobertura da base e como o indicador selecionado se comporta no tempo?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 1.1 | Cabeçalho | Caixa de texto | 24,24,1392,48 | Marca, título "Visão geral", safra e data de carga | Nenhuma |
| 1.2 | Navegação | Navegador de páginas | 24,80,1392,44 | 6 páginas | Nenhuma |
| 1.3 | Período | Segmentação de dados (intervalo) | 24,152,320,40 | `Dim_Calendario[Data]` | Nenhuma |
| 1.4 | Fonte | Segmentação de dados (lista) | 348,152,212,40 | `Fato_Medicoes[Fonte]` | Nenhuma |
| 1.5 | Limpar filtros | Botão | 1268,152,148,40 | Ação de limpar segmentações | Nenhuma |
| 1.6 | Cobertura da base | 5 cartões | 24,220,1392,88 | Nenhum | `Dias com Dados`, `Registros Validados`, `Quantidade de Indicadores`, `Quantidade de Fontes`, `Ultima Data com Dados` |
| 1.7 | Indicador | Segmentação de dados | 24,336,300,40 | `Dim_Indicador[Nome_Original]` | Nenhuma |
| 1.8 | Contrato do indicador | 4 cartões | 348,336,1068,40 | `Dim_Indicador[Unidade_Confirmada]`, `Status do Indicador` | `Quantidade de Leituras` |
| 1.9 | Evolução diária | Gráfico de linhas com marcadores | 24,412,896,322 | `Fato_Medicoes[Data]` no eixo | `Media Aritmetica Nao Ponderada` |
| 1.10 | Cobertura por fonte | Gráfico de barras horizontais | 936,412,480,322 | `Fato_Medicoes[Fonte]` no eixo | `Quantidade de Registros` |
| 1.11 | Rodapé | Caixa de texto | 24,750,1392,36 | Fonte do arquivo, pendências, link para Qualidade | `Registros Pendentes`, `Indicadores Pendentes` |

**Pergunta do visual 1.9:** como as leituras se distribuem no tempo e onde existem lacunas.
**Tooltip:** data, valor em mg/L, quantidade de leituras do dia.
**Regra de cor:** linha em `#4E7966`. Lacuna aparece como ausência, nunca como linha contínua.
**Por que linha e não coluna:** são 236 leituras em 244 dias, densidade alta demais para coluna.

**Pergunta do visual 1.10:** quem carrega a base.
**Tooltip:** fonte, registros, dias com dado.
**Regra de cor:** verde cana para frentes, sálvia para laboratório.

---

## Página 2: Evolução

Pergunta da página: como o indicador muda no tempo e como o período atual se compara ao anterior?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 2.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 2.2 | Contexto do indicador | Segmentação e cartões | 24,220,1392,64 | `Dim_Indicador[Nome_Original]`, `Dim_Indicador[Unidade_Confirmada]` | `Quantidade de Leituras`, `Dias com Dado da Fonte`, `Rotulo Agregacao Recomendada`, `Status do Indicador` |
| 2.3 | Aviso de ponderação | Caixa de texto com ícone | 1160,232,256,40 | Texto fixo condicionado | `Rotulo Agregacao Recomendada` |
| 2.4 | Série diária | Gráfico de linhas com marcadores | 24,300,1392,266 | `Dim_Calendario[Data]` | `Media Aritmetica Nao Ponderada` |
| 2.5 | Média mensal | Gráfico de linhas com marcadores | 24,582,896,152 | `Dim_Calendario[Nome_Mes]` ordenado por `Numero_Mes` | `Media Aritmetica Nao Ponderada` |
| 2.6 | Comparação de períodos | Tabela | 936,582,480,152 | Rótulo de período | `Media do Periodo Anterior`, `Variacao Absoluta vs Periodo Anterior`, `Variacao Percentual vs Periodo Anterior` |

**Pergunta do visual 2.4:** o indicador tem 237 leituras em 342 dias. Mostrar como pontos evita sugerir continuidade entre leituras distantes.
**Implementação:** gráfico de linhas, marcadores ligados, largura de linha 0 px e transparência da linha em 100%. Eixo y de 100 a 135.
**Tooltip:** data, valor em kg/t, leituras do dia.

**Pergunta do visual 2.5:** a média mensal se move, e quanto.
**Regra de eixo:** começa em 105 porque a série é uma linha, não coluna. Linha não codifica magnitude por área, então o eixo truncado não distorce.

**Pergunta do visual 2.6:** o período atual está acima ou abaixo do anterior, e em quanto.
**Regra:** quando não existe período anterior comparável, as três medidas ficam vazias. A tabela mostra "Dados insuficientes" nesse caso, nunca zero.

---

## Página 3: Fontes

Pergunta da página: as frentes de colheita se comportam de forma diferente para o mesmo indicador?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 3.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 3.2 | Contexto | Segmentação e cartões | 24,220,1392,64 | `Dim_Indicador[Nome_Original]` | `Frentes com Dado do Indicador`, `Status do Indicador` |
| 3.3 | Faixa observada | Gráfico de barras empilhadas | 24,300,520,434 | `Fato_Medicoes[Fonte]` | `Minimo Observado` e amplitude calculada |
| 3.4 | Matriz de comparação | Matriz | 560,300,856,434 | `Fato_Medicoes[Fonte]` | `Quantidade de Leituras`, `Dias com Dado da Fonte`, `Primeiro dado`, `Ultimo dado`, `Minimo Observado`, `Maximo Observado` |
| 3.5 | Nota do laboratório | Caixa de texto | 24,690,520,32 | Texto fixo | Nenhuma |

**Pergunta do visual 3.3:** onde as frentes se sobrepõem e onde alguma se separa.
**Por que faixa e não barra de média:** a média ponderada por TC está bloqueada. A faixa mostra mínimo e máximo observados, que são fatos, e deixa visível que as sete frentes se sobrepõem quase inteiras.
**Implementação:** duas séries em barras empilhadas horizontais. A primeira recebe `Minimo Observado` com cor igual ao fundo (invisível) e atua como base. A segunda recebe `Maximo Observado - Minimo Observado`. Eixo x de 104 a 132.
**Regra de cor:** segmento em `#4E7966`.

**Pergunta do visual 3.4:** qual é a cobertura exata de cada frente.
**Regra:** leituras por frente variam de 126 a 136. A matriz informa a contagem para que ninguém leia diferença pequena como superioridade operacional.

---

## Página 4: Indicadores

Pergunta da página: qual é o contrato do indicador e como os valores se distribuem?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 4.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 4.2 | Contrato | Segmentação e cartões | 24,220,1392,96 | `Dim_Indicador[Codigo]`, `Nome_Padronizado`, `Unidade_Confirmada`, `Descricao_Confirmada`, `Observacoes_Tecnicas` | `Rotulo Agregacao Recomendada`, `Status do Indicador`, `Quantidade de Leituras` |
| 4.3 | Estatísticas | 5 cartões | 24,332,1392,72 | Nenhum | `Mediana do Indicador`, `Minimo Observado`, `Maximo Observado`, `Quantidade de Leituras` e a medida de média quando aprovada |
| 4.4 | Série temporal | Gráfico de linhas | 24,420,896,314 | `Dim_Calendario[Data]` | `Media Aritmetica Nao Ponderada` e `Media Movel 7 Dias` |
| 4.5 | Distribuição | Gráfico de colunas | 936,420,480,314 | Faixa de valor (grupo criado no Desktop) | `Quantidade de Leituras` |

**Pergunta do visual 4.5:** os valores se espalham de que forma.
**Implementação:** não existe histograma nativo. Criar grupo sobre `Fato_Medicoes[Valor]` em Agrupar dados, com 14 intervalos iguais, e usar esse grupo no eixo do gráfico de colunas.
**Regra:** se o indicador selecionado for TC, este visual mostra a contagem por faixa e o aviso de unidade não confirmada, em vez de estatísticas agregadas.

**Tratamento de TC nesta página:** o cartão de média fica vazio, o de mediana também, e aparece a mensagem "Unidade não confirmada" com a referência `P_TC_01`. TC nunca é rotulado como tonelagem.

**Tratamento de pH:** a medida de média não existe para pH. O visual 4.3 usa `pH Mediana` rotulado como mediana. Não substituir por média aritmética.

---

## Página 5: Qualidade

Pergunta da página: o que está pendente, onde há lacuna e o que foi preservado?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 5.1 | Cabeçalho, navegação e filtros | Iguais à página 1, mais filtro de status | 24,24 até 24,204 | | |
| 5.2 | Resumo | 5 cartões | 24,220,1392,88 | Nenhum | `Quantidade de Registros`, `Registros Pendentes`, `Percentual de Registros Pendentes`, `Registros com Ajuste de Escala`, `Copias Exatas Preservadas` |
| 5.3 | Registros por mês | Gráfico de colunas | 24,324,896,160 | `Dim_Calendario[Nome_Mes]` | `Quantidade de Registros` |
| 5.4 | Status de validação | Gráfico de barras horizontais | 936,324,480,160 | `Fato_Medicoes[Status_Validacao]` | `Quantidade de Registros` |
| 5.5 | Pendências | Tabela | 24,500,1392,234 | `Pendencias_Validacao[ID_Pendencia, Indicador, Problema, Acao_Recomendada, Status]` | Nenhuma |

**Pergunta do visual 5.3:** a coleta é uniforme ao longo do ano.
**Regra:** colunas a partir de zero. É a leitura que mostra janeiro a março e dezembro com 11 indicadores e cerca de 8 dias, contra abril a novembro com 23 indicadores e mês cheio.
**Tooltip:** registros, dias com dado, indicadores disponíveis no mês.

**Pergunta do visual 5.4:** como a base se divide entre validado, normalizado e pendente.
**Regra de cor:** validado `#4E7966`, normalizado `#A8B9A0`, pendente `#C17A4A`. Vermelho não é usado, porque pendência não é erro comprovado.

**Pergunta do visual 5.5:** o que está travado e o que já foi resolvido.
**Regra:** quatro linhas, texto completo, sem reticências. "Resolvida na Fato, aberta no legado" precisa aparecer inteiro, senão o significado muda.

---

## Página 6: Detalhes

Pergunta da página: qual é o registro exato, seu valor original e a regra aplicada?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 6.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 6.2 | Contexto | Segmentação e cartões | 24,220,1392,64 | `Dim_Indicador[Nome_Original]`, `Dim_Indicador[Unidade_Confirmada]` | `Registros com Ajuste de Escala`, `Quantidade de Registros`, `Status do Indicador` |
| 6.3 | Tabela de registros | Tabela | 24,300,1016,434 | `ID_Registro`, `Data`, `Fonte`, `Valor`, `Valor_Original`, `Ajuste_Aplicado`, `Status_Validacao` | Nenhuma |
| 6.4 | Rastreabilidade | Cartões e caixa de texto | 1056,300,360,434 | `ID_Registro` selecionado | `Valor Original do Registro`, `Fator Aplicado do Registro`, `Regra de Transformacao do Registro`, `Status Anterior do Registro` |

**Pergunta do visual 6.3:** qual linha exata gerou o número que estou olhando.
**Regra:** ordenar por data decrescente e fonte. Destacar a linha selecionada pela seleção cruzada, não por cor fixa.
**Coluna de ajuste:** mostrar o texto de `Ajuste_Aplicado`, não um ícone.

**Pergunta do visual 6.4:** de onde veio a transformação desse registro.
**Regra:** quando o registro não tem linha em `Auditoria_Dados`, as quatro medidas ficam vazias. Não preencher com "sem transformação", porque ausência de auditoria não prova ausência de ajuste.

---

## Visuais proibidos neste projeto

| Visual | Motivo |
| --- | --- |
| Pizza e rosca | Comparação de parte com todo exige denominador claro, e nenhum indicador aqui tem |
| Medidor | Não existe meta na fonte, então o arco não tem escala de referência |
| Mapa | A base não tem coordenada, município nem regional |
| Árvore de decomposição | Nenhuma hierarquia além de ano, mês e dia |
| Previsão | Não há série longa o suficiente e o brief não pede previsão |

## Diferenças entre o desenho aprovado e a implementação nativa

| Desenho | Implementação | Motivo |
| --- | --- | --- |
| Raio de 18px nos painéis | Raio de 12px no tema | O Power BI não aplica raio maior que 12px em todos os contêineres |
| Faixa de KPI sem cartão | 5 cartões sem borda | Não existe contêiner de faixa; o efeito é obtido removendo borda e fundo dos cartões |
| Marca em SVG | Imagem no cabeçalho | O símbolo é exportado como PNG e inserido como imagem |

O desenho completo está em `.kombai/canvas/cana-intelligence.canvas`, com as seis páginas.
