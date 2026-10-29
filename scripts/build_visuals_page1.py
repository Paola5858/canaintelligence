"""Gera os visuais da pagina 1 (Visao geral) no definition do relatorio PBIR.

Por que um gerador e nao arquivos escritos a mao: as posicoes seguem a grade de
docs/DESIGN_SYSTEM.md e qualquer ajuste de layout precisa ser refeito nas seis
paginas. Com o gerador, a grade vive em um lugar so.

Uso: python scripts/build_visuals_page1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "dashboard_cana.Report" / "definition" / "pages" / "5a36b06c01771dee7876"
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
            "fontColor": cor("#25312D"),
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


def cabecalho():
    return {
        "general": [{"properties": {"paragraphs": [{
            "textRuns": [
                {"value": "CANA INTELLIGENCE", "textStyle": {
                    "fontSize": "20pt",
                    "fontFamily": "Segoe UI Semibold",
                    "color": "#173F35",
                    "fontWeight": "600",
                }},
                {"value": "     Visao geral", "textStyle": {
                    "fontSize": "12pt",
                    "fontFamily": "Segoe UI",
                    "color": "#25312D",
                }},
            ],
            "horizontalTextAlignment": "left",
        }]}}]
    }


def main() -> int:
    # 1. cabecalho
    novo_visual("textbox", 24, 24, 1392, 48, objects=cabecalho(), container=sem_cromo())

    # 2. filtros: data em faixa, fonte e indicador em lista
    novo_visual("slicer", 24, 152, 320, 40,
                {"Values": {"projections": [coluna("Dim_Calendario", "Data")]}},
                container=sem_cromo())
    novo_visual("slicer", 360, 152, 200, 120,
                {"Values": {"projections": [coluna("Fato_Medicoes", "Fonte")]}},
                container=sem_cromo())
    novo_visual("slicer", 576, 152, 320, 120,
                {"Values": {"projections": [coluna("Dim_Indicador", "Nome_Original")]}},
                container=sem_cromo())

    # 3. faixa de cobertura: cinco cartoes abertos, sem borda
    cartoes = [
        ("Dias com Dados", 152),
        ("Registros Validados", 408),
        ("Quantidade de Indicadores", 664),
        ("Quantidade de Fontes", 920),
        ("Ultima Data com Dados", 1176),
    ]
    for nome_medida, x in cartoes:
        novo_visual(
            "card", x, 290, 240, 96,
            {"Values": {"projections": [medida("_Medidas", nome_medida)]}},
            objects={
                "labels": [{"properties": {
                    "fontSize": inteiro(26),
                    "fontFamily": texto("Segoe UI Semibold"),
                    "color": cor("#173F35"),
                }}],
                "categoryLabels": [{"properties": {
                    "show": lit("true"),
                    "fontSize": inteiro(10),
                    "fontFamily": texto("Segoe UI"),
                    "color": cor("#76817B"),
                }}],
            },
            container=sem_cromo(),
        )

    # 4. serie temporal do indicador de laboratorio
    novo_visual(
        "lineChart", 24, 410, 896, 322,
        {
            "Category": {"projections": [coluna("Dim_Calendario", "Data")]},
            "Y": {"projections": [medida("_Medidas", "Acidez Total Media")]},
        },
        objects={"labels": [{"properties": {"show": lit("false")}}]},
        container=titulo("Acidez Total", "Media diaria em mg/L, 236 dias com leitura"),
    )

    # 5. cobertura por fonte
    novo_visual(
        "barChart", 936, 410, 480, 322,
        {
            "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
            "Y": {"projections": [medida("_Medidas", "Quantidade de Registros")]},
        },
        objects={"labels": [{"properties": {
            "show": lit("true"),
            "fontSize": inteiro(11),
            "fontFamily": texto("Segoe UI"),
            "color": cor("#25312D"),
        }}]},
        container=titulo("Cobertura por fonte", "Registros de todos os indicadores"),
    )

    print(f"{len(gerados)} visuais gerados em {PAGINA.name}")
    for nome, tipo, x, y, w, h in gerados:
        print(f"  {nome} {tipo:<12} {x:>4},{y:<4} {w}x{h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
