#!/usr/bin/env python3
"""Genera images/snake.svg: la culebrita que se come las contribuciones.

Descarga el calendario público de contribuciones de GitHub, arma el grid con
la paleta tokyonight y anima una serpiente (SMIL, bucle infinito) que recorre
el grid en serpentina devorando las celdas; al final del ciclo reaparecen.
Autocontenido: no depende de Actions externas ni de la rama `output`.
"""
import datetime
import os
import re
import urllib.request

USER = "TenebrisOne"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "snake.svg")

CELL, GAP = 11, 3
PITCH = CELL + GAP
PAD = 14
DUR = 40.0  # segundos por ciclo

# paleta «Aurora Nocturna» (scripts/tokens.py): fondo, celda vacía, rampa, serpiente
BG, BORDER, EMPTY = "#0d1226", "#272f55", "#1c2342"
RAMP = ["#3a4a85", "#6b7fe8", "#9d7bff", "#5ee7ff"]
SNAKE = "#ff9e64"
MUTED = "#5d6791"


def fetch():
    req = urllib.request.Request(
        f"https://github.com/users/{USER}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (snake-gen)"},
    )
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def parse(page):
    days = []
    for m in re.finditer(r'<td[^>]*data-date="(\d{4}-\d\d-\d\d)"[^>]*>', page):
        lvl = re.search(r'data-level="(\d)"', m.group(0))
        if lvl:
            days.append((datetime.date.fromisoformat(m.group(1)), int(lvl.group(1))))
    total = re.search(r"([\d.,]+)\s+contributions?\s+in the last year", page)
    return sorted(days), (total.group(1) if total else None)


days, total = parse(fetch())
if not days:
    raise SystemExit("No se pudo leer el calendario de contribuciones")

d0 = days[0][0]
grid_start = d0 - datetime.timedelta(days=(d0.weekday() + 1) % 7)  # domingo de la 1.ª semana
cells = {}
for d, lvl in days:
    delta = (d - grid_start).days
    cells[(delta // 7, delta % 7)] = lvl
COLS = max(c for c, _ in cells) + 1

W = PAD * 2 + COLS * PITCH - GAP
H = PAD * 2 + 7 * PITCH - GAP + 26  # + fila de leyenda


def cx(c):
    return PAD + c * PITCH + CELL / 2


def cy(r):
    return PAD + r * PITCH + CELL / 2


# ─── camino en serpentina y tiempo en que la cabeza pasa por cada celda ───
COLRUN = 6 * PITCH          # recorrido vertical de una columna
HOP = PITCH                 # salto horizontal entre columnas
TOTAL_DIST = (COLS - 1) * (COLRUN + HOP) + COLRUN

path = [f"M{cx(0)},{cy(0)}"]
for c in range(COLS):
    path.append(f"V{cy(6) if c % 2 == 0 else cy(0)}")
    if c < COLS - 1:
        path.append(f"H{cx(c + 1)}")
PATH = " ".join(path)


def eat_frac(c, r):
    d = c * (COLRUN + HOP) + (r * PITCH if c % 2 == 0 else (6 - r) * PITCH)
    return max(0.002, min(0.995, d / TOTAL_DIST))


parts = [
    f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
    f"font-family=\"'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif\" role=\"img\" "
    f'aria-label="Serpiente animada comiéndose las contribuciones de {USER}">',
    '<defs><filter id="gw" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="2.5" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
    f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>',
]

# celdas: base vacía + capa de color que la serpiente se come
for (c, r), lvl in sorted(cells.items()):
    x, y = PAD + c * PITCH, PAD + r * PITCH
    parts.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{EMPTY}"/>')
    if lvl > 0:
        tf = eat_frac(c, r)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{RAMP[lvl - 1]}">'
            f'<animate attributeName="opacity" calcMode="discrete" values="1;0;1" '
            f'keyTimes="0;{tf:.4f};0.998" dur="{DUR}s" repeatCount="indefinite"/></rect>'
        )

# cuerpo de la serpiente (segmentos que siguen el mismo camino, desfasados)
seg_dt = PITCH / TOTAL_DIST * DUR
for k in range(7, 0, -1):
    size = 13 - k * 0.7
    op = 1 - k * 0.09
    begin = seg_dt * k
    parts.append(
        f'<rect x="{-size / 2}" y="{-size / 2}" width="{size}" height="{size}" rx="3" '
        f'fill="{SNAKE}" opacity="0">'
        f'<set attributeName="opacity" to="{op:.2f}" begin="{begin:.3f}s"/>'
        f'<animateMotion path="{PATH}" dur="{DUR}s" repeatCount="indefinite" '
        f'begin="{begin:.3f}s"/></rect>'
    )
# cabeza con ojos, orientada según la dirección
parts.append(
    f'<g filter="url(#gw)"><rect x="-6.5" y="-6.5" width="13" height="13" rx="4" fill="{SNAKE}"/>'
    f'<circle cx="3" cy="-3" r="1.7" fill="{BG}"/><circle cx="3" cy="3" r="1.7" fill="{BG}"/>'
    f'<animateMotion path="{PATH}" dur="{DUR}s" repeatCount="indefinite" rotate="auto"/></g>'
)

# leyenda + total
ly = PAD + 7 * PITCH - GAP + 10
label = f"{total} contribuciones en el último año" if total else "contribuciones del último año"
parts.append(f'<text x="{PAD}" y="{ly + 10}" font-size="11" fill="{MUTED}">🐍 {label}</text>')
lx = W - PAD - 5 * PITCH - 66
parts.append(f'<text x="{lx - 6}" y="{ly + 10}" text-anchor="end" font-size="11" fill="{MUTED}">Menos</text>')
for i, col in enumerate([EMPTY] + RAMP):
    parts.append(f'<rect x="{lx + i * PITCH}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" fill="{col}"/>')
parts.append(f'<text x="{lx + 5 * PITCH + 4}" y="{ly + 10}" font-size="11" fill="{MUTED}">Más</text>')
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))
print(f"Culebrita generada: {COLS} semanas, {len(cells)} días → {OUT}")
