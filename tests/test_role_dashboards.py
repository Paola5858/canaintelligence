"""Valida campos, cores e grade das experiências hierárquicas nos dois PBIPs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ("dashboard_canaol1.Report", "dashboard_canaol2.Report")
ROLE_PAGE_IDS = (
    "f6172b40a8c94d3ea101",
    "d7a41c93e60b2f8154aa",
    "a72b45c91d064e3b8f12",
    "e8b52d04f71c3a9265bb",
    "c83d56e0f1a74a629b23",
    "f9c63e15a82d4b0376cc",
)

RE_TABLE = re.compile(r"^table\s+(.+?)\s*$")
RE_COLUMN = re.compile(r"^\s+column\s+(.+?)\s*$")
RE_MEASURE = re.compile(r"^\s+measure\s+('?)(.+?)\1\s*=")
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))


def parse_model(report: str) -> dict[str, dict[str, set[str]]]:
    tables: dict[str, dict[str, set[str]]] = {}
    current: str | None = None
    path = ROOT / report.replace(".Report", ".SemanticModel") / "definition" / "tables"
    for file in path.glob("*.tmdl"):
        for line in file.read_text(encoding="utf-8").splitlines():
            match = RE_TABLE.match(line)
            if match:
                current = match.group(1).strip("'")
                tables.setdefault(current, {"columns": set(), "measures": set()})
            elif current:
                match = RE_COLUMN.match(line)
                if match:
                    tables[current]["columns"].add(match.group(1).strip("'"))
                match = RE_MEASURE.match(line)
                if match:
                    tables[current]["measures"].add(match.group(2).strip("'"))
    return tables


def field_references(value):
    if isinstance(value, dict):
        for kind in ("Measure", "Column"):
            field = value.get(kind)
            if isinstance(field, dict):
                entity = field.get("Expression", {}).get("SourceRef", {}).get("Entity")
                prop = field.get("Property")
                if entity and prop:
                    yield kind, entity, prop
        for child in value.values():
            yield from field_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from field_references(child)


def query_refs(visual: dict) -> set[str]:
    return {
        f"{entity}.{prop}"
        for _, entity, prop in field_references(visual.get("visual", {}).get("query", {}))
    }


def validate_grid(page_name: str, width: int, height: int, visuals: list[dict]) -> None:
    areas: list[tuple[str, int, int, int, int]] = []
    seen_z: set[int] = set()
    seen_tab: set[int] = set()
    drawer_names = {f"v{number:019d}" for number in range(21, 35)}
    panel_name = f"v{24:019d}"
    for visual in visuals:
        name = visual["name"]
        pos = visual["position"]
        x, y, w, h = (pos[key] for key in ("x", "y", "width", "height"))
        check(f"{page_name}/{name}: dentro da página", x >= 0 and y >= 0 and x + w <= width and y + h <= height)
        check(f"{page_name}/{name}: dimensões legíveis", w >= 40 and h >= 24)
        check(f"{page_name}/{name}: z único", pos.get("z") not in seen_z)
        check(f"{page_name}/{name}: tabOrder único", pos.get("tabOrder") not in seen_tab)
        seen_z.add(pos.get("z"))
        seen_tab.add(pos.get("tabOrder"))
        for other, ox, oy, ow, oh in areas:
            if name in drawer_names or other in drawer_names:
                continue
            header = (ow >= 1400 and oy == 0 and oh <= 70) or (w >= 1400 and y == 0 and h <= 70)
            separated = header or x >= ox + ow or ox >= x + w or y >= oy + oh or oy >= y + h
            check(f"{page_name}/{name}: sem sobreposição com {other}", separated)
        areas.append((name, x, y, w, h))


for report in REPORTS:
    pages_root = ROOT / report / "definition" / "pages"
    model = parse_model(report)
    pages_meta = json.loads((pages_root / "pages.json").read_text(encoding="utf-8"))
    expected_order = list(ROLE_PAGE_IDS) + ["b7c2d91e4a6f4c3b8d2e"]
    check(f"{report}: ordem segue a hierarquia",
          pages_meta["pageOrder"] == expected_order)
    check(f"{report}: inicia na visão macro da Diretoria",
          pages_meta["activePageName"] == ROLE_PAGE_IDS[0])
    theme_path = ROOT / report / "StaticResources" / "SharedResources" / "BaseThemes" / "CanaIntelligence.json"
    theme = json.loads(theme_path.read_text(encoding="utf-8"))
    check(f"{report}: paleta semáforo", theme["dataColors"][:3] == ["#2E7D32", "#F2C94C", "#C62828"])
    check(f"{report}: estados semânticos", (theme["good"], theme["neutral"], theme["bad"]) == ("#2E7D32", "#F2C94C", "#C62828"))

    for page_id in ROLE_PAGE_IDS:
        page_dir = pages_root / page_id
        page = json.loads((page_dir / "page.json").read_text(encoding="utf-8"))
        visual_files = sorted((page_dir / "visuals").glob("*/visual.json"))
        visuals = [json.loads(path.read_text(encoding="utf-8")) for path in visual_files]
        check(f"{report}/{page_id}: três visuais analíticos", all(
            (page_dir / "visuals" / ("v" + str(number).zfill(19)) / "visual.json").exists()
            for number in (16, 17, 18)
        ))
        validate_grid(f"{report}/{page_id}", page["width"], page["height"], visuals)

        drawer_visuals = [visual for visual in visuals if visual["name"] in {
            f"v{number:019d}" for number in range(21, 35)
        }]
        check(f"{report}/{page_id}: drawer recolhido por padrão",
              len(drawer_visuals) == 14 and all(visual.get("isHidden") is True for visual in drawer_visuals))

        open_id = f"open_sidebar_{page_id}"
        close_id = f"close_sidebar_{page_id}"
        bookmarks_dir = ROOT / report / "definition" / "bookmarks"
        trigger_path = page_dir / "visuals" / "v0000000000000000003" / "visual.json"
        trigger = json.loads(trigger_path.read_text(encoding="utf-8"))
        trigger_link = trigger["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
        check(f"{report}/{page_id}: hambúrguer abre o drawer",
              trigger_link["type"]["expr"]["Literal"]["Value"] == "'Bookmark'"
              and trigger_link["bookmark"]["expr"]["Literal"]["Value"] == f"'{open_id}'"
              and trigger["position"]["x"] == 1280)
        panel_path = page_dir / "visuals" / f"v{24:019d}" / "visual.json"
        panel = json.loads(panel_path.read_text(encoding="utf-8"))
        check(f"{report}/{page_id}: menu é card suspenso à direita",
              panel["position"]["x"] == 1000 and panel["position"]["width"] == 416)
        for bookmark_id, mode in ((open_id, "elevation"), (close_id, "hidden")):
            bookmark_path = bookmarks_dir / f"{bookmark_id}.bookmark.json"
            exists = bookmark_path.exists()
            check(f"{report}/{page_id}/{bookmark_id}: bookmark existe", exists)
            if exists:
                bookmark = json.loads(bookmark_path.read_text(encoding="utf-8"))
                states = bookmark["explorationState"]["sections"][page_id]["visualContainers"]
                check(f"{report}/{page_id}/{bookmark_id}: controla todos os itens",
                      len(states) == 14 and all(
                          state["singleVisual"]["display"]["mode"] == mode
                          for state in states.values()
                      ))
        close_button_path = page_dir / "visuals" / f"v{34:019d}" / "visual.json"
        close_button = json.loads(close_button_path.read_text(encoding="utf-8"))
        close_link = close_button["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
        check(f"{report}/{page_id}: fechar e clicar fora recolhem o menu",
              all(
                  json.loads(
                      (page_dir / "visuals" / f"v{number:019d}" / "visual.json").read_text(
                          encoding="utf-8"
                      )
                  )["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
                  ["bookmark"]["expr"]["Literal"]["Value"] == f"'{close_id}'"
                  for number in (21, 22, 23, 34)
              ) and close_link["type"]["expr"]["Literal"]["Value"] == "'Bookmark'")

        nav_targets = []
        active_navigation_items = 0
        for number in (26, 27, 29, 30, 32, 33):
            nav_path = page_dir / "visuals" / f"v{number:019d}" / "visual.json"
            nav_visual = json.loads(nav_path.read_text(encoding="utf-8"))
            nav_link = nav_visual["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
            if nav_link["type"]["expr"]["Literal"]["Value"] == "'PageNavigation'":
                target = nav_link["navigationSection"]["expr"]["Literal"]["Value"].strip("'")
                nav_targets.append(target)
                fill = nav_visual["visual"]["objects"]["fill"][1]["properties"]["fillColor"]
                text_color = nav_visual["visual"]["objects"]["text"][1]["properties"]["fontColor"]
                active_navigation_items += int(
                    target == page_id
                    and fill["solid"]["color"]["expr"]["Literal"]["Value"] == "'#173F35'"
                    and text_color["solid"]["color"]["expr"]["Literal"]["Value"] == "'#FFFFFF'"
                )
        check(f"{report}/{page_id}: drawer liga as seis visões",
              nav_targets == list(ROLE_PAGE_IDS))
        check(f"{report}/{page_id}: destaca a página ativa", active_navigation_items == 1)

        section_names = {
            json.loads(
                (page_dir / "visuals" / f"v{number:019d}" / "visual.json").read_text(
                    encoding="utf-8"
                )
            )["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]
            ["textRuns"][0]["value"]
            for number in (25, 28, 31)
        }
        check(f"{report}/{page_id}: menu agrupa por público",
              section_names == {"DIRETORIA", "GESTÃO", "FUNCIONÁRIO"})

        for visual in visuals:
            for kind, entity, prop in field_references(visual):
                check(
                    f"{report}/{page_id}/{visual['name']}: {entity}.{prop} existe",
                    entity in model and prop in model[entity]["measures" if kind == "Measure" else "columns"],
                )

        expected_charts = {
            "f6172b40a8c94d3ea101": (
                ("Dim_Calendario.Data", "_Medidas.Mediana do Indicador"),
                ("Fato_Medicoes.Fonte", "_Medidas.Registros Validados",
                 "_Medidas.Registros Normalizados", "_Medidas.Registros Pendentes"),
            ),
            "a72b45c91d064e3b8f12": (
                ("Fato_Medicoes.Fonte", "_Medidas.Registros Validados",
                 "_Medidas.Registros Normalizados", "_Medidas.Registros Pendentes"),
                ("Dim_Calendario.Data", "_Medidas.Mediana do Indicador"),
            ),
            "c83d56e0f1a74a629b23": (
                ("Dim_Calendario.Data", "_Medidas.Mediana do Indicador"),
                ("Fato_Medicoes.Status_Validacao", "_Medidas.Quantidade de Registros"),
            ),
            "f9c63e15a82d4b0376cc": (
                ("Dim_Calendario.Data", "_Medidas.Mediana do Indicador"),
                ("Dim_Indicador.Nome_Original", "_Medidas.Quantidade de Leituras"),
            ),
        }
        if page_id in expected_charts:
            for number, expected in zip((16, 17), expected_charts[page_id]):
                path = page_dir / "visuals" / f"v{number:019d}" / "visual.json"
                chart = json.loads(path.read_text(encoding="utf-8"))
                check(f"{report}/{page_id}: gráfico {number} responde à métrica do público",
                      query_refs(chart) == set(expected))

    for page_id in ROLE_PAGE_IDS[-2:]:
        notice_path = pages_root / page_id / "visuals" / "v0000000000000000005" / "visual.json"
        notice = json.loads(notice_path.read_text(encoding="utf-8"))
        text = json.dumps(notice, ensure_ascii=False)
        check(f"{report}/{page_id}: limitações individuais explícitas",
              "não possui ID de funcionário nem RLS" in text)

failures = [(name, detail) for name, ok, detail in results if not ok]
for name, detail in failures:
    print(f"[FAIL] {name}" + (f" — {detail}" if detail else ""))
print(f"{len(results)} verificações | {len(results) - len(failures)} aprovadas | {len(failures)} falhas")
sys.exit(1 if failures else 0)
