# Catálogo de medidas

72 medidas na tabela `_Medidas`, organizadas em 7 pastas de exibição. Todas em português, com nome curto e descrição quando o nome não basta. O recorte inicial seguro é ATR, usado quando o slicer de indicador está em Todos; o usuário pode trocar para qualquer indicador.

## Regra que governa o catálogo

Nenhuma medida genérica soma ou tira média de todos os valores da fato. Quando o slicer está em Todos, o modelo aplica explicitamente ATR como recorte exploratório padrão. Somar pH com acidez e ATR produz um número sem significado, e um número sem significado em um cartão é pior que um cartão vazio.

Por isso as medidas de agregação genérica exigem duas condições:

```dax
Valor Medio do Indicador =
VAR Codigo = [Codigo do Indicador no Contexto]
VAR Agregacao = CALCULATE (
    SELECTEDVALUE ( Dim_Indicador[Tipo_Agregacao_Recomendada] ),
    Dim_Indicador[Codigo] = Codigo
)
RETURN IF (
    Agregacao = "Média aritmética",
    CALCULATE ( AVERAGE ( Fato_Medicoes[Valor] ), Dim_Indicador[Codigo] = Codigo ),
    BLANK ()
)
```

1. Um indicador no contexto, ou o recorte padrão ATR quando o slicer está em Todos.
2. Comportamento de média reconhecido no catálogo do indicador.

Fora disso, o resultado é vazio, nunca zero.

## 00 | Base e qualidade

Descrevem a cobertura da fato. Não sugerem qualidade de cana.

| Medida | Formato | O que responde |
|---|---|---|
| `Quantidade de Registros` | `#,##0` | Quantas medições existem no filtro. 19.532 no total. |
| `Quantidade de Indicadores` | `#,##0` | Quantos indicadores distintos existem. 23. |
| `Quantidade de Fontes` | `#,##0` | Quantas fontes distintas existem. 8. |
| `Dias com Dados` | `#,##0` | Dias com pelo menos uma medição. 274. |
| `Primeira Data com Dados` | `dd/mm/yyyy` | Início da janela observada. |
| `Ultima Data com Dados` | `dd/mm/yyyy` | Fim da janela observada. |
| `Registros Pendentes` | `#,##0` | Registros com status Pendente. 903. |
| `Registros Normalizados` | `#,##0` | Registros que passaram por normalização. 1.806. |
| `Registros Validados` | `#,##0` | Registros sem ajuste. 16.823. |
| `Percentual de Registros Pendentes` | `0.00%` | Proporção pendente. 4,62%. |
| `Indicadores Validados` | `#,##0` | Indicadores sem pendência. 22. |
| `Indicadores Pendentes` | `#,##0` | Indicadores com pendência. 1. |
| `Registros com Ajuste de Escala` | `#,##0` | Linhas com divisão por 1.000 ou 10.000. 1.585. |
| `Copias Exatas Preservadas` | `#,##0` | Cópias idênticas mantidas. 135. |
| `Dias no Calendario da Janela` | `#,##0` | Dias corridos entre a primeira e a última medição. 342. |
| `Dias sem Medicao` | `#,##0` | 342 menos dias com dado. 68. |
| `Cobertura de Calendario` | `0.0%` | Proporção de dias com dado na janela. |

## 01 | Indicadores

Agregações por indicador. As genéricas têm guarda; as nomeadas são fixas por código.

| Medida | Formato | Guarda |
|---|---|---|
| `Quantidade de Leituras` | `#,##0` | Nenhuma. Contagem é sempre válida. |
| `Valor Medio do Indicador` | `0.00` | Exige um indicador e agregação aritmética aprovada |
| `Media Aritmetica Nao Ponderada` | `0.00` | Exige um indicador. Ignora a recomendação de ponderação e declara isso no nome |
| `Mediana do Indicador` | `0.00` | Exige um indicador. Válida para qualquer unidade |
| `Minimo Observado` | `0.00` | Exige um indicador |
| `Maximo Observado` | `0.00` | Exige um indicador |
| `Amplitude Observada` | `0.00` | Derivada de mínimo e máximo |
| `Leitura da Ultima Data` | `0.00` | Média das leituras da última data do contexto |
| `Leitura da Primeira Data` | `0.00` | Média das leituras da primeira data do contexto |

### Medidas nomeadas por indicador

Existem para carregar o formato correto sem depender de configuração manual de cada visual.

| Medida | Indicador | Formato | Resultado |
|---|---|---|---|
| `PC Medio` | `PC` | `0.00"%"` | 11,71% |
| `ArCana Medio` | `AR` | `0.00"%"` | 0,60% |
| `Pureza Media` | `PUREZA` | `0.00"%"` | 85,37% |
| `Brix Medio` | `BRIX` | `0.00"%"` | 16,35% |
| `Pol Medio` | `POL` | `0.00"%"` | 13,98% |
| `Fibra Media` | `FIBRA` | `0.00"%"` | 12,43% |
| `Umidade Cana Media` | `UMIDADE_CANA` | `0.00"%"` | 80,53% |
| `Impureza Mineral Media` | `IMP_MIN` | `0.00"%"` | 1,40% |
| `Impureza Vegetal Medio` | `IMP_VEG` | `0.00"%"` | 4,90% |
| `ATR Medio` | `ATR` | `0.00" kg/t"` | 117,08 kg/t |
| `Acidez Total Media` | `ACIDEZ` | `0.00" mg/L"` | 8,98 mg/L |
| `pH Mediana` | `PH` | `0.00` | 7,23 (mediana, não média) |
| `Umidade Laboratorio Media` | `UMIDADE_LAB` | `0.0%` | 9,0% |

Três decisões embutidas nessa tabela:

1. **Percentual em escala direta usa formato personalizado.** `0.00"%"` exibe 11,7174 como 11,71% sem multiplicar o valor.
2. **UMIDADE_LAB usa formato percentual padrão.** O dado já está em fração decimal, então 0,09 vira 9%.
3. **pH não tem medida de média.** A fonte recomenda média logarítmica, que não foi homologada para esta base. A mediana é exibida como mediana, não como substituta silenciosa da média.

Não existe medida de média ponderada por TC. A decisão está registrada em [DATA_QUALITY.md](DATA_QUALITY.md).

## 02 | Tempo

| Medida | Formato | O que faz |
|---|---|---|
| `Dias no Periodo Selecionado` | `#,##0` | Duração do período filtrado, em dias |
| `Media Movel 7 Dias` | `0.00` | Média das leituras dos 7 dias anteriores ao fim do contexto. Não é previsão |

## 03 | Comparações

| Medida | Formato | Regra |
|---|---|---|
| `Media do Periodo Anterior` | `0.00` | Desloca o filtro pelo mesmo número de dias do período atual e calcula a média lá |
| `Variacao Absoluta vs Periodo Anterior` | `0.00` | Diferença entre atual e anterior, vazia se não houver anterior |
| `Variacao Percentual vs Periodo Anterior` | `0.00%` | Vazia se não houver anterior ou se a base for zero |

O deslocamento usa a duração real do período, não um mês fixo:

```dax
VAR QtdDias = [Dias no Periodo Selecionado]
RETURN CALCULATE (
    [Valor Medio do Indicador],
    DATEADD ( Dim_Calendario[Data], - QtdDias, DAY )
)
```

Assim, um período de 15 dias é comparado com os 15 dias anteriores, e um de 60 dias com 60 dias. Quando não existe período comparável dentro da janela, o resultado é vazio. Zero seria uma afirmação falsa.

## 04 | Fontes

| Medida | Formato | O que faz |
|---|---|---|
| `Frentes com Dado do Indicador` | `#,##0` | Quantas frentes medem o indicador selecionado |
| `Dias com Dado da Fonte` | `#,##0` | Dias distintos com leitura por fonte |

## 05 | Formatação e UX

Medidas de texto, usadas em títulos dinâmicos. Não devem ser usadas em cartão de valor.

| Medida | O que devolve |
|---|---|
| `Titulo Dinamico do Indicador` | Nome original e unidade, ou "Selecione um indicador" |
| `Mensagem Sem Dados` | "Sem medições no período" quando a contagem é zero |
| `Rotulo Agregacao Recomendada` | Compatibilidade legada; o painel usa `Rotulo Regra Recomendada` para exibir a recomendação sem confundi-la com o cálculo aplicado |
| `Rotulo Regra Recomendada` | Regra declarada na dimensão, por exemplo média ponderada por TC |
| `Rotulo Agregacao Utilizada` | Média aritmética não ponderada exploratória; TC fica bloqueado |
| `Aviso Agregacao Utilizada` | Explica quando a recomendação depende de TC ou de regra logarítmica |
| `Pendencias Abertas na Origem` | Pendências com correção ainda aberta no sistema legado |
| `Pendencias Tratadas na Analitica` | Pendências normalizadas ou documentadas na camada analítica |
| `Aviso Unidade Desconhecida` | "Unidade não confirmada" quando a unidade é Desconhecida |
| `Status do Indicador` | Status de validação do indicador selecionado |

### Medidas de rótulo para cartão

O Desktop abrevia 19.532 como "20 Mil" e ignora as quatro variações de `displayUnits` testadas no sandbox em 30/10/2026 (`labels`, `calloutValue`, literal `'None'` e apenas `precision`). A saída foi formatar em DAX e ligar o cartão em uma medida de texto.

| Medida | Expressão | Resultado |
| --- | --- | --- |
| `Rotulo Registros` | `FORMAT ( [Quantidade de Registros], "#,##0" )` | 19.532 |
| `Rotulo Registros Validados` | `FORMAT ( [Registros Validados], "#,##0" )` | 16.823 |
| `Rotulo Leituras` | `FORMAT ( [Quantidade de Leituras], "#,##0" )` | 903 |
| `Rotulo Ajustes de Escala` | `FORMAT ( [Registros com Ajuste de Escala], "#,##0" )` | 1.585 |
| `Rotulo Valor Original` | `FORMAT ( [Valor Original do Registro], "#,##0" )` | 120.400 |
| `Rotulo Fator Aplicado` | `FORMAT ( [Fator Aplicado do Registro], "#,##0" )` | 10.000 |

Regras:

1. **Só em cartão.** Texto não entra em eixo, legenda, ordenação ou cálculo.
2. **Nunca substituir a medida numérica na regra de negócio.** `Quantidade de Registros` continua sendo a medida oficial; a versão de rótulo é irmã dela.
3. **Se o Desktop passar a aceitar `displayUnits`, estas seis podem ser aposentadas.** O teste de campos avisa se algum visual apontar para medida removida.

## 06 | Rastreabilidade

Consultam `Auditoria_Dados` por `LOOKUPVALUE`, sem relacionamento modelado.

| Medida | O que devolve |
|---|---|
| `Regra de Transformacao do Registro` | Regra aplicada ao registro selecionado |
| `Fator Aplicado do Registro` | Fator de divisão aplicado |
| `Valor Original do Registro` | Valor antes do ajuste |
| `Status Anterior do Registro` | Status antes da normalização |

## Testes aplicados ao catálogo

A suite `tests/test_model_structure.py` verifica, entre outras coisas:

- Toda medida referenciada entre colchetes dentro de uma DAX existe.
- Toda medida tem pasta de exibição.
- As medidas críticas têm descrição.
- A média genérica exige indicador único e agregação aprovada.
- A comparação temporal devolve vazio quando não há período.
- Os formatos `0.00"%"`, `0.00" kg/t"` e `0.0%` estão aplicados nas medidas corretas.

Nenhuma medida foi validada em execução no Power BI. Ver [TEST_PLAN.md](TEST_PLAN.md).
