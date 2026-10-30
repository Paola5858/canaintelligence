"""Gera os visuais da pagina 1 (Visao geral) na grade executiva premium.

Inclui:
- Header executivo com identidade e abas pill no topo
- Faixa de controle com segmentações e chip de escopo ativo
- 5 cards KPI no topo com título, subtítulo e valores de alto impacto
- Trilho lateral com 3 cards contextuais do indicador selecionado
- Série temporal diária ampliada com eixos limpos
- Gráfico de barras horizontais de distribuição por fonte
- Rodapé institucional Cana Intelligence com governança de dados

Uso: python scripts/build_visuals_page1.py
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

PAGINA = "5a36b06c01771dee7876"


def visao_geral() -> Pagina:
    p = Pagina(PAGINA, "Visão geral", indice_pagina=1)
    p.limpar()

    # 1. Header com identidade e abas de navegação no formato pill
    p.barra_navegacao_app(indice_ativo=1)

    # 2. Faixa de filtros com chip de escopo
    p.filtro_data(x=24, y=72, w=300, h=46)
    p.filtro("Fato_Medicoes", "Fonte", x=334, w=230, y=72, h=46)
    p.filtro("Dim_Indicador", "Nome_Original", x=574, w=330, y=72, h=46)
    p.scope_chip(
        "RECORTE ATIVO  ·  ATR (kg/t)  ·  8 fontes  ·  19.532 linhas",
        x=914, y=72, w=502, h=46
    )

    # 3. Faixa superior de 5 KPI Cards (y = 126 a 238, h = 112)
    kpis = [
        ("DIAS MONITORADOS", "80,1% de cobertura contínua", "Dias com Dados"),
        ("REGISTROS VÁLIDOS", "86,1% sem pendência técnica", "Rotulo Registros Validados"),
        ("INDICADORES ATIVOS", "22 homologados · 1 sob revisão", "Quantidade de Indicadores"),
        ("FONTES DE COLETA", "7 frentes + 1 laboratório", "Quantidade de Fontes"),
        ("ÚLTIMA MEDIÇÃO", "Safra 2026/2027 atualizada", "Ultima Data com Dados"),
    ]
    largura = (1392 - 16 * (len(kpis) - 1)) // len(kpis)  # 265px cada
    for i, (titulo_card, subtitulo_card, nome_medida) in enumerate(kpis):
        p.cartao_kpi(
            24 + i * (largura + 16), 126, largura, 114,
            titulo_card, subtitulo_card, "_Medidas", nome_medida, valor_px=24
        )

    # 4. Trilho do Indicador Selecionado (3 cards à esquerda: x = 24, w = 290, h = 500)
    trilho_itens = [
        ("VOLUME DE LEITURAS", "Total no escopo selecionado", "Rotulo Leituras"),
        ("REGRA RECOMENDADA", "Diretriz técnica Dim_Indicador", "Rotulo Regra Recomendada Curta"),
        ("STATUS DE VALIDAÇÃO", "Conformidade na dimensão", "Status do Indicador"),
    ]
    h_card = (500 - 14 * 2) // 3  # 157px
    for i, (tit, sub, med) in enumerate(trilho_itens):
        p.cartao_kpi(
            24, 248 + i * (h_card + 14), 290, h_card,
            tit, sub, "_Medidas", med, valor_px=20
        )

    # 5. Série Temporal Diária do Indicador (Centro: x = 324, y = 248, w = 700, h = 500)
    p.add(
        "lineChart", 324, 248, 700, 500,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=painel_card(
            "Evolução Temporal do Indicador",
            "Média diária não ponderada; ponderação por TC bloqueada até P_TC_01"
        ),
    )

    # 6. Distribuição por Fonte (Direita: x = 1034, y = 248, w = 382, h = 500)
    p.add(
        "barChart", 1034, 248, 382, 500,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=painel_card(
            "Distribuição por Fonte Operacional",
            "Volume total de medições por frente e laboratório"
        ),
    )

    # 7. Rodapé institucional
    p.rodape_tela()
    return p


def main() -> int:
    pagina = visao_geral()
    print(pagina.relatorio())

    problemas = conferir_dentro_da_pagina(pagina)
    if problemas:
        print("\nPROBLEMAS DE GRADE")
        for item in problemas:
            print("  - " + item)
        return 1

    print("\n[OK] Pagina 1 (Visao geral) gerada com sucesso na grade executiva premium.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
