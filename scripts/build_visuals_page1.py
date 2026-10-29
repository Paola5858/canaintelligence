"""Gera os visuais da pagina 1 (Visao geral) na grade nova.

Reescrito sobre scripts/pbir_lib.py: a pagina nasceu no piloto com helpers
proprios e na grade antiga (cards em y=290, grafico em y=410). Agora usa a mesma
grade das paginas 2 a 6, com faixa de indicadores em y=220, trilho em x=24 e
conteudo analitico de 340 a 1416.

O script limpa a pasta visuals antes de gerar. Sem isso, um visual removido do
codigo continuaria no relatorio como arquivo orfao.

Posicoes e campos: docs/VISUAL_SPECIFICATION.md, pagina 1.

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
    titulo,
)

PAGINA = "5a36b06c01771dee7876"


def visao_geral() -> Pagina:
    p = Pagina("5a36b06c01771dee7876", "Visão geral")
    p.limpar()

    p.cabecalho_tela()
    p.filtro_data()
    p.filtro("Fato_Medicoes", "Fonte", 360, w=200)
    p.filtro("Dim_Indicador", "Nome_Original", 576, w=320)

    # 1.6 faixa de cobertura: cinco cartoes abertos, 1392px de largura
    cobertura = [
        ("Dias com dados", "Dias com Dados"),
        ("Registros validados", "Registros Validados"),
        ("Indicadores", "Quantidade de Indicadores"),
        ("Fontes", "Quantidade de Fontes"),
        ("Última medição", "Ultima Data com Dados"),
    ]
    largura = (1392 - 16 * (len(cobertura) - 1)) // len(cobertura)
    for i, (rotulo, nome) in enumerate(cobertura):
        # 120px: o cartao do Desktop escala o valor sozinho e cortava a base em 92px
        p.cartao(24 + i * (largura + 16), 220, largura, 120, rotulo, "_Medidas", nome, valor_px=18)

    # 1.8 trilho do indicador
    # tres cartoes de 112px: quatro de 88px cortavam o valor
    p.trilho([
        ("Leituras", "_Medidas", "Quantidade de Leituras"),
        ("Agregação", "_Medidas", "Rotulo Agregacao Recomendada"),
        ("Status do indicador", "_Medidas", "Status do Indicador"),
    ], y=356, h=112, gap=16)

    # 1.9 evolucao diaria
    p.add(
        "lineChart", 340, 356, 684, 378,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=titulo("Série diária", "Média aritmética não ponderada do indicador selecionado"),
    )

    # 1.10 cobertura por fonte
    p.add(
        "barChart", 1040, 356, 376, 378,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=titulo("Cobertura por fonte", "Registros de todos os indicadores"),
    )

    # 1.10 rodape: origem do dado. Contagens de pendencia ficam no painel de qualidade.
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

    print("\nPagina na grade nova: faixa em 220 com 120px, trilho e analise de 356 a 734.")
    print("Pendente no Desktop: formatacao fina (unidade de exibicao, eixos, rotulos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
