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
    """Contêiner padrão para cards e gráficos analíticos com título e subtítulo contextuais.
    
    Fundo branco, raio de borda 12 e sombra suave são herdados do tema CanaIntelligence.json.
    """
    container = {
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


def rotulo_cartao(valor_px: int = 24, cor_valor: str = "#173F35") -> dict:
    return {
        "labels": [{"properties": {
            "fontSize": inteiro(valor_px),
            "fontFamily": texto("Aptos Display"),
            "color": cor(cor_valor),
        }}],
        "categoryLabels": [{"properties": {
            "show": lit("false"),
        }}],
    }


# ------------------------------------------------------------------ pagina

def modo_dropdown(rotulo: str) -> dict:
    """Dropdown com cabeçalho explícito, para a seleção não virar adivinhação."""
    return {
        "data": [{"properties": {"mode": texto("Dropdown")}}],
        "header": [{"properties": {
            "show": lit("true"),
            "text": texto(rotulo),
        }}],
    }


def padding_slicer() -> dict:
    # Qualquer VCO tira o padding herdado do tema. Sem isso o Power BI encosta
    # o cabeçalho no contorno e corta a seleção, especialmente no dropdown.
    return {"padding": [{"properties": {
        "top": inteiro(8),
        "bottom": inteiro(8),
        "left": inteiro(8),
        "right": inteiro(8),
    }}]}


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

    def barra_navegacao_app(
        self,
        indice_ativo: int | None = None,
        incluir_visoes: bool = False,
    ):
        """Cabeçalho e navegação real do relatório.

        A versão anterior desenhava cinco abas como texto dentro de uma caixa.
        Bonito, sim; clicável, não. Cada aba agora é um actionButton com
        PageNavigation explícito, inclusive na página atualmente aberta.
        """
        idx = indice_ativo if indice_ativo is not None else self.indice_pagina

        # 1. Faixa superior de marca. O contraste vem da composicao, nao de emoji.
        self.add(
            "textbox", 0, 0, 1440, 64,
            objects={"general": [{"properties": {"paragraphs": [{
                "textRuns": [{"value": "", "textStyle": {"fontSize": "1pt"}}]
            }]}}]},
            container={
                "background": [{"properties": {"show": lit("true"), "color": cor("#F5F7F2")}}],
                "border": [{"properties": {"show": lit("true"), "color": cor("#D8DDD5")}}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

        # 2. Brand Logo & Title Box (Left)
        self.add(
            "textbox", 24, 8, 470, 48,
            objects={"general": [{"properties": {"paragraphs": [
                {
                    "textRuns": [
                        {"value": "CANA INTELLIGENCE", "textStyle": {
                            "fontSize": "15pt",
                            "fontFamily": "Aptos Display",
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
                            "fontFamily": "Aptos",
                            "color": "#76817B",
                        }},
                    ],
                    "horizontalTextAlignment": "left",
                },
            ]}}]},
            container=sem_cromo(),
        )

        # 3. Navegação horizontal em botões reais, não em texto decorativo.
        paginas_info = [
            (1, "Visão Geral", "5a36b06c01771dee7876"),
            (2, "Evolução", "a1c4e77b0d92f3aa5510"),
            (3, "Fontes", "b2d5f88c1ea304bb6621"),
            (4, "Indicadores", "c3e6091d2fb415cc7732"),
            (5, "Qualidade", "d4f71a2e30c526dd8843"),
            (6, "Detalhes", "e50b2b3f41d637ee9954"),
        ]
        if incluir_visoes:
            paginas_info.extend([
                (7, "Diretoria", "f6172b40a8c94d3ea101"),
                (8, "Gerência", "a72b45c91d064e3b8f12"),
                (9, "Operação", "c83d56e0f1a74a629b23"),
            ])

        x0, y0, gap, h = 504, 10, 4, 44
        w = 96 if incluir_visoes else 146
        for num, nome, page_id in paginas_info:
            ativo = num == idx
            texto_cor = "#FFFFFF" if ativo else "#365247"
            fill_cor = "#173F35" if ativo else "#FFFFFF"
            fill_transparencia = 0 if ativo else 78
            self.add(
                "actionButton", x0 + (num - 1) * (w + gap), y0, w, h,
                objects={
                    "icon": [
                        {"properties": {"show": lit("false")}},
                        {
                            "properties": {
                                "shapeType": {"expr": {"Literal": {"Value": "'blank'"}}},
                                "placement": texto("left"),
                            },
                            "selector": {"id": "default"},
                        },
                    ],
                    "text": [
                        {"properties": {"show": lit("true")}},
                        {
                            "properties": {
                                "text": texto(nome),
                                "fontColor": cor(texto_cor),
                                "fontSize": inteiro(10),
                                "bold": lit("true" if ativo else "false"),
                                "horizontalAlignment": texto("center"),
                            },
                            "selector": {"id": "default"},
                        },
                    ],
                    "fill": [
                        {"properties": {"show": lit("true")}},
                        {
                            "properties": {
                                "fillColor": cor(fill_cor),
                                "transparency": inteiro(fill_transparencia),
                            },
                            "selector": {"id": "default"},
                        }, {
                        "properties": {
                            "fillColor": cor("#FFFFFF"),
                            "transparency": inteiro(70),
                        },
                        "selector": {"id": "hover"},
                    }, {
                        "properties": {
                            "fillColor": cor("#D8E7DB"),
                            "transparency": inteiro(0),
                        },
                        "selector": {"id": "selected"},
                    }],
                    "outline": [{"properties": {"show": lit("false")}}],
                    "shape": [
                        {"properties": {
                            "tileShape": texto("rectangleRounded"),
                            "roundEdge": inteiro(12),
                        }},
                        {"properties": {
                            "tileShape": texto("rectangleRounded"),
                        }, "selector": {"id": "default"}},
                    ],
                },
                container={
                    "visualLink": [{"properties": {
                        "show": lit("true"),
                        "type": texto("PageNavigation"),
                        "navigationSection": texto(page_id),
                    }}],
                    "background": [{"properties": {"show": lit("false")}}],
                    "border": [{"properties": {"show": lit("false")}}],
                    "visualHeader": [{"properties": {"show": lit("false")}}],
                },
            )

    def scope_chip(self, texto_escopo: str, x=946, y=72, w=470, h=80):
        """Card de contexto ativo / status de escopo."""
        partes = [parte.strip() for parte in texto_escopo.split("·", 1)]
        paragrafos = [{
            "textRuns": [{"value": partes[0], "textStyle": {
                "fontSize": "9.5pt",
                "fontFamily": "Segoe UI Semibold",
                "color": "#173F35",
                "fontWeight": "700",
            }}],
            "horizontalTextAlignment": "center",
        }]
        if len(partes) == 2:
            paragrafos.append({
                "textRuns": [{"value": partes[1], "textStyle": {
                    "fontSize": "10pt",
                    "fontFamily": "Segoe UI",
                    "color": "#365247",
                }}],
                "horizontalTextAlignment": "center",
            })
        self.add(
            "textbox", x, y, w, h,
            objects={"general": [{"properties": {"paragraphs": paragrafos}}]},
            container={
                "background": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#F2F5F0"),
                    "transparency": inteiro(0),
                }}],
                "border": [{"properties": {
                    "show": lit("true"),
                    "color": cor("#D8DDD5"),
                    "radius": inteiro(12),
                }}],
                "dropShadow": [{"properties": {"show": lit("false")}}],
            },
        )

    def limpar_filtros_button(self, x=1330, y=72, w=86, h=80):
        """Botao nativo para limpar todos os slicers da pagina atual."""
        self.add(
            "actionButton", x, y, w, h,
            objects={
                "icon": [{
                    "properties": {"shapeType": {"expr": {"Literal": {"Value": "'blank'"}}}},
                    "selector": {"id": "default"},
                }],
                "text": [
                    {"properties": {"show": lit("true")}},
                    {"properties": {
                        "text": texto("LIMPAR"),
                        "fontColor": cor("#173F35"),
                        "bold": lit("true"),
                        "fontSize": inteiro(9),
                    }, "selector": {"id": "default"}},
                ],
                "fill": [
                    {"properties": {"show": lit("true")}},
                    {"properties": {
                        "fillColor": cor("#FFFFFF"),
                        "transparency": inteiro(0),
                    }, "selector": {"id": "default"}},
                ],
                "outline": [{"properties": {
                    "lineColor": cor("#D8DDD5"),
                }, "selector": {"id": "default"}}],
            },
            container={
                "visualLink": [{"properties": {
                    "show": lit("true"),
                    "type": texto("ClearAllSlicers"),
                }}],
                "background": [{"properties": {"show": lit("false")}}],
                "border": [{"properties": {"show": lit("false")}}],
                "visualHeader": [{"properties": {"show": lit("false")}}],
            },
        )

    def rodape_tela(self, linha: str | None = None):
        linha = linha or (
            "CANA INTELLIGENCE  ·  Fonte: Base_Usina_PowerBI_Final_v4.xlsx  ·  "
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

    def filtro_data(self, x=24, y=72, w=300, h=80):
        self.add(
            "slicer", x, y, w, h,
            {"Values": {"projections": [coluna("Dim_Calendario", "Data")]}},
            objects=modo_dropdown("Período"),
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
                **padding_slicer(),
            },
        )

    def filtro(self, tabela, campo, x, w=220, y=72, h=80):
        rotulos = {
            "Fonte": "Fonte de coleta",
            "Nome_Original": "Indicador",
            "Grupo_Fonte": "Grupo de fonte",
            "Status_Validacao": "Status de validação",
        }
        self.add(
            "slicer", x, y, w, h,
            {"Values": {"projections": [coluna(tabela, campo)]}},
            objects=modo_dropdown(rotulos.get(campo, campo.replace("_", " "))),
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
                **padding_slicer(),
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
            fundo_header = (ow >= 1400 and oy == 0 and oh <= 70) or (w >= 1400 and y == 0 and h <= 70)
            decorativo = (w <= 48 and h <= 30) or (ow <= 48 and oh <= 30)
            separado = fundo_header or decorativo or x >= ox + ow or ox >= x + w or y >= oy + oh or oy >= y + h
            if not separado:
                problemas.append(f"{nome} ({tipo}) sobrepoe {onome} ({outro}): {x},{y} {w}x{h} vs {ox},{oy} {ow}x{oh}")
        areas.append((tipo, x, y, w, h, nome))
    return problemas
