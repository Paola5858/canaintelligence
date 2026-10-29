# Plano de teste e resultados

Data de referência dos resultados: 29/10/2026.

## Resumo

| Suite | Verificações | Aprovadas | Falhas | Executada |
| --- | --- | --- | --- | --- |
| `tests/test_data_contract.py` | 47 | 47 | 0 | Sim |
| `tests/test_model_structure.py` | 31 | 31 | 0 | Sim |
| `tests/test_report_structure.py` | 43 | 43 | 0 | Sim |
| `tests/test_tmdl_parser.py` (parser oficial do Power BI) | 1 | 1 | 0 | Sim |
| Total automatizado | 122 | 122 | 0 | Sim |
| Abertura do relatório no Power BI Desktop | 1 | 1 | 0 | Sim, em 29/10/2026 |
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
| Medidas | 55 medidas, toda referência entre colchetes existe, todas com pasta de exibição, medidas críticas com descrição |
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
Total: 7 tabelas, 55 medidas, 2 relacionamentos
```

O teste valida estrutura do modelo, não semântica de DAX. Expressão DAX com erro de lógica ou de tipo continua dependendo de execução no Desktop.

## O que não foi executado e por quê

### Abertura completa no Power BI Desktop

Executada em 29/10/2026, depois das duas correções. Resultado observado na sessão do Desktop, produto 2.157.879.0:

1. O projeto abre e o título da janela passa a `dashboard_cana`.
2. Nenhum snapshot de erro novo é gerado em `Power BI Desktop Store App`.
3. O modelo carrega, as 7 tabelas são avaliadas e as 55 medidas aparecem no painel de dados.
4. A lista de problemas do relatório fica vazia, depois da correção de `reportVersionAtImport`.

O que o Desktop ainda não confirma por si só: se cada página tem a composição prevista, porque os visuais não foram montados. A abertura prova o arquivo, não o desenho.

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

Não executadas, porque os visuais ainda não existem no projeto. Ver checklist em [RUNBOOK.md](RUNBOOK.md#checklist-de-aceite-do-relatorio).

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
