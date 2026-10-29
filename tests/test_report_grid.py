"""Testes de grade dos visuais do relatorio PBIR.

Existe porque posicao de visual e o tipo de defeito que nao quebra a abertura do
arquivo: o Desktop abre, a pagina renderiza, e o grafico fica em cima do outro.
Nenhuma das outras suites olha para isso.

O que confere, em cada uma das seis paginas:
- nome do arquivo igual ao nome da pasta (o Power BI usa o nome como chave)
- schema declarado no visual
- posicao dentro dos limites da pagina declarada em page.json
- visual com largura e altura maiores que o minimo legivel
- nenhum par de visuais se sobrepondo
- z e tabOrder unicos, para a ordem de empilhamento nao ser ambiguidade
- pagina nao vazia

Nao confere se o visual renderiza, nem se o campo existe no modelo. Isso e papel
da suite de estrutura do modelo e da abertura no Desktop.

Uso: python tests/test_report_grid.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "dashboard_cana.Report" / "definition" / "pages"

LARGURA_MINIMA = 40
ALTURA_MINIMA = 24

results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, "PASS" if ok else "FAIL", detail))


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def inteiro(valor) -> bool:
    return isinstance(valor, int) and not isinstance(valor, bool)


# ---------------------------------------------------------------- coleta

meta = load(PAGES / "pages.json")
ordem = meta.get("pageOrder", [])
check("pages.json declara paginas", len(ordem) > 0, f"{len(ordem)} paginas")

paginas: list[tuple[str, str, int, int, list[dict]]] = []

for page_id in ordem:
    pasta_pagina = PAGES / page_id
    arquivo_pagina = pasta_pagina / "page.json"
    if not arquivo_pagina.exists():
        check(f"{page_id}: page.json existe", False)
        continue

    page = load(arquivo_pagina)
    largura_pagina = page.get("width")
    altura_pagina = page.get("height")
    nome_pagina = str(page.get("displayName", page_id))

    if not (inteiro(largura_pagina) and inteiro(altura_pagina)):
        check(f"{nome_pagina}: pagina declara largura e altura", False)
        continue

    visuais: list[dict] = []
    pasta_visuais = pasta_pagina / "visuals"
    if pasta_visuais.exists():
        for pasta_visual in sorted(pasta_visuais.iterdir()):
            if not pasta_visual.is_dir():
                continue
            arquivo = pasta_visual / "visual.json"
            if not arquivo.exists():
                check(f"{nome_pagina}: {pasta_visual.name} tem visual.json", False)
                continue
            visuais.append({"pasta": pasta_visual.name, "dados": load(arquivo)})

    paginas.append((page_id, nome_pagina, largura_pagina, altura_pagina, visuais))

check("Toda pagina da ordem tem page.json", len(paginas) == len(ordem),
      f"{len(paginas)} de {len(ordem)}")

# ---------------------------------------------------------------- verificacao

total_visuais = 0

for page_id, nome_pagina, largura_pagina, altura_pagina, visuais in paginas:
    prefixo = f"{nome_pagina}"
    total_visuais += len(visuais)

    check(f"{prefixo}: tem pelo menos um visual", len(visuais) > 0, f"{len(visuais)}")

    nomes_vistos: set[str] = set()
    z_vistos: set[int] = set()
    tab_vistos: set[int] = set()
    areas: list[tuple[str, int, int, int, int]] = []

    for item in visuais:
        pasta = item["pasta"]
        dados = item["dados"]
        nome = dados.get("name")
        rotulo = f"{prefixo} / {pasta}"

        check(f"{rotulo}: nome igual ao da pasta", nome == pasta, str(nome))
        check(f"{rotulo}: declara schema", "$schema" in dados)
        check(f"{rotulo}: declara tipo de visual",
              bool(dados.get("visual", {}).get("visualType")),
              str(dados.get("visual", {}).get("visualType")))

        if pasta in nomes_vistos:
            check(f"{rotulo}: nome unico na pagina", False)
        nomes_vistos.add(pasta)

        pos = dados.get("position", {})
        x, y, w, h = pos.get("x"), pos.get("y"), pos.get("width"), pos.get("height")

        if not all(inteiro(v) for v in (x, y, w, h)):
            check(f"{rotulo}: posicao completa e inteira", False, str(pos))
            continue

        dentro = x >= 0 and y >= 0 and x + w <= largura_pagina and y + h <= altura_pagina
        check(f"{rotulo}: dentro da pagina",
              dentro, f"{x},{y} {w}x{h} em {largura_pagina}x{altura_pagina}")

        legivel = w >= LARGURA_MINIMA and h >= ALTURA_MINIMA
        check(f"{rotulo}: tamanho legivel", legivel, f"{w}x{h}")

        z = pos.get("z")
        if inteiro(z):
            if z in z_vistos:
                check(f"{rotulo}: z unico na pagina", False, str(z))
            z_vistos.add(z)

        tab = pos.get("tabOrder")
        if inteiro(tab):
            if tab in tab_vistos:
                check(f"{rotulo}: tabOrder unico na pagina", False, str(tab))
            tab_vistos.add(tab)

        for outro_nome, ox, oy, ow, oh in areas:
            separado = x >= ox + ow or ox >= x + w or y >= oy + oh or oy >= y + h
            if not separado:
                check(f"{rotulo}: nao sobrepoe {outro_nome}", False,
                      f"{x},{y} {w}x{h} contra {ox},{oy} {ow}x{oh}")
        areas.append((pasta, x, y, w, h))

check("Relatorio tem visuais gerados", total_visuais > 0, f"{total_visuais} visuais")

# ---------------------------------------------------------------- relatorio

largura_saida = 68
print("=" * largura_saida)
print("TESTES DE GRADE DOS VISUAIS")
print("=" * largura_saida)
falhas = 0
for nome, status, detalhe in results:
    if status == "FAIL":
        falhas += 1
        print(f"[{status}] {nome}")
        if detalhe:
            print(f"        -> {detalhe}")
print("-" * largura_saida)
print(f"{len(results)} verificacoes | {len(results) - falhas} aprovadas | {falhas} falhas")
print(f"{len(paginas)} paginas | {total_visuais} visuais")
print("=" * largura_saida)
sys.exit(1 if falhas else 0)
