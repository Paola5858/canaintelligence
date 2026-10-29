"""Helpers compartilhados para gerar visuais PBIR por arquivo.

Usado pelos geradores das paginas 3 a 6. As paginas 1 e 2 foram escritas antes
deste modulo existir e continuam com os proprios helpers; o formato de saida e o
mesmo, entao as tres abordagens convivem.

Decisoes que valem para todos os geradores:
- schema visualContainer/1.4.0, o unico que o Desktop aceitou no piloto da pagina 1
- posicao sempre em px absolutos na grade de 1440x810
- nada de sombra; o tema cuida de fundo, borda e tipografia
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


def titulo(titulo_texto: str, subtitulo_texto: str | None = None) -> dict:
    container = {
        "title": [{"properties": {
            "show": lit("true"),
            "text": texto(titulo_texto),
            "fontColor": cor("#173F35"),
            "alignment": texto("left"),
        }}]
    }
    if subtitulo_texto:
        container["subTitle"] = [{"properties": {
            "show": lit("true"),
            "text": texto(subtitulo_texto),
            "fontColor": cor("#76817B"),
            "alignment": texto("left"),
        }}]
    return container


def cabecalho(titulo_pagina: str) -> dict:
    return {
        "general": [{"properties": {"paragraphs": [{
            "textRuns": [
                {"value": "CANA INTELLIGENCE", "textStyle": {
                    "fontSize": "20pt",
                    "fontFamily": "Segoe UI Semibold",
                    "color": "#173F35",
                    "fontWeight": "600",
                }},
                {"value": "     " + titulo_pagina, "textStyle": {
                    "fontSize": "12pt",
                    "fontFamily": "Segoe UI",
                    "color": "#25312D",
                }},
            ],
            "horizontalTextAlignment": "left",
        }]}}]
    }


def rodape(linha: str) -> dict:
    """Caixa de texto do rodape: 9pt, cinza neutro, sem cromo."""
    return {
        "general": [{"properties": {"paragraphs": [{
            "textRuns": [
                {"value": linha, "textStyle": {
                    "fontSize": "9pt",
                    "fontFamily": "Segoe UI",
                    "color": "#76817B",
                }},
            ],
            "horizontalTextAlignment": "left",
        }]}}]
    }


def rotulo_cartao(valor_px: int = 26) -> dict:
    return {
        "labels": [{"properties": {
            "fontSize": inteiro(valor_px),
            "fontFamily": texto("Segoe UI Semibold"),
            "color": cor("#173F35"),
        }}],
        "categoryLabels": [{"properties": {
            "show": lit("true"),
            "fontSize": inteiro(10),
            "fontFamily": texto("Segoe UI"),
            "color": cor("#76817B"),
        }}],
    }


# ------------------------------------------------------------------ pagina

class Pagina:
    """Escreve visuais em definition/pages/<id>/visuals/<nome>/visual.json."""

    def __init__(self, page_id: str, nome_pagina: str):
        self.pasta = PAGINAS / page_id
        self.nome_pagina = nome_pagina
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
                "x": x, "y": y, "z": 1000 + self.contador,
                "width": w, "height": h, "tabOrder": self.contador,
            },
            "visual": visual,
        }
        pasta = self.pasta / "visuals" / nome
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "visual.json").write_text(
            json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self.gerados.append((nome, tipo, x, y, w, h))
        return nome

    # atalhos que todo gerador usa -------------------------------------------

    def limpar(self) -> int:
        """Remove os visuais gerados antes. Só mexe na pasta visuals desta página.

        O OneDrive marca pasta sincronizada como somente leitura, e ai rmtree
        falha com PermissionError. O tratador tira o atributo e repete, em vez de
        deixar a pagina pela metade.
        """
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

        pasta = self.pasta / "visuals"
        removidos = 0
        if pasta.exists():
            for filho in pasta.iterdir():
                if filho.is_dir():
                    shutil.rmtree(filho, onerror=tratar)
                    if not filho.exists():
                        removidos += 1
        return removidos

    def cabecalho_tela(self):
        self.add("textbox", 24, 24, 1392, 48,
                 objects=cabecalho(self.nome_pagina), container=sem_cromo())

    def filtro_data(self, x=24, y=152, w=320):
        self.add("slicer", x, y, w, 40,
                 {"Values": {"projections": [coluna("Dim_Calendario", "Data")]}},
                 container=sem_cromo())

    def filtro(self, tabela, campo, x, w=220, y=152):
        self.add("slicer", x, y, w, 44,
                 {"Values": {"projections": [coluna(tabela, campo)]}},
                 container=sem_cromo())

    def cartao(self, x, y, w, h, rotulo, tabela, nome_medida, valor_px=26):
        self.add("card", x, y, w, h,
                 {"Values": {"projections": [medida(tabela, nome_medida)]}},
                 objects=rotulo_cartao(valor_px),
                 container=sem_cromo() if not rotulo else titulo(rotulo))

    def trilho(self, medidas: list[tuple[str, str, str]], x=24, y=220, w=300, h=72, gap=8,
               valor_px=18):
        """Empilha cartoes no trilho de 300px. Cada item: (rotulo, tabela, medida)."""
        atual = y
        for rotulo, tabela, nome in medidas:
            self.cartao(x, atual, w, h, rotulo, tabela, nome, valor_px=valor_px)
            atual += h + gap
        return atual - gap

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
            if x < ox + ow and ox < x + w and y < oy + oh and oy < y + h:
                problemas.append(f"{nome} ({tipo}) sobrepoe {onome} ({outro})")
        areas.append((tipo, x, y, w, h, nome))
    return problemas
