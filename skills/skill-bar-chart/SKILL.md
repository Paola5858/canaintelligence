---
name: skill-bar-chart
description: Regras para barras horizontais, colunas e gráfico de faixa observada no relatório Cana Intelligence, incluindo o caso em que o valor comparado é quase igual entre grupos.
---

# Barras e colunas

## Escolha da forma

| Pergunta | Forma |
| --- | --- |
| Comparar categorias com nomes longos | Barra horizontal |
| Comparar meses do ano | Coluna vertical |
| Mostrar duas grandezas por categoria (mínimo e máximo) | Faixa observada |
| Mostrar distribuição de uma variável | Coluna agrupada por intervalo |

Barra horizontal é o padrão para fonte, frente e indicador, porque os nomes são longos e giram mal em eixo vertical.

## Escala

1. **Barra e coluna começam em zero.** Sem exceção. A altura codifica magnitude, e cortar a base distorce a leitura.
2. **Se a diferença real é pequena, o gráfico deve mostrar diferença pequena.** Não truncar eixo para fabricar contraste.
3. **Quando as categorias têm valores quase idênticos, barra não é a forma certa.** Exemplo real deste projeto: as 7 frentes têm entre 126 e 136 leituras de ATR, então todas as barras ficam entre 92% e 100% da escala e o gráfico não compara nada. Nesse caso, trocar a grandeza ou trocar a forma.

## Faixa observada

Para comparar grupos quando a média ponderada está bloqueada, use a faixa de mínimo e máximo observados:

- Uma linha por grupo, com segmento de 4px entre mínimo e máximo.
- Ponto de 7px nas duas extremidades.
- Eixo com 5 a 7 marcações, sempre incluindo os limites dos dados.
- Colunas numéricas à direita com mínimo e máximo exatos, em 14px tabular.

Implementação no Power BI: gráfico de barras empilhadas horizontais com duas séries. A primeira recebe o mínimo com cor igual ao fundo e serve de base; a segunda recebe a diferença entre máximo e mínimo.

Essa forma prova sobreposição, que é o que interessa: se as sete faixas se sobrepõem quase inteiras, nenhuma frente se destaca.

## Ordenação

- Ordenar por valor quando a pergunta é ranking.
- Ordenar por nome quando a pergunta é presença e o ranking não faz sentido.
- Nunca ordenar por uma medida diferente da que está desenhada.

## Rótulos

- Rótulo de valor permitido em barra com até 8 categorias.
- Rótulo de categoria em 14px, `#25312D`, sem negrito.
- Nunca usar rótulo de dados com 2 casas decimais em barra: polui. Duas casas só em tabela.

## Cores

| Situação | Cor |
| --- | --- |
| Série única | `#4E7966` |
| Grupo frente de colheita | `#4E7966` |
| Grupo laboratório | `#A8B9A0` |
| Pendência | `#C17A4A` |
| Alerta classificado | `#B94D4D` |

Não usar cor para "destacar a maior barra" sem que isso signifique algo. A maior barra de leituras não é a melhor frente.

## Checklist

- [ ] Forma adequada ao tamanho da diferença real
- [ ] Eixo começando em zero em barra e coluna
- [ ] Ordenação coerente com a pergunta
- [ ] Rótulo de valor apenas quando cabe sem poluir
- [ ] Nenhuma cor usada como julgamento
- [ ] Grupo vazio não aparece como barra zerada
