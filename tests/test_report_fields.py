"""Confere que todo campo citado pelos visuais existe no modelo TMDL.

A suite de grade garante que o visual nao se sobrepoe. Esta garante que ele
aponta para algo que existe. Sem isso, o defeito aparece so quando o Desktop
abre o relatorio e reclama de campo ausente, ou pior, renderiza um visual vazio
sem dizer por que.

O que confere:
- toda entidade citada em Measure ou Column existe como tabela no TMDL
- toda medida citada existe na tabela citada
- toda coluna citada existe na tabela citada
- o queryRef de cada projecao bate com tabela e nome do campo

Nao confere tipos, formato nem semantica de DAX. Isso e papel da suite de
estrutura do modelo e da execucao no Desktop.

Uso: python tests/test_report_fields.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TABELAS = ROOT / "dashboard_cana.SemanticModel" / "definition" / "tables"
PAGES = ROOT / "dashboard_cana.Report" / "definition" / "pages"

RE_TABELA = re.compile(r"^table\s+(.+?)\s*$")
RE_COLUNA = re.compile(r"^\s+column\s+(.+?)\s*$")
RE_MEDIDA = re.compile(r"^\s+measure\s+('?)(.+?)\1\s*=")

results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, "PASS" if ok else "FAIL", detail))


def sem_aspas(nome: str) -> str:
    nome = nome.strip()
    if len(nome) >= 2 and nome[0] == "'" and nome[-1] == "'":
        return nome[1:-1].replace("''", "'")
    return nome


# ---------------------------------------------------------------- modelo

modelo: dict[str, dict[str, set[str]]] = {}
tabela_atual: str | None = None

for arquivo in sorted(TABELAS.glob("*.tmdl")):
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        m_tabela = RE_TABELA.match(linha)
        if m_tabela:
            tabela_atual = sem_aspas(m_tabela.group(1))
            modelo.setdefault(tabela_atual, {"measures": set(), "columns": set()})
            continue
        if tabela_atual is None:
            continue
        m_coluna = RE_COLUNA.match(linha)
        if m_coluna:
            modelo[tabela_atual]["columns"].add(sem_aspas(m_coluna.group(1)))
            continue
        m_medida = RE_MEDIDA.match(linha)
        if m_medida:
            modelo[tabela_atual]["measures"].add(sem_aspas(m_medida.group(2)))

check("TMDL tem tabelas", len(modelo) > 0, f"{len(modelo)} tabelas")
total_medidas = sum(len(t["measures"]) for t in modelo.values())
total_colunas = sum(len(t["columns"]) for t in modelo.values())
check("TMDL tem medidas e colunas", total_medidas > 0 and total_colunas > 0,
      f"{total_medidas} medidas, {total_colunas} colunas")


# ---------------------------------------------------------------- visuais

def referencias(no) -> list[tuple[str, str, str]]:
    """Devolve (tipo, entidade, propriedade) para cada Measure/Column do JSON."""
    achados: list[tuple[str, str, str]] = []

    def percorrer(valor) -> None:
        if isinstance(valor, dict):
            for tipo in ("Measure", "Column"):
                bloco = valor.get(tipo)
                if isinstance(bloco, dict):
                    expressao = bloco.get("Expression", {})
                    entidade = expressao.get("SourceRef", {}).get("Entity")
                    propriedade = bloco.get("Property")
                    if entidade and propriedade:
                        achados.append((tipo, entidade, propriedade))
            for filho in valor.values():
                percorrer(filho)
        elif isinstance(valor, list):
            for filho in valor:
                percorrer(filho)

    percorrer(no)
    return achados


def projecoes(no) -> list[tuple[str, str, str]]:
    """Devolve (query_ref, entidade, propriedade) para checar consistencia."""
    achados: list[tuple[str, str, str]] = []

    def percorrer(valor) -> None:
        if isinstance(valor, dict):
            query_ref = valor.get("queryRef")
            campo = valor.get("field")
            if isinstance(query_ref, str) and isinstance(campo, dict):
                for tipo in ("Measure", "Column"):
                    bloco = campo.get(tipo)
                    if isinstance(bloco, dict):
                        entidade = bloco.get("Expression", {}).get("SourceRef", {}).get("Entity")
                        propriedade = bloco.get("Property")
                        if entidade and propriedade:
                            achados.append((query_ref, entidade, propriedade))
            for filho in valor.values():
                percorrer(filho)
        elif isinstance(valor, list):
            for filho in valor:
                percorrer(filho)

    percorrer(no)
    return achados


visuals = sorted(PAGES.glob("*/visuals/*/visual.json"))
check("Relatorio tem visuais para conferir", len(visuals) > 0, f"{len(visuals)} visuais")

usados: set[tuple[str, str, str]] = set()
for arquivo in visuals:
    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    pagina = arquivo.parent.parent.parent.name
    rotulo = f"{pagina}/{arquivo.parent.name}"

    for tipo, entidade, propriedade in referencias(dados):
        usados.add((tipo, entidade, propriedade))

        if entidade not in modelo:
            check(f"{rotulo}: tabela {entidade} existe", False,
                  f"{tipo} {entidade}[{propriedade}]")
            continue

        chave = "measures" if tipo == "Measure" else "columns"
        existe = propriedade in modelo[entidade][chave]
        alvo = "medida" if tipo == "Measure" else "coluna"
        check(f"{rotulo}: {alvo} {entidade}[{propriedade}] existe", existe)

    for query_ref, entidade, propriedade in projecoes(dados):
        esperado = f"{entidade}.{propriedade}"
        check(f"{rotulo}: queryRef de {propriedade} bate com o campo",
              query_ref == esperado, f"{query_ref} != {esperado}")

check("Visuais citam campos do modelo", len(usados) > 0, f"{len(usados)} referencias distintas")

# ---------------------------------------------------------------- relatorio

largura_saida = 68
print("=" * largura_saida)
print("TESTES DE CAMPOS DOS VISUAIS")
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
print(f"{len(visuals)} visuais | {len(usados)} referencias distintas a campos")
print("=" * largura_saida)
sys.exit(1 if falhas else 0)
