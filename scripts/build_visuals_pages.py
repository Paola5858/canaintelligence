"""Gera os visuais das paginas 3 a 6 (Fontes, Indicadores, Qualidade, Detalhes).

Posicoes e campos vem de docs/VISUAL_SPECIFICATION.md. Cada pagina usa a mesma
grade: cabecalho em 24,24; filtros em y=152; conteudo de 220 a 734.

O que fica para o Desktop, e esta escrito em docs/RUNBOOK.md:
- formatacao fina (unidade de exibicao, rotulo de dado, eixos)
- o grupo de faixas da distribuicao, na pagina Indicadores
- a matriz de Fontes com faixa observada empilhada, que exige serie invisivel
- o botao Voltar, que depende de acao de navegacao

Uso: python scripts/build_visuals_pages.py
"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from pbir_lib import Pagina, coluna, conferir_dentro_da_pagina, lit, medida, sem_cromo, titulo  # noqa: E402

FONTES = "b2d5f88c1ea304bb6621"
INDICADORES = "c3e6091d2fb415cc7732"
QUALIDADE = "d4f71a2e30c526dd8843"
DETALHES = "e50b2b3f41d637ee9954"


def cartoes_em_linha(pagina: Pagina, itens, x0, y, largura_total, h, gap=16, valor_px=22):
    """Distribui cartoes com a mesma largura dentro de uma faixa."""
    n = len(itens)
    largura = (largura_total - gap * (n - 1)) // n
    for i, (rotulo, tabela, nome) in enumerate(itens):
        pagina.cartao(x0 + i * (largura + gap), y, largura, h, rotulo, tabela, nome, valor_px)


# ------------------------------------------------------------------ page 3

def fontes() -> Pagina:
    p = Pagina(FONTES, "Fontes")
    p.limpar()
    p.cabecalho_tela()
    p.filtro_data()
    p.filtro("Dim_Indicador", "Nome_Original", 360, w=320)
    p.filtro("Fato_Medicoes", "Grupo_Fonte", 696, w=200)

    p.trilho([
        ("Leituras", "_Medidas", "Rotulo Leituras"),
        ("Frentes", "_Medidas", "Frentes com Dado do Indicador"),
        ("Status", "_Medidas", "Status do Indicador"),
        ("Agregação", "_Medidas", "Rotulo Agregacao Recomendada"),
    ])

    # faixa observada: minimo e maximo como duas series do mesmo eixo
    p.add(
        "barChart", 340, 220, 420, 514,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [
                medida("_Medidas", "Minimo Observado"),
                medida("_Medidas", "Maximo Observado"),
            ]},
        },
        container=titulo("Faixa observada", "Mínimo e máximo por frente"),
    )

    # Matriz, nao tabela: a tabela descartou as quatro medidas e mostrou so a
    # coluna Fonte. A linha de total da matriz precisa ser desligada no Desktop,
    # porque a propriedade subTotals nao foi aceita na versao de 30/10/2026.
    p.add(
        "matrix", 776, 220, 640, 514,
        {
            "Rows": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Values": {"projections": [
                medida("_Medidas", "Quantidade de Leituras"),
                medida("_Medidas", "Dias com Dado da Fonte"),
                medida("_Medidas", "Minimo Observado"),
                medida("_Medidas", "Maximo Observado"),
            ]},
        },
        container=titulo("Comparação por fonte", "Leituras, cobertura e faixa"),
    )
    p.rodape_tela()
    return p


# ------------------------------------------------------------------ page 4

def indicadores() -> Pagina:
    p = Pagina(INDICADORES, "Indicadores")
    p.limpar()
    p.cabecalho_tela()
    p.filtro_data()
    p.filtro("Fato_Medicoes", "Fonte", 360, w=200)
    p.filtro("Dim_Indicador", "Nome_Original", 576, w=320)

    p.trilho([
        ("Leituras", "_Medidas", "Rotulo Leituras"),
        ("Frentes", "_Medidas", "Frentes com Dado do Indicador"),
        ("Status", "_Medidas", "Status do Indicador"),
        ("Agregação", "_Medidas", "Rotulo Agregacao Recomendada"),
    ])

    # 96px: com 72px o valor era cortado na base do cartao, igual as outras paginas
    cartoes_em_linha(p, [
        ("Mediana", "_Medidas", "Mediana do Indicador"),
        ("Média não ponderada", "_Medidas", "Media Aritmetica Nao Ponderada"),
        ("Mínimo", "_Medidas", "Minimo Observado"),
        ("Máximo", "_Medidas", "Maximo Observado"),
        ("Leituras", "_Medidas", "Rotulo Leituras"),
    ], x0=340, y=220, largura_total=1076, h=96)

    # A serie ocupa o painel esquerdo; o painel direito fica reservado para a
    # distribuicao, cuja faixa depende do indicador escolhido.
    p.add(
        "lineChart", 340, 332, 620, 402,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [
                medida("_Medidas", "Media Aritmetica Nao Ponderada"),
                medida("_Medidas", "Media Movel 7 Dias"),
            ]},
        },
        container=titulo("Série temporal", "Média não ponderada e média móvel de 7 dias"),
    )

    # 4.5 distribuicao: sem o grupo de faixas nao existe eixo honesto.
    # Em vez de deixar um vazio silencioso, o relatorio explica a limitacao.
    # Um bin fixo misturaria escalas incompatíveis quando o indicador muda.
    p.add(
        "textbox", 976, 332, 440, 402,
        objects={"general": [{"properties": {"paragraphs": [{
            "textRuns": [
                {"value": "Distribuição por faixas não configurada", "textStyle": {
                    "fontSize": "16pt", "fontFamily": "Segoe UI Semibold",
                    "color": "#173F35", "fontWeight": "600",
                }},
                {"value": "\n\nO eixo precisa de faixas calculadas para o indicador selecionado.\n"
                         "Como os indicadores usam escalas e unidades diferentes, uma faixa fixa"
                         " no modelo misturaria grandezas incompatíveis.\n\n"
                         "Configure o agrupamento de Fato_Medicoes[Valor] no Power BI Desktop "
                         "com 14 intervalos iguais após selecionar um indicador.",
                 "textStyle": {
                    "fontSize": "12pt", "fontFamily": "Segoe UI",
                    "color": "#76817B",
                }},
            ],
            "horizontalTextAlignment": "left",
        }]}}]},
        container=sem_cromo(),
    )
    p.rodape_tela()
    return p


# ------------------------------------------------------------------ page 5

def qualidade() -> Pagina:
    p = Pagina(QUALIDADE, "Qualidade")
    p.limpar()
    p.cabecalho_tela()
    p.filtro_data()
    p.filtro("Fato_Medicoes", "Status_Validacao", 360, w=240)
    p.filtro("Dim_Indicador", "Nome_Original", 616, w=280)

    # quatro cartoes de 120px: seis de 76px cortavam todos os valores
    p.trilho([
        ("Registros", "_Medidas", "Rotulo Registros"),
        ("Pendentes", "_Medidas", "Registros Pendentes"),
        ("% pendente", "_Medidas", "Percentual de Registros Pendentes"),
        ("Ajustes", "_Medidas", "Rotulo Ajustes de Escala"),
    ])

    p.add(
        "columnChart", 340, 220, 660, 184,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Nome_Mes")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=titulo("Registros por mês", "Todos os indicadores · 19.532 registros"),
    )

    p.add(
        "barChart", 1016, 220, 400, 184,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Status_Validacao")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        container=titulo("Status de validação", "Registros por status"),
    )

    p.add(
        "tableEx", 340, 420, 1076, 314,
        {"Values": {"projections": [
            coluna("Pendencias_Validacao", "ID_Pendencia"),
            coluna("Pendencias_Validacao", "Indicador"),
            coluna("Pendencias_Validacao", "Problema"),
            coluna("Pendencias_Validacao", "Acao_Recomendada"),
            coluna("Pendencias_Validacao", "Status"),
        ]}},
        container=titulo("Pendências de validação", "4 registros na origem"),
    )
    p.rodape_tela("Base_Usina_PowerBI_Final_v4.xlsx · Fato_Medicoes, "
                  "Pendencias_Validacao, Auditoria_Dados")
    return p


# ------------------------------------------------------------------ page 6

def detalhes() -> Pagina:
    p = Pagina(DETALHES, "Detalhes")
    p.limpar()
    p.cabecalho_tela()
    p.filtro_data()
    p.filtro("Dim_Indicador", "Nome_Original", 360, w=240)
    p.filtro("Fato_Medicoes", "Fonte", 616, w=200)

    p.trilho([
        ("Valor original", "_Medidas", "Rotulo Valor Original"),
        ("Fator aplicado", "_Medidas", "Rotulo Fator Aplicado"),
        ("Regra", "_Medidas", "Regra de Transformacao do Registro"),
        ("Status anterior", "_Medidas", "Status Anterior do Registro"),
    ])

    # 96px: com 64px o valor era cortado na base do cartao
    cartoes_em_linha(p, [
        ("Registros no recorte", "_Medidas", "Rotulo Registros"),
        ("Com ajuste de escala", "_Medidas", "Rotulo Ajustes de Escala"),
        ("Status do indicador", "_Medidas", "Status do Indicador"),
        ("Primeira data", "_Medidas", "Primeira Data com Dados"),
        ("Última data", "_Medidas", "Ultima Data com Dados"),
    ], x0=340, y=220, largura_total=1076, h=96)

    p.add(
        "tableEx", 340, 332, 1076, 402,
        {"Values": {"projections": [
            coluna("Fato_Medicoes", "ID_Registro"),
            coluna("Fato_Medicoes", "Data"),
            coluna("Fato_Medicoes", "Fonte"),
            coluna("Fato_Medicoes", "Valor"),
            coluna("Fato_Medicoes", "Valor_Original"),
            coluna("Fato_Medicoes", "Ajuste_Aplicado"),
            coluna("Fato_Medicoes", "Status_Validacao"),
        ]}},
        sort_by=coluna("Fato_Medicoes", "Data"),
        container=titulo("Registros", "Data decrescente · 903 registros no recorte"),
    )
    p.rodape_tela("Base_Usina_PowerBI_Final_v4.xlsx · Fato_Medicoes, "
                  "Auditoria_Dados, Dim_Indicador")
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
    print(f"{total} visuais gerados em {len(montadas)} paginas")
    print("Pendente no Desktop: formatacao fina, grupo de faixas, faixa empilhada e botão Voltar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
