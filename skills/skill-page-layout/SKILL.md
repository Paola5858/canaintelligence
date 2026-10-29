---
name: skill-page-layout
description: Regras de grade, hierarquia, cabeçalho, navegação e rodapé das páginas do relatório Cana Intelligence em 1440x810.
---

# Layout de página

## Canvas

Página de 1440 x 810 px, proporção 16:9. Margem externa de 24px em todos os lados. Área útil de 1392 x 762 px.

## Grade vertical

| Região | Altura | Posição y |
| --- | --- | --- |
| Margem | 24 | 0 |
| Cabeçalho | 48 | 24 |
| Intervalo | 8 | 72 |
| Navegação | 44 | 80 |
| Intervalo | 16 | 124 |
| Filtros | 64 | 140 |
| Intervalo | 16 | 204 |
| Conteúdo | 514 | 220 |
| Intervalo | 16 | 734 |
| Rodapé | 36 | 750 |
| Margem | 24 | 786 |

A página Visão geral usa 88px de faixa de cobertura dentro da área de conteúdo, e por isso o restante do conteúdo fica com 410px. As demais páginas usam os 514px inteiros.

## Hierarquia

Ordem de leitura que o desenho precisa respeitar:

1. **Marca e página.** Onde estou.
2. **Navegação.** Para onde posso ir.
3. **Filtros.** O que está aplicado.
4. **Resumo.** Qual é o estado da base.
5. **Análise.** O gráfico principal.
6. **Detalhe.** Tabela, comparação, distribuição.
7. **Rodapé.** De onde vem o dado.

Um elemento de cada nível. Três títulos no topo competindo por atenção é erro de hierarquia, não de estilo.

## Cabeçalho

- Marca em verde floresta, 28px, peso 600, com o símbolo à esquerda.
- Divisor vertical de 1px e 22px de altura.
- Nome da página em 17px, peso 600.
- À direita: safra e data de carga em 14px, cinza neutro.
- Data de carga é a data de atualização do modelo, **não** a última data de medição. Confundir as duas produz um aviso falso.

## Navegação

- Seis abas em uma linha de 44px, separadas por 28px.
- Aba ativa com sublinhado de 2px em `#173F35` e peso 600.
- Aba inativa em `#76817B` sem peso.
- Sem ícone em cada aba. Ícone decorativo em navegação é ruído.
- Borda inferior de 1px em toda a largura.

## Filtros

- Rótulo de 14px acima do controle, sempre visível. Placeholder que desaparece não serve.
- Altura do controle 40px, raio 8px, borda `rgba(37,49,45,0.14)`.
- Ação de limpar filtros à direita, alinhada ao fim da faixa.
- Não repetir o mesmo slicer em duas posições da página.

## Conteúdo

- Intervalo de 16px entre painéis.
- Painel branco, borda hairline, raio 18px, padding interno 16px.
- Título do painel em 17px peso 600, subtítulo em 14px cinza quando carrega unidade ou escopo.
- Densidade: no máximo 3 blocos analíticos por linha. Acima disso, o texto encolhe abaixo do mínimo legível.

## Rodapé

- Altura 36px, borda superior hairline, 8px de respiro.
- Esquerda: origem dos dados, 12px, cinza neutro.
- Direita: contagem de pendências com ponto cobre e link para a página Qualidade.
- O rodapé não é decorativo: ele responde "de onde veio isso" para quem chega na página depois.

## Acessibilidade

- Contraste mínimo de 4.5:1 para texto. Grafite sobre marfim atende. Cinza neutro em texto de 12px é o limite: só usar em rodapé.
- Nenhuma informação transmitida apenas por cor. Status tem ponto e texto.
- Ordem de tabulação igual à ordem de leitura.
- Rótulo em todo controle.

## Checklist

- [ ] Página em 1440 x 810
- [ ] Margem de 24px respeitada
- [ ] Uma hierarquia, sem título competindo
- [ ] Navegação com aba ativa visível
- [ ] Todo filtro com rótulo fixo
- [ ] Intervalo de 16px entre painéis
- [ ] Rodapé com origem e pendências
- [ ] Nenhum dado abaixo de 14px
- [ ] Nenhuma informação só por cor
