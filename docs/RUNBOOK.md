# Runbook

Como abrir, atualizar, validar e dar manutenção no projeto.

## Pré-requisitos

- Power BI Desktop instalado. O projeto foi escrito para o formato PBIP com modelo semântico TMDL, suportado nas versões atuais.
- Python 3.10 ou superior, com `pandas` e `openpyxl`, apenas para rodar auditoria e testes. O relatório não depende de Python.
- A planilha `data/Base_Usina_PowerBI_Final_v4.xlsx`.

## Primeira abertura

1. Confirme que a planilha está em `data/` com o nome exato.
2. Abra `dashboard_cana.pbip` no Power BI Desktop.
3. O Desktop mostra o modelo e o relatório como itens separados. Se aparecer aviso sobre caminho de arquivo, siga a seção de atualização de caminho.
4. Verifique se as seis páginas aparecem nesta ordem: Visão geral, Evolução, Fontes, Indicadores, Qualidade, Detalhes.
5. Abra a exibição de modelo e confirme os dois relacionamentos: `Dim_Calendario[Data]` para `Fato_Medicoes[Data]` e `Dim_Indicador[Codigo]` para `Fato_Medicoes[Indicador_Codigo]`.

Se o Desktop recusar o arquivo, o erro estará no TMDL. O primeiro suspeito é formatação de propriedade com aspas, que já foi checada por teste, e o segundo é a ordem de declaração de coluna e partição. Rode `python tests/test_model_structure.py` antes de editar nada.

## Atualizar o caminho da planilha

O caminho existe em um único lugar.

1. No Desktop, abra Transformar dados, Início, Gerenciar parâmetros.
2. Selecione `CaminhoDaBase` e ajuste para o caminho da sua máquina.
3. Ou edite direto `dashboard_cana.SemanticModel/definition/expressions.tmdl` e reabra o projeto.

Depois de alterar, rode `python tests/test_model_structure.py`. Ele falha se alguém cravar caminho absoluto dentro de uma consulta.

## Atualizar os dados

1. Substitua a planilha em `data/`.
2. No Desktop, Atualizar.
3. As abas precisam manter os nomes das tabelas estruturadas: `tbl_Fato_Medicoes`, `tbl_Dim_Indicador`, `tbl_Dim_Calendario`, `tbl_Auditoria_Dados`, `tbl_Pendencias_Validacao`, `tbl_Resumo_Qualidade`, e as mesmas colunas.
4. Se uma coluna esperada desaparecer, a consulta falha com erro explícito de coluna não encontrada. Isso é intencional: falhar alto é melhor que carregar dado errado em silêncio.
5. Rode `python tests/run_tests.py` e confira se as contagens esperadas mudaram de propósito.

## Montar os visuais

As páginas existem vazias. A ordem de montagem recomendada segue a dependência entre visuais.

Por página:

1. Abra a página no Desktop.
2. Aplique o plano de fundo `#F7F6F0` se o tema ainda não aplicou.
3. Insira primeiro os elementos estruturais: caixa de texto do cabeçalho, navegador de páginas, segmentações de dados.
4. Depois os cartões e as medidas.
5. Por último os gráficos.

Use [VISUAL_SPECIFICATION.md](VISUAL_SPECIFICATION.md) para posição, tamanho, campos e medidas de cada visual. As posições em pixels assumem a página de 1440 x 810.

Configurações que precisam ser feitas no Desktop, porque não são expressáveis no TMDL:

- Sincronização de segmentação de dados entre páginas, no painel Sincronizar segmentações.
- Drill-through para a página Detalhes, arrastando Data, Fonte e Indicador para o campo de drill-through.
- Grupo de faixas para o histograma da página Indicadores: selecionar `Valor`, Agrupar dados, 14 intervalos.
- Séries invisíveis do gráfico de faixa observada, na página Fontes.

## Checklist de aceite do relatório

Execute depois de montar os visuais.

| Item | Como verificar |
| --- | --- |
| As 6 páginas existem e navegam | Clicar em cada aba do navegador |
| Nenhum visual cortado ou sobreposto | Olhar cada página com a resolução final |
| Filtro de período funciona | Mudar o intervalo e ver os cartões reagirem |
| Slicer de Fonte funciona | Filtrar FRENTE 11 e conferir que laboratório desaparece |
| Laboratório não aparece vazio na página Fontes | Selecionar um indicador de laboratório |
| TC aparece como pendente | Selecionar TC na página Indicadores |
| Nenhum visual sugere meta | Não deve existir linha de meta nem faixa de aceitável |
| Tooltip mostra unidade e leitura | Passar o mouse em um ponto da série |
| Página Qualidade distingue pendência de erro | A cor de pendente é cobre, não vermelho |
| Rodapé aponta a fonte dos dados | Ler o texto do rodapé |

## Publicar

O projeto é local. Se for publicar no Power BI Service:

1. Confirme a política de dados da usina antes de enviar a planilha para a nuvem.
2. Considere trocar a origem de arquivo local por um gateway ou por uma fonte versionada.
3. O parâmetro `CaminhoDaBase` deixa de fazer sentido no Service. Trocar por uma origem acessível ao gateway.

## Manutenção

### Adicionar um indicador novo

1. O indicador precisa chegar na planilha, na aba da fato e na `Dim_Indicador`.
2. Rodar `python scripts/data_audit.py` para ver a faixa, a unidade e o status.
3. Se a unidade for confirmada, criar a medida nomeada em `_Medidas.tmdl` com o formato correto, no padrão dos existentes.
4. Se a unidade não for confirmada, não criar medida de valor. Criar apenas o aviso.
5. Se a agregação recomendada depender de TC, não implementar ponderação.
5. Atualizar `docs/DATA_DICTIONARY.md` e [MEASURES_CATALOG.md](MEASURES_CATALOG.md).
6. Rodar `python tests/run_tests.py`. O teste de estrutura reprova medida referenciada que não existe.

### Corrigir uma pendência

Quando `P_TC_01` for resolvida:

1. Atualizar unidade e agregação de TC na `Dim_Indicador`.
2. Mudar o status de TC de Pendente para Validado.
3. Criar a medida de TC com o formato da unidade confirmada.
4. Implementar a ponderação por TC nos 10 indicadores que a recomendam, com o peso documentado.
5. Atualizar a tabela de pendências e o rodapé do relatório.
6. Revisar as páginas Visão geral, Evolução, Fontes e Indicadores, que hoje avisam sobre o bloqueio.

### Problemas comuns

| Sintoma | Causa provável | Ação |
| --- | --- | --- |
| Desktop não abre o projeto | Erro de sintaxe no TMDL | Rodar a suite de estrutura e ler o primeiro erro |
| Consulta falha com coluna não encontrada | Planilha trocada com cabeçalho diferente | Conferir os nomes das colunas na aba |
| Consulta falha com item não encontrado | Tabela estruturada removida no Excel | Recriar a tabela nomeada com o nome esperado |
| Cartão mostra número gigante | Alguém somou `Valor` sem medida | Usar medida do catálogo, nunca arrastar `Valor` com soma |
| Percentual aparece 1.171% | Formato padrão aplicado em escala direta | Usar `0.00"%"` na medida |
| Mês aparece em ordem alfabética | `sortByColumn` perdido | Conferir `Nome_Mes` ordenado por `Numero_Mes` |

## Git

O repositório está inicializado. A planilha não é versionada, por ser dado operacional. Ver [data/README.md](../data/README.md).

Antes de commitar:

```powershell
python tests/run_tests.py
git status
```

Se a suite falhar, não commitar.
