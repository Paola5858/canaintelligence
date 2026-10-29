---
name: skill-tooltip-and-interactions
description: Regras de tooltip, filtro cruzado, drill-through e estados de filtro no relatório Cana Intelligence.
---

# Tooltip e interações

## Tooltip

Tooltip é onde a unidade, a contagem e o contexto cabem sem poluir o gráfico.

### Conteúdo mínimo

| Campo | Obrigatório |
| --- | --- |
| Data ou categoria | Sim |
| Valor com unidade | Sim |
| Quantidade de leituras | Sim |
| Fonte | Sim, quando o gráfico agrega mais de uma fonte |
| Status de validação | Sim, quando o dado pode estar pendente |

### Regras

1. **Unidade sempre no valor do tooltip**, mesmo que o eixo já tenha unidade.
2. **Contagem de leituras sempre.** Um valor médio de 11,7% calculado sobre 2 leituras não é o mesmo que sobre 40, e o leitor precisa saber.
3. **Vazio não aparece.** Ponto sem valor não gera tooltip com zero.
4. **Fundo grafite `#25312D`, texto branco, raio 8px, padding 12px, fonte 14px.** Contraste alto, sem sombra.
5. **Sem texto explicativo.** O tooltip carrega dado, não instrução de leitura.

### Tooltip de página

Reservado para um caso: o detalhe do registro na página Detalhes. Não criar tooltip de página decorativa com resumo de texto.

## Interação cruzada

Regra padrão do projeto: **destaque**, não filtro.

- Clicar em uma barra destaca as linhas correspondentes nos outros visuais da página.
- Nenhum visual é configurado como filtro, com uma exceção: a matriz de Fontes filtra a tabela da mesma página, porque ali a seleção de fonte é a intenção principal.
- Desligar interação quando o cruzamento produziria leitura falsa. Exemplo: clicar em um mês na cobertura de registros não deve filtrar o painel de status, porque os dois respondem a perguntas independentes.

## Sincronização de segmentação

- Período: sincronizado em todas as páginas.
- Fonte: sincronizado em Visão geral, Evolução, Fontes e Detalhes. Não sincronizar em Qualidade, para que a auditoria não seja escondida por um filtro de fonte.
- Indicador: sincronizado entre as quatro páginas analíticas.

## Drill-through

Para a página Detalhes:

1. Campos de drill: `Dim_Calendario[Data]`, `Fato_Medicoes[Fonte]`, `Dim_Indicador[Codigo]`.
2. Manter todos os filtros ligados por padrão.
3. A página de destino precisa ter um botão de retorno visível. Drill-through sem volta prende o leitor.
4. Se a página de detalhe for aberta sem contexto de drill, ela mostra os registros do filtro global, não uma tela vazia.

## Estado de filtro

O leitor precisa saber o que está aplicado. Regras:

- Slicer sempre visível, nunca escondido atrás de painel.
- Se existir filtro fixo no relatório, ele é declarado no rodapé.
- Botão de limpar filtros presente e funcional. Botão que não faz nada é pior que ausência de botão.
- Título dinâmico mostra o indicador e a unidade do contexto: use `Titulo Dinamico do Indicador`.

## Estados vazios

Todo visual precisa de comportamento definido para contexto vazio:

| Situação | Mensagem |
| --- | --- |
| Sem medição no período | "Sem medições no período" |
| Período sem comparação possível | "Dados insuficientes" |
| Indicador sem unidade confirmada | "Unidade não confirmada" |
| Indicador com agregação bloqueada | "Ponderação por TC não disponível" |

Nunca usar zero como substituto de vazio, e nunca deixar o visual em branco sem explicação.

## Checklist

- [ ] Tooltip com data, valor, unidade e leituras
- [ ] Status no tooltip quando o dado pode estar pendente
- [ ] Interação em destaque, com exceções declaradas
- [ ] Sincronização de slicer conferida página a página
- [ ] Drill-through com botão de volta
- [ ] Botão de limpar filtros funcional
- [ ] Quatro estados vazios com mensagem, nenhum com zero
