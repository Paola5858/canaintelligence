---
name: skill-card-kpi
description: Regras para cartões de valor único e faixas de indicador no relatório Cana Intelligence. Use ao criar qualquer cartão de KPI, faixa de cobertura ou cartão de contrato de indicador.
---

# Cartão de KPI

## Quando usar

Use cartão quando existe **um número com significado fechado**: contagem, data única, cobertura percentual, média de um indicador aprovado.

Não use cartão para:

- Variação inventada, seta de tendência ou comparação com meta inexistente.
- Número que depende de mais de um indicador no mesmo cálculo.
- Texto longo. Para texto existe a medida de formatação, não o cartão.

## Regras de conteúdo

1. **Uma medida por cartão.** Se precisar de duas, são dois cartões.
2. **Sempre com rótulo.** O rótulo diz o que é o número: "Dias com dados", não "Total".
3. **Unidade no número ou no rótulo.** `117,08 kg/t` ou `117,08` com rótulo "ATR em kg/t". Nunca só `117,08`.
4. **Vazio é vazio.** Se a medida retorna vazio, o cartão mostra vazio. Não configurar valor padrão zero.
5. **Formato sempre pela medida.** O formato mora na medida, não no visual. Isso evita o mesmo indicador aparecer com formatos diferentes em páginas diferentes.

## Regras de tipografia e cor

| Elemento | Regra |
| --- | --- |
| Valor | Segoe UI Semibold, 28px, `#173F35` |
| Rótulo | Segoe UI, 14px, `#76817B` |
| Alinhamento | Esquerda, valor acima do rótulo |
| Fundo | Branco, ou transparente quando o cartão faz parte de uma faixa |
| Borda | Desligada quando o cartão está em faixa; hairline quando está isolado |

Nunca aplicar cor condicional que sugira meta: verde para "bom", vermelho para "ruim". A fonte não define meta. Cobre só entra em contagem de pendência.

## Faixa de indicadores

Cinco cartões alinhados, sem borda e sem fundo individual, formam uma faixa aberta. Regras:

- Altura fixa de 88px, cartões alinhados pela mesma linha de base.
- Separador vertical hairline de 1px entre cartões, com 14px de respiro no topo e na base.
- A faixa inteira é contextual: se um cartão é filtrado por outro visual, os outros também precisam ser, senão o conjunto mente.

## Sensibilidade ao filtro

Antes de publicar o cartão, responda: **este número deve reagir ao slicer de indicador?**

- Contagens de base (registros, dias, fontes): não devem reagir ao indicador. Use as medidas da pasta `00`.
- Média de indicador: deve reagir. Use as medidas da pasta `01`.

Se um cartão de base começa a cair quando você seleciona um indicador, ele está ligado ao filtro errado.

## Checklist

- [ ] Uma medida por cartão
- [ ] Rótulo presente e específico
- [ ] Unidade visível
- [ ] Formato vem da medida
- [ ] Vazio não virou zero
- [ ] Nenhuma seta, meta ou cor de julgamento
- [ ] Reage (ou não reage) ao filtro conforme a intenção declarada
