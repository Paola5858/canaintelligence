---
name: skill-line-chart
description: Regras para séries temporais no relatório Cana Intelligence, incluindo o tratamento de lacunas de medição e o uso de marcadores em séries diárias irregulares.
---

# Gráfico de linha

## Quando usar

Use linha quando a pergunta é **como algo muda ao longo do tempo** e o eixo temporal é contínuo.

Não use linha para comparar categorias (use barra), nem para mostrar composição (não use nada, composição não está no escopo).

## Tratamento de lacuna

Esta base tem 274 dias com medição em 342 dias corridos, e o indicador ATR tem 237 leituras em 342 dias. A regra:

1. **Eixo com todos os dias da janela**, não apenas os dias com dado.
2. **Dia sem medição fica vazio.** Nunca interpolar, nunca repetir o último valor, nunca transformar em zero.
3. **Linha quebrada não se reconecta.** Desligar a opção de conectar pontos por cima de vazio.
4. **Quando a lacuna é frequente, trocar linha por marcadores.** Com 30% de dias vazios espalhados, a linha vira uma sequência de tracinhos e o leitor não consegue seguir a série. Marcadores mostram a nuvem de observações e deixam a lacuna explícita.

Implementação do modo marcador: espessura de linha em 0 px, marcador de 3 a 4 px, mesma cor da linha.

## Eixos

| Item | Regra |
| --- | --- |
| Eixo x | Rótulo de mês abreviado, 14px, `#76817B`, sem linha de grade vertical |
| Eixo y | Grade horizontal em `#EDEAE2`, 1px, rótulo em 14px com vírgula decimal |
| Título de eixo | Desligado. A unidade aparece no subtítulo do visual |
| Escala zero | Obrigatória em coluna e barra. Opcional em linha, porque linha não codifica magnitude por área |
| Segundo eixo | Proibido. Nunca criar dois eixos com escalas diferentes |

## Série agregada sobre série de observação

Quando existe uma série diária ruidosa, é permitido sobrepor a média mensal, desde que:

- A linha agregada seja mais espessa e mais escura que a diária (`#173F35` contra `#7C9E8B`).
- A legenda nomeie as duas.
- A agregada seja calculada, não desenhada à mão.

Nunca sobrepor previsão, tendência estatística ou "linha de referência" sem declarar o que é.

## Cores

| Papel | Cor |
| --- | --- |
| Série principal | `#4E7966` |
| Observação diária | `#7C9E8B` |
| Série agregada | `#173F35` |
| Série secundária | `#A8B9A0` |

Máximo de três séries por gráfico. Acima disso, separar em small multiples ou trocar o visual.

## Legenda

Legenda só existe quando há mais de uma série. Com uma série, a legenda some e o título carrega a informação.

## Checklist

- [ ] Eixo temporal contínuo, incluindo dias vazios
- [ ] Lacuna sem interpolação e sem zero
- [ ] Modo marcador quando a densidade de lacuna passa de 20%
- [ ] Um único eixo y
- [ ] Unidade visível no subtítulo
- [ ] Escala zero respeitada se o visual for de linha com preenchimento
- [ ] Legenda apenas com duas séries ou mais
