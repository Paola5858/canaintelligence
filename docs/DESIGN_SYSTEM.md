# Sistema de design

Identidade visual do Cana Intelligence. O sistema é aplicado no arquivo `dashboard_cana.Report/StaticResources/SharedResources/BaseThemes/CanaIntelligence.json`, registrado como tema personalizado do relatório.

## Princípio

O relatório é ferramenta de análise da qualidade de um produto agrícola, não peça de marketing. A informação é protagonista. Cor tem função, não decoração.

## Paleta

| Papel | Hexadecimal | Uso |
| --- | --- | --- |
| Verde floresta | `#173F35` | Marca, título principal, valor de destaque, série agregada |
| Verde cana | `#4E7966` | Série principal, barras, colunas, estado validado |
| Sálvia | `#A8B9A0` | Série secundária, laboratório, estado normalizado |
| Marfim | `#F7F6F0` | Fundo da página |
| Branco | `#FFFFFF` | Superfície de leitura (painéis, tabelas, controles) |
| Grafite | `#25312D` | Texto principal |
| Cinza neutro | `#76817B` | Rótulo, eixo, texto secundário |
| Cobre | `#C17A4A` | Pendência de definição, transformação documentada |
| Vermelho discreto | `#B94D4D` | Alerta técnico classificado |

### Regras de cor

1. **Vermelho só para alerta real.** Pendência de definição não é alerta. Pendência usa cobre.
2. **Verde não indica meta.** A fonte não tem meta, então verde indica presença de dado ou família de série, nunca conformidade.
3. **Nada de arco-íris.** Existem 23 indicadores e 2 grupos. A cor distingue grupo, não indicador: verde cana para frente de colheita, sálvia para laboratório.
4. **Sem gradiente e sem fundo escuro.** Fundo marfim, painéis brancos.
5. **Nenhuma sombra.** Profundidade vem de borda hairline de 1px em `rgba(37,49,45,0.12)` e do espaço em branco.

## Tipografia

| Uso | Fonte | Tamanho | Peso |
| --- | --- | --- | --- |
| Marca | Segoe UI Semibold | 28 px | 600 |
| Título de página | Segoe UI, 600 | 17 px | 600 |
| Título de painel | Segoe UI, 600 | 17 px | 600 |
| Valor de KPI | Segoe UI, 600 | 28px | 600 |
| Texto e rótulo | Segoe UI | 14 px | 400 |
| Dado em tabela | Segoe UI tabular | 14 px | 400 |
| Rodapé | Segoe UI | 12 px | 400 |

Regras:

- **Nenhum dado analítico abaixo de 14px.** Rótulo, número, eixo, tooltip: 14px é o piso.
- **Algarismos tabulares** (`font-feature-settings: "tnum"`) em qualquer coluna de número, para que a vírgula alinhe.
- **Apenas fontes instaladas no Windows.** Segoe UI e Segoe UI Semibold vêm com o sistema. Nada de fonte baixada, porque o arquivo abre em outra máquina.
- **Aptos Display** pode substituir Segoe UI Semibold em títulos quando disponível, sem quebrar o layout.

## Grade e espaçamento

Base de 8px.

| Token | Valor | Uso |
| --- | --- | --- |
| `xxs` | 4 px | Distância entre valor e rótulo de célula |
| `xs` | 8 px | Distância entre itens relacionados |
| `sm` | 12 px | Padding interno de tabela |
| `md` | 16 px | Intervalo entre painéis, padding de painel |
| `lg` | 24 px | Margem externa da página, coluna de rótulo |
| `xl` | 48 px | Não usado em página de relatório |

Página de 1440 x 810 px, proporção 16:9. Margem externa de 24px deixa 1392 px úteis.

### Esqueleto vertical da página

| Região | Altura |
| --- | --- |
| Margem superior | 24 px |
| Cabeçalho | 48 px |
| Intervalo | 8 px |
| Navegação | 44 px |
| Intervalo | 16 px |
| Filtros | 64 px |
| Intervalo | 16 px |
| Conteúdo | 514 px (514 + 88 na Visão geral) |
| Intervalo | 16 px |
| Rodapé | 36 px |
| Margem inferior | 24 px |

## Componentes

| Componente | Regra |
| --- | --- |
| Painel | Branco, borda 1px `rgba(37,49,45,0.12)`, raio 18px, padding 16px |
| Controle (campo, seletor) | Branco, borda 1px `rgba(37,49,45,0.14)`, raio 8px, altura 40px |
| Navegação | Aba textual de 14px, ativa com sublinhado de 2px em `#173F35` e peso 600 |
| Faixa de KPI | Células abertas separadas por hairline vertical, sem cartão individual |
| Cabeçalho de tabela | 40px, 14px, peso 600, cinza neutro, borda inferior hairline |
| Linha de tabela | 32px, 14px, sem borda vertical, zebra opcional em `#FBFAF6` |
| Estado | Ponto de 6px mais texto. Nunca pílula colorida |
| Tooltip | Fundo `#25312D`, texto branco, raio 8px, padding 12px, 14px |

## Marca

O símbolo é um caule de cana desenhado em três traços: caule em verde floresta, folha em verde cana e um detalhe em cobre. Ele aparece apenas no cabeçalho, com 22 x 30 px. Não existe imagem decorativa dentro das páginas.

Motivos geométricos inspirados em sulcos agrícolas podem aparecer em divisores e na navegação, com no máximo 1px de espessura e opacidade baixa. Nunca como ilustração de fundo.

## O que o sistema proíbe

- Gráfico de pizza, medidor, mapa e qualquer visual escolhido por estar disponível.
- Cartão com seta de tendência e variação percentual inventada.
- Texto que interpreta o resultado ("a qualidade caiu em abril").
- Fundo escuro, neon, vidro fosco e gradiente.
- Número sem unidade quando a unidade existe.
- Ícone decorativo em cada item de navegação.

## Tema do Power BI

O arquivo de tema define:

- `dataColors` na ordem da paleta, para que qualquer visual novo já nasça na cor certa.
- Cores semânticas `good`, `neutral` e `bad` mapeadas para verde cana, cobre e vermelho discreto.
- `textClasses` para valor, título, cabeçalho e rótulo.
- Estilo de visual sem sombra, com borda hairline e raio 12px (o raio do tema é menor que o do desenho, porque o Power BI não aceita raio 18px em todos os visuais).
- Eixo com grade horizontal em `#EDEAE2`, rótulo em cinza neutro, sem título de eixo.
- Tabela sem grade vertical, cabeçalho em cinza neutro e peso 600.

O tema base continua sendo o Fluent2 do Power BI para não perder comportamentos nativos. O tema Cana Intelligence entra como tema personalizado por cima.
