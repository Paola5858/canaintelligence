"""Testes de contrato entre o modelo e a planilha de origem.

Verificam os fatos em que o modelo e o relatorio se apoiam: contagens,
integridade das chaves, cobertura de calendario, escalas e status.
Se a planilha nao estiver presente, a suite e marcada como nao executada.

Uso: python tests/test_data_contract.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "Base_Usina_PowerBI_Final_v4.xlsx"

results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, "PASS" if ok else "FAIL", detail))


def skip_all(reason: str) -> None:
    results.append(("Suite de dados", "SKIP", reason))


def run() -> None:
    try:
        import pandas as pd
    except ImportError:
        skip_all("pandas nao instalado")
        return

    if not XLSX.exists():
        skip_all(f"planilha ausente em {XLSX.relative_to(ROOT)}")
        return

    fato = pd.read_excel(XLSX, sheet_name="Fato_Medicoes")
    dim = pd.read_excel(XLSX, sheet_name="Dim_Indicador")
    cal = pd.read_excel(XLSX, sheet_name="Dim_Calendario")
    aud = pd.read_excel(XLSX, sheet_name="Auditoria_Dados")
    res = pd.read_excel(XLSX, sheet_name="Resumo_Qualidade")
    pen = pd.read_excel(XLSX, sheet_name="Pendencias_Validacao")

    # 1. Contagens ---------------------------------------------------------
    check("Fato tem 19.532 registros", len(fato) == 19532, f"encontrado {len(fato)}")
    check("Resumo oficial confirma a contagem de entrada",
          int(res.loc[0, "Registros_Entrada"]) == len(fato))
    check("Resumo oficial confirma a contagem de saida",
          int(res.loc[0, "Registros_Saida"]) == len(fato),
          "se divergir, houve filtro silencioso na origem")
    check("Dimensao de indicador tem 23 linhas", len(dim) == 23, f"encontrado {len(dim)}")

    # 2. Chaves ------------------------------------------------------------
    check("ID_Registro e unico na fato", bool(fato["ID_Registro"].is_unique))
    check("Codigo e unico na dimensao", bool(dim["Codigo"].is_unique))
    check("Dim_Calendario tem uma linha por data", bool(cal["Data"].is_unique))
    check("Nenhum codigo da fato ausente na dimensao",
          set(fato["Indicador_Codigo"]) <= set(dim["Codigo"]),
          str(sorted(set(fato["Indicador_Codigo"]) - set(dim["Codigo"]))))
    check("Nenhum codigo da dimensao ausente na fato",
          set(dim["Codigo"]) <= set(fato["Indicador_Codigo"]),
          str(sorted(set(dim["Codigo"]) - set(fato["Indicador_Codigo"]))))

    # 3. Nulos e tipos -----------------------------------------------------
    chaves = ["ID_Registro", "Data", "Fonte", "Indicador_Codigo", "Valor", "Status_Validacao"]
    nulos = {c: int(fato[c].isna().sum()) for c in chaves if int(fato[c].isna().sum()) > 0}
    check("Colunas-chave da fato sem nulos", not nulos, str(nulos))
    check("Valor e numerico", pd.api.types.is_numeric_dtype(fato["Valor"]))
    check("Data e data", pd.api.types.is_datetime64_any_dtype(fato["Data"]))
    check("Data nao foi convertida em texto", fato["Data"].dtype != object)

    # 4. Calendario --------------------------------------------------------
    check("Calendario cobre o inicio da fato", cal["Data"].min() <= fato["Data"].min())
    check("Calendario cobre o fim da fato", cal["Data"].max() >= fato["Data"].max())
    check("Calendario e continuo (365 dias em 2026)", len(cal) == 365)
    janela = pd.date_range(cal["Data"].min(), cal["Data"].max(), freq="D")
    check("Calendario sem lacuna de data", len(set(janela) - set(cal["Data"])) == 0)
    ordem = cal.sort_values("Numero_Mes")["Nome_Mes"].drop_duplicates().tolist()
    check("Nome do mes ordena pelo numero do mes",
          ordem == ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
          str(ordem))
    por_numero = cal.groupby("Numero_Mes")["Nome_Mes"].nunique()
    check("Cada numero de mes aponta para um unico nome",
          bool((cal.groupby("Numero_Mes")["Nome_Mes"].nunique() == 1).all()))

    # 5. Escalas -----------------------------------------------------------
    pc = fato.loc[fato["Indicador_Codigo"] == "PC", "Valor"]
    ar = fato[fato["Indicador_Codigo"] == "AR"]["Valor"]
    ulab = fato[fato["Indicador_Codigo"] == "UMIDADE_LAB"]["Valor"]
    ucana = fato[fato["Indicador_Codigo"] == "UMIDADE_CANA"]["Valor"]
    check("PC esta em escala percentual direta", bool(10 < pc.min() and pc.max() < 20),
          f"faixa {pc.min()} a {pc.max()}")
    check("ArCana esta em escala percentual direta", bool(0 < ar.min() and ar.max() < 2),
          f"faixa {ar.min()} a {ar.max()}")
    check("Nenhum valor percentual foi multiplicado por 100 por engano",
          bool(pc.max() < 100 and ar.max() < 100))
    check("UMIDADE_LAB esta em fracao entre 0 e 1",
          bool(0 <= ulab.min() and ulab.max() <= 1), f"faixa {ulab.min()} a {ulab.max()}")
    check("UMIDADE_CANA esta em percentual entre 0 e 100",
          bool(70 <= ucana.min() and ucana.max() <= 90), f"faixa {ucana.min()} a {ucana.max()}")
    check("UMIDADE_LAB e UMIDADE_CANA nao compartilham escala",
          bool(ulab.max() < 1 and ucana.min() > 70))

    # 6. Pendencia TC ------------------------------------------------------
    tc = fato[fato["Indicador_Codigo"] == "TC"]
    dim_tc = dim[dim["Codigo"] == "TC"].iloc[0]
    check("TC existe na fato com 903 leituras", len(tc) == 903, f"encontrado {len(tc)}")
    check("TC tem unidade desconhecida em todas as linhas",
          set(tc["Unidade"].unique()) == {"Desconhecida"})
    check("TC esta pendente em todas as linhas", set(tc["Status_Validacao"].unique()) == {"Pendente"})
    check("TC nao tem unidade confirmada na dimensao",
          str(dim_tc["Unidade_Confirmada"]) == "Desconhecida")
    check("Agregacao de TC segue pendente na dimensao",
          "Pendente" in str(dim_tc["Tipo_Agregacao_Recomendada"]))

    # 7. Status ------------------------------------------------------------
    permitidos = {"Validado", "Normalizado", "Pendente"}
    check("Status de validacao usa apenas valores conhecidos",
          set(fato["Status_Validacao"].unique()) <= permitidos,
          str(set(fato["Status_Validacao"].unique()) - permitidos))
    contagem = fato["Status_Validacao"].value_counts()
    check("Soma dos status fecha o total da fato", int(contagem.sum()) == len(fato))
    check("Pendentes totais conferem com TC", int(contagem.get("Pendente", 0)) == len(tc))

    # 8. Duplicidades ------------------------------------------------------
    dup = fato[fato["Duplicidade_Exata"] != "Nao"]
    check("135 duplicidades foram preservadas", len(dup) == 135, f"encontrado {len(dup)}")
    grupo = fato.groupby(["Data", "Fonte", "Indicador_Codigo", "Valor", "Valor_Original"]).size()
    pares = dup.merge(
        grupo.rename("n").reset_index(),
        on=["Data", "Fonte", "Indicador_Codigo", "Valor", "Valor_Original"],
        how="left",
    )
    check("Toda linha marcada como copia exata tem par identico",
          bool((pares["n"] > 1).all()), f"{int((pares['n'] <= 1).sum())} linhas sem par")

    # 9. Auditoria ---------------------------------------------------------
    check("Toda linha da auditoria existe na fato",
          set(aud["ID_Registro"]) <= set(fato["ID_Registro"]))
    check("ID_Registro e unico na auditoria", bool(aud["ID_Registro"].is_unique))
    ajustes = fato[fato["Ajuste_Aplicado"] != "Nenhum"]
    check("Quantidade de ajustes de escala confere com a auditoria",
          len(ajustes) == len(aud), f"fato {len(ajustes)} x auditoria {len(aud)}")
    regra = aud["Regra_Transformacao"].str.contains("10.000", na=False)
    check("Auditoria registra as duas regras de escala", bool(regra.any() and (~regra).any()))

    # 10. Fontes -----------------------------------------------------------
    check("Existem 8 fontes distintas", fato["Fonte"].nunique() == 8,
          f"encontrado {fato['Fonte'].nunique()}")
    frentes = fato[fato["Grupo_Fonte"] == "Frente de colheita"]
    lab = fato[fato["Grupo_Fonte"] == "Laboratorio"]
    check("Frente de colheita cobre 11 indicadores", frentes["Indicador_Codigo"].nunique() == 11)
    check("Laboratorio cobre 12 indicadores", lab["Indicador_Codigo"].nunique() == 12)
    check("Frentes e Laboratorio nao medem o mesmo indicador",
          set(frentes["Indicador_Codigo"]).isdisjoint(set(lab["Indicador_Codigo"])))

    # 11. Pendencias registradas -------------------------------------------
    check("Existem 4 pendencias registradas", len(pen) == 4, f"encontrado {len(pen)}")
    check("Pendencia de TC segue aberta",
          pen.loc[pen["Indicador"] == "TC", "Status"].iloc[0] == "Aberta")

    # 12. Safra e ano ------------------------------------------------------
    check("Safra tem um unico valor, logo nao e filtro util",
          fato["Safra"].nunique() == 1, f"valores {list(fato['Safra'].unique())}")
    check("Ano tem um unico valor, logo nao e filtro util", fato["Ano"].nunique() == 1)


def main() -> int:
    run()
    width = 68
    print("=" * width)
    print("TESTES DE CONTRATO DE DADOS")
    print("=" * width)
    failures = 0
    for name, status, detail in results:
        if status == "FAIL":
            failures += 1
        print(f"[{status}] {name}")
        if detail and status in {"FAIL", "SKIP"}:
            print(f"        -> {detail}")
    total = len(results)
    passed = sum(1 for _, s, _ in results if s == "PASS")
    print("-" * width)
    print(f"{total} verificacoes | {passed} aprovadas | {failures} falhas")
    print("=" * width)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
