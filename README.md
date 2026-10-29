# Cana Intelligence

Relatório analítico em Power BI (formato PBIP) para os indicadores de qualidade de uma usina sucroenergética. O projeto é versionável, editável fora do Power BI Desktop e tem o modelo semântico em TMDL.

Fonte única de dados: `data/Base_Usina_PowerBI_Final_v4.xlsx`. Todas as contagens da documentação foram medidas nesse arquivo, não estimadas.

## Situação atual

| Item | Estado |
| --- | --- |
| Modelo semântico aceito pelo parser oficial | Sim, 7 tabelas, 55 medidas, 2 relacionamentos |
| Relatório abre no Power BI Desktop | Sim, aberto e carregado em 29/10/2026 |
| Modelo semântico em TMDL | Implementado, 6 tabelas e 55 medidas |
| Relacionamentos | 2, ambos de um para muitos e filtro simples |
| Páginas do relatório | 6 criadas, sem visuais |
| Tema visual | Implementado em `CanaIntelligence.json` |
| Testes de dados | 47 verificações, todas aprovadas |
| Testes de estrutura do modelo | 31 verificações, todas aprovadas |
| Testes de estrutura do relatório | 43 verificações, todas aprovadas |
| Visuais nativos | Não implementados. Ver a seção de limitações |

As páginas existem, mas estão vazias de visuais. Cada visual tem posição, campos, medida e regra de cor definidos em [docs/VISUAL_SPECIFICATION.md](docs/VISUAL_SPECIFICATION.md), pronto para ser montado no Desktop em poucos minutos por página.

## Estrutura

```text
.
├── dashboard_cana.pbip                  ponto de abertura do projeto
├── dashboard_cana.SemanticModel/
│   └── definition/
│       ├── model.tmdl                   cultura pt-BR, comportamento de filtro
│       ├── expressions.tmdl             parâmetro CaminhoDaBase
│       ├── relationships.tmdl           2 relacionamentos
│       └── tables/                      6 tabelas em TMDL
├── dashboard_cana.Report/
│   ├── definition/report.json           tema base e tema personalizado
│   ├── definition/pages/                6 páginas
│   └── StaticResources/.../BaseThemes/  CanaIntelligence.json
├── data/                                planilha de origem (não versionada)
├── design/references/                   referências visuais enviadas
├── design/canvas/                       desenho das 6 páginas aprovado
├── docs/                                documentação do projeto
├── skills/                              regras locais de visual e layout
├── scripts/data_audit.py                inventário da planilha
└── tests/                               suites de teste executáveis
```

## Como abrir

1. Instale o Power BI Desktop.
2. Confirme que a planilha está em `data/Base_Usina_PowerBI_Final_v4.xlsx`.
2. Abra `dashboard_cana.pbip`.
3. Se o Power BI reclamar do caminho do arquivo, vá em Transformar dados, abra a consulta do parâmetro `CaminhoDaBase` e ajuste para o caminho da sua máquina.
4. Atualize o modelo.

O caminho fica em um único lugar: `dashboard_cana.SemanticModel/definition/expressions.tmdl`. Nenhuma consulta tem caminho absoluto cravado, e existe teste automatizado que falha se alguém cravar um.

## Como rodar os testes

```powershell
python tests/run_tests.py
```

Quatro suites:

- `tests/test_data_contract.py`: confere a planilha contra as regras do modelo (contagens, chaves, escalas, duplicidades, pendência de TC).
- `tests/test_model_structure.py`: confere o TMDL (relacionamentos resolvem, medidas referenciadas existem, formatos percentuais corretos, caminho centralizado).
- `tests/test_report_structure.py`: confere a cadeia de abertura do PBIP, a ligação entre páginas e a declaração do tema.
- `tests/test_tmdl_parser.py`: deserializa o modelo com o parser TMDL oficial que vem com o Power BI Desktop. É o único teste que prova que o projeto realmente abre.

Para rodar só o validador do modelo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_tmdl.ps1
```

Para gerar o inventário da planilha:

```powershell
python scripts/data_audit.py
```

## Documentação

- [Brief do projeto](docs/PROJECT_BRIEF.md)
- [Dicionário de dados](docs/DATA_DICTIONARY.md)
- [Modelo de dados](docs/DATA_MODEL.md)
- [Catálogo de medidas](docs/MEASURES_CATALOG.md)
- [Qualidade dos dados](docs/DATA_QUALITY.md)
- [Sistema de design](docs/DESIGN_SYSTEM.md)
- [Especificação dos visuais](docs/VISUAL_SPECIFICATION.md)
- [Plano e resultados de teste](docs/TEST_PLAN.md)
- [Runbook](docs/RUNBOOK.md)

## Limitações conhecidas

1. **Visuais não implementados.** Escrever o JSON de visuais à mão, sem uma instância do Power BI para serializar e validar, produz visuais que não renderizam ou que o Desktop descarta na abertura. As páginas foram criadas vazias de propósito. O passo a passo de montagem está em [docs/RUNBOOK.md](docs/RUNBOOK.md).
2. **Validação no Desktop pendente.** O modelo foi checado por testes estáticos e pela leitura da planilha, mas não foi aberto em uma instância do Power BI Desktop neste ambiente. O primeiro passo do runbook é essa abertura.
3. **Ponderação por TC bloqueada.** A fonte recomenda média ponderada por TC para 10 indicadores, e TC não tem unidade nem regra confirmadas. Nenhuma medida do modelo calcula média ponderada. Onde é preciso mostrar valor, existe média aritmética declarada como não ponderada.
4. **Safra e ano não são filtros.** A base tem um único valor em cada coluna, `2026/2027` e `2026`. Os filtros ficam como texto no cabeçalho, porque um seletor de valor único não filtra nada.
5. **Auditoria sem relacionamento.** `Auditoria_Dados` não tem relacionamento modelado com a fato. A ligação é feita por `LOOKUPVALUE` usando `ID_Registro`, para não impor uma cardinalidade um para um sem necessidade.

## Dados no Git

A planilha é dado operacional e está no `.gitignore`. Para clonar o projeto em outra máquina, copie o arquivo para `data/`. Instruções em [data/README.md](data/README.md).
