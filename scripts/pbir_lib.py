"""Helpers compartilhados para gerar visuais PBIR por arquivo.

Suporta layout premium, paleta executiva Cana Intelligence, navegação por abas
em formato pill, cards KPI com título e subtítulo contextuais, e validação rigorosa de grade.

Schema: visualContainer/1.4.0 (compatível com Power BI Desktop)
Resolução padrão: 1440 x 810 px
"""

from __future__ import annotations

import json
from pathlib import Path

SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
    "visualContainer/1.4.0/schema.json"
)

RAIZ = Path(__file__).resolve().parent.parent
PAGINAS = RAIZ / "dashboard_cana.Report" / "definition" / "pages"


# ------------------------------------------------------------------ literais

def lit(valor: str) -> dict:
    return {"expr": {"Literal": {"Value": valor}}}


def cor(hexadecimal: str) -> dict:
    return {"solid": {"color": lit("'" + hexadecimal + "'")}}


def texto(t: str) -> dict:
    return lit("'" + str(t).replace("'", "''") + "'")


def inteiro(n: int) -> dict:
    return lit(f"{n}D")


def medida(tabela: str, nome: str) -> dict:
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": nome}},
        "queryRef": f"{tabela}.{nome}",
        "nativeQueryRef": nome,
    }


def coluna(tabela: str, nome: str) -> dict:
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": nome}},
        "queryRef": f"{tabela}.{nome}",
        "nativeQueryRef": nome,
        "active": True,
    }


# ------------------------------------------------------------------ estilos

def sem_cromo() -> dict:
    """Caixa de texto e segmentacao: sem fundo, sem borda, sem sombra."""
    return {
        "background": [{"properties": {"show": lit("false")}}],
        "border": [{"properties": {"show": lit("false")}}],
        "dropShadow": [{"properties": {"show": lit("false")}}],
    }


def painel_card(titulo_texto: str, subtitulo_texto: str | None = None) -> dict:
    """Contêiner padrão para cards e gráficos analíticos com borda e sombra suaves."""
    container = {
        "background": [{"properties": {
            "show": lit("true"),
            "color": cor("#FFFFFF"),
            "transparency": inteiro(0),
        }}],
        "border": [{"properties": {
            "show": lit("true"),
            "color": cor("#D8DDD5"),
            "radius": inteiro(12),
        }}],
        "dropShadow": [{"properties": {
            "show": lit("true"),
            "color": cor("#173F35"),
            "transparency": inteiro(94),
            "blur": inteiro(10),
            "angle": inteiro(135),
            "distance": inteiro(3),
        }}],
        "title": [{"properties": {
            "show": lit("true"),
            "text": texto(titulo_texto),
            "fontColor": cor("#173F35"),
            "alignment": texto("left"),
        }}],
    }
    if subtitulo_texto:
        container["subTitle"] = [{"properties": {
            "show": lit("true"),
            "text": texto(subtitulo_texto),
            "fontColor": cor("#76817B"),
            "alignment": texto("left"),
        }}]
    return container


def titulo(titulo_texto: str, subtitulo_texto: str | None = None) -> dict:
    """Alias para painel_card."""
    return painel_card(titulo_texto, subtitulo_texto)


def rotulo_cartao(valor_px: int = 26, cor_valor: str = "#173F35") -> dict:
    return {
        "labels": [{"properties": {
            "fontSize": inteiro(valor_px),
            "fontFamily": texto("Segoe UI Semibold"),
            "color": cor(cor_valor),
        }}],
        "categoryLabels": [{"properties": {
            "show": lit("false"),
        }}],
    }


# ------------------------------------------------------------------ pagina

MODO_DROPDOWN = {"data": [{"properties": {"mode": texto("Dropdown")}}]}


def limpar_visuais(pasta_pagina: Path) -> int:
    """Apaga os visuais gerados de uma pagina de forma segura."""
    import os
    import shutil
    import stat

    def tratar(func, caminho, _excecao):
        try:
            if os.path.isdir(caminho):
                os.chmod(caminho, stat.S_IWRITE)
            func(caminho)
        except OSError:
            pass

    pasta = pasta_pagina / "visuals"
    removidos = 0
    if pasta.exists():
        for filho in pasta.iterdir():
            if filho.is_dir():
                shutil.rmtree(filho, onerror=tratar)
                if not filho.exists():
                    removidos += 1
    return removidos


class Pagina:
    """Escreve visuais em definition/pages/<id>/visuals/<nome>/visual.json."""

    def __init__(self, page_id: str, nome_pagina: str, indice_pagina: int = 1):
        self.pasta = PAGINAS / page_id
        self.nome_pagina = nome_pagina
        self.indice_pagina = indice_pagina
        self.contador = 0
        self.gerados: list[tuple[str, str, int, int, int, int]] = []
        if not self.pasta.exists():
            raise FileNotFoundError(f"pagina nao encontrada: {self.pasta}")

    def add(self, tipo, x, y, w, h, query_state=None, objects=None, container=None):
        self.contador += 1
        nome = "v" + str(self.contador).zfill(19)
        visual = {"visualType": tipo}
        if query_state is not None:
            visual["query"] = {"queryState": query_state}
        visual["drillFilterOtherVisuals"] = True
        if objects:
            visual["objects"] = objects
        if container:
            visual["visualContainerObjects"] = container
        dados = {
            "$schema": SCHEMA,
            "name": nome,
            "position": {
                "x": int(x), "y": int(y), "z": 1000 + self.contador,
                "width": int(w), "height": int(h), "tabOrder": self.contador,
            },
            "visual": visual,
        }
        pasta = self.pasta / "visuals" / nome
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "visual.json").write_text(
            json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self.gerados.append((nome, tipo, int(x), int(y), int(w), int(h)))
        return nome

    def limpar(self) -> int:
        return limpar_visuais(self.pasta)

    # -------------------------------------------------------------- componentes premium

    def barra_navegacao_app(self, indice_ativo: int | None = None):
        """Header executivo moderno: marca à esquerda e abas de navegação no formato pill à direita."""
        idx = indice_ativo if indice_ativo is not None else self.indice_pagina

        # 1. Brand Logo & Title Box (Left)
        self.add(
            "textbox", 24, 16, 470, 48,
            objects={"general": [{"properties": {"paragraphs": [
                {
                    "textRuns": [
                        {"value": "🌿 CANA INTELLIGENCE", "textStyle": {
                            "fontSize": "15pt",
                            "fontFamily": "Segoe UI Semibold",
                            "color": "#173F35",
                            "fontWeight": "700",
                        }},
                    ],
                    "horizontalTextAlignment": "left",
                },
                {
                    "textRuns": [
                        {"value": "USINA SUCROENERGÉTICA · SAFRA 2026/2027 · PAINEL EXECUTIVO", "textStyle": {
                            "fontSize": "8pt",
                            "fontFamily": "Segoe UI",
                            "color": "#76817B",
                        }},
                    ],
                    "horizontalTextAlignment": "left",
                },
            ]}}]},
            container=sem_cromo(),
        )

        # 2. Pill Navigation Tabs (Right)
        paginas_info = [
            (1, "1. Visão Geral"),
            (2, "2. Evolução"),
            (3, "3. Fontes"),
            (4, "4. Indicadores"),
            (5, "5. Qualidade"),
            (6, "6. Detalhes"),
        ]

        text_runs = []
        for i, (num, nome) in enumerate(paginas_info):
            if num == idx:
                text_runs.append({
                    "value": f" [ {nome.upper()} ] ",
                    "textStyle": {
                        "fontSize": "9pt",
                        "fontFamily": "Segoe UI Semibold",
                        "color": "#173F35",
                        "fontWeight": "700",
                    },
                })
            else:
                text_runs.append({
                    "value": f"  {nome}  ",
                    "textStyle": {
                        "fontSize": "9pt",
                        "fontFamily": "Segoe UI",
                        "color": "#76817B",
                    },
                })
            if i < len(paginas_info) - 1:
                text_runs.append({
                    "value": "·",
                    "textStyle": {
                        "fontSize": "8pt",
                        "fontFamily": "Segoe UI",
                        "color": "#D8DDD5",
                    },
                })

        self.add(
            "textbox", 504, 16, 912, 48,
            objects={"general": [{"properties": {"paragraphs": [{
                "textRuns": text_runs,
                "horizontalTextAlignment": "right",
            }]}}]},
            container={
                "background": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#FFFFFF"),
                    "transparency": inteiro(0),
                }}],
                "border": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#D8DDD5"),
                    "radius": inteiro(8),
                }}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

    def scope_chip(self, texto_escopo: str, x=946, y=72, w=470, h=46):
        """Card de contexto ativo / status de escopo."""
        self.add(
            "textbox", x, y, w, h,
            objects={"general": [{"properties": {"paragraphs": [{
                "textRuns": [
                    {"value": texto_escopo, "textStyle": {
                        "fontSize": "8.5pt",
                        "fontFamily": "Segoe UI Semibold",
                        "color": "#4E7966",
                    }},
                ],
                "horizontalTextAlignment": "center",
            }]}}]},
            container={
                "background": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#F2F5F0"),
                    "transparency": inteiro(0),
                }}],
                "border": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#D8DDD5"),
                    "radius": inteiro(8),
                }}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

    def rodape_tela(self, linha: str | None = None):
        linha = linha or (
            "🌿 CANA INTELLIGENCE v2.0  ·  Fonte: Base_Usina_PowerBI_Final_v4.xlsx  ·  "
            "Fato_Medicoes (19.532 Linhas)  ·  Dim_Indicador (23 Indicadores)  ·  Dim_Calendario (365 Dias)  ·  Auditoria Ativa"
        )
        self.add(
            "textbox", 24, 756, 1392, 38,
            objects={"general": [{"properties": {"paragraphs": [{
                "textRuns": [
                    {"value": linha, "textStyle": {
                        "fontSize": "8.5pt",
                        "fontFamily": "Segoe UI",
                        "color": "#76817B",
                    }},
                ],
                "horizontalTextAlignment": "center",
            }]}}]},
            container={
                "background": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#FFFFFF"),
                    "transparency": inteiro(0),
                }}],
                "border": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#D8DDD5"),
                    "radius": inteiro(8),
                }}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

    def filtro_data(self, x=24, y=72, w=300, h=46):
        self.add(
            "slicer", x, y, w, h,
            {"Values": {"projections": [coluna("Dim_Calendario", "Data")]}},
            objects=MODO_DROPDOWN,
            container={
                "background": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#FFFFFF"),
                    "transparency": inteiro(0),
                }}],
                "border": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#D8DDD5"),
                    "radius": inteiro(8),
                }}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

    def filtro(self, tabela, campo, x, w=220, y=72, h=46):
        self.add(
            "slicer", x, y, w, h,
            {"Values": {"projections": [coluna(tabela, campo)]}},
            objects=MODO_DROPDOWN,
            container={
                "background": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#FFFFFF"),
                    "transparency": inteiro(0),
                }}],
                "border": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#D8DDD5"),
                    "radius": inteiro(8),
                }}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

    def cartao_kpi(self, x, y, w, h, titulo_card, subtitulo_card, tabela, nome_medida, valor_px=26, cor_valor="#173F35"):
        """Card KPI refinado com título em destaque, valor grande e subtítulo explicativo."""
        container = painel_card(titulo_card, subtitulo_card)
        self.add(
            "card", x, y, w, h,
            {"Values": {"projections": [medida(tabela, nome_medida)]}},
            objects=rotulo_cartao(valor_px, cor_valor),
            container=container,
        )

    def relatorio(self) -> str:
        linhas = [
            f"{len(self.gerados)} visuais em {self.pasta.name} ({self.nome_pagina})"
        ]
        for nome, tipo, x, y, w, h in self.gerados:
            linhas.append(f"  {nome} {tipo:<12} {x:>4},{y:<4} {w}x{h}")
        return "\n".join(linhas)


def conferir_dentro_da_pagina(pagina: Pagina, largura=1440, altura=810) -> list[str]:
    """Aponta visual que estoura a pagina ou se sobrepoe a outro."""
    problemas: list[str] = []
    areas = []
    for nome, tipo, x, y, w, h in pagina.gerados:
        if x < 0 or y < 0 or x + w > largura or y + h > altura:
            problemas.append(f"{nome} ({tipo}) sai da pagina: {x},{y} {w}x{h}")
        for outro, ox, oy, ow, oh, onome in areas:
            decorativo = (w <= 48 and h <= 30) or (ow <= 48 and oh <= 30)
            separado = decorativo or x >= ox + ow or ox >= x + w or y >= oy + oh or oy >= y + h
            if not separado:
                problemas.append(f"{nome} ({tipo}) sobrepoe {onome} ({outro}): {x},{y} {w}x{h} vs {ox},{oy} {ow}x{oh}")
        areas.append((tipo, x, y, w, h, nome))
    return problemas
