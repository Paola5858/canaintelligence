"""Executa todas as suites de teste do projeto.

Uso: python tests/run_tests.py
Codigo de saida 1 quando qualquer suite falha.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUITES = [
    ("Contrato de dados", ROOT / "tests" / "test_data_contract.py"),
    ("Estrutura do modelo", ROOT / "tests" / "test_model_structure.py"),
    ("Estrutura do relatorio", ROOT / "tests" / "test_report_structure.py"),
    ("Grade dos visuais", ROOT / "tests" / "test_report_grid.py"),
    ("Campos dos visuais", ROOT / "tests" / "test_report_fields.py"),
    ("Dashboards hierárquicos", ROOT / "tests" / "test_role_dashboards.py"),
    ("Parser oficial do Power BI", ROOT / "tests" / "test_tmdl_parser.py"),
]


def main() -> int:
    falhas: list[str] = []
    for nome, caminho in SUITES:
        print(f"\n>>> {nome} ({caminho.name})")
        resultado = subprocess.run([sys.executable, str(caminho)], cwd=ROOT)
        if resultado.returncode != 0:
            falhas.append(nome)

    print("\n" + "=" * 68)
    if falhas:
        print(f"SUITES COM FALHA: {', '.join(falhas)}")
        return 1
    print(f"TODAS AS {len(SUITES)} SUITES APROVADAS")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
