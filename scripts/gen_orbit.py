#!/usr/bin/env python3
"""Genera images/stack-orbit.svg: tecnologías orbitando el monograma CR.

Dos anillos girando en sentidos opuestos (SMIL) con cometas de estela,
chips glass contra-rotados siempre legibles, núcleo con resplandor y ondas
de pulso. Paleta «Aurora Nocturna» de tokens.py.
"""
import os

from tokens import (FONT, MONO, PALETTE, REDUCED, TW_STYLE, flow_gradient,
                    glow_filter, stars)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "stack-orbit.svg")

P = PALETTE
S, C = 420, 210  # tamaño y centro

RINGS = [
    # (radio, dur_s, reverse, accent, items[(nombre, angulo)])
    (100, 26, False, P["cyan"], [("PHP", 0), ("Python", 90), ("MySQL", 180), ("Flask", 270)]),
    (158, 40, True, P["violet"], [("Odoo", 0), ("Apache", 60), ("Nginx", 120),
                                  ("Linux", 180), ("Firebase", 240), ("Git", 300)]),
]

STYLE = (
    "<style>"
    ".p{transform-box:fill-box;transform-origin:center;animation:pu 4s ease-out infinite}"
    ".p2{animation-delay:2s}"
    "@keyframes pu{0%{transform:scale(1);opacity:.5}80%,100%{transform:scale(1.9);opacity:0}}"
    + TW_STYLE
    + REDUCED
    + "</style>"
)


def item(name, ang, r, dur, reverse, accent):
    w = len(name) * 7 + 22
    a_to = ang - 360 if reverse else ang + 360
    c_to = -a_to
    return (
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'from="{ang} {C} {C}" to="{a_to} {C} {C}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g transform="translate({C} {C - r})">'
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'from="{-ang} 0 0" to="{c_to} 0 0" dur="{dur}s" repeatCount="indefinite"/>'
        f'<rect x="{-w / 2}" y="-12" width="{w}" height="24" rx="12" fill="{P["glass"]}" '
        f'stroke="{accent}" stroke-opacity="0.6"/>'
        f'<text y="4" text-anchor="middle" font-size="11" font-weight="700" '
        f'fill="{accent}">{name}</text>'
        f"</g></g></g>"
    )


def comet(r, dur, reverse, accent, start):
    a_to = start - 360 if reverse else start + 360
    return (
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'from="{start} {C} {C}" to="{a_to} {C} {C}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<circle cx="{C}" cy="{C - r}" r="3" fill="{accent}" filter="url(#gw)"/>'
        f'<circle cx="{C}" cy="{C - r}" r="6.5" fill="{accent}" opacity=".18"/>'
        f"</g>"
    )


parts = [
    f'<svg width="{S}" height="{S}" viewBox="0 0 {S} {S}" xmlns="http://www.w3.org/2000/svg" '
    f'font-family="{FONT}" role="img" aria-label="Stack de TenebrisOne orbitando">',
    STYLE,
    "<defs>" + flow_gradient("g") + glow_filter("gw", 3) + "</defs>",
    stars([(40, 50, 0.3), (380, 60, 1.5), (60, 370, 2.4), (370, 350, 0.9),
           (210, 22, 1.9), (25, 210, 0.6), (398, 210, 2.8)], color=P["violet"]),
]
for r, _, _, _, _ in RINGS:
    parts.append(
        f'<circle cx="{C}" cy="{C}" r="{r}" fill="none" stroke="{P["muted"]}" '
        f'stroke-opacity="0.4" stroke-dasharray="3 7"/>'
    )
parts += [
    f'<circle class="p" cx="{C}" cy="{C}" r="52" fill="none" stroke="{P["cyan"]}" stroke-width="1.5"/>',
    f'<circle class="p p2" cx="{C}" cy="{C}" r="52" fill="none" stroke="{P["violet"]}" stroke-width="1.5"/>',
    f'<circle cx="{C}" cy="{C}" r="52" fill="{P["glass"]}" stroke="url(#g)" stroke-width="1.8" filter="url(#gw)"/>',
    f'<text x="{C}" y="{C - 2}" text-anchor="middle" font-size="26" font-weight="800" fill="url(#g)">CR</text>',
    f'<text x="{C}" y="{C + 20}" text-anchor="middle" font-size="10.5" '
    f'font-family="{MONO}" fill="{P["muted"]}">TenebrisOne</text>',
]
for i, (r, dur, rev, accent, items) in enumerate(RINGS):
    parts.append(comet(r, dur, rev, accent, 45 + i * 130))
    for name, ang in items:
        parts.append(item(name, ang, r, dur, rev, accent))
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))
print(f"Órbita generada en {OUT}")
