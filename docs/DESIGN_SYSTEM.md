# Sistema de design

Identidade visual do Cana Intelligence. O sistema é aplicado no arquivo `dashboard_cana.Report/StaticResources/SharedResources/BaseThemes/CanaIntelligence.json`, registrado como tema personalizado do relatório, e replicado no desenho do canvas em `.kombai/canvas/cana-intelligence.canvas`.

## Princípio

O relatório é ferramenta de análise da qualidade de um produto agrícola, não peça de marketing. A informação é protagonista. Cor tem função, não decoração.

O desenho é contido por escolha: fundo marfim, painéis brancos, uma sombra difusa por painel, tipografia do sistema. O que parece caro aqui não é efeito, é alinhamento. Números tabulares, colunas que batem, rótulos no mesmo lugar em todas as páginas.

## Paleta

| Papel | Hexadecimal | Uso |
| --- | --- | --- |
| Verde floresta | `#173F35` | Marca, valor de KPI, título de painel, aba ativa, série agregada |
| Verde cana | `#4E7966` | Série principal, barras, estado validado |
| Sálvia | `#A8B9A0` | Série secundária, laboratório, estado normalizado |
| Marfim esverdeado | `#EEF1EA` | Fundo da página |
| Branco | `#FFFFFF` | Superfície de painel, tabela, controle |
| Grafite | `#25312D` | Texto principal |
| Cinza neutro | `#76817B` | Rótulo, eixo, texto secundário |
| Cobre | `#C17A4A` | Pendência de definição, transformação documentada |
| Vermelho discreto | `#B94D4D` | Alerta técnico classificado |

### Regras de cor

1. **Vermelho só para alerta real.** Pendência de definição não é alerta. Pendência usa cobre.
2. **Verde não indica meta.** A fonte não tem meta, então verde indica presença de dado ou família de série, nunca conformidade.
3. **Nada de arco-íris.** Existem 23 indicadores e 2 grupos. A cor distingue grupo, não indicador: verde cana para frente de colheita, sálvia para laboratório.
4. **Sem gradiente.** Nem no fundo, nem em série, nem em preenchimento de área.
5. **Cor nunca é o único portador de informação.** Todo estado tem ponto de 6px e texto.

## Superfícies

Uma superfície tem **um** separador. Não se acumula borda, preenchimento, sombra e desfoque no mesmo elemento.

| Nível | Tratamento | Uso |
| --- | --- | --- |
| Fundo | Marfim esverdeado `#EEF1EA`, sem borda | Página |
| Painel | Branco, raio 24px, sombra `0 1px 2px rgba(23,63,53,.045), 0 18px 44px -26px rgba(23,63,53,.30)`, sem borda | Todo bloco analítico |
| Divisória interna | Hairline 1px `rgba(37,49,45,.07)` | Células de faixa, linhas de tabela |
| Controle | Fundo `#FBFAF6`, borda 1px `rgba(37,49,45,.09)`, raio 12px | Campos de filtro |

Regra prática: se o painel já é branco sobre marfim, ele não precisa de borda. Se a divisória já separa, ela não precisa de sombra.

## Tipografia

Famílias instaladas no Windows. Nada de fonte baixada, porque o arquivo abre em outra máquina.

| Uso | Fonte | Tamanho | Peso |
| --- | --- | --- | --- |
| Marca | Segoe UI Variable Display / Segoe UI Semibold | 26 px | 600 |
| Título de página | Segoe UI, 600 | 16 px | 600 |
| Título de painel | Segoe UI, 600 | 16 px | 600 |
| Subtítulo de painel | Segoe UI | 13 px | 400 |
| Valor de KPI | Segoe UI Semibold | 26 a 30 px | 600 |
| Rótulo de campo | Segoe UI | 12 px | 400 |
| Dado em tabela | Segoe UI tabular | 14 px | 400 |
| Rodapé | Segoe UI | 12 px | 400 |

Regras:

- **Nenhum dado analítico abaixo de 14px.** Rótulo, número, eixo: 14px é o piso. Os 12px ficam reservados para rótulo de campo, legenda de eixo e rodapé.
- **Algarismos tabulares** (`font-feature-settings: "tnum"`) em qualquer número, para que a vírgula alinhe.
- **Aptos Display** pode substituir Segoe UI Semibold em títulos quando disponível, sem quebrar o layout.

## Grade e espaçamento

Base de 8px.

| Token | Valor | Uso |
| --- | --- | --- |
| `xxs` | 4 px | Distância entre valor e rótulo de célula |
| `xs` | 8 px | Distância entre itens relacionados |
| `sm` | 12 px | Padding interno de tabela, gap entre coluna de rótulo e valor |
| `md` | 16 px | Intervalo entre painéis, padding de painel |
| `lg` | 24 px | Margem externa da página |
| `xl` | 48 px | Não usado em página de relatório |

Página de 1440 x 810 px, proporção 16:9. Margem externa de 24px deixa 1392 px úteis.

### Esqueleto vertical da página

| Região | Altura | Posição y |
| --- | --- | --- |
| Margem superior | 24 | 0 |
| Cabeçalho | 48 | 24 |
| Intervalo | 8 | 72 |
| Navegação | 44 | 80 |
| Intervalo | 16 | 124 |
| Filtros | 64 | 140 |
| Intervalo | 16 | 204 |
| Conteúdo | 514 | 220 |
| Intervalo | 16 | 734 |
| Rodapé | 36 | 750 |
| Margem inferior | 24 | 786 |

A Visão geral usa 92px de faixa de indicadores dentro do conteúdo, e o restante da linha fica com 406px. As demais páginas usam os 514px inteiros.

### Colunas

| Layout | Divisão |
| --- | --- |
| Visão geral | 300 + 16 + 684 + 16 + 376 |
| Com trilho do indicador | 300 + 16 + restante |
| Duas colunas iguais | 688 + 16 + 688 |
| Tabela com procedência | 1016 + 16 + 360 |

## Componentes

| Componente | Regra |
| --- | --- |
| Cabeçalho | Marca 26px, divisor de 1px com 22px de altura, nome da página 16px. À direita, safra e carga do modelo em 13px cinza |
| Navegação | Barra segmentada em pílula branca, raio 999px, 4px de padding. Aba ativa preenchida em `#173F35` com texto branco, 14px peso 600. Aba inativa em cinza |
| Barra de filtros | Um painel branco de 64px. Rótulo de 12px acima do controle, sempre visível. Controle de 34px, raio 12px. Ação de limpar à direita |
| Faixa de indicadores | Painel único com células abertas separadas por hairline vertical. Valor em 26 a 30px, rótulo em 12px acima |
| Trilho do indicador | Painel de 300px com seletor de 54px e propriedades em duas colunas: unidade, status, agregação, leituras. Fecha com janela observada e a fonte que mede |
| Título de painel | 16px peso 600, subtítulo de 13px cinza. Unidade alinhada à direita, no mesmo eixo do título |
| Cabeçalho de tabela | 40px, 12px, peso 600, cinza neutro, borda inferior hairline |
| Linha de tabela | 32px, 14px, sem borda vertical. Linha selecionada em `#F3F6F2` |
| Estado | Ponto de 6px mais texto. Nunca pílula colorida |
| Rodapé | Origem dos dados à esquerda, contagens de pendência e link para Qualidade à direita. 12px |

## Marca

O símbolo é um caule de cana desenhado em três traços: caule em verde floresta, folha em verde cana e um detalhe em cobre. Aparece apenas no cabeçalho, com 22 x 30 px. Não existe imagem decorativa dentro das páginas.

Motivos geométricos inspirados em sulcos agrícolas podem aparecer em divisores, com no máximo 1px de espessura e opacidade baixa. Nunca como ilustração de fundo.

## Gráficos

| Elemento | Regra |
| --- | --- |
| Linha | 1,1 a 1,6px, verde cana. Preenchimento de área em `rgba(78,121,102,.075)`. Lacuna quebra a linha, nunca interpola |
| Marcadores | Só em série curta ou agregada. Série diária densa fica sem marcador |
| Série agregada | Verde floresta, mais espessa que a diária |
| Eixo y | Grade horizontal em `rgba(37,49,45,.07)`, rótulo de 12px, sem título de eixo |
| Eixo x | Rótulo de mês abreviado em 12px, sem grade vertical |
| Coluna | Começa em zero, raio de 4px no topo, gap de 8px |
| Barra horizontal | Trilho de 8px em `#EFEDE5`, segmento de 8px arredondado |
| Faixa observada | Segmento de 4px, pontos de 10px nas extremidades, eixo com 5 marcações |

## O que o sistema proíbe

- Gráfico de pizza, medidor, mapa e qualquer visual escolhido por estar disponível.
- Cartão com seta de tendência e variação percentual inventada.
- Texto que interpreta o resultado ("a qualidade caiu em abril").
- Fundo escuro, neon, vidro fosco e gradiente.
- Borda e sombra no mesmo painel.
- Número sem unidade quando a unidade existe.
- Ícone decorativo em cada item de navegação.

## Tema do Power BI

O arquivo de tema define:

- `dataColors` na ordem da paleta, para que qualquer visual novo já nasça na cor certa.
- Cores semânticas `good`, `neutral` e `bad` mapeadas para verde cana, cobre e vermelho discreto.
- `textClasses` para valor, título, cabeçalho e rótulo.
- Estilo de visual sem sombra, com borda hairline e raio 12px (o raio do tema é menor que os 24px do desenho, porque o Power BI não aceita raio maior que 12px em todos os visuais).
- Eixo com grade horizontal em `#EDEAE2`, rótulo em cinza neutro, sem título de eixo.
- Tabela sem grade vertical, cabeçalho em cinza neutro e peso 600, padding de linha reduzido para 4.

O tema base continua sendo o Fluent2 do Power BI para não perder comportamentos nativos. O tema Cana Intelligence entra como tema personalizado por cima.

## Diferença entre desenho e implementação

| Desenho | Implementação | Motivo |
| --- | --- | --- |
| Raio de 24px no painel | Raio de 12px no tema | Limite do Power BI em contêiner de visual |
| Sombra difusa no painel | Sem sombra no tema, borda hairline | O Desktop não entrega a sombra do desenho; a borda preserva a separação |
| Pílula de navegação | Navegador de páginas nativo | O controle é nativo; o desenho define cor e estado ativo |
| Faixa de KPI como painel único | Cinco cartões sem borda e sem fundo | Não existe contêiner de faixa |
| Marca em SVG | Imagem PNG no cabeçalho | O símbolo é exportado para imagem |
