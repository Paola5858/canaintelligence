"""Atualiza os visuais hierárquicos dos PBIPs canaol1 e canaol2."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from pbir_lib import (  # noqa: E402
    Pagina,
    coluna,
    conferir_dentro_da_pagina,
    cor,
    lit,
    medida,
    painel_card,
)

REPORTS = ("dashboard_canaol1.Report", "dashboard_canaol2.Report")
PAGES = {
    "diretoria_estrategia": ("f6172b40a8c94d3ea101", "Diretoria · Estratégia", 2),
    "diretoria_governanca": ("d7a41c93e60b2f8154aa", "Diretoria · Governança", 3),
    "gerencia_acompanhamento": ("a72b45c91d064e3b8f12", "Gerência · Acompanhamento", 4),
    "gerencia_validacao": ("e8b52d04f71c3a9265bb", "Gerência · Validação", 5),
    "funcionario_consulta": ("c83d56e0f1a74a629b23", "Funcionário · Consulta", 6),
    "funcionario_rastreabilidade": ("f9c63e15a82d4b0376cc", "Funcionário · Rastreabilidade", 7),
}

SEMANTIC_COLORS = {
    "PEND": "#C62828",
    "NORMALIZ": "#F2C94C",
    "VALID": "#2E7D32",
}
DRAWER_BOOKMARK_SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
    "bookmark/2.1.0/schema.json"
)
BOOKMARKS_METADATA_SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
    "bookmarksMetadata/1.0.0/schema.json"
)
VISUAL_SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
    "visualContainer/1.4.0/schema.json"
)
DRAWER_LINKS = (
    ("DIRETORIA · ESTRATÉGIA", "f6172b40a8c94d3ea101"),
    ("DIRETORIA · GOVERNANÇA", "d7a41c93e60b2f8154aa"),
    ("GERÊNCIA · ACOMPANHAMENTO", "a72b45c91d064e3b8f12"),
    ("GERÊNCIA · VALIDAÇÃO", "e8b52d04f71c3a9265bb"),
    ("FUNCIONÁRIO · CONSULTA", "c83d56e0f1a74a629b23"),
    ("FUNCIONÁRIO · RASTREABILIDADE", "f9c63e15a82d4b0376cc"),
)


def visual_path(pagina: Pagina, numero: int) -> Path:
    return pagina.pasta / "visuals" / ("v" + str(numero).zfill(19)) / "visual.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def adicionar_grafico(
    pagina: Pagina,
    tipo: str,
    x: int,
    y: int,
    largura: int,
    altura: int,
    eixo: list[dict],
    valores: list[dict],
    titulo: str,
    subtitulo: str,
    objetos: dict | None = None,
) -> None:
    pagina.add(
        tipo,
        x,
        y,
        largura,
        altura,
        {"Category": {"projections": eixo}, "Y": {"projections": valores}},
        objects=objetos,
        container=painel_card(titulo, subtitulo),
    )


def adicionar_tabela(
    pagina: Pagina,
    x: int,
    y: int,
    largura: int,
    altura: int,
    campos: list[dict],
    titulo: str,
    subtitulo: str,
) -> None:
    pagina.add(
        "tableEx",
        x,
        y,
        largura,
        altura,
        {"Values": {"projections": campos}},
        container=painel_card(titulo, subtitulo),
    )


def desenhar_pagina(chave: str, relatorio: str) -> Pagina:
    page_id, nome, indice = PAGES[chave]
    pagina = Pagina(page_id, nome, indice, report_dir=relatorio)
    pagina.contador = 15

    if chave == "diretoria_estrategia":
        adicionar_grafico(
            pagina, "columnChart", 24, 286, 850, 260,
            [coluna("Dim_Calendario", "AnoMes")],
            [medida("_Medidas", "Quantidade de Registros")],
            "Volume mensal de medições",
            "Tendência macro da coleta; use os filtros para recortar indicador ou fonte",
        )
        adicionar_grafico(
            pagina, "barChart", 890, 286, 526, 260,
            [coluna("Fato_Medicoes", "Status_Validacao")],
            [medida("_Medidas", "Quantidade de Registros")],
            "Composição da base por situação",
            "Registros validados, normalizados e pendentes no período selecionado",
        )
        adicionar_tabela(
            pagina, 24, 566, 1392, 198,
            [
                coluna("Pendencias_Validacao", "Indicador"),
                coluna("Pendencias_Validacao", "Problema"),
                coluna("Pendencias_Validacao", "Acao_Recomendada"),
                coluna("Pendencias_Validacao", "Status"),
            ],
            "Ações técnicas registradas",
            "Plano cadastrado para correção; a tabela de pendências não é filtrada pela data",
        )
    elif chave == "diretoria_governanca":
        adicionar_grafico(
            pagina, "barChart", 24, 302, 650, 200,
            [coluna("Fato_Medicoes", "Fonte")],
            [
                medida("_Medidas", "Registros Validados"),
                medida("_Medidas", "Registros Normalizados"),
                medida("_Medidas", "Registros Pendentes"),
            ],
            "Situação da coleta por fonte",
            "Verde: validado · amarelo: normalizado · vermelho: pendente",
            objetos={"legend": [{"properties": {"show": lit("true")}}]},
        )
        adicionar_grafico(
            pagina, "barChart", 690, 302, 726, 200,
            [coluna("Dim_Indicador", "Status_Validacao")],
            [medida("_Medidas", "Quantidade de Indicadores")],
            "Indicadores por situação cadastral",
            "Acompanha a validação do cadastro, não o volume de medições",
        )
        adicionar_tabela(
            pagina, 24, 518, 1392, 224,
            [
                coluna("Dim_Indicador", "Codigo"),
                coluna("Dim_Indicador", "Nome_Original"),
                coluna("Dim_Indicador", "Unidade_Confirmada"),
                coluna("Dim_Indicador", "Tipo_Agregacao_Recomendada"),
                coluna("Dim_Indicador", "Status_Validacao"),
                coluna("Dim_Indicador", "Observacoes_Tecnicas"),
            ],
            "Regras e confiabilidade dos indicadores",
            "Unidade e agregação permanecem explícitas; não compare grandezas diferentes",
        )
    elif chave == "gerencia_acompanhamento":
        adicionar_grafico(
            pagina, "barChart", 24, 302, 416, 200,
            [coluna("Fato_Medicoes", "Fonte")],
            [medida("_Medidas", "Registros Pendentes")],
            "Pendências por fonte",
            "Origem dos registros pendentes; não identifica uma pessoa responsável",
        )
        adicionar_grafico(
            pagina, "lineChart", 456, 302, 960, 200,
            [coluna("Dim_Calendario", "Data")],
            [medida("_Medidas", "Registros Pendentes")],
            "Quando as pendências aparecem",
            "Contagem diária no recorte ativo; lacunas sem registro não são interpoladas",
        )
        adicionar_tabela(
            pagina, 24, 528, 1392, 214,
            [
                coluna("Fato_Medicoes", "Data"),
                coluna("Fato_Medicoes", "Fonte"),
                coluna("Fato_Medicoes", "ID_Registro"),
                coluna("Fato_Medicoes", "Indicador_Codigo"),
                coluna("Fato_Medicoes", "Valor"),
                coluna("Fato_Medicoes", "Valor_Original"),
                coluna("Fato_Medicoes", "Status_Validacao"),
            ],
            "Registros que explicam o desvio",
            "A origem está disponível por fonte e registro; não há identificação de funcionário",
        )
    elif chave == "gerencia_validacao":
        adicionar_grafico(
            pagina, "barChart", 24, 302, 440, 200,
            [coluna("Dim_Indicador", "Nome_Original")],
            [medida("_Medidas", "Registros Pendentes")],
            "Pendências por indicador",
            "Identifica o indicador que concentra registros aguardando regra técnica",
        )
        adicionar_grafico(
            pagina, "lineChart", 480, 302, 936, 200,
            [coluna("Dim_Calendario", "Data")],
            [medida("_Medidas", "Registros Pendentes")],
            "Evolução diária das pendências",
            "Use o período e a fonte para localizar onde a ocorrência começou",
        )
        adicionar_tabela(
            pagina, 24, 528, 1392, 214,
            [
                coluna("Pendencias_Validacao", "ID_Pendencia"),
                coluna("Pendencias_Validacao", "Indicador"),
                coluna("Pendencias_Validacao", "Problema"),
                coluna("Pendencias_Validacao", "Acao_Recomendada"),
                coluna("Pendencias_Validacao", "Status"),
            ],
            "Problema e ação recomendada",
            "Ações registradas na base técnica; não são aplicadas automaticamente",
        )
    elif chave == "funcionario_consulta":
        mover_rodape_consulta(pagina)
        adicionar_grafico(
            pagina, "columnChart", 24, 312, 684, 192,
            [coluna("Dim_Calendario", "AnoMes")],
            [medida("_Medidas", "Quantidade de Registros")],
            "Medições registradas por mês",
            "Consulta rápida da atividade no recorte selecionado",
        )
        adicionar_grafico(
            pagina, "barChart", 732, 312, 684, 192,
            [coluna("Fato_Medicoes", "Status_Validacao")],
            [medida("_Medidas", "Quantidade de Registros")],
            "Situação das medições",
            "Validado, normalizado ou pendente; selecione uma fonte para detalhar",
        )
        adicionar_tabela(
            pagina, 24, 516, 1392, 226,
            [
                coluna("Fato_Medicoes", "Data"),
                coluna("Fato_Medicoes", "Fonte"),
                coluna("Fato_Medicoes", "ID_Registro"),
                coluna("Fato_Medicoes", "Indicador_Codigo"),
                coluna("Fato_Medicoes", "Valor"),
                coluna("Fato_Medicoes", "Status_Validacao"),
            ],
            "Consulta detalhada por registro",
            "A base não contém ID de funcionário; a consulta não é individual nem restringe acesso",
        )
        atualizar_aviso_funcionario(pagina)
    else:
        adicionar_grafico(
            pagina, "columnChart", 24, 302, 440, 200,
            [coluna("Dim_Calendario", "AnoMes")],
            [medida("_Medidas", "Registros com Ajuste de Escala")],
            "Ajustes de escala ao longo do tempo",
            "Localize quando as normalizações se concentram no período selecionado",
        )
        adicionar_grafico(
            pagina, "barChart", 480, 302, 936, 200,
            [coluna("Fato_Medicoes", "Fonte")],
            [medida("_Medidas", "Registros com Ajuste de Escala")],
            "Onde os ajustes foram aplicados",
            "Distribuição por fonte; fonte indica origem do dado, não autoria individual",
        )
        atualizar_aviso_funcionario(pagina)

    if chave == "diretoria_estrategia":
        ajustar_filtro_status(pagina)
    colorir_cartoes(pagina)
    adicionar_drawer(pagina)
    falhas = conferir_dentro_da_pagina(pagina)
    if falhas:
        raise ValueError(f"{nome}: " + "; ".join(falhas))
    return pagina


def nome_visual(numero: int) -> str:
    return "v" + str(numero).zfill(19)


def texto_lit(valor: str) -> dict:
    return lit("'" + valor.replace("'", "''") + "'")


def visual_drawer_base(
    numero: int,
    visual_type: str,
    x: int,
    y: int,
    width: int,
    height: int,
    z: int,
) -> dict:
    return {
        "$schema": VISUAL_SCHEMA,
        "name": nome_visual(numero),
        "position": {
            "x": x,
            "y": y,
            "z": z,
            "width": width,
            "height": height,
            "tabOrder": 30 + numero - 21,
        },
        "isHidden": True,
        "visual": {"visualType": visual_type, "drillFilterOtherVisuals": True},
    }


def botao_drawer(
    pagina: Pagina,
    numero: int,
    label: str,
    x: int,
    y: int,
    width: int,
    height: int,
    z: int,
    destino_tipo: str,
    destino_id: str,
    fundo: str = "#EEF1EA",
    cor_texto: str = "#173F35",
    tamanho_fonte: str = "10D",
) -> dict:
    visual = visual_drawer_base(numero, "actionButton", x, y, width, height, z)
    visual["visual"]["objects"] = {
        "icon": [{"properties": {"show": lit("false")}}],
        "text": [
            {"properties": {"show": lit("true")}},
            {
                "properties": {
                    "text": texto_lit(label),
                    "fontColor": cor(cor_texto),
                    "fontSize": lit(tamanho_fonte),
                    "bold": lit("true"),
                    "horizontalAlignment": texto_lit("center"),
                },
                "selector": {"id": "default"},
            },
        ],
        "fill": [
            {"properties": {"show": lit("true")}},
            {
                "properties": {
                    "fillColor": cor(fundo),
                    "transparency": lit("0D"),
                },
                "selector": {"id": "default"},
            },
            {
                "properties": {
                    "fillColor": cor("#FFFFFF"),
                    "transparency": lit("10D"),
                },
                "selector": {"id": "hover"},
            },
            {
                "properties": {
                    "fillColor": cor("#D8E7DB"),
                    "transparency": lit("0D"),
                },
                "selector": {"id": "selected"},
            },
        ],
        "outline": [{"properties": {"show": lit("false")}}],
        "shape": [
            {
                "properties": {
                    "tileShape": texto_lit("rectangleRounded"),
                    "roundEdge": lit("12D"),
                }
            }
        ],
    }
    link_properties = {
        "show": lit("true"),
        "type": texto_lit(destino_tipo),
        "tooltip": texto_lit(label),
    }
    if destino_tipo == "Bookmark":
        link_properties["bookmark"] = texto_lit(destino_id)
    else:
        link_properties["navigationSection"] = texto_lit(destino_id)
    visual["visual"]["visualContainerObjects"] = {
        "visualLink": [{"properties": link_properties}],
        "background": [{"properties": {"show": lit("false")}}],
        "border": [{"properties": {"show": lit("false")}}],
        "visualHeader": [{"properties": {"show": lit("false")}}],
    }
    return visual


def visual_scrim(pagina: Pagina, numero: int, close_id: str) -> dict:
    visual = botao_drawer(
        pagina, numero, "", 360, 0, 1080, 810, 3021,
        "Bookmark", close_id, fundo="#25312D", cor_texto="#25312D",
    )
    visual["visual"]["objects"]["text"][0]["properties"]["show"] = lit("false")
    visual["visual"]["objects"]["fill"][1]["properties"]["transparency"] = lit("58D")
    visual["visual"]["objects"]["fill"][1]["properties"]["fillColor"] = cor("#25312D")
    visual["visual"]["objects"]["fill"][1]["selector"] = {"id": "default"}
    visual["visual"]["objects"]["shape"][0]["properties"]["tileShape"] = texto_lit("rectangle")
    visual["visual"]["objects"]["shape"][0]["properties"].pop("roundEdge", None)
    return visual


def visual_painel(numero: int) -> dict:
    visual = visual_drawer_base(numero, "textbox", 0, 0, 360, 810, 3022)
    visual["visual"]["objects"] = {
        "general": [{"properties": {"paragraphs": [
            {
                "textRuns": [{"value": "CANA INTELLIGENCE", "textStyle": {
                    "fontSize": "14pt",
                    "fontFamily": "Aptos Display",
                    "fontWeight": "700",
                    "color": "#173F35",
                }}],
                "horizontalTextAlignment": "left",
            },
            {
                "textRuns": [{"value": "NAVEGAÇÃO POR NÍVEL", "textStyle": {
                    "fontSize": "9pt",
                    "fontFamily": "Aptos",
                    "fontWeight": "700",
                    "color": "#76817B",
                }}],
                "horizontalTextAlignment": "left",
            },
        ]}}],
    }
    visual["visual"]["visualContainerObjects"] = {
        "background": [{"properties": {"show": lit("true"), "color": cor("#FFFFFF")}}],
        "border": [{"properties": {"show": lit("false")}}],
        "dropShadow": [{"properties": {"show": lit("true")}}],
        "padding": [{"properties": {
            "top": lit("24D"),
            "bottom": lit("24D"),
            "left": lit("24D"),
            "right": lit("24D"),
        }}],
        "visualHeader": [{"properties": {"show": lit("false")}}],
    }
    return visual


def adicionar_drawer(pagina: Pagina) -> None:
    page_id = pagina.pasta.name
    open_id = f"open_sidebar_{page_id}"
    close_id = f"close_sidebar_{page_id}"
    ids = [nome_visual(numero) for numero in range(21, 30)]

    trigger_path = visual_path(pagina, 3)
    trigger = load_json(trigger_path)
    link = trigger["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
    link["type"] = texto_lit("Bookmark")
    link["bookmark"] = texto_lit(open_id)
    link.pop("navigationSection", None)
    save_json(trigger_path, trigger)

    visuals = [
        visual_scrim(pagina, 21, close_id),
        visual_painel(22),
    ]
    for offset, (label, target_page) in enumerate(DRAWER_LINKS):
        selecionado = target_page == page_id
        visuals.append(
            botao_drawer(
                pagina, 23 + offset, label, 24, 126 + offset * 58, 312, 46,
                3023 + offset, "PageNavigation", target_page,
                fundo="#173F35" if selecionado else "#EEF1EA",
                cor_texto="#FFFFFF" if selecionado else "#173F35",
            )
        )
    visuals.append(
        botao_drawer(
            pagina, 29, "FECHAR", 284, 18, 52, 40, 3030,
            "Bookmark", close_id, fundo="#EEF1EA", tamanho_fonte="8D",
        )
    )

    for visual in visuals:
        save_json(visual_path(pagina, int(visual["name"][-19:])), visual)

    bookmarks_folder = pagina.pasta.parent.parent / "bookmarks"
    bookmarks_folder.mkdir(parents=True, exist_ok=True)
    bookmark_states = (
        (open_id, "Abrir menu lateral", "elevation"),
        (close_id, "Fechar menu lateral", "hidden"),
    )
    metadata_items = []
    for bookmark_id, display_name, mode in bookmark_states:
        section_visuals = {}
        for visual in visuals:
            section_visuals[visual["name"]] = {
                "singleVisual": {
                    "visualType": visual["visual"]["visualType"],
                    "objects": {},
                    "display": {"mode": mode},
                }
            }
        bookmark = {
            "$schema": DRAWER_BOOKMARK_SCHEMA,
            "displayName": display_name,
            "name": bookmark_id,
            "options": {
                "applyOnlyToTargetVisuals": True,
                "targetVisualNames": ids,
                "suppressData": True,
            },
            "explorationState": {
                "version": "1.3",
                "activeSection": page_id,
                "sections": {
                    page_id: {"visualContainers": section_visuals},
                },
            },
        }
        save_json(bookmarks_folder / f"{bookmark_id}.bookmark.json", bookmark)
        metadata_items.append({"name": bookmark_id})

    metadata_path = bookmarks_folder / "bookmarks.json"
    existing_items = []
    if metadata_path.exists():
        existing = load_json(metadata_path)
        existing_items = [
            item for item in existing.get("items", [])
            if item.get("name") not in {open_id, close_id}
        ]
    metadata = {
        "$schema": BOOKMARKS_METADATA_SCHEMA,
        "items": existing_items + metadata_items,
    }
    save_json(metadata_path, metadata)


def ajustar_filtro_status(pagina: Pagina) -> None:
    caminho = visual_path(pagina, 9)
    dados = load_json(caminho)
    dados["position"]["width"] = 150
    save_json(caminho, dados)


def mover_rodape_consulta(pagina: Pagina) -> None:
    origem = visual_path(pagina, 18)
    destino = visual_path(pagina, 19)
    if not origem.exists():
        return
    dados = load_json(origem)
    if dados.get("visual", {}).get("visualType") != "textbox" or dados.get("position", {}).get("y") < 750:
        return
    dados["name"] = destino.parent.name
    dados["position"]["z"] = 1019
    dados["position"]["tabOrder"] = 19
    destino.parent.mkdir(parents=True, exist_ok=True)
    save_json(destino, dados)
    shutil.rmtree(origem.parent)


def atualizar_aviso_funcionario(pagina: Pagina) -> None:
    dados = load_json(visual_path(pagina, 5))
    runs = dados["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"]
    runs[1]["value"] = (
        "  · Consulta operacional por registro; esta base não possui ID de funcionário nem RLS"
    )
    save_json(visual_path(pagina, 5), dados)


def colorir_cartoes(pagina: Pagina) -> None:
    for numero in range(12, 16):
        caminho = visual_path(pagina, numero)
        if not caminho.exists():
            continue
        dados = load_json(caminho)
        titulo = dados.get("visualContainerObjects", {}).get("title", [{}])[0]
        texto_titulo = titulo.get("properties", {}).get("text", {}).get("expr", {}).get(
            "Literal", {}
        ).get("Value", "").upper()
        cor_estado = next(
            (valor for termo, valor in SEMANTIC_COLORS.items() if termo in texto_titulo),
            None,
        )
        if cor_estado:
            labels = dados["visual"].setdefault("objects", {}).setdefault("labels", [{"properties": {}}])
            labels[0].setdefault("properties", {})["color"] = cor(cor_estado)
            save_json(caminho, dados)


def atualizar_tema(relatorio: str) -> None:
    caminho = (
        Path(__file__).resolve().parent.parent
        / relatorio
        / "StaticResources"
        / "SharedResources"
        / "BaseThemes"
        / "CanaIntelligence.json"
    )
    tema = load_json(caminho)
    tema["dataColors"] = [
        "#2E7D32",
        "#F2C94C",
        "#C62828",
        "#173F35",
        "#4E7966",
        "#A8B9A0",
        "#76817B",
        "#25312D",
    ]
    tema["good"] = "#2E7D32"
    tema["neutral"] = "#F2C94C"
    tema["bad"] = "#C62828"
    tema["tableAccent"] = "#2E7D32"
    save_json(caminho, tema)


def organizar_relatorio(relatorio: str) -> None:
    pages_path = (
        Path(__file__).resolve().parent.parent
        / relatorio
        / "definition"
        / "pages"
        / "pages.json"
    )
    pages = load_json(pages_path)
    pages["pageOrder"] = [spec[0] for spec in PAGES.values()] + ["b7c2d91e4a6f4c3b8d2e"]
    pages["activePageName"] = PAGES["diretoria_estrategia"][0]
    save_json(pages_path, pages)


def main() -> int:
    total = 0
    for relatorio in REPORTS:
        atualizar_tema(relatorio)
        paginas = [desenhar_pagina(chave, relatorio) for chave in PAGES]
        organizar_relatorio(relatorio)
        for pagina in paginas:
            print(f"{relatorio}: {pagina.nome_pagina} — {len(pagina.gerados)} visuais analíticos")
        total += len(paginas)
    print(f"[OK] {total} páginas hierárquicas atualizadas em {len(REPORTS)} PBIPs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
