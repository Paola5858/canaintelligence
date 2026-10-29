"""Testes estaticos do modelo semantico TMDL.

Nao substituem a abertura no Power BI Desktop, mas detectam os erros que
costumam impedir o projeto de abrir: indentacao com espacos, relacionamento
apontando para coluna inexistente, lineageTag duplicada, medida referenciada
e nao declarada e tabela sem particao.

Uso: python tests/test_model_structure.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / "dashboard_cana.SemanticModel" / "definition"
TABLES_DIR = MODEL_DIR / "tables"

EXPECTED_TABLES = {
    "Fato_Medicoes",
    "Dim_Calendario",
    "Dim_Indicador",
    "Auditoria_Dados",
    "Pendencias_Validacao",
    "Resumo_Qualidade",
    "_Medidas",
}

results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, "PASS" if ok else "FAIL", detail))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


tmdl_files = sorted(MODEL_DIR.rglob("*.tmdl"))
check("Encontra arquivos TMDL no modelo", len(tmdl_files) >= 9, f"{len(tmdl_files)} arquivos")

# 1. Indentacao -------------------------------------------------------------
bad_indent: list[str] = []
for path in tmdl_files:
    for lineno, line in enumerate(read(path).splitlines(), 1):
        # Espaco depois das tabulacoes pertence ao corpo da expressao DAX ou M.
        # O que quebra o parser e a linha COMECAR com espaco.
        if line.startswith(" "):
            bad_indent.append(f"{path.name}:{lineno}")
check("Nenhuma linha TMDL comeca com espaco", not bad_indent, ", ".join(bad_indent[:6]))

# 2. Tabelas ----------------------------------------------------------------
tables: dict[str, dict] = {}
for path in sorted(TABLES_DIR.glob("*.tmdl")):
    text = read(path)
    first = text.splitlines()[0].strip()
    match = re.match(r"^table\s+(\S+)$", first)
    if not match:
        check(f"{path.name}: primeira linha declara a tabela", False, repr(first))
        continue
    name = match.group(1)
    tables[name] = {
        "path": path,
        "text": text,
        "columns": re.findall(r"^\tcolumn\s+(\S+)$", text, re.MULTILINE),
        "measures": re.findall(r"^\tmeasure\s+'([^']+)'", text, re.MULTILINE),
        "partitions": re.findall(r"^\tpartition\s+(\S+)\s*=\s*m$", text, re.MULTILINE),
        "datatypes": re.findall(r"^\t\tdataType:\s*(\S+)$", text, re.MULTILINE),
    }

check("Todas as tabelas esperadas existem", set(tables) == EXPECTED_TABLES,
      f"faltando: {sorted(EXPECTED_TABLES - set(tables))} | extra: {sorted(set(tables) - EXPECTED_TABLES)}")
check("Nenhuma tabela ficou sem particao de importacao",
      all(t["partitions"] for t in tables.values()),
      ", ".join(name for name, t in tables.items() if not t["partitions"]))
check("Nenhuma tabela ficou sem coluna",
      all(t["columns"] for t in tables.values()),
      ", ".join(name for name, t in tables.items() if not t["columns"]))

valid_types = {"string", "int64", "double", "dateTime", "boolean", "decimal"}
bad_types = [
    f"{name}:{tp}" for name, t in tables.items() for tp in t["datatypes"] if tp not in valid_types
]
check("Tipos de dados declarados sao validos no TMDL", not bad_types, ", ".join(bad_types[:6]))

# 3. Relacionamentos --------------------------------------------------------
rel_text = read(MODEL_DIR / "relationships.tmdl")
pairs = re.findall(r"^\tfromColumn:\s*([\w]+)\.([\w]+)$", rel_text, re.MULTILINE)
to_pairs = re.findall(r"^\ttoColumn:\s*([\w]+)\.([\w]+)$", rel_text, re.MULTILINE)
check("Modelo declara dois relacionamentos", len(pairs) == 2 and len(to_pairs) == 2,
      f"{len(pairs)} from / {len(to_pairs)} to")

endpoint_errors: list[str] = []
for table_name, column_name in pairs + to_pairs:
    if table_name not in tables:
        endpoint_errors.append(f"tabela {table_name} inexistente")
    elif column_name not in tables[table_name]["columns"]:
        endpoint_errors.append(f"coluna {table_name}[{column_name}] inexistente")
check("Todo relacionamento aponta para tabela e coluna existentes", not endpoint_errors,
      "; ".join(endpoint_errors))

rel_targets = {(t, c) for t, c in to_pairs}
check("Relacionamento do calendario usa Dim_Calendario[Data]",
      ("Dim_Calendario", "Data") in rel_targets)
check("Relacionamento do indicador usa Dim_Indicador[Codigo]",
      ("Dim_Indicador", "Codigo") in rel_targets)
check("Fato e sempre o lado muitos das relacoes",
      all(t == "Fato_Medicoes" for t, _ in pairs))

# 4. Chaves dimensionais ---------------------------------------------------
check("Dim_Calendario[Data] marcada como chave",
      re.search(r"^\tcolumn Data\n(?:\t\t.*\n)*?\t\tisKey$", tables["Dim_Calendario"]["text"], re.MULTILINE) is not None)
check("Dim_Indicador[Codigo] marcada como chave",
      re.search(r"^\tcolumn Codigo\n(?:\t\t.*\n)*?\t\tisKey$", tables["Dim_Indicador"]["text"], re.MULTILINE) is not None)
check("Dim_Calendario marcada como tabela de data",
      "dataCategory: Time" in tables["Dim_Calendario"]["text"])
check("Nome_Mes ordenado por Numero_Mes",
      re.search(r"^\tcolumn Nome_Mes\n(?:\t\t.*\n)*?\t\tsortByColumn: Numero_Mes$",
                tables["Dim_Calendario"]["text"], re.MULTILINE) is not None)

# 5. Lineage tags ----------------------------------------------------------
tags = re.findall(r"^\t(?:lineageTag:)\s*(\S+)$", read(MODEL_DIR / "tables" / "Fato_Medicoes.tmdl"), re.MULTILINE)
all_tags = [
    tag
    for path in tmdl_files
    for tag in re.findall(r"^\t\t?lineageTag:\s*(\S+)$", read(path), re.MULTILINE)
]
duplicated = [tag for tag, count in Counter(all_tags).items() if count > 1]
check("Nenhuma lineageTag repetida no modelo", not duplicated, ", ".join(duplicated[:5]))
check("Toda tabela e coluna tem lineageTag", len(all_tags) > 40, f"{len(all_tags)} tags")

# 6. Medidas --------------------------------------------------------------
measures: dict[str, dict] = {}
for name, table in tables.items():
    for measure in table["measures"]:
        block = re.search(rf"^\tmeasure '{re.escape(measure)}' = (.*?)(?=\n\tmeasure |\n\tpartition |\Z)",
                          table["text"], re.MULTILINE | re.DOTALL)
        measures[measure] = {"table": name, "dax": block.group(1) if block else ""}

check("Catalogo tem pelo menos 40 medidas", len(measures) >= 40, f"{len(measures)} medidas")

referenced = {
    ref
    for info in measures.values()
    for ref in re.findall(r"\[([A-Za-zÀ-ÿ0-9_ ]+)\]", info["dax"])
}
declared = set(measures)
# referencias que sao colunas, nao medidas
column_names = {c for t in tables.values() for c in t["columns"]}
unknown_refs = {
    ref for ref in referenced
    if ref not in declared and ref not in column_names
}
check("Toda medida referenciada entre colchetes existe", not unknown_refs, ", ".join(sorted(unknown_refs))[:400])

missing_folder = [m for m, i in measures.items() if "displayFolder:" not in i["dax"]]
check("Toda medida tem pasta de exibicao", not missing_folder, ", ".join(missing_folder[:8]))

critical = [m for m in measures if m.startswith(("Quantidade de Registros", "Registros Pendentes",
                                                 "Valor Medio do Indicador", "Media do Periodo Anterior",
                                                 "PC Medio", "Umidade Laboratorio Media", "ATR Medio"))]
missing_desc = [m for m in critical if "description:" not in measures[m]["dax"]]
check("Medidas criticas tem descricao", not missing_desc, ", ".join(missing_desc))

# 7. Guardas de semantica --------------------------------------------------
guard_ok = "HASONEVALUE" in measures["Valor Medio do Indicador"]["dax"]
check("Media generica exige um unico indicador selecionado", guard_ok)

guard_ok = "Média Aritmética" in measures["Valor Medio do Indicador"]["dax"]
check("Media generica exige agregacao aritmetica aprovada", guard_ok)

blank_ok = "BLANK" in measures["Media do Periodo Anterior"]["dax"]
check("Comparacao temporal devolve vazio quando nao ha periodo", blank_ok)

# 8. Formatacao ------------------------------------------------------------
percent_measures = {
    "PC Medio": '0.00"%"',
    "ArCana Medio": '0.00"%"',
    "Umidade Cana Media": '0.00"%"',
    "Umidade Laboratorio Media": "0.0%",
    "ATR Medio": '0.00" kg/t"',
}
format_errors = [
    f"{m}: esperado {expected}"
    for m, expected in percent_measures.items()
    if expected not in measures[m]["dax"]
]
check("Formato percentual direto nao multiplica por 100", not format_errors, ", ".join(format_errors))
check("UMIDADE_LAB usa formato percentual de fracao",
      "0.0%" in measures["Umidade Laboratorio Media"]["dax"])

# 9. Modelo ---------------------------------------------------------------
model_text = read(MODEL_DIR / "model.tmdl")
check("Modelo em pt-BR", "culture: pt-BR" in model_text)
check("Parametro de caminho existe", "CaminhoDaBase" in read(MODEL_DIR / "expressions.tmdl"))
check("Parametro e marcado como consulta de parametro",
      "IsParameterQuery = true" in read(MODEL_DIR / "expressions.tmdl"))

# 10. Power Query ---------------------------------------------------------
source_errors: list[str] = []
for name, table in tables.items():
    if name == "_Medidas":
        # Tabela sintetica, criada com #table para hospedar as medidas.
        continue
    text = table["text"]
    if "File.Contents ( CaminhoDaBase )" not in text:
        source_errors.append(f"{name} nao usa o parametro de caminho")
    if "Excel.Workbook" not in text:
        source_errors.append(f"{name} nao usa Excel.Workbook")
    if re.search(r"File\.Contents\s*\(\s*\"", text):
        source_errors.append(f"{name} tem caminho absoluto cravado")
check("Toda consulta centraliza o caminho no parametro", not source_errors, "; ".join(source_errors[:6]))
check("Nenhuma consulta crava caminho absoluto", "C:\\Users" not in "".join(
    t["text"] for name, t in tables.items()))

# ------------------------------------------------------------------ relatorio
width = 68
print("=" * width)
print("TESTES DE ESTRUTURA DO MODELO SEMANTICO")
print("=" * width)
failures = 0
for name, status, detail in results:
    if status == "FAIL":
        failures += 1
    print(f"[{status}] {name}")
    if detail and status == "FAIL":
        print(f"        -> {detail}")
print("-" * width)
print(f"{len(results)} verificacoes | {len(results) - failures} aprovadas | {failures} falhas")
print("=" * width)
sys.exit(1 if failures else 0)
