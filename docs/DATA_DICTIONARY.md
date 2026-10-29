# Dicionário de dados

Tudo aqui foi medido na planilha `data/Base_Usina_PowerBI_Final_v4.xlsx`. Nenhuma faixa, contagem ou unidade foi estimada.

## Colunas da fato

| Coluna | Tipo | Nulo | Descrição | Uso no modelo |
| --- | --- | --- | --- | --- |
| `ID_Registro` | inteiro | não | Identificador único da medição | Chave de rastreabilidade e ligação com a auditoria |
| `Data` | data | não | Data da medição | Chave da dimensão de calendário |
| `Ano` | inteiro | não | Ano civil | Descartado, está no calendário |
| `Mes` | inteiro | não | Mês numérico | Descartado, está no calendário |
| `Mes_Nome` | texto | não | Nome do mês | Descartado, está no calendário |
| `Trimestre` | texto | não | T1 a T4 | Descartado, está no calendário |
| `AnoMes` | texto | não | AAAA-MM | Descartado, está no calendário |
| `Dia_Semana` | texto | não | Dia da semana | Descartado, está no calendário |
| `Safra` | texto | não | Safra informada | Mantido, valor único `2026/2027` |
| `Fonte` | texto | não | Frente de colheita ou Laboratório | Atributo de comparação |
| `Grupo_Fonte` | texto | não | Frente de colheita ou Laboratorio | Atributo de agrupamento |
| `Indicador` | texto | não | Nome do indicador | Descartado, está na dimensão |
| `Indicador_Codigo` | texto | não | Código do indicador | Chave da dimensão de indicador |
| `Grupo_Indicador` | texto | não | Qualidade da cana ou Análise laboratorial | Descartado, virou `Dim_Indicador[Categoria]` |
| `Unidade` | texto | não | Unidade da linha | Descartado, está na dimensão, com zero divergência |
| `Valor` | decimal | não | Valor na unidade do indicador | Valor analítico |
| `Valor_Original` | decimal | não | Valor antes da normalização de escala | Rastreabilidade |
| `Ajuste_Aplicado` | texto | não | Regra de escala aplicada | Rastreabilidade |
| `Duplicidade_Exata` | texto | não | Marca cópia exata preservada | Qualidade |
| `Linha_Origem` | inteiro | não | Linha da planilha de origem | Rastreabilidade |
| `Status_Validacao` | texto | não | Validado, Normalizado ou Pendente | Qualidade |

## Catálogo de indicadores

23 indicadores, todos presentes na fato e na dimensão, sem código órfão em nenhum dos dois lados.

### Qualidade da cana, medidos nas 7 frentes de colheita

| Código | Nome original | Nome padronizado | Unidade | Agregação recomendada | Status | Mínimo | Mediana | Máximo | Leituras |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ATR` | ATR | ATR | kg/t | Média ponderada por TC | Validado | 104,04 | 117,08 | 131,32 | 903 |
| `AR` | ArCana | ArCana | % | Média ponderada por TC | Normalizado | 0,5302 | 0,6029 | 0,6699 | 903 |
| `PC` | PC | PC | % | Média ponderada por TC | Normalizado | 10,3231 | 11,7174 | 13,2129 | 903 |
| `POL` | Pol | Pol | % | Média ponderada por TC | Validado | 12,22 | 13,98 | 15,63 | 903 |
| `FIBRA` | Fibra | Fibra | % | Média ponderada por TC | Validado | 11,70 | 12,43 | 13,49 | 903 |
| `BRIX` | Brix | Brix | % | Média ponderada por TC | Validado | 14,57 | 16,35 | 17,93 | 903 |
| `PUREZA` | Pureza | Pureza | % | Média ponderada por TC | Validado | 83,20 | 85,37 | 87,76 | 903 |
| `UMIDADE_CANA` | Umidade | Umidade Cana | % | Média ponderada por TC | Validado | 78,91 | 80,53 | 82,41 | 903 |
| `IMP_MIN` | IMP Min | Impureza Mineral | % | Média ponderada por TC | Validado | 0,00 | 1,40 | 2,60 | 903 |
| `IMP_VEG` | IMP Veg | Impureza Vegetal | % | Média ponderada por TC | Validado | 0,07 | 4,895 | 9,98 | 902 |
| `TC` | TC | TC | Desconhecida | Pendente de validação | Pendente | 148,07 | 571,00 | 779,82 | 903 |

### Análise laboratorial, medidas no Laboratório

| Código | Nome original | Nome padronizado | Unidade | Agregação recomendada | Status | Mínimo | Mediana | Máximo | Leituras |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ACIDEZ` | Acidez Total (mg/L) | Acidez Total | mg/L | Média aritmética | Validado | 6,50 | 8,98 | 11,49 | 800 |
| `AM` | AM (%) | Açúcares Redutores | % | Média aritmética | Validado | 0,650 | 0,781 | 0,899 | 800 |
| `AMIDO` | Amido (ppm) | Amido | ppm | Média aritmética | Validado | 130 | 188 | 250 | 800 |
| `CINZAS` | Cinzas (%) | Cinzas Solúveis | % | Média aritmética | Validado | 0,070 | 0,099 | 0,130 | 800 |
| `CONDUTIVIDADE` | Condutividade (µS/m) | Condutividade | µS/m | Média aritmética | Validado | 15,02 | 64,70 | 114,98 | 800 |
| `COR` | Cor (UI) | Cor ICUMSA | UI | Média aritmética | Validado | 700 | 873 | 1.050 | 800 |
| `CV` | CV (%) | Coeficiente de Variação | % | Média aritmética | Validado | 29,02 | 38,815 | 48,97 | 800 |
| `DEXTRANA` | Dextrana (ppm) | Dextrana | ppm | Média aritmética | Validado | 20 | 43 | 65 | 800 |
| `PH` | pH | pH | pH | Média logarítmica / ponderada | Validado | 6,80 | 7,23 | 7,70 | 800 |
| `RI` | RI (mg/L) | Resíduo Insolúvel | mg/L | Média aritmética | Validado | 270 | 353 | 439 | 800 |
| `TEOR_ALCOOLICO` | Teor Alcoólico (INPM) | Teor Alcoólico | ° INPM | Média aritmética | Validado | 92,90 | 93,17 | 93,40 | 800 |
| `UMIDADE_LAB` | Umidade (%) | Umidade Laboratório | fração (0-1) | Média aritmética | Validado | 0,055 | 0,090 | 0,125 | 800 |

## Unidades e escala

Dez unidades distintas. As quatro armadilhas que o modelo trata explicitamente:

| Indicador | Armazenamento real | Como exibir | O que não fazer |
| --- | --- | --- | --- |
| `PC` | Percentual direto. 11,7174 é 11,7174% | `0.00"%"` | Multiplicar por 100 ou somar entre indicadores |
| `AR` | Percentual direto. 0,6029 é 0,6029% | `0.00"%"` | Tratar como fração e formatar como percentual padrão |
| `UMIDADE_CANA` | Percentual direto. 80,53 é 80,53% | `0.00"%"` | Combinar com `UMIDADE_LAB` na mesma média |
| `UMIDADE_LAB` | Fração decimal. 0,09 é 9% | `0.0%` | Multiplicar por 100 antes de formatar |
| `PH` | Escala logarítmica | `0.00` | Média aritmética como se fosse grandeza linear |
| `TC` | Unidade não confirmada | Nenhuma, com aviso de pendência | Apresentar como tonelagem, produtividade ou volume |

## Fontes

| Fonte | Grupo | Registros | Dias com dado | Indicadores | Primeira data | Última data |
| --- | --- | --- | --- | --- | --- | --- |
| FRENTE 11 | Frente de colheita | 1.496 | 159 | 11 | 06/01/2026 | 11/12/2026 |
| FRENTE 12 | Frente de colheita | 1.496 | 152 | 11 | 06/01/2026 | 11/12/2026 |
| FRENTE 13 | Frente de colheita | 1.396 | 150 | 11 | 04/01/2026 | 11/12/2026 |
| FRENTE 14 | Frente de colheita | 1.386 | 149 | 11 | 04/01/2026 | 11/12/2026 |
| FRENTE 23 | Frente de colheita | 1.386 | 147 | 11 | 05/01/2026 | 11/12/2026 |
| FRENTE 31 | Frente de colheita | 1.386 | 145 | 11 | 04/01/2026 | 11/12/2026 |
| FRENTE 41 | Frente de colheita | 1.386 | 149 | 11 | 04/01/2026 | 11/12/2026 |
| Laboratorio | Laboratorio | 9.600 | 236 | 12 | 01/04/2026 | 30/11/2026 |

## Glossário

- **Leitura**: uma linha da fato, ou seja, uma medição de um indicador em uma data por uma fonte.
- **Pendência**: regra técnica ainda não confirmada. Não é sinônimo de erro.
- **Cópia exata**: registro idêntico a outro, mantido de propósito na base.
- **Ajuste de escala**: divisão por 1.000 ou 10.000 aplicada na origem para trazer PC e ArCana para a escala percentual.
- **Frente**: frente de colheita, grupo que mede qualidade da cana no campo.
- **Ponderação por TC**: agregação recomendada pela fonte que depende de TC como peso. Bloqueada porque TC não tem unidade definida.
