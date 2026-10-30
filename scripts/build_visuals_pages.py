"""Gera os visuais das paginas 3 a 6 (Fontes, Indicadores, Qualidade, Detalhes)
na grade executiva premium.

Inclui:
- Header executivo com identidade e abas pill no topo (destaque na aba ativa)
- Faixa de controle com segmentações e chip de escopo contextual
- Cards KPI de alto impacto no topo de cada página
- Painéis analíticos com cantos arredondados, bordas sutis e sombras suaves
- Rodapé institucional Cana Intelligence com governança de dados

Uso: python scripts/build_visuals_pages.py
"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from pbir_lib import (  # noqa: E402
    Pagina,
    coluna,
    conferir_dentro_da_pagina,
    medida,
    painel_card,
)

FONTES = "b2d5f88c1ea304bb6621"
INDICADORES = "c3e6091d2fb415cc7732"
QUALIDADE = "d4f71a2e30c526dd8843"
DETALHES = "e50b2b3f41d637ee9954"


# ------------------------------------------------------------------ page 3: Fontes

def fontes() -> Pagina:
    p = Pagina(FONTES, "Fontes", indice_pagina=3)
    p.limpar()

    # 1. Header com abas (aba 3 ativa)
    p.barra_navegacao_app(indice_ativo=3)

    # 2. Filtros e chip de escopo
    p.filtro_data(x=24, y=72, w=300, h=46)
    p.filtro("Dim_Indicador", "Nome_Original", x=334, w=320, y=72, h=46)
    p.filtro("Fato_Medicoes", "Grupo_Fonte", x=664, w=240, y=72, h=46)
    p.scope_chip(
        "ESCOPO FONTES  ·  7 frentes de colheita  ·  laboratório central",
        x=914, y=72, w=502, h=46
    )

    # 3. Faixa de 4 KPI Cards (y = 126 a 238, h = 112)
    kpis = [
        ("VOLUME DE LEITURAS", "Total no indicador ativo", "Rotulo Leituras"),
        ("FRENTES COM DADO", "Frentes com cobertura ativa", "Frentes com Dado do Indicador"),
        ("CONFORMIDADE TÉCNICA", "Status de homologação", "Status do Indicador"),
        ("REGRA RECOMENDADA", "Diretriz técnica Dim_Indicador", "Rotulo Regra Recomendada Curta"),
    ]
    largura = (1392 - 16 * (len(kpis) - 1)) // len(kpis)  # 336px
    for i, (tit, sub, med) in enumerate(kpis):
        p.cartao_kpi(
            24 + i * (largura + 16), 126, largura, 114,
            tit, sub, "_Medidas", med, valor_px=22
        )

    # 4. Gráfico da Faixa Observada (Esquerda: x = 24, y = 248, w = 550, h = 500)
    p.add(
        "barChart", 24, 248, 550, 500,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [
                medida("_Medidas", "Minimo Observado"),
                medida("_Medidas", "Maximo Observado"),
            ]},
        },
        container=painel_card(
            "Dispersão Operacional por Fonte",
            "Mínimo e máximo observados por frente de colheita"
        ),
    )

    # 5. Matriz de Comparação por Fonte (Direita: x = 588, y = 248, w = 828, h = 500)
    p.add(
        "matrix", 588, 248, 828, 500,
        {
            "Rows": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Values": {"projections": [
                medida("_Medidas", "Quantidade de Leituras"),
                medida("_Medidas", "Dias com Dado da Fonte"),
                medida("_Medidas", "Minimo Observado"),
                medida("_Medidas", "Maximo Observado"),
            ]},
        },
        container=painel_card(
            "Matriz Comparativa de Desempenho por Fonte",
            "Volumetria de leituras, dias cobertos e extremos operacionais"
        ),
    )

    # 6. Rodapé institucional
    p.rodape_tela()
    return p


# ------------------------------------------------------------------ page 4: Indicadores

def indicadores() -> Pagina:
    p = Pagina(INDICADORES, "Indicadores", indice_pagina=4)
    p.limpar()

    # 1. Header com abas (aba 4 ativa)
    p.barra_navegacao_app(indice_ativo=4)

    # 2. Filtros e chip de escopo
    p.filtro_data(x=24, y=72, w=300, h=46)
    p.filtro("Fato_Medicoes", "Fonte", x=334, w=230, y=72, h=46)
    p.filtro("Dim_Indicador", "Nome_Original", x=574, w=330, y=72, h=46)
    p.scope_chip(
        "EXPLORADOR ANALÍTICO  ·  estatísticas descritivas  ·  distribuição por faixas",
        x=914, y=72, w=502, h=46
    )

    # 3. Faixa de 5 KPI Cards Estatísticos (y = 126 a 238, h = 112)
    kpis = [
        ("MÉDIA NÃO PONDERADA", "Escala direta do indicador", "Media Aritmetica Nao Ponderada"),
        ("MEDIANA OBSERVADA", "Valor central robusto", "Mediana do Indicador"),
        ("MÍNIMO REGISTRADO", "Limite inferior observado", "Minimo Observado"),
        ("MÁXIMO REGISTRADO", "Limite superior observado", "Maximo Observado"),
        ("TOTAL DE LEITURAS", "Amostras na safra 2026", "Rotulo Leituras"),
    ]
    largura = (1392 - 16 * (len(kpis) - 1)) // len(kpis)  # 265px
    for i, (tit, sub, med) in enumerate(kpis):
        p.cartao_kpi(
            24 + i * (largura + 16), 126, largura, 114,
            tit, sub, "_Medidas", med, valor_px=22
        )

    # 4. Série Temporal com Média Móvel (Esquerda: x = 24, y = 248, w = 710, h = 500)
    p.add(
        "lineChart", 24, 248, 710, 500,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [
                medida("_Medidas", "Media Aritmetica Nao Ponderada"),
                medida("_Medidas", "Media Movel 7 Dias"),
            ]},
        },
        container=painel_card(
            "Comportamento Temporal e Tendência (7 Dias)",
            "Média diária observada e curva de suavização móvel de 7 dias"
        ),
    )

    # 5. Histograma de Distribuição em 14 Faixas (Direita: x = 748, y = 248, w = 668, h = 500)
    p.add(
        "columnChart", 748, 248, 668, 500,
        {
            "Category": {"projections": [coluna("Dim_Faixa_Valor", "Faixa_Label")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Leituras por Faixa")]},
        },
        container=painel_card(
            "Histograma de Distribuição de Frequência",
            "Contagem em 14 faixas relativas; não representa limite técnico homologado"
        ),
    )

    # 6. Rodapé institucional
    p.rodape_tela()
    return p


# ------------------------------------------------------------------ page 5: Qualidade

def qualidade() -> Pagina:
    p = Pagina(QUALIDADE, "Qualidade", indice_pagina=5)
    p.limpar()

    # 1. Header com abas (aba 5 ativa)
    p.barra_navegacao_app(indice_ativo=5)

    # 2. Filtros e chip de escopo
    p.filtro_data(x=24, y=72, w=300, h=46)
    p.filtro("Fato_Medicoes", "Status_Validacao", x=334, w=240, y=72, h=46)
    p.filtro("Dim_Indicador", "Nome_Original", x=584, w=320, y=72, h=46)
    p.scope_chip(
        "AUDITORIA ATIVA  ·  19.532 linhas  ·  1.585 ajustes  ·  TC pendente",
        x=914, y=72, w=502, h=46
    )

    # 3. Faixa de 4 KPI Cards de Qualidade (y = 126 a 238, h = 112)
    kpis = [
        ("REGISTROS TOTAIS", "Total carregado da fato", "Rotulo Registros"),
        ("REGISTROS PENDENTES", "Regra não homologada (TC)", "Registros Pendentes"),
        ("TAXA DE PENDÊNCIA", "Proporção sobre o total", "Percentual de Registros Pendentes"),
        ("AJUSTES DE ESCALA", "Tratamento aplicado na camada analítica", "Rotulo Ajustes de Escala"),
    ]
    largura = (1392 - 16 * (len(kpis) - 1)) // len(kpis)  # 336px
    for i, (tit, sub, med) in enumerate(kpis):
        p.cartao_kpi(
            24 + i * (largura + 16), 126, largura, 114,
            tit, sub, "_Medidas", med, valor_px=22
        )

    # 4. Gráficos do Meio (y = 248 a 486, h = 238)
    # 4.1 Registros por Mês (Esquerda: x = 24, w = 684)
    p.add(
        "columnChart", 24, 248, 684, 238,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Nome_Mes")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=painel_card(
            "Volumetria de Coleta por Mês",
            "Tratamento analítico aplicado; pendências na origem continuam visíveis"
        ),
    )

    # 4.2 Status de Validação (Direita: x = 722, w = 694)
    p.add(
        "barChart", 722, 248, 694, 238,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Status_Validacao")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=painel_card(
            "Composição por Status de Validação",
            "Registros validados (16.823), normalizados (1.806) e pendentes (903)"
        ),
    )

    # 5. Tabela de Pendências de Validação (Abaixo: x = 24, y = 496, w = 1392, h = 250)
    p.add(
        "tableEx", 24, 496, 1392, 250,
        {"Values": {"projections": [
            coluna("Pendencias_Validacao", "ID_Pendencia"),
            coluna("Pendencias_Validacao", "Indicador"),
            coluna("Pendencias_Validacao", "Problema"),
            coluna("Pendencias_Validacao", "Acao_Recomendada"),
            coluna("Pendencias_Validacao", "Status"),
        ]}},
        container=painel_card(
            "Inventário Oficial de Pendências Técnicas de Auditoria",
            "Tratamento analítico aplicado; correção no legado ainda pode estar aberta"
        ),
    )

    # 6. Rodapé institucional
    p.rodape_tela(
        "Base_Usina_PowerBI_Final_v4.xlsx · Fato_Medicoes, Pendencias_Validacao, Auditoria_Dados · P_TC_01 Aberta"
    )
    return p


# ------------------------------------------------------------------ page 6: Detalhes

def detalhes() -> Pagina:
    p = Pagina(DETALHES, "Detalhes", indice_pagina=6)
    p.limpar()

    # 1. Header com abas (aba 6 ativa)
    p.barra_navegacao_app(indice_ativo=6)

    # 2. Filtros e chip de escopo
    p.filtro_data(x=24, y=72, w=300, h=46)
    p.filtro("Dim_Indicador", "Nome_Original", x=334, w=320, y=72, h=46)
    p.filtro("Fato_Medicoes", "Fonte", x=664, w=240, y=72, h=46)
    p.scope_chip(
        "RASTREABILIDADE OPERACIONAL  ·  inspeção linha a linha  ·  histórico de ajustes",
        x=914, y=72, w=502, h=46
    )

    # 3. Faixa de 4 KPI Cards de Contexto (y = 126 a 238, h = 112)
    kpis = [
        ("REGISTROS NO FILTRO", "Medições selecionadas", "Rotulo Registros"),
        ("COM AJUSTE DE ESCALA", "Passaram por auditoria", "Rotulo Ajustes de Escala"),
        ("PRIMEIRA DATA", "Início da coleta na safra", "Primeira Data com Dados"),
        ("ÚLTIMA DATA", "Encerramento da coleta", "Ultima Data com Dados"),
    ]
    largura = (1392 - 16 * (len(kpis) - 1)) // len(kpis)  # 336px
    for i, (tit, sub, med) in enumerate(kpis):
        p.cartao_kpi(
            24 + i * (largura + 16), 126, largura, 114,
            tit, sub, "_Medidas", med, valor_px=22
        )

    # 4. Trilho de Rastreabilidade via LOOKUPVALUE (Esquerda: x = 24, y = 248, w = 310, h = 500)
    trilho_itens = [
        ("VALOR ORIGINAL", "Auditados ou pré-ajuste", "Rotulo Valor Original"),
        ("FATOR APLICADO", "Divisão efetuada na carga", "Rotulo Fator Aplicado"),
        ("REGRA APLICADA", "Fundamentação técnica", "Rotulo Regra Aplicada"),
    ]
    h_card = (500 - 14 * 2) // 3  # 157px
    for i, (tit, sub, med) in enumerate(trilho_itens):
        p.cartao_kpi(
            24, 248 + i * (h_card + 14), 290, h_card,
            tit, sub, "_Medidas", med, valor_px=18
        )

    # 5. Tabela Detalhada Linha a Linha (Direita: x = 324, y = 248, w = 1092, h = 500)
    p.add(
        "tableEx", 324, 248, 1092, 500,
        {"Values": {"projections": [
            coluna("Fato_Medicoes", "ID_Registro"),
            coluna("Fato_Medicoes", "Data"),
            coluna("Fato_Medicoes", "Fonte"),
            coluna("Fato_Medicoes", "Indicador_Codigo"),
            coluna("Fato_Medicoes", "Valor"),
            coluna("Fato_Medicoes", "Valor_Original"),
            coluna("Fato_Medicoes", "Status_Validacao"),
        ]}},
        container=painel_card(
            "Rastreabilidade Operacional Registro a Registro",
            "Identificador, data, fonte, indicador, medição atual, valor original e validação"
        ),
    )

    # 6. Rodapé institucional
    p.rodape_tela(
        "Base_Usina_PowerBI_Final_v4.xlsx · Fato_Medicoes (19.532) · Auditoria_Dados (1.585) · Dim_Indicador (23)"
    )
    return p


def main() -> int:
    montadas: list[Pagina] = []
    falhas: list[str] = []

    for montar in (fontes, indicadores, qualidade, detalhes):
        pagina = montar()
        print(pagina.relatorio())
        falhas.extend(conferir_dentro_da_pagina(pagina))
        montadas.append(pagina)
        print()

    if falhas:
        print("PROBLEMAS DE GRADE")
        for item in falhas:
            print("  - " + item)
        return 1

    total = sum(len(p.gerados) for p in montadas)
    print(f"[OK] {total} visuais gerados com sucesso em {len(montadas)} paginas na grade executiva premium.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
