# Dados de origem

## Como colocar a planilha

O arquivo `Base_Usina_PowerBI_Final_v4.xlsx` precisa estar nesta pasta, com este nome exato:

```text
data/Base_Usina_PowerBI_Final_v4.xlsx
```

Se o arquivo tiver outro nome, ajuste o parâmetro `CaminhoDaBase` em `dashboard_cana.SemanticModel/definition/expressions.tmdl`.

## Por que a planilha não está no Git

O arquivo tem 1,8 MB e conteúdo operacional de uma unidade industrial. Ele está no `.gitignore` por dois motivos:

1. Dado de processo não deve trafegar em repositório sem decisão explícita de quem é dono do dado.
2. O repositório fica pequeno e o histórico não carrega uma planilha nova a cada atualização.

Ao clonar o projeto em outra máquina, copie a planilha para cá. Sem ela, o modelo não atualiza e a suite de dados é marcada como não executada.

Se a decisão do projeto mudar e o arquivo passar a ser versionado, remova a linha `data/*.xlsx` do `.gitignore` e commite com uma mensagem que registre a decisão.

## Contrato de estrutura

A planilha precisa manter 6 abas, cada uma como tabela estruturada do Excel:

| Aba | Tabela estruturada | Linhas na versão atual | Papel |
| --- | --- | --- | --- |
| `Fato_Medicoes` | `tbl_Fato_Medicoes` | 19.532 | Uma linha por medição |
| `Dim_Indicador` | `tbl_Dim_Indicador` | 23 | Catálogo de indicadores |
| `Dim_Calendario` | `tbl_Dim_Calendario` | 365 | Calendário diário de 2026 |
| `Auditoria_Dados` | `tbl_Auditoria_Dados` | 1.585 | Histórico de normalização de escala |
| `Pendencias_Validacao` | `tbl_Pendencias_Validacao` | 4 | Pendências declaradas |
| `Resumo_Qualidade` | `tbl_Resumo_Qualidade` | 1 | Resumo oficial da carga |

Esses nomes foram lidos da planilha real. As consultas navegam pela tabela estruturada, então renomear uma tabela no Excel quebra a atualização com erro explícito de item não encontrado. Esse comportamento é intencional.

## Colunas obrigatórias na fato

`ID_Registro`, `Data`, `Fonte`, `Indicador_Codigo`, `Valor`, `Status_Validacao` são obrigatórias. As demais colunas consumidas pelo modelo são `Safra`, `Grupo_Fonte`, `Valor_Original`, `Ajuste_Aplicado`, `Duplicidade_Exata` e `Linha_Origem`.

## O que não fazer com a planilha

- Não alterar valores para "melhorar" o relatório.
- Não remover as 135 linhas marcadas como cópia exata. Elas são pares idênticos comprovados e foram preservadas por decisão registrada.
- Não preencher datas sem medição com valor zero.
- Não converter a fato para formato largo. O modelo depende do formato longo, com uma linha por medição.
