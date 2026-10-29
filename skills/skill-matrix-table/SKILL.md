---
name: skill-matrix-table
description: Regras para matriz de comparação e tabela de detalhe por registro no relatório Cana Intelligence, incluindo alinhamento numérico, largura de coluna e ordenação.
---

# Matriz e tabela

## Quando usar matriz

Matriz existe quando existe **duas dimensões e pelo menos uma medida**, e o leitor precisa cruzar linha com coluna. Exemplo deste projeto: fonte por indicador.

Se só existe uma dimensão, é tabela. Matriz com uma dimensão é tabela com passos extras.

## Quando usar tabela

Tabela é para **rastreabilidade**: cada linha é um registro identificável, e o leitor precisa de valor original, status e chave.

## Largura das colunas

| Tipo de coluna | Alinhamento | Largura |
| --- | --- | --- |
| Nome, rótulo, texto | Esquerda | A maior do bloco |
| Número | Direita | Mínima que caiba o maior valor, mais 16px |
| Data | Esquerda ou direita, mas sempre igual na coluna | 100px para `dd/mm/yyyy` |
| Chave, ID | Direita quando numérica, esquerda quando texto | 84px |
| Status | Esquerda, com ponto de 6px | 130px |

Regra de ouro: **número à direita, texto à esquerda, e nunca misturar na mesma coluna.**

## Cabeçalho

- Altura 40px.
- 14px, peso 600, `#76817B`.
- Borda inferior hairline `rgba(37,49,45,0.12)`.
- Nunca abreviar por falta de espaço. Ajustar a largura, não o nome.
- Unidade no cabeçalho quando todas as linhas compartilham a mesma: "Leituras", "Dias com dados", "Mínimo (kg/t)".

## Linhas

- Altura 32px para uma linha de texto, 36 a 40px quando a célula quebra em duas.
- Sem linha de grade vertical. Só horizontal, em `#EDEAE2`.
- Zebra opcional em `#FBFAF6`, nunca em cor saturada.
- Texto completo. Reticências que mudam o significado são proibidas: "Resolvida na Fato, aberta no legado" precisa aparecer inteiro.

## Números

- Algarismos tabulares obrigatórios.
- Separador de milhar e vírgula decimal, conforme pt-BR.
- Duas casas quando o indicador tem duas casas na origem. Não arredondar para inteiro "para ficar limpo".
- Número vazio aparece como vazio, não como `0` nem como `-`.

## Totais

- Total só quando a soma tem significado. Somar `Valor` de indicadores diferentes é proibido.
- Total de contagem é seguro: leituras, registros, fontes.
- Total de percentual não existe como soma. Se precisar, é média ponderada, e a ponderação está bloqueada neste projeto.

## Ordenação

- Detalhe: data decrescente, depois fonte.
- Matriz de comparação: por valor quando é ranking, por nome quando é presença.
- Nunca deixar a ordem padrão do Power BI decidir. Ordem padrão produz leitura aleatória.

## Interação

- Selecionar uma linha de tabela pode filtrar outro visual da mesma página.
- Drill-through a partir de tabela é permitido, desde que os campos de drill estejam declarados.
- Não configurar a tabela para filtrar visuais de outra página, porque a seleção se perde na navegação e o leitor não sabe mais o que está aplicado.

## Checklist

- [ ] Forma certa: matriz só com duas dimensões
- [ ] Número à direita, texto à esquerda
- [ ] Cabeçalho com unidade quando ela é comum às linhas
- [ ] Texto completo, sem reticência que altere o sentido
- [ ] Algarismos tabulares
- [ ] Vazio diferente de zero
- [ ] Ordenação explícita
- [ ] Nenhum total sem significado
