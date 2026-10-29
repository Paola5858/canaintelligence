---
name: skill-data-quality-table
description: Regras para a página de qualidade dos dados, incluindo a tabela de pendências, a distinção entre pendência e erro e a apresentação de registros preservados.
---

# Tabela de qualidade dos dados

## Princípio

Qualidade de base não é qualidade do produto. A página existe para mostrar o que a base tem, o que ela não tem e o que está pendente. Nada aqui classifica a cana.

## O que a página mostra

| Bloco | Conteúdo |
| --- | --- |
| Resumo | Total de registros, pendentes, percentual pendente, ajustes de escala, cópias preservadas |
| Cobertura | Registros por mês, com dias e indicadores no tooltip |
| Status | Validado, Normalizado, Pendente |
| Pendências | Tabela com ID, indicador, problema, ação recomendada e situação |

## Regras de linguagem

1. **"Pendente" não é "erro".** Pendente significa regra técnica não confirmada. A interface nunca escreve "falha", "inválido" ou "reprovado".
2. **"Cópia exata preservada" não é "duplicidade indesejada".** Foram mantidas por decisão, com par idêntico comprovado.
3. **Nenhum texto interpreta o resultado.** Proibido: "a base está boa", "qualidade melhorou", "dados confiáveis". mostrar contagem e deixar a conclusão com quem lê.
4. **Nenhum índice composto.** Não criar "score de qualidade" sem definição matemática acordada.

## Cores

| Estado | Cor | Marcador |
| --- | --- | --- |
| Validado | `#4E7966` | Ponto de 6px |
| Normalizado | `#A8B9A0` | Ponto de 6px |
| Pendente | `#C17A4A` | Ponto de 6px |
| Alerta técnico classificado | `#B94D4D` | Só quando existe regra que classifica |

Vermelho nunca entra para pendência de definição. Verde nunca entra para dizer que está tudo bem.

## Tabela de pendências

| Coluna | Regra |
| --- | --- |
| Identificador | Código real da fonte, como `P_TC_01` |
| Indicador | Código do indicador afetado |
| Problema | Texto completo da origem, sem reescrever |
| Ação recomendada | Texto completo da origem |
| Situação | Texto completo. "Resolvida na Fato, aberta no legado" não pode virar "Resolvida" |

Se a coluna de situação não couber, aumentar a coluna. Cortar o texto muda o significado, e mudar o significado em uma tabela de auditoria é pior que uma tabela larga.

## Cobertura e lacuna

- A lacuna é ausência de qualquer medição na janela, não falha de coleta de um indicador específico.
- Gráfico de cobertura usa coluna a partir de zero.
- Não pintar mês de cobertura baixa de vermelho. Cobertura baixa em janeiro é escopo de coleta, não incidente.

## Extremos

- Valor extremo pode ser sinalizado, nunca rotulado como erro.
- Se existir sinalização, ela precisa de regra declarada: 3 desvios padrão, por exemplo, e a palavra na tela é "sinalizado".
- A regra precisa estar escrita na página ou na documentação, não implícita.

## Checklist

- [ ] Pendência nunca chamada de erro
- [ ] Cópia preservada nunca chamada de duplicidade indesejada
- [ ] Nenhum texto interpretando a qualidade
- [ ] Situação com texto completo
- [ ] Vermelho ausente
- [ ] Percentual de pendência com denominador explícito
- [ ] Regra de sinalização de extremo declarada, se existir
