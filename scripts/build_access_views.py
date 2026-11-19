"""Gera as três páginas de experiência por público no relatório PBIR.

As páginas organizam a navegação e os dados para cada público, mas não
restringem acesso: o modelo semântico ainda não tem RLS.
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
    sem_cromo,
)

DIRETORIA = "f6172b40a8c94d3ea101"
GERENCIA = "a72b45c91d064e3b8f12"
OPERACAO = "c83d56e0f1a74a629b23"


def faixa_perfil(pagina: Pagina, perfil: str, descricao: str) -> None:
    pagina.add(
        "textbox", 24, 66, 1392, 26,
        objects={"general": [{"properties": {"paragraphs": [{
            "textRuns": [
                {"value": perfil, "textStyle": {
                    "fontSize": "10pt",
                    "fontFamily": "Aptos Display",
                    "fontWeight": "700",
                    "color": "#173F35",
                }},
                {"value": "  ·  " + descricao, "textStyle": {
                    "fontSize": "9pt",
                    "fontFamily": "Aptos",
                    "color": "#8B4F38",
                }},
            ],
            "horizontalTextAlignment": "left",
        }]}}]},
        container=sem_cromo(),
    )


def filtros(pagina: Pagina, escopo: str) -> None:
    pagina.filtro_data(x=24, y=94, w=240, h=64)
    pagina.filtro("Dim_Indicador", "Nome_Original", x=274, w=240, y=94, h=64)
    pagina.filtro("Fato_Medicoes", "Fonte", x=524, w=210, y=94, h=64)
    pagina.filtro("Fato_Medicoes", "Status_Validacao", x=744, w=180, y=94, h=64)
    pagina.scope_chip(escopo, x=934, y=94, w=384, h=64)
    pagina.limpar_filtros_button(x=1330, y=94, w=86, h=64)


def faixa_kpis(pagina: Pagina, itens: list[tuple[str, str, str, str]]) -> None:
    largura = (1392 - 16 * (len(itens) - 1)) // len(itens)
    for i, (titulo, subtitulo, tabela, medida_nome) in enumerate(itens):
        pagina.cartao_kpi(
            24 + i * (largura + 16), 174, largura, 96,
            titulo, subtitulo, tabela, medida_nome, valor_px=22,
        )


def diretoria() -> Pagina:
    p = Pagina(DIRETORIA, "Diretoria", indice_pagina=7)
    p.limpar()
    p.barra_navegacao_app(indice_ativo=7, incluir_visoes=True)
    faixa_perfil(p, "DIRETORIA · VISÃO ESTRATÉGICA",
                 "Experiência visual; não restringe dados (RLS não configurada)")
    filtros(p, "RECORTE EXECUTIVO  ·  indicadores, safra e cobertura")
    faixa_kpis(p, [
        ("DIAS COM DADO", "Cobertura observada", "_Medidas", "Dias com Dados"),
        ("LEITURAS", "No recorte selecionado", "_Medidas", "Rotulo Registros"),
        ("FONTES ATIVAS", "Frentes e laboratório", "_Medidas", "Quantidade de Fontes"),
        ("PENDÊNCIAS", "Registros em revisão", "_Medidas", "Registros Pendentes"),
    ])
    p.add(
        "lineChart", 24, 286, 850, 220,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=painel_card(
            "Evolução do indicador selecionado",
            "Média não ponderada; não representa meta ou limite técnico"
        ),
    )
    p.add(
        "barChart", 890, 286, 526, 220,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=painel_card(
            "Volume por fonte",
            "Distribuição das leituras no recorte ativo"
        ),
    )
    p.add(
        "tableEx", 24, 518, 1392, 224,
        {"Values": {"projections": [
            coluna("Dim_Indicador", "Codigo"),
            coluna("Dim_Indicador", "Nome_Original"),
            coluna("Dim_Indicador", "Unidade_Confirmada"),
            coluna("Dim_Indicador", "Status_Validacao"),
            medida("_Medidas", "Quantidade de Leituras"),
        ]}},
        container=painel_card(
            "Indicadores e situação de validação",
            "A unidade permanece explícita; indicadores não são somados entre si"
        ),
    )
    p.rodape_tela(
        "Visão executiva · experiência de navegação, não controle de acesso · modelo sem RLS"
    )
    return p


def gerencia() -> Pagina:
    p = Pagina(GERENCIA, "Gerência", indice_pagina=8)
    p.limpar()
    p.barra_navegacao_app(indice_ativo=8, incluir_visoes=True)
    faixa_perfil(p, "GERÊNCIA · VISÃO TÁTICA",
                 "Acompanhamento por fonte e registro; não restringe dados (RLS não configurada)")
    filtros(p, "RECORTE TÁTICO  ·  localizar variações e pendências")
    faixa_kpis(p, [
        ("REGISTROS", "No recorte ativo", "_Medidas", "Rotulo Registros"),
        ("PENDENTES", "Aguardam regra técnica", "_Medidas", "Registros Pendentes"),
        ("NORMALIZADOS", "Com ajuste de escala", "_Medidas", "Registros Normalizados"),
        ("VALIDADOS", "Sem ajuste na carga", "_Medidas", "Registros Validados"),
    ])
    p.add(
        "barChart", 24, 286, 416, 216,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=painel_card(
            "Registros por fonte",
            "Use os filtros para localizar uma frente ou grupo"
        ),
    )
    p.add(
        "lineChart", 456, 286, 960, 216,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=painel_card(
            "Evolução diária do indicador",
            "Média aritmética não ponderada; ponderação por TC não disponível"
        ),
    )
    p.add(
        "tableEx", 24, 518, 1392, 224,
        {"Values": {"projections": [
            coluna("Fato_Medicoes", "Data"),
            coluna("Fato_Medicoes", "Fonte"),
            coluna("Fato_Medicoes", "ID_Registro"),
            coluna("Fato_Medicoes", "Indicador_Codigo"),
            coluna("Fato_Medicoes", "Valor"),
            coluna("Fato_Medicoes", "Valor_Original"),
            coluna("Fato_Medicoes", "Status_Validacao"),
        ]}},
        container=painel_card(
            "Registros para investigar",
            "O modelo não contém identificador de funcionário; a análise disponível é por fonte e registro"
        ),
    )
    p.rodape_tela(
        "Visão tática · dados agregados e registro a registro · modelo sem identificador de funcionário e sem RLS"
    )
    return p


def operacao() -> Pagina:
    p = Pagina(OPERACAO, "Operação", indice_pagina=9)
    p.limpar()
    p.barra_navegacao_app(indice_ativo=9, incluir_visoes=True)
    faixa_perfil(p, "OPERAÇÃO · VISÃO OPERACIONAL",
                 "Consulta da base carregada; não restringe dados (RLS não configurada)")
    filtros(p, "RECORTE OPERACIONAL  ·  dados normalizados e status de carga")
    faixa_kpis(p, [
        ("REGISTROS", "No recorte ativo", "_Medidas", "Rotulo Registros"),
        ("PENDENTES", "Regra técnica não confirmada", "_Medidas", "Registros Pendentes"),
        ("AJUSTES DE ESCALA", "Registros normalizados", "_Medidas", "Registros com Ajuste de Escala"),
        ("DIAS COM DADO", "Janela observada", "_Medidas", "Dias com Dados"),
    ])
    p.add(
        "tableEx", 24, 286, 1392, 456,
        {"Values": {"projections": [
            coluna("Fato_Medicoes", "Data"),
            coluna("Fato_Medicoes", "Fonte"),
            coluna("Fato_Medicoes", "ID_Registro"),
            coluna("Fato_Medicoes", "Indicador_Codigo"),
            coluna("Fato_Medicoes", "Valor_Original"),
            coluna("Fato_Medicoes", "Valor"),
            coluna("Fato_Medicoes", "Ajuste_Aplicado"),
            coluna("Fato_Medicoes", "Status_Validacao"),
            coluna("Fato_Medicoes", "Linha_Origem"),
        ]}},
        container=painel_card(
            "Dados normalizados e rastreabilidade da carga",
            "Valor de origem, valor tratado, ajuste aplicado, status e linha de origem"
        ),
    )
    p.rodape_tela(
        "Visão operacional · o modelo não contém identificador de funcionário · modelo sem RLS"
    )
    return p


def main() -> int:
    paginas = [diretoria(), gerencia(), operacao()]
    problemas = [
        f"{pagina.nome_pagina}: {problema}"
        for pagina in paginas
        for problema in conferir_dentro_da_pagina(pagina)
    ]
    for pagina in paginas:
        print(pagina.relatorio())
    if problemas:
        print("\nPROBLEMAS DE GRADE")
        for problema in problemas:
            print("  - " + problema)
        return 1
    print("\n[OK] Três páginas por público geradas e dentro da grade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
