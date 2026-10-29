"""Auditoria da planilha de origem.

Le a planilha e imprime o inventario que sustenta a documentacao:
abas, colunas, tipos, nulos, distintos, cobertura de datas, indicadores,
fontes, unidades, status, pendencias e escalas por indicador.

Nao altera a planilha. Escreve um JSON em scripts/output/ para comparacao
entre execucoes.

Uso: python scripts/data_audit.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "Base_Usina_PowerBI_Final_v4.xlsx"
OUTPUT_DIR = ROOT / "scripts" / "output"

# O console do Windows abre em cp1252 e transforma acentos em lixo.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass


def main() -> int:
    try:
        import pandas as pd
    except ImportError:
        print("pandas nao instalado. Rode: pip install pandas openpyxl")
        return 1

    if not XLSX.exists():
        print(f"Planilha nao encontrada em {XLSX.relative_to(ROOT)}")
        print("Copie o arquivo para data/ antes de rodar o inventario.")
        return 1

    abas = pd.read_excel(XLSX, sheet_name=None)
    inventario: dict = {"arquivo": XLSX.name, "abas": {}}

    for nome, df in abas.items():
        colunas = {}
        for coluna in df.columns:
            serie = df[coluna]
            info = {
                "tipo_detectado": str(serie.dtype),
                "nulos": int(serie.isna().sum()),
                "distintos": int(serie.nunique(dropna=True)),
            }
            if pd.api.types.is_datetime64_any_dtype(serie):
                info["min"] = str(serie.min().date())
                info["max"] = str(serie.max().date())
            elif pd.api.types.is_numeric_dtype(serie):
                info["min"] = float(serie.min())
                info["max"] = float(serie.max())
            colunas[str(coluna)] = info
        inventario["abas"][nome] = {"linhas": int(len(df)), "colunas": colunas}

    fato = abas["Fato_Medicoes"]
    dim = abas["Dim_Indicador"]
    cal = abas["Dim_Calendario"]

    janela = pd.date_range(fato["Data"].min(), fato["Data"].max(), freq="D")
    cobertura = {
        "primeira_data": str(fato["Data"].min().date()),
        "ultima_data": str(fato["Data"].max().date()),
        "dias_com_dado": int(fato["Data"].nunique()),
        "dias_no_intervalo": int(len(janela)),
        "dias_sem_dado": int(len(set(janela) - set(fato["Data"]))),
    }

    por_indicador = []
    for codigo, grupo in fato.groupby("Indicador_Codigo"):
        linha_dim = dim[dim["Codigo"] == codigo].iloc[0]
        valores = grupo["Valor"]
        por_indicador.append({
            "codigo": codigo,
            "unidade": str(linha_dim["Unidade_Confirmada"]),
            "agregacao_recomendada": str(linha_dim["Tipo_Agregacao_Recomendada"]),
            "status_dimensao": str(linha_dim["Status_Validacao"]),
            "leituras": int(len(grupo)),
            "dias": int(grupo["Data"].nunique()),
            "fontes": int(grupo["Fonte"].nunique()),
            "min": round(float(valores.min()), 4),
            "mediana": round(float(valores.median()), 4),
            "max": round(float(valores.max()), 4),
            "media": round(float(valores.mean()), 4),
            "amplitude": round(float(valores.max() - valores.min()), 4),
        })

    inventario["cobertura"] = cobertura
    inventario["indicadores"] = sorted(por_indicador, key=lambda x: x["codigo"])
    inventario["fontes"] = {
        str(chave): int(valor) for chave, valor in fato["Fonte"].value_counts().items()
    }
    inventario["status"] = {
        str(chave): int(valor) for chave, valor in fato["Status_Validacao"].value_counts().items()
    }
    inventario["ajustes"] = {
        str(chave): int(valor) for chave, valor in fato["Ajuste_Aplicado"].value_counts().items()
    }
    inventario["duplicidades"] = {
        str(chave): int(valor) for chave, valor in fato["Duplicidade_Exata"].value_counts().items()
    }
    inventario["safras"] = [str(valor) for valor in fato["Safra"].unique()]
    inventario["anos"] = sorted(int(valor) for valor in fato["Ano"].unique())

    # divergencias entre a dimensao e a fato
    unidades_fato = fato.groupby("Indicador_Codigo")["Unidade"].unique().to_dict()
    divergencias = []
    for codigo, unidades in unidades_fato.items():
        unidade_dim = str(dim[dim["Codigo"] == codigo].iloc[0]["Unidade_Confirmada"])
        if set(unidades) != {unidade_dim}:
            divergencias.append({"codigo": codigo, "fato": list(unidades), "dimensao": unidade_dim})
    inventario["divergencias_unidade"] = divergencias

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destino = OUTPUT_DIR / "data_inventory.json"
    destino.write_text(json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 74)
    print(f"INVENTARIO DE {XLSX.name}")
    print("=" * 74)
    for nome, info in inventario["abas"].items():
        print(f"\n[{nome}] {info['linhas']} linhas, {len(info['colunas'])} colunas")
        for coluna, meta in info["colunas"].items():
            faixa = ""
            if "min" in meta:
                faixa = f" | faixa {meta['min']} a {meta['max']}"
            print(f"  {coluna:<28} {meta['tipo_detectado']:<12} "
                  f"nulos={meta['nulos']:<5} distintos={meta['distintos']}{faixa}")

    print("\n--- cobertura de datas ---")
    for chave, valor in cobertura.items():
        print(f"  {chave}: {valor}")
    print(f"  safras: {inventario['safras']}")
    print(f"  anos: {inventario['anos']}")
    print(f"  status: {inventario['status']}")
    print(f"  ajustes: {inventario['ajustes']}")
    print(f"  duplicidades: {inventario['duplicidades']}")

    print("\n--- indicadores ---")
    print(f"  {'cod':<14}{'un.':<15}{'leituras':>9}{'dias':>7}{'min':>10}{'mediana':>10}{'max':>10}")
    for item in inventario["indicadores"]:
        print(f"  {item['codigo']:<14}{item['unidade']:<15}{item['leituras']:>9}"
              f"{item['dias']:>7}{item['min']:>10}{item['mediana']:>10}{item['max']:>10}")

    print(f"\nDivergencias de unidade entre fato e dimensao: {len(divergencias)}")
    print(f"JSON salvo em {destino.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
