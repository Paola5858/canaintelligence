# Especificação dos visuais

Inventário de cada visual das seis páginas, com a pergunta que ele responde, os campos, as medidas, a posição em pixels e a regra de cor.

## Estado da implementação

| Página | Desenho no canvas | Visuais em PBIR |
| --- | --- | --- |
| Visão geral | Redesenhada | **Migrada para a grade nova em JSON**. A verificação no Desktop de 29/10/2026 foi feita na grade antiga; a versão migrada ainda não foi reaberta |
| Evolução | Redesenhada | **Implementada em JSON**: cabeçalho, filtros, trilho, série, média mensal e comparação |
| Fontes | Redesenhada | **Implementada em JSON**, com faixa em duas séries e matriz. A faixa empilhada fica para o Desktop |
| Indicadores | Redesenhada | Implementada parcialmente: contrato, estatísticas e série. Falta a distribuição, que depende do grupo de faixas |
| Qualidade | Redesenhada | **Implementada em JSON**: trilho de resumo, dois gráficos e tabela de pendências |
| Detalhes | Redesenhada | **Implementada em JSON**: trilho de auditoria, contexto e tabela. Falta o botão Voltar |

Todas as páginas são geradas por script, que escreve um `visual.json` por visual em `definition/pages/<pagina>/visuals/<id>/`. O schema usado é `visualContainer/1.4.0` e ele é aceito pelo Desktop.

| Gerador | Páginas | Observação |
| --- | --- | --- |
| `scripts/build_visuals_page1.py` | Visão geral | Migrada para a biblioteca e para a grade nova. Limpa a pasta `visuals` antes de gerar, para não deixar arquivo órfão |
| `scripts/build_visuals_page2.py` | Evolução | Escrito no piloto, com helpers próprios |
| [scripts/build_visuals_pages.py](scripts/build_visuals_pages.py) | Fontes, Indicadores, Qualidade, Detalhes | Usa `scripts/pbir_lib.py` e confere estouro de página e sobreposição antes de sair |

O verificador de grade roda a cada geração: se um visual sair da página de 1440x810 ou cobrir outro, o script falha e imprime o par. Nenhum visual das páginas 3 a 6 foi gerado fora da grade.

O que está funcionando com dado real, confirmado na sessão do app:

- Cartões com 274, 23, 8 e 11/12/2026.
- Gráfico de linhas da Acidez Total plotando a série, com tooltip mostrando 9,58 mg/L em 05/07/2026.
- Barras horizontais de cobertura por fonte, com as 8 fontes.
- Segmentação de período em faixa de datas e duas segmentações em lista.
- Cabeçalho em caixa de texto com a marca e o nome da página.

### Dois desenhos no canvas

O canvas tem dois conjuntos de telas, e eles não são a mesma coisa:

- **Conjunto V2**, seis páginas, é o desenho de referência deste documento. Cada página analítica abre com um trilho de 300px que traz unidade, agregação, leituras e status do indicador. A ideia é impedir leitura errada de escala: PC e ArCana estão em percentual direto, UMIDADE_LAB em fração.
- **Variante V3**, apenas a Visão geral, inverte a ordem e coloca a cobertura por fonte antes da série, sem trilho, com faixa de contexto horizontal. Serve para comparar arquitetura, não para implementar.

As telas antigas (marcadas `01` a `06`) continuam no canvas como histórico do desenho anterior: abas com sublinhado, painéis de raio 18px e faixa de KPI sem cartão.

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

## Regras que valem nas seis páginas

- Rodapé em 24,750,1392,36 com a origem do dado, gerado em todas as páginas.
- Cartão de valor com título precisa de 120px de altura. Abaixo disso o Desktop corta o número, confirmado por captura em 29/10/2026.
- O rótulo de categoria do cartão fica desligado, porque repete o título e consome a área do valor.
- Trilho com mais de quatro itens não cabe em 514px com altura legível. Acima disso, dividir em colunas ou trocar por cartão de várias linhas.
- Segmentação só fecha com `objects.data[0].properties.mode = 'Dropdown'`. `general` e `selection` não têm efeito, testado no sandbox em 30/10/2026.
- `sortDefinition` dentro de `query` derruba o carregamento do relatório, sem detalhe no diálogo. Ordenação de tabela e matriz é manual, pelo menu da coluna.
- Tabela com coluna e medidas no mesmo `Values` renderiza só a coluna. Para cruzar dimensão com medida, usar matriz.
- `subTotals` não desliga a linha de total da matriz nesta versão. Desligar em Formatar visual, Subtotais.
- As medidas `Copias Exatas Preservadas` e `Dias sem Medicao` saíram do trilho da página Qualidade quando ele passou a quatro cartões. Continuam no modelo e podem voltar numa segunda coluna de trilho.

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
| 1.1 | Cabeçalho | Caixa de texto | 24,24,1392,48 | Marca, título "Visão geral", safra e carga do modelo | Nenhuma |
| 1.2 | Navegação | Navegador de páginas | 24,80,1392,44 | 6 páginas | Nenhuma |
| 1.3 | Período | Segmentação de dados (intervalo) | 24,152,320,40 | `Dim_Calendario[Data]` | Nenhuma |
| 1.4 | Fonte | Segmentação de dados (lista) | 360,152,200,44 | `Fato_Medicoes[Fonte]` | Nenhuma |
| 1.5 | Indicador | Segmentação de dados (lista) | 576,152,320,44 | `Dim_Indicador[Nome_Original]` | Nenhuma |
| 1.6 | Cobertura da base | 5 cartões abertos | 24,220 até 1413, 120 | Nenhum | `Dias com Dados`, `Registros Validados`, `Quantidade de Indicadores`, `Quantidade de Fontes`, `Ultima Data com Dados` |
| 1.7 | Trilho do indicador | 3 cartões empilhados | 24,356,300,112 cada, 16px de intervalo | `Dim_Indicador` no cartão de agregação e status | `Quantidade de Leituras`, `Rotulo Agregacao Recomendada`, `Status do Indicador` |
| 1.8 | Evolução diária | Gráfico de linhas | 340,356,684,378 | `Fato_Medicoes[Data]` no eixo | `Media Aritmetica Nao Ponderada` |
| 1.9 | Cobertura por fonte | Gráfico de barras horizontais | 1040,356,376,378 | `Fato_Medicoes[Fonte]` no eixo | `Quantidade de Registros` |
| 1.10 | Rodapé | Caixa de texto | 24,750,1392,36 | Origem do dado | Nenhuma |

**Altura de 120px na faixa:** o cartão do Desktop escala o valor sozinho. Com 92px o número era cortado na base, confirmado em captura da sessão de 29/10/2026. A fonte do cartão não controla esse dimensionamento.

**Botão Limpar filtros:** previsto no desenho em 1268,152, mas não gerado. Depende de ação de navegador sobre segmentações, que é configuração de Desktop.

**Estado vazio na abertura:** sem indicador selecionado na segmentação, a série diária fica vazia e os cartões de agregação e status mostram "(Em branco)". É consequência das medidas exigirem um indicador único, e não um defeito de layout. Selecionar um indicador preenche os três.

**Unidade no trilho:** o painel único do desenho virou quatro cartões, porque o Power BI não agrupa visuais em contêiner próprio. A unidade aparece no subtítulo do gráfico e no contrato da página Indicadores.

**Pergunta do visual 1.9:** como as leituras se distribuem no tempo e onde existem lacunas.
**Tooltip:** data, valor em mg/L, quantidade de leituras do dia.
**Regra de cor:** linha em `#4E7966` com área em `rgba(78,121,102,.075)`. Lacuna aparece como ausência, nunca como linha contínua.
**Por que linha e não coluna:** são 236 leituras em 244 dias, densidade alta demais para coluna.

**Pergunta do visual 1.10:** quem carrega a base.
**Tooltip:** fonte, registros, dias com dado.
**Regra de cor:** verde cana para frentes, sálvia para laboratório. Trilho de 8px em `#EFEDE5`.

---

## Página 2: Evolução

Pergunta da página: como o indicador muda no tempo e como o período atual se compara ao anterior?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 2.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 2.2 | Contrato do indicador | Trilho 300x514 | 24,220,300,514 | `Dim_Indicador[Nome_Original]`, `Unidade_Confirmada`, `Status_Validacao`, `Categoria` | `Quantidade de Leituras`, `Frentes com Dado do Indicador`, `Rotulo Agregacao Recomendada` |
| 2.3 | Série diária | Gráfico de linhas | 340,220,1076,286 | `Dim_Calendario[Data]` | `Media Aritmetica Nao Ponderada` |
| 2.4 | Média mensal | Gráfico de linhas com marcadores | 340,522,620,212 | `Dim_Calendario[Nome_Mes]` ordenado por `Numero_Mes` | `Media Aritmetica Nao Ponderada` |
| 2.5 | Comparação de períodos | 3 cartões | 976,522,440,212, 141 cada | Nenhum | `Media Aritmetica Nao Ponderada`, `Media do Periodo Anterior`, `Variacao Percentual vs Periodo Anterior` |
| 2.6 | Rodapé | Caixa de texto | 24,750,1392,36 | Origem do dado | Nenhuma |

**Pergunta do visual 2.3:** o indicador tem 237 leituras em 342 dias para ATR. Mostrar como pontos evita sugerir continuidade entre leituras distantes.
**Implementação:** gráfico de linhas, marcadores ligados, largura de linha 0 px e transparência da linha em 100%. Eixo y de 100 a 135.
**Tooltip:** data, valor em kg/t, leituras do dia.

**Pergunta do visual 2.4:** a média mensal se move, e quanto.
**Regra de eixo:** começa em 105 porque a série é uma linha, não coluna. Linha não codifica magnitude por área, então o eixo truncado não distorce.

**Pergunta do visual 2.5:** o período atual está acima ou abaixo do anterior, e em quanto.
**Regra:** quando não existe período anterior comparável, as três medidas ficam vazias. A tabela mostra "Dados insuficientes" nesse caso, nunca zero.

---

## Página 3: Fontes

Pergunta da página: as frentes de colheita se comportam de forma diferente para o mesmo indicador?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 3.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 3.2 | Contrato do indicador | Trilho 300x514 | 24,220,300,514 | `Dim_Indicador[Nome_Original]`, `Unidade_Confirmada`, `Status_Validacao` | `Frentes com Dado do Indicador`, `Rotulo Agregacao Recomendada` |
| 3.3 | Faixa observada | Gráfico de barras empilhadas | 340,220,420,514 | `Fato_Medicoes[Fonte]` | `Minimo Observado` e amplitude calculada |
| 3.4 | Comparação por fonte | Matriz | 776,220,640,514 | `Fato_Medicoes[Fonte]` | `Quantidade de Leituras`, `Dias com Dado da Fonte`, `Minimo Observado`, `Maximo Observado` |
| 3.5 | Nota do laboratório | Caixa de texto | 24,690,300,32 | Texto fixo | Nenhuma |

**Pergunta do visual 3.3:** onde as frentes se sobrepõem e onde alguma se separa.
**Por que faixa e não barra de média:** a média ponderada por TC está bloqueada. A faixa mostra mínimo e máximo observados, que são fatos, e deixa visível que as sete frentes se sobrepõem quase inteiras.
**Implementação:** duas séries em barras empilhadas horizontais. A primeira recebe `Minimo Observado` com cor igual ao fundo (invisível) e atua como base. A segunda recebe `Maximo Observado - Minimo Observado`. Eixo x de 104 a 132.
**Regra de cor:** segmento em `#4E7966`.

**Pergunta do visual 3.4:** qual é a cobertura exata de cada frente.
**Regra:** leituras por frente variam de 126 a 136. A tabela informa a contagem para que ninguém leia diferença pequena como superioridade operacional.
**Por que matriz e não tabela:** a tabela com coluna e medidas no mesmo `Values` descartou as quatro medidas e renderizou só `Fonte`, testado em 30/10/2026. A matriz renderiza tudo.
**Linha de total:** a matriz abre com `Total`. Desligar em Formatar visual, Subtotais, porque a propriedade `subTotals` do arquivo não foi aceita nesta versão. O total de `Dias com Dado da Fonte` soma dias entre fontes e não tem significado, então essa linha não pode ficar.

---

## Página 4: Indicadores

Pergunta da página: qual é o contrato do indicador e como os valores se distribuem?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 4.1 | Cabeçalho, navegação e filtros | Iguais à página 1 | 24,24 até 24,204 | | |
| 4.2 | Contrato do indicador | Trilho 300x514 | 24,220,300,514 | `Dim_Indicador[Codigo]`, `Nome_Padronizado`, `Unidade_Confirmada`, `Descricao_Confirmada`, `Observacoes_Tecnicas` | `Rotulo Agregacao Recomendada`, `Status do Indicador`, `Quantidade de Leituras` |
| 4.3 | Estatísticas | 5 cartões | 340,220,1076,96 | Nenhum | `Mediana do Indicador`, `Media Aritmetica Nao Ponderada`, `Minimo Observado`, `Maximo Observado`, `Rotulo Leituras` |
| 4.4 | Série temporal | Gráfico de linhas | 340,332,620,402 | `Dim_Calendario[Data]` | `Media Aritmetica Nao Ponderada` e `Media Movel 7 Dias` |
| 4.5 | Distribuição | Gráfico de colunas | 976,308,440,426 | Faixa de valor (grupo criado no Desktop) | `Quantidade de Leituras` |

**Pergunta do visual 4.5:** os valores se espalham de que forma.
**Estado:** o grupo de faixas não é criado por arquivo de definição nesta versão. O espaço de 976,308,440,426 recebe um aviso explicando a limitação e o procedimento manual. Não são usados bins globais, porque isso misturaria escalas incompatíveis quando o indicador muda.
**Implementação:** criar grupo sobre `Fato_Medicoes[Valor]` em Agrupar dados, com 14 intervalos iguais, e usar esse grupo no eixo do gráfico de colunas.
**Regra de cor:** coluna única em `#4E7966`. Não pintar faixa por posição na distribuição.
**Regra:** se o indicador selecionado for TC, este visual mostra a contagem por faixa e o aviso de unidade não confirmada, em vez de estatísticas agregadas.

**Tratamento de TC nesta página:** o cartão de média fica vazio, o de mediana também, e aparece a mensagem "Unidade não confirmada" com a referência `P_TC_01`. TC nunca é rotulado como tonelagem.

**Tratamento de pH:** a medida de média não existe para pH. O visual 4.3 usa `pH Mediana` rotulado como mediana. Não substituir por média aritmética.

---

## Página 5: Qualidade

Pergunta da página: o que está pendente, onde há lacuna e o que foi preservado?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 5.1 | Cabeçalho, navegação e filtros | Iguais à página 1, mais filtro de status | 24,24 até 24,204 | | |
| 5.2 | Resumo da base | 4 cartões empilhados | 24,220,300,120 cada, 8px de intervalo | Nenhum | `Quantidade de Registros`, `Registros Pendentes`, `Percentual de Registros Pendentes`, `Registros com Ajuste de Escala` |
| 5.3 | Registros por mês | Gráfico de colunas | 340,220,660,184 | `Dim_Calendario[Nome_Mes]` | `Quantidade de Registros` |
| 5.4 | Status de validação | Gráfico de barras horizontais | 1016,220,400,184 | `Fato_Medicoes[Status_Validacao]` | `Quantidade de Registros` |
| 5.5 | Pendências | Tabela | 340,420,1076,314 | `Pendencias_Validacao[ID_Pendencia, Indicador, Problema, Acao_Recomendada, Status]` | Nenhuma |

**Pergunta do visual 5.3:** a coleta é uniforme ao longo do ano.
**Regra:** colunas a partir de zero. É a leitura que mostra janeiro a março e dezembro com 11 indicadores e cerca de 8 dias, contra abril a novembro com 23 indicadores e mês cheio. Sálvia nos meses em que só as frentes mediram, verde cana nos meses com laboratório, com legenda nomeando os dois.
**Tooltip:** registros, dias com dado, indicadores disponíveis no mês.

**Pergunta do visual 5.4:** como a base se divide entre validado, normalizado e pendente.
**Regra de cor:** validado `#4E7966`, normalizado `#A8B9A0`, pendente `#C17A4A`. Vermelho não é usado, porque pendência não é erro comprovado.

**Pergunta do visual 5.5:** o que está travado e o que já foi resolvido.
**Regra:** quatro linhas, altura de 51px para permitir duas linhas de texto, sem reticências. "Resolvida na fato, aberta no legado" precisa aparecer inteiro, senão o significado muda.

---

## Página 6: Detalhes

Pergunta da página: qual é o registro exato, seu valor original e a regra aplicada?

| # | Visual | Tipo nativo | Posição (x,y,w,h) | Campos | Medidas |
| --- | --- | --- | --- | --- | --- |
| 6.1 | Cabeçalho, navegação e filtros | Iguais à página 1, mais botão Voltar | 24,24 até 24,204 | | |
| 6.2 | Contexto do recorte | 5 cartões | 340,220,1076,96 | `Dim_Indicador[Nome_Original]`, `Unidade_Confirmada` | `Rotulo Registros`, `Rotulo Ajustes de Escala`, `Status do Indicador`, `Primeira Data com Dados`, `Ultima Data com Dados` |
| 6.3 | Registros | Tabela | 340,332,1076,402 | `ID_Registro`, `Data`, `Fonte`, `Valor`, `Valor_Original`, `Ajuste_Aplicado`, `Status_Validacao` | Nenhuma |
| 6.4 | Rastreabilidade | Trilho 300x514 | 24,220,300,514 | `ID_Registro` selecionado | `Valor Original do Registro`, `Fator Aplicado do Registro`, `Regra de Transformacao do Registro` |

**Pergunta do visual 6.3:** qual linha exata gerou o número que estou olhando.
**Regra:** ordenar por data decrescente e fonte. Destacar a linha selecionada pela seleção cruzada, não por cor fixa.
**Coluna de ajuste:** mostrar o texto de `Ajuste_Aplicado`, não um ícone.

**Pergunta do visual 6.4:** de onde veio a transformação desse registro.
**Regra:** quando o registro não tem linha em `Auditoria_Dados`, as medidas ficam vazias. Não preencher com "sem transformação", porque ausência de auditoria não prova ausência de ajuste.
**Botão Voltar:** visível no cabeçalho. Drill-through sem volta prende o leitor.

---

## Visuais proibidos neste projeto

| Visual | Motivo |
| --- | --- |
| Pizza e rosca | Comparação de parte com todo exige denominador claro, e nenhum indicador aqui tem |
| Medidor | Não existe meta na fonte, então o arco não tem escala de referência |
| Mapa | A base não tem coordenada, município nem regional |
| Árvore de decomposição | Nenhuma hierarquia além de ano, mês e dia |
| Previsão | Não há série longa o suficiente e o brief não pede previsão |

## Diferenças entre o desenho e a implementação nativa

| Desenho | Implementação | Motivo |
| --- | --- | --- |
| Raio de 24px nos painéis | Raio de 12px no tema | O Power BI não aplica raio maior que 12px em todos os contêineres |
| Sombra difusa nos painéis | Sem sombra, borda hairline | O Desktop não reproduz a sombra do desenho; a borda mantém a separação |
| Faixa de KPI como painel único | 5 cartões sem borda e sem fundo | Não existe contêiner de faixa |
| Trilho do indicador como um painel | Cartões e caixa de texto posicionados no mesmo bloco | O Power BI não agrupa visuais em um contêiner próprio |
| Marca em SVG | Imagem no cabeçalho | O símbolo é exportado como PNG e inserido como imagem |

O desenho de referência está em `.kombai/canvas/cana-intelligence.canvas`, com as seis páginas do conjunto V2, e a variante V3 da Visão geral.
