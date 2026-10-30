"""Gera os visuais da pagina 2 (Evolucao) na grade executiva premium.

Inclui:
- Header executivo com identidade e abas pill no topo (destaque na aba Evolução)
- Faixa de controle com segmentações e chip de escopo temporal
- Trilho lateral à esquerda com 4 cards contextuais
- Gráfico de série temporal diária ampliado
- Gráfico de sazonalidade mensal da safra
- Bloco analítico de comparação temporal (Média Atual, Média Anterior, Variação %)
- Rodapé institucional Cana Intelligence

Uso: python scripts/build_visuals_page2.py
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

PAGINA = "a1c4e77b0d92f3aa5510"


def evolucao() -> Pagina:
    p = Pagina(PAGINA, "Evolução", indice_pagina=2)
    p.limpar()

    # 1. Header com identidade e abas de navegação (aba 2 ativa)
    p.barra_navegacao_app(indice_ativo=2)

    # 2. Faixa de filtros com chip de escopo
    p.filtro_data(x=24, y=72, w=300, h=46)
    p.filtro("Fato_Medicoes", "Fonte", x=334, w=230, y=72, h=46)
    p.filtro("Dim_Indicador", "Nome_Original", x=574, w=330, y=72, h=46)
    p.scope_chip(
        "🎯 ESCOPO TEMPORAL: Janela 04/01 a 11/12/2026  |  274 Dias com Leituras",
        x=914, y=72, w=502, h=46
    )

    # 3. Trilho do Indicador à esquerda (4 cards: x = 24, w = 290, y = 126 a 748, h = 622)
    trilho_itens = [
        ("📈 VOLUME DE LEITURAS", "Contagem no período", "Rotulo Leituras"),
        ("🏭 FRENTES COM DADO", "Frentes que medem", "Frentes com Dado do Indicador"),
        ("🛡️ CONFORMIDADE TÉCNICA", "Status homologado", "Status do Indicador"),
        ("📐 REGRA DE AGREGAÇÃO", "Diretriz da dimensão", "Rotulo Agregacao Recomendada"),
    ]
    h_card = (622 - 12 * 3) // 4  # 146px
    for i, (tit, sub, med) in enumerate(trilho_itens):
        h_atual = h_card if i < 3 else (622 - 3 * (h_card + 12))
        p.cartao_kpi(
            24, 126 + i * (h_card + 12), 290, h_atual,
            tit, sub, "_Medidas", med, valor_px=20
        )

    # 4. Gráfico Principal Superior: Série Diária Ampla (x = 324, y = 126, w = 1092, h = 368)
    p.add(
        "lineChart", 324, 126, 1092, 368,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=painel_card(
            "Comportamento Temporal Contínuo do Indicador",
            "Série diária da média aritmética ao longo da safra 2026"
        ),
    )

    # 5. Gráfico Inferior Esquerdo: Sazonalidade Mensal (x = 324, y = 504, w = 590, h = 244)
    p.add(
        "lineChart", 324, 504, 590, 244,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Nome_Mes")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=painel_card(
            "Sazonalidade Mensal da Safra",
            "Média consolidada por mês da colheita e moagem"
        ),
    )

    # 6. Bloco Inferior Direito: Comparação de Períodos (3 cards: x = 924, y = 504, w = 492, h = 244)
    comparacao = [
        ("📅 PERÍODO ATUAL", "Média na janela", "Media Aritmetica Nao Ponderada"),
        ("⏮️ PERÍODO ANTERIOR", "Média deslocada", "Rotulo Media do Periodo Anterior"),
        ("📊 VARIAÇÃO %", "Diferença relativa", "Rotulo Variacao Percentual"),
    ]
    w_comp = (492 - 12 * 2) // 3  # 156px
    for i, (tit, sub, med) in enumerate(comparacao):
        p.cartao_kpi(
            924 + i * (w_comp + 12), 504, w_comp, 244,
            tit, sub, "_Medidas", med, valor_px=18
        )

    # 7. Rodapé institucional
    p.rodape_tela()
    return p


def main() -> int:
    pagina = evolucao()
    print(pagina.relatorio())

    problemas = conferir_dentro_da_pagina(pagina)
    if problemas:
        print("\nPROBLEMAS DE GRADE")
        for item in problemas:
            print("  - " + item)
        return 1

    print("\n[OK] Pagina 2 (Evolucao) gerada com sucesso na grade executiva premium.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
