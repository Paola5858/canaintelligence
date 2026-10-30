# Plano de teste e resultados

Data de referência dos resultados: 29/10/2026.

## Resumo

| Suite | Verificações | Aprovadas | Falhas | Executada |
| --- | --- | --- | --- | --- |
| `tests/test_data_contract.py` | 47 | 47 | 0 | Sim |
| `tests/test_model_structure.py` | 31 | 31 | 0 | Sim |
| `tests/test_report_structure.py` | 43 | 43 | 0 | Sim |
| `tests/test_report_grid.py` | 419 | 419 | 0 | Sim |
| `tests/test_report_fields.py` | 192 | 192 | 0 | Sim |
| `tests/test_tmdl_parser.py` (parser oficial do Power BI) | 1 | 1 | 0 | Sim |
| Total automatizado | 733 | 733 | 0 | Sim |
| Abertura do relatório no Power BI Desktop | 2 | 2 | 0 | Sim, em 29/10/2026 (antes e depois da migração da grade) |
| Execução de DAX | 0 | 0 | 0 | **Não** |
| Renderização de visuais | 0 | 0 | 0 | **Não** |

```powershell
python tests/run_tests.py
```

Nenhum teste foi marcado como aprovado sem execução correspondente.

## Suite de contrato de dados

Executa leitura real da planilha e confere as afirmações em que o modelo se apoia.

| Grupo | O que verifica |
| --- | --- |
| Contagem | Fato com 19.532 linhas, dimensão com 23, resumo oficial igual à entrada e à saída |
| Chaves | `ID_Registro` único, `Codigo` único, uma linha por data no calendário, zero órfão nos dois sentidos |
| Nulos e tipos | Colunas-chave sem nulo, `Valor` numérico, `Data` como data e não como texto |
| Calendário | Cobre o início e o fim da fato, contínuo em 365 dias, sem lacuna, mês ordena por número |
| Escalas | PC entre 10 e 20, ArCana entre 0 e 2, nenhum percentual multiplicado por 100, UMIDADE_LAB entre 0 e 1, UMIDADE_CANA entre 70 e 90 |
| TC | 903 leituras, unidade Desconhecida e status Pendente em todas, agregacão pendente na dimensão |
| Status | Apenas três valores conhecidos, soma fechando o total, pendentes iguais a TC |
| Duplicidades | 135 preservadas e cada uma com par idêntico comprovado |
| Auditoria | Todos os IDs existem na fato, ID único, quantidade de ajustes igual à quantidade de linhas da auditoria |
| Fontes | 8 fontes, 11 indicadores nas frentes, 12 no laboratório, interseção vazia |
| Pendências | 4 registradas, `P_TC_01` aberta |
| Safra e ano | Um único valor em cada, o que confirma que não servem como filtro |

## Suite de estrutura do modelo

Não substitui abrir o projeto, mas pega os erros que impedem a abertura.

| Grupo | O que verifica |
| --- | --- |
| Indentação | Nenhuma linha TMDL começa com espaço |
| Tabelas | As 7 tabelas existem, todas com partição de importação e colunas |
| Tipos | `dataType` declara apenas tipos válidos de TMDL |
| Relacionamentos | Dois relacionamentos, todos os extremos existem, a fato é sempre o lado muitos |
| Dimensões | `Data` e `Codigo` marcadas como chave, calendário marcado como tabela de data, `Nome_Mes` ordenado por `Numero_Mes` |
| Lineage tags | Nenhuma repetida, todas as tabelas e colunas com tag |
| Medidas | 61 medidas, toda referência entre colchetes existe, todas com pasta de exibição, medidas críticas com descrição |
| Guardas | Média genérica exige indicador único e agregação aprovada, comparação temporal devolve vazio quando não há período |
| Formatos | Percentual direto em `0.00"%"`, UMIDADE_LAB em `0.0%`, ATR em `0.00" kg/t"` |
| Fonte | Caminho centralizado no parâmetro, nenhum caminho absoluto cravado em consulta |

## Suite de estrutura do relatório

Confere a camada que o Power BI lê primeiro.

| Grupo | O que verifica |
| --- | --- |
| Cadeia de abertura | `.pbip` declara a pasta do relatório, `definition.pbir` aponta para o modelo, `definition.pbism` existe |
| Páginas | Seis páginas na ordem, toda página da ordem tem pasta e toda pasta está na ordem, sem repetição |
| Metadados de página | `name` igual ao nome da pasta, página em 1440 x 810, schema declarado |
| Nomes | Ordem exata: Visão geral, Evolução, Fontes, Indicadores, Qualidade, Detalhes |
| Tema | Tema personalizado declarado como SharedResources, base Fluent2 presente, ambos os arquivos existem em disco |
| Conteúdo do tema | Nome correto, paleta com oito cores começando no verde cana, verde floresta presente, sombra desligada, fundo marfim, classes de texto definidas |
| Documentação | Toda página do projeto aparece na especificação de visuais |

## Suite de grade dos visuais

Existe porque posição de visual não quebra a abertura do arquivo. O Desktop abre, a página renderiza e o gráfico fica em cima do outro. Nenhuma das outras suites olha para isso.

| Grupo | O que verifica |
| --- | --- |
| Identidade | Nome do arquivo igual ao nome da pasta, schema declarado, tipo de visual preenchido, nome único na página |
| Limites | Posição completa e inteira, visual dentro da largura e altura declaradas em `page.json`, sem coordenada negativa |
| Legibilidade | Largura mínima de 40px e altura mínima de 24px |
| Empilhamento | `z` único e `tabOrder` único por página |
| Sobreposição | Nenhum par de visuais se cruza, testado em todos os pares de cada página |
| Cobertura | Toda página da ordem tem `page.json` e pelo menos um visual |

Resultado atual: 424 verificações, 424 aprovadas, 6 páginas e 83 visuais. O teste não confere se o visual renderiza nem se o campo existe no modelo; isso continua com a suite de estrutura do modelo e com a abertura no Desktop.

O teste já pagou o custo: pegou um visual órfão na página Qualidade, sobra de uma geração anterior em que o trilho tinha seis cartões. O arquivo continuava na pasta e se sobrepunha ao cartão novo. A correção foi fazer todo gerador limpar a pasta `visuals` antes de escrever.

## Suite de campos dos visuais

A suíte de grade garante que o visual não se sobrepõe. Esta garante que ele aponta para algo que existe no modelo. Sem isso, o campo ausente só aparece quando o Desktop reclama, ou pior, o visual renderiza vazio sem explicar.

| Grupo | O que verifica |
| --- | --- |
| Entidade | Toda tabela citada em `Measure` ou `Column` existe no TMDL |
| Medida | Toda medida citada existe na tabela citada, lendo `measure` do arquivo `.tmdl` |
| Coluna | Toda coluna citada existe na tabela citada, lendo `column` do arquivo `.tmdl` |
| Consistência | O `queryRef` de cada projeção bate com `Tabela.Propriedade` |
| Cobertura | Existe pelo menos uma referência a campo nos 83 visuais |

Resultado atual: 192 verificações, 192 aprovadas, 83 visuais e 44 referências distintas a campos. O teste não confere tipo, formato nem semântica de DAX.

## Validação com o parser oficial do Power BI

`scripts/validate_tmdl.ps1` carrega a assembly `Microsoft.PowerBI.Tabular.dll` que vem com o Power BI Desktop, chama `TmdlSerializer.DeserializeModelFromFolder` sobre a pasta `definition` e reporta o resultado real.

Esse teste existe porque os testes estáticos não pegavam o defeito que mais importa: sintaxe que o parser recusa. Foi ele que reproduziu o erro de abertura relatado em 29/10/2026.

Resultado atual:

```text
PARSE OK
  Auditoria_Dados    | colunas=11 medidas=0
  Dim_Calendario     | colunas=9  medidas=0
  Dim_Indicador      | colunas=10 medidas=0
  Fato_Medicoes      | colunas=12 medidas=0
  Pendencias_Validacao | colunas=5 medidas=0
  Resumo_Qualidade   | colunas=7  medidas=0
  _Medidas           | colunas=1  medidas=55
  relacao: Fato_Medicoes[Data] -> Dim_Calendario[Data]
  relacao: Fato_Medicoes[Indicador_Codigo] -> Dim_Indicador[Codigo]
Total: 7 tabelas, 61 medidas, 2 relacionamentos
```

O teste valida estrutura do modelo, não semântica de DAX. Expressão DAX com erro de lógica ou de tipo continua dependendo de execução no Desktop.

## O que não foi executado e por quê

### Abertura completa no Power BI Desktop

Executada em 29/10/2026, depois das duas correções. Resultado observado na sessão do Desktop, produto 2.157.879.0:

1. O projeto abre e o título da janela passa a `dashboard_cana`.
2. Nenhum snapshot de erro novo é gerado em `Power BI Desktop Store App`.
3. O modelo carrega, as 7 tabelas são avaliadas e as 55 medidas aparecem no painel de dados.
4. A lista de problemas do relatório fica vazia, depois da correção de `reportVersionAtImport`.

O que o Desktop ainda não confirma por si só: se cada página tem a composição prevista. A abertura prova o arquivo, não o desenho.

Depois da migração da Visão geral para a grade nova, o projeto foi aberto outra vez em 29/10/2026 às 23:33. A janela subiu com o título `dashboard_cana` e a sessão não alterou nenhum arquivo do repositório. A composição da página migrada não foi conferida visualmente por quem escreveu este documento, então ela continua pendente de aceite.

### Execução de medidas DAX

Sem o modelo carregado, não há como executar DAX. Os valores abaixo foram calculados direto na planilha com Python, e servem de gabarito para conferência no Desktop.

| Medida | Valor esperado | Como conferir |
| --- | --- | --- |
| `Quantidade de Registros` | 19.532 | Cartão sem filtro |
| `Quantidade de Indicadores` | 23 | Cartão sem filtro |
| `Quantidade de Fontes` | 8 | Cartão sem filtro |
| `Dias com Dados` | 274 | Cartão sem filtro |
| `Primeira Data com Dados` | 04/01/2026 | Cartão sem filtro |
| `Ultima Data com Dados` | 11/12/2026 | Cartão sem filtro |
| `Registros Validados` | 16.823 | Somar com normalizados e pendentes deve dar 19.532 |
| `Registros Normalizados` | 1.806 | Idem |
| `Registros Pendentes` | 903 | Idem |
| `Percentual de Registros Pendentes` | 4,62% | 903 dividido por 19.532 |
| `Indicadores Validados` | 22 | Cartão sem filtro |
| `Indicadores Pendentes` | 1 | Cartão sem filtro |
| `Registros com Ajuste de Escala` | 1.585 | Igual à contagem da tabela `Auditoria_Dados` |
| `Copias Exatas Preservadas` | 135 | Cartão sem filtro |
| `Dias no Calendario da Janela` | 342 | 04/01 a 11/12 |
| `Dias sem Medicao` | 68 | 342 menos 274 |
| `Cobertura de Calendario` | 80,1% | 274 dividido por 342 |
| `ATR Medio` sem filtro | 117,23 kg/t | Indicador ATR selecionado |
| `PC Medio` | 11,74% | Indicador PC selecionado |
| `ArCana Medio` | 0,60% | Indicador ArCana selecionado |
| `Umidade Cana Media` | 80,54% | Indicador Umidade Cana selecionado |
| `Umidade Laboratorio Media` | 9,0% | Indicador Umidade Laboratorio selecionado |
| `Acidez Total Media` | 8,98 mg/L | Indicador Acidez Total selecionado |
| `pH Mediana` | 7,23 | Indicador pH selecionado |
| `Quantidade de Leituras` de ATR | 903 | Indicador ATR selecionado |
| `Frentes com Dado do Indicador` de ATR | 7 | Indicador ATR selecionado, nenhuma fonte filtrada |
| `Media do Periodo Anterior` de ATR, período 01/09 a 30/11/2026 | 117,52 kg/t | Período atual 119,25 kg/t, diferença +1,73 kg/t, variação +1,47% |

### Testes de contexto vazio e filtro

Não executados. Roteiro para o Desktop:

1. Selecionar um indicador do laboratório e filtrar Fonte = FRENTE 11. O resultado deve ser vazio, não zero, porque frente nenhuma mede indicador de laboratório.
2. Selecionar o período 01/01/2026 a 02/01/2026, que está dentro do calendário e fora da fato. `Quantidade de Registros` deve ser 0 e `Mensagem Sem Dados` deve aparecer.
3. Selecionar TC. Média e mediana devem ficar vazias, e o aviso de unidade não confirmada deve aparecer.
4. Comparar 01/01/2026 a 31/01/2026 com o período anterior. As medidas de variação devem ficar vazias, porque não existe período anterior dentro da janela.

### Renderização e interação

Três páginas foram conferidas por captura da janela do Desktop em 29/10/2026, com o projeto aberto e a página trocada por clique na aba: Visão geral, Evolução e Qualidade.

| Página | Observação | Resultado |
| --- | --- | --- |
| Visão geral | Faixa com 274, 23, 8 e 11/12/2026 | Confere |
| Visão geral | Registros validados | "17 Mil", abreviado por unidade de exibição |
| Visão geral | Trilho, série e cobertura | No lugar, sem sobreposição |
| Visão geral | Rodapé | Confere |
| Evolução | Trilho com quatro cartões | Valores inteiros, sem corte |
| Evolução | Série diária e média mensal | Vazias, porque nenhum indicador está selecionado |
| Evolução | Comparação de períodos em três cartões | Confere, rótulos em uma linha |
| Evolução | Rodapé | Confere |
| Qualidade | Trilho de resumo com quatro cartões | Valores inteiros: 20 Mil, 903, 4,62%, 1.585 |
| Qualidade | Registros por mês e status de validação | Plotam com dado real, sem filtro de indicador |
| Qualidade | Tabela de pendências | Renderiza, mas corta o texto e exige rolagem horizontal |
| Qualidade | Rodapé | Confere |

### Defeitos encontrados e corrigidos nesta revisão

| Defeito | Causa | Correção |
| --- | --- | --- |
| Números cortados na base dos cartões, nas três páginas | O cartão do Desktop escala o valor sozinho, e a altura de 72 a 92px não deixava área. O rótulo de categoria repetia o título e consumia mais espaço | `categoryLabels` desligado e altura mínima de 120px no cartão com título. Na Visão geral o trilho passou de quatro cartões de 88px para três de 112px |
| Rodapé ausente em cinco páginas | Só a Visão geral havia recebido o rodapé | `rodape_tela()` na biblioteca, chamado por todos os geradores |
| Comparação de períodos ilegível | Quatro colunas de medida em 440px geravam rolagem horizontal e nenhum valor | Três cartões de 141x212, com rótulos curtos |
| Visual órfão na Qualidade | O gerador não limpava a pasta `visuals`, e o sexto cartão antigo continuava lá | Todo gerador limpa a pasta antes de escrever. A suíte de grade reprovou o caso |

### Segunda rodada, Fontes, Indicadores e Detalhes

| Página | Observação | Resultado |
| --- | --- | --- |
| Fontes | Segmentações de data, indicador e grupo | Fechadas com seta, modo lista suspensa aplicado |
| Fontes | Cartão de leituras | 19.532 inteiro, sem "20 Mil" |
| Fontes | Matriz de comparação | Renderiza as quatro medidas, com linha de total a desligar no Desktop |
| Fontes | Faixa observada | Vazia, porque nenhum indicador está selecionado |
| Indicadores | Cinco cartões de estatística | Sem corte depois de subir para 96px |
| Indicadores | Série temporal | Largura cheia, vazia até selecionar indicador |
| Detalhes | Cinco cartões de contexto | 19.532, 1.585, 04/01/2026 e 11/12/2026 legíveis |
| Detalhes | Tabela de sete colunas | Cabe na largura, sem rolagem horizontal |

### Descobertas de 30/10/2026 no sandbox

| Propriedade | Teste | Resultado |
| --- | --- | --- |
| `labels.displayUnits` | Cartão com `1D` | Abreviado, sem efeito |
| `calloutValue.displayUnits` | Cartão com `1D` | Abreviado, sem efeito |
| `labels.displayUnits` literal `'None'` | Cartão | Abreviado, sem efeito |
| `precision` sozinho | Cartão | Abreviado, sem efeito |
| `general.mode` | Segmentação `Dropdown` | Lista aberta, sem efeito |
| `data.mode` | Segmentação `Dropdown` | **Funciona**, caixa fechada com seta |
| `selection.mode` | Segmentação `Dropdown` | Lista aberta, sem efeito |
| `data.mode` | Segmentação `List` e `Between` | Sem efeito |

A unidade de exibição virou solução por medida de texto, registrada em [MEASURES_CATALOG.md](MEASURES_CATALOG.md). A ordenação declarada em `sortDefinition` foi tentada e **derrubou o carregamento do relatório**, então voltou atrás e ficou manual.

### O que continua pendente de verificação visual

As seis páginas já foram abertas ao menos uma vez. O que falta é conferir cada uma depois da última geração, porque qualquer mudança no gerador muda o resultado. Ver checklist em [RUNBOOK.md](RUNBOOK.md#checklist-de-aceite-do-relatorio).

## Falhas encontradas durante a construção

| Momento | Falha | Correção |
| --- | --- | --- |
| Escrita do primeiro script de inspeção | Arquivo chamado `inspect.py` sombreou o módulo `inspect` da biblioteca padrão e quebrou o `import pandas` | Arquivo renomeado para `probe_xlsx.py` |
| Script de auditoria | `int()` aplicado a uma Series ao percorrer as fontes | Laço explícito por fonte |
| Teste de contrato | Comparava 365 linhas de calendário com uma lista de 12 meses | `drop_duplicates()` antes de comparar |
| Teste de estrutura | Acusava espaço na indentação dentro de expressão M, que é legítimo | Passou a checar só linha que começa com espaço |
| Teste de estrutura | Cobrava origem Excel da tabela `_Medidas`, que é sintética | Exceção documentada no teste |
| Catálogo de medidas | Três medidas com numeração de pasta inconsistente | Renumeração de 00 a 06 |
| Abertura no Power BI Desktop (29/10/2026) | `description:` usado como linha de propriedade em coluna e em medida. O TMDL recusa a chave inteira e o projeto não abre. Erro reproduzido localmente com `TmdlSerializer.DeserializeModelFromFolder` | As 45 descrições viraram comentários `///` acima de cada declaração, que é a forma da propriedade embutida |
| Teste de estrutura | Cobrava `description:` dentro do bloco da medida, que é justamente o formato inválido | Passou a exigir comentário `///` antes da declaração e a proibir a chave antiga |
| Segunda abertura (29/10/2026) | `customTheme` sem `reportVersionAtImport`. O Desktop recusa a definição do relatório com "A propriedade necessária reportVersionAtImport não foi incluída na propriedade /themeCollection/customTheme" | Propriedade adicionada, e o teste de estrutura do relatório passou a exigi-la |
