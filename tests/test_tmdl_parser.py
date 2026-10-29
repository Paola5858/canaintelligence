"""Valida o modelo semantico com o parser TMDL oficial do Power BI Desktop.

Roda scripts/validate_tmdl.ps1, que carrega Microsoft.PowerBI.Tabular.dll e
deserializa a pasta definition. Se o Power BI nao estiver instalado na maquina,
a suite e marcada como nao executada em vez de falhar.

Uso: python tests/test_tmdl_parser.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_tmdl.ps1"


def main() -> int:
    largura = 68
    print("=" * largura)
    print("TESTE DO MODELO COM O PARSER TMDL DO POWER BI")
    print("=" * largura)

    if not SCRIPT.exists():
        print(f"[FAIL] script ausente: {SCRIPT.relative_to(ROOT)}")
        return 1

    comando = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRIPT),
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True, cwd=ROOT)
    saida = (resultado.stdout or "") + (resultado.stdout and "" or "") + (resultado.stderr or "")

    for linha in resultado.stdout.splitlines():
        print("  " + linha)

    if "SKIP:" in resultado.stdout:
        print("-" * largura)
        print("NAO EXECUTADO: o parser do Power BI nao esta disponivel nesta maquina")
        print("=" * largura)
        return 0

    if resultado.returncode == 0 and "PARSE OK" in resultado.stdout:
        print("-" * largura)
        print("APROVADO: o modelo deserializa no parser oficial")
        print("=" * largura)
        return 0

    print("-" * largura)
    print("FALHOU: o parser oficial recusou o modelo")
    if resultado.stderr.strip():
        print(resultado.stderr.strip()[:2000])
    print("=" * largura)
    return 1


if __name__ == "__main__":
    sys.exit(main())
