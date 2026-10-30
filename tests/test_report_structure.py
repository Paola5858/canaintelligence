"""Testes de estrutura do relatorio PBIR.

Confere a ligacao entre pbip, report, paginas e tema. Erro nessa camada
impede o projeto de abrir ou faz o Power BI descartar paginas em silencio.

Uso: python tests/test_report_structure.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "dashboard_cana.Report"
PAGES = REPORT / "definition" / "pages"
THEMES = REPORT / "StaticResources" / "SharedResources" / "BaseThemes"
MODEL = ROOT / "dashboard_cana.SemanticModel"

results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, "PASS" if ok else "FAIL", detail))


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# 1. Cadeia de abertura -----------------------------------------------------
pbip_path = ROOT / "dashboard_cana.pbip"
check("Arquivo .pbip existe", pbip_path.exists())
if pbip_path.exists():
    pbip = load(pbip_path)
    caminhos = [artefato.get("report", {}).get("path") for artefato in pbip.get("artifacts", [])]
    check("pbip aponta para a pasta do relatorio", "dashboard_cana.Report" in caminhos, str(caminhos))
    check("pbip declara schema", "$schema" in pbip)

pbir = load(REPORT / "definition.pbir")
dataset = pbir.get("datasetReference", {})
check("definition.pbir referencia o modelo semantico por caminho",
      dataset.get("byPath", {}).get("path") == "../dashboard_cana.SemanticModel",
      str(dataset))
check("A pasta do modelo semantico existe no caminho referenciado",
      (REPORT / ".." / "dashboard_cana.SemanticModel").resolve().exists())
check("definition.pbism existe", (MODEL / "definition.pbism").exists())

# 2. Paginas ---------------------------------------------------------------
meta = load(PAGES / "pages.json")
ordem = meta.get("pageOrder", [])
check("pages.json declara seis paginas", len(ordem) == 6, f"{len(ordem)} paginas")
check("Pagina ativa existe na ordem", meta.get("activePageName") in ordem, str(meta.get("activePageName")))

pastas = {p.name for p in PAGES.iterdir() if p.is_dir()}
check("Toda pagina da ordem tem pasta", set(ordem) <= pastas,
      f"faltando: {sorted(set(ordem) - pastas)}")
check("Toda pasta de pagina esta na ordem", pastas <= set(ordem),
      f"sobrando: {sorted(pastas - set(ordem))}")
check("Nenhuma pagina repetida na ordem", len(ordem) == len(set(ordem)))

nomes: list[str] = []
for page_id in ordem:
    arquivo = PAGES / page_id / "page.json"
    if not arquivo.exists():
        check(f"{page_id}: page.json existe", False)
        continue
    page = load(arquivo)
    check(f"{page_id}: name igual ao nome da pasta", page.get("name") == page_id, str(page.get("name")))
    check(f"{page_id}: largura e altura em 1440x810",
          page.get("width") == 1440 and page.get("height") == 810,
          f"{page.get('width')}x{page.get('height')}")
    check(f"{page_id}: declara schema", "$schema" in page)
    nomes.append(str(page.get("displayName", "")))

check("Nomes das paginas na ordem certa",
      nomes == ["Visão geral", "Evolução", "Fontes", "Indicadores", "Qualidade", "Detalhes"],
      str(nomes))

# 3. Tema ------------------------------------------------------------------
report = load(REPORT / "definition" / "report.json")
colecao = report.get("themeCollection", {})
custom = colecao.get("customTheme", {})
check("report.json declara tema personalizado", custom.get("name") == "CanaIntelligence", str(custom))
check("Tema personalizado e do tipo SharedResources", custom.get("type") == "SharedResources")
# Sem reportVersionAtImport o Desktop recusa o relatorio inteiro com
# "A propriedade necessária reportVersionAtImport não foi incluída".
check("Tema personalizado tem reportVersionAtImport",
      isinstance(custom.get("reportVersionAtImport"), dict)
      and {"visual", "report", "page"} <= set(custom.get("reportVersionAtImport", {})),
      str(custom.get("reportVersionAtImport")))

pacotes = report.get("resourcePackages", [])
itens = [item for pacote in pacotes for item in pacote.get("items", [])]
declarados = {item.get("name"): item for item in itens}
check("Tema base Fluent2 declarado", "Fluent2-CY26SU08" in declarados)
check("Tema Cana Intelligence declarado nos recursos", "CanaIntelligence" in declarados)

faltando = [nome for nome, item in declarados.items() if not (REPORT / "StaticResources" / "SharedResources" / item["path"]).exists()]
check("Todo recurso declarado existe em disco", not faltando, ", ".join(faltando))

tema = load(THEMES / "CanaIntelligence.json")
check("Tema tem nome", tema.get("name") == "Cana Intelligence", str(tema.get("name")))
check("Tema tem paleta de dados", len(tema.get("dataColors", [])) >= 8)
check("Paleta comeca no verde cana", tema.get("dataColors", [""])[0] == "#4E7966", str(tema.get("dataColors", [""])[:1]))
check("Tema contem o verde floresta da marca", "#173F35" in tema.get("dataColors", []))
check("Tema desliga sombra", tema["visualStyles"]["*"]["*"]["dropShadow"][0]["show"] is False)
check("Fundo da pagina em marfim",
      tema["visualStyles"]["page"]["*"]["background"][0]["color"]["solid"]["color"] == "#EEF1EA")
check("Tema define classes de texto", set(tema.get("textClasses", {})) >= {"callout", "title", "header", "label"})

# 4. Coerencia entre paginas e documentacao --------------------------------
spec = ROOT / "docs" / "VISUAL_SPECIFICATION.md"
if spec.exists():
    texto = spec.read_text(encoding="utf-8")
    ausentes = [nome for nome in nomes if nome and f"Página" in texto and nome not in texto]
    check("Toda pagina aparece na especificacao de visuais", not ausentes, ", ".join(ausentes))
else:
    check("Especificacao de visuais existe", False)

width = 68
print("=" * width)
print("TESTES DE ESTRUTURA DO RELATORIO")
print("=" * width)
falhas = 0
for nome, status, detalhe in results:
    if status == "FAIL":
        falhas += 1
    print(f"[{status}] {nome}")
    if detalhe and status == "FAIL":
        print(f"        -> {detalhe}")
print("-" * width)
print(f"{len(results)} verificacoes | {len(results) - falhas} aprovadas | {falhas} falhas")
print("=" * width)
sys.exit(1 if falhas else 0)
