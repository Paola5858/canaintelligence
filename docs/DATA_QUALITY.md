# Qualidade dos dados

Esta página descreve o que a base tem, o que ela não tem, e o que foi feito para não transformar ausência em zero nem pendência em erro.

## Números de partida

| Indicador de qualidade | Valor | Como foi medido |
| --- | --- | --- |
| Registros na fato | 19.532 | `COUNTROWS` na aba, confirmado pelo `Resumo_Qualidade` |
| Registros na saída | 19.532 | Nenhuma linha removida |
| Dias com pelo menos uma medição | 274 | Datas distintas na fato |
| Janela observada | 04/01/2026 a 11/12/2026 | Menor e maior data |
| Dias corridos na janela | 342 | Calendário contínuo |
| Dias sem nenhuma medição | 68 | 342 menos 274 |
| Indicadores | 23 | Códigos distintos, todos na dimensão |
| Fontes | 8 | 7 frentes e o laboratório |
| Registros validados | 16.823 | `Status_Validacao = "Validado"` |
| Registros normalizados | 1.806 | `Status_Validacao = "Normalizado"` |
| Registros pendentes | 903 | `Status_Validacao = "Pendente"` |
| Percentual pendente | 4,62% | 903 dividido por 19.532 |
| Registros com ajuste de escala | 1.585 | `Ajuste_Aplicado <> "Nenhum"` |
| Cópias exatas preservadas | 135 | `Duplicidade_Exata = "Sim - copia exata (mantida)"` |

## Cobertura por mês

A cobertura não é uniforme. Isso é um fato da base, não uma falha do relatório.

| Mês | Registros | Dias com dado | Indicadores |
| --- | --- | --- | --- |
| Janeiro | 330 | 8 | 11 |
| Fevereiro | 385 | 7 | 11 |
| Março | 330 | 8 | 11 |
| Abril | 2.190 | 30 | 23 |
| Maio | 2.135 | 31 | 23 |
| Junho | 2.080 | 30 | 23 |
| Julho | 2.256 | 30 | 23 |
| Agosto | 2.278 | 31 | 23 |
| Setembro | 2.267 | 30 | 23 |
| Outubro | 2.189 | 31 | 23 |
| Novembro | 2.773 | 30 | 23 |
| Dezembro | 319 | 8 | 11 |

Leitura correta: de janeiro a março e em dezembro a base tem apenas as frentes, com cerca de 8 dias por mês. O laboratório começa em 01/04/2026 e termina em 30/11/2026. Qualquer gráfico mensal que ignore isso sugere queda de produção onde existe, na verdade, mudança de escopo de coleta.

## O que NÃO foi feito com os dados

1. **Nenhuma deduplicação.** As 135 linhas marcadas como cópia exata continuam na fato. O teste confirma que cada uma delas tem um par idêntico em data, fonte, indicador, valor e valor original. Sem evidência de que sejam erro de coleta, removê-las destruiria informação.
2. **Nenhum nulo virou zero.** A base não tem nulos nas colunas-chave, mas dias sem medição continuam sem medição. Medida em dia vazio retorna vazio, e a mensagem `Sem medições no período` cobre o caso.
3. **Nenhum valor foi reescalado pelo relatório.** PC e ArCana já chegaram em escala percentual, com 1.585 transformações registradas na auditoria. O relatório apenas exibe.
4. **Nenhum registro foi classificado como erro por ser extremo.** Os mínimos e máximos do dicionário são observações reais, inclusive `IMP_MIN = 0,00` e `COR = 1.050`.

## Pendências

Quatro pendências estão registradas na origem. A tabela do modelo é `Pendencias_Validacao`. O campo `Status` separa o tratamento analítico já aplicado da correção ainda aberta no sistema legado.

| ID | Indicador | Problema | Situação |
| --- | --- | --- | --- |
| `P_PC_01` | PC | Escalas heterogêneas (x1, x1000, x10000) nos sistemas legados | Resolvida na fato, aberta no legado |
| `P_AR_01` | ArCana | Variação de escala na entrada de dados de recepção de cana | Resolvida na fato, aberta no legado |
| `P_TC_01` | TC | Definição técnica e unidade não confirmadas | **Aberta** |
| `P_UMB_01` | Umidade | UMIDADE_LAB gravada como fração decimal em vez de percentual | Documentada, pronta para o PBI |

`P_TC_01` é a única que bloqueia análise: 903 registros (4,62% da base) não têm unidade, não têm regra de agregação e não devem ser lidos como tonelagem, produtividade ou volume.

`P_UMB_01` não é um problema de dado, é de formato. Resolvida com `0.0%` na medida `Umidade Laboratorio Media`.

## Normalização de escala

1.585 registros de PC e ArCana passaram por divisão na origem, antes de entrar na planilha:

| Regra | Registros | Indicadores |
| --- | --- | --- |
| Divisão por 10.000 (escala ppm para %) | 1.445 | PC e ArCana |
| Divisão por 1.000 (escala x1000 para %) | 140 | PC e ArCana |

Cada linha afetada tem registro em `Auditoria_Dados`, com valor original, valor final, fator e regra. Os 1.585 IDs da auditoria existem todos na fato, e o número de linhas com ajuste na fato é exatamente igual ao número de linhas da auditoria (verificado por teste).

## Assimetria entre grupos

| Grupo | Registros | Indicadores | Janela |
| --- | --- | --- | --- |
| Frente de colheita | 9.932 | 11 | 04/01 a 11/12/2026 |
| Laboratório | 9.600 | 12 | 01/04 a 30/11/2026 |

Os dois grupos não compartilham um único indicador. Comparar "frente contra laboratório" não tem sentido físico, e o relatório impede isso: na página Fontes, a comparação acontece entre as 7 frentes, e o laboratório aparece como nota quando o indicador selecionado é de campo.

## Quantidade de leituras por frente

Para o indicador ATR, as sete frentes têm entre 126 e 136 leituras, e entre 94 e 104 dias com dado. A diferença de média entre frentes é pequena diante da dispersão. Conclusão que o relatório não tira, de propósito: não existe dado suficiente para afirmar que uma frente é melhor que outra.

## Riscos residuais

1. **TC sem definição.** Enquanto `P_TC_01` estiver aberta, nenhum número derivado de TC deve sair do relatório.
2. **Cobertura irregular no início e no fim do ano.** Comparações que incluam janeiro a março misturam 11 indicadores com meses de 23.
3. **Ponderação indisponível.** Médias de ATR, PC, ArCana, Pol, Fibra, Brix, Pureza, Umidade Cana e impurezas são aritméticas na tela, não ponderadas por TC. Isso está escrito na interface e no catálogo de medidas.
