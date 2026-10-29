"""Gera os visuais da pagina 2 (Evolucao) no definition do relatorio PBIR.

Mesmo contrato do gerador da pagina 1: as posicoes seguem a grade de
docs/DESIGN_SYSTEM.md e docs/VISUAL_SPECIFICATION.md, e o schema usado e
visualContainer/1.4.0, que o Desktop aceita.

O que este gerador NAO faz, e continua sendo trabalho de Desktop:
- formatacao fina (unidades de exibicao, rotulos de dado, eixos)
- o trilho do indicador, que e um bloco de cartoes e caixa de texto montado na mao
- o periodo anterior, que depende da segmentacao de datas estar ativa

Uso: python scripts/build_visuals_page2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pbir_lib import limpar_visuais

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "dashboard_cana.Report" / "definition" / "pages" / "a1c4e77b0d92f3aa5510"
SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
    "visualContainer/1.4.0/schema.json"
)

contador = 0
gerados: list[tuple[str, str, int, int, int, int]] = []


def lit(valor: str) -> dict:
    return {"expr": {"Literal": {"Value": valor}}}


def cor(hexadecimal: str) -> dict:
    return {"solid": {"color": lit("'" + hexadecimal + "'")}}


def texto(t: str) -> dict:
    return lit("'" + t.replace("'", "''") + "'")


def inteiro(n: int) -> dict:
    return lit(f"{n}D")


def medida(tabela: str, nome: str) -> dict:
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": nome}},
        "queryRef": f"{tabela}.{nome}",
        "nativeQueryRef": nome,
    }


def coluna(tabela: str, nome: str) -> dict:
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": nome}},
        "queryRef": f"{tabela}.{nome}",
        "nativeQueryRef": nome,
        "active": True,
    }


def novo_visual(tipo, x, y, w, h, query_state=None, objects=None, container=None):
    global contador
    contador += 1
    nome = "v" + str(contador).zfill(19)
    visual = {"visualType": tipo}
    if query_state is not None:
        visual["query"] = {"queryState": query_state}
    visual["drillFilterOtherVisuals"] = True
    if objects:
        visual["objects"] = objects
    if container:
        visual["visualContainerObjects"] = container
    dados = {
        "$schema": SCHEMA,
        "name": nome,
        "position": {"x": x, "y": y, "z": 1000 + contador, "width": w, "height": h, "tabOrder": contador},
        "visual": visual,
    }
    pasta = PAGINA / "visuals" / nome
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "visual.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    gerados.append((nome, tipo, x, y, w, h))


def titulo(titulo_texto, subtitulo_texto=None):
    container = {
        "title": [{"properties": {
            "show": lit("true"),
            "text": texto(titulo_texto),
            "fontColor": cor("#173F35"),
            "alignment": texto("left"),
        }}]
    }
    if subtitulo_texto:
        container["subTitle"] = [{"properties": {
            "show": lit("true"),
            "text": texto(subtitulo_texto),
            "fontColor": cor("#76817B"),
            "alignment": texto("left"),
        }}]
    return container


def sem_cromo():
    return {
        "background": [{"properties": {"show": lit("false")}}],
        "border": [{"properties": {"show": lit("false")}}],
        "dropShadow": [{"properties": {"show": lit("false")}}],
    }


def cabecalho(titulo_pagina: str):
    return {
        "general": [{"properties": {"paragraphs": [{
            "textRuns": [
                {"value": "CANA INTELLIGENCE", "textStyle": {
                    "fontSize": "20pt",
                    "fontFamily": "Segoe UI Semibold",
                    "color": "#173F35",
                    "fontWeight": "600",
                }},
                {"value": "     " + titulo_pagina, "textStyle": {
                    "fontSize": "12pt",
                    "fontFamily": "Segoe UI",
                    "color": "#25312D",
                }},
            ],
            "horizontalTextAlignment": "left",
        }]}}]
    }


def main() -> int:
    if not PAGINA.exists():
        print(f"pagina nao encontrada: {PAGINA}")
        return 1

    limpar_visuais(PAGINA)

    # 2.1 cabecalho
    novo_visual("textbox", 24, 24, 1392, 48, objects=cabecalho("Evolução"), container=sem_cromo())

    # filtros: periodo, fonte e indicador
    novo_visual("slicer", 24, 152, 320, 40,
                {"Values": {"projections": [coluna("Dim_Calendario", "Data")]}},
                container=sem_cromo())
    novo_visual("slicer", 360, 152, 200, 44,
                {"Values": {"projections": [coluna("Fato_Medicoes", "Fonte")]}},
                container=sem_cromo())
    novo_visual("slicer", 576, 152, 320, 44,
                {"Values": {"projections": [coluna("Dim_Indicador", "Nome_Original")]}},
                container=sem_cromo())

    # 2.3 serie diaria: linha sem marcador visivel, largura zero quando configurado no Desktop
    novo_visual(
        "lineChart", 340, 220, 1076, 286,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        objects={"labels": [{"properties": {"show": lit("false")}}]},
        container=titulo("Série diária", "Média aritmética não ponderada"),
    )

    # 2.4 media mensal
    novo_visual(
        "lineChart", 340, 522, 620, 212,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Nome_Mes")]},
            "Y": {"projections": [medida("_Medidas", "Media Aritmetica Nao Ponderada")]},
        },
        container=titulo("Média mensal", "Média das leituras do mês"),
    )

    # 2.5 comparacao de periodos: tres cartoes, porque quatro colunas de medida
    # em 440px geravam barra de rolagem horizontal e nenhuma leitura
    comparacao = [
        ("Média atual", "Media Aritmetica Nao Ponderada"),
        ("Média anterior", "Media do Periodo Anterior"),
        ("Variação %", "Variacao Percentual vs Periodo Anterior"),
    ]
    largura_cartao = (440 - 8 * (len(comparacao) - 1)) // len(comparacao)
    for indice, (rotulo, nome_medida) in enumerate(comparacao):
        novo_visual(
            "card", 976 + indice * (largura_cartao + 8), 522, largura_cartao, 212,
            {"Values": {"projections": [medida("_Medidas", nome_medida)]}},
            objects={
                "labels": [{"properties": {
                    "fontSize": inteiro(18),
                    "fontFamily": texto("Segoe UI Semibold"),
                    "color": cor("#173F35"),
                }}],
                "categoryLabels": [{"properties": {"show": lit("false")}}],
            },
            container=titulo(rotulo),
        )

    # trilho do indicador: quatro cartoes abertos na coluna de 300px
    trilho = [
        ("Leituras", "Quantidade de Leituras"),
        ("Frentes com dado", "Frentes com Dado do Indicador"),
        ("Status do indicador", "Status do Indicador"),
        ("Agregação", "Rotulo Agregacao Recomendada"),
    ]
    for indice, (rotulo, nome_medida) in enumerate(trilho):
        novo_visual(
            "card", 24, 220 + indice * 128, 300, 120,
            {"Values": {"projections": [medida("_Medidas", nome_medida)]}},
            objects={
                "labels": [{"properties": {
                    "fontSize": inteiro(22),
                    "fontFamily": texto("Segoe UI Semibold"),
                    "color": cor("#173F35"),
                }}],
                # sem o rotulo de categoria: ele repete o titulo e corta o valor
                "categoryLabels": [{"properties": {"show": lit("false")}}],
            },
            container=titulo(rotulo),
        )

    # rodape com a origem do dado
    novo_visual(
        "textbox", 24, 750, 1392, 36,
        objects={
            "general": [{"properties": {"paragraphs": [{
                "textRuns": [{
                    "value": ("Base_Usina_PowerBI_Final_v4.xlsx · Fato_Medicoes, "
                              "Dim_Indicador, Dim_Calendario"),
                    "textStyle": {
                        "fontSize": "9pt",
                        "fontFamily": "Segoe UI",
                        "color": "#76817B",
                    },
                }],
                "horizontalTextAlignment": "left",
            }]}}]
        },
        container=sem_cromo(),
    )

    print(f"{len(gerados)} visuais gerados em {PAGINA.name} (Evolução)")
    for nome, tipo, x, y, w, h in gerados:
        print(f"  {nome} {tipo:<12} {x:>4},{y:<4} {w}x{h}")
    print("\nPendente no Desktop: formatacao fina (unidade de exibicao, eixos, rotulos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
