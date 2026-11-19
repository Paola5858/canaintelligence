"""Gera a página de decisão do gestor, preservando as páginas de investigação."""
import sys
from pbir_lib import Pagina, coluna, conferir_dentro_da_pagina, cor, inteiro, lit, medida, painel_card

PAGINA = "5a36b06c01771dee7876"
STATUS = {
    "Registros Validados": "#32835D",
    "Registros Normalizados": "#D6A719",
    "Registros Pendentes": "#B54040",
}


def visao_geral() -> Pagina:
    p = Pagina(PAGINA, "Visão geral")
    p.limpar()
    p.barra_navegacao_app(indice_ativo=1)
    p.filtro_data(x=24, w=272)
    p.filtro("Fato_Medicoes", "Fonte", x=312, w=360)
    p.filtro("Dim_Indicador", "Nome_Original", x=688, w=566)
    p.limpar_filtros_button(x=1270, w=146)

    p.cartao_kpi(24, 168, 1392, 82, "Próxima ação", None, "_Medidas", "Orientacao de Validacao", valor_px=17)
    p.add("columnChart", 24, 266, 832, 478, {
        "Category": {"projections": [coluna("Dim_Calendario", "AnoMes")]},
        "Y": {"projections": [medida("_Medidas", nome) for nome in STATUS]},
    }, objects={
        "dataPoint": [{"selector": {"metadata": "_Medidas." + nome},
                       "properties": {"fill": cor(codigo)}} for nome, codigo in STATUS.items()],
        "legend": [{"properties": {"show": lit("true")}}],
    }, container=painel_card("Situação das medições por mês", "Número de registros por situação de validação"))
    p.add("barChart", 872, 266, 544, 478, {
        "Category": {"projections": [coluna("Fato_Medicoes", "Fonte")]},
        "Y": {"projections": [medida("_Medidas", "Registros Pendentes")]},
    }, objects={
        "dataPoint": [{"properties": {"defaultColor": cor(STATUS["Registros Pendentes"])}}],
        "labels": [{"properties": {"show": lit("true"), "labelDisplayUnits": inteiro(1)}}],
    }, container=painel_card("Onde estão as pendências?", "Registros que aguardam confirmação técnica, por fonte"))
    p.rodape_tela("O semáforo classifica os dados, não o desempenho da usina. Para conferir uma medição, abra Detalhes e selecione a fonte e o período.")
    return p


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pagina = visao_geral()
    problemas = conferir_dentro_da_pagina(pagina)
    print("\n".join(problemas) if problemas else pagina.relatorio())
    sys.exit(bool(problemas))
