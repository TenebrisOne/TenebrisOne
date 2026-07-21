#!/usr/bin/env python3
"""Genera images/stack-orbit.svg: tecnologías orbitando el monograma CR.

Dos anillos girando en sentidos opuestos (SMIL). Cada chip se contra-rota
para mantenerse siempre legible. Ondas de pulso emanan del centro.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "stack-orbit.svg")

S, C = 420, 210  # tamaño y centro

RINGS = [
    # (radio, dur_s, reverse, accent, items[(nombre, angulo)])
    (100, 26, False, "#7aa2f7", [("PHP", 0), ("Python", 90), ("MySQL", 180), ("Flask", 270)]),
    (158, 40, True, "#bb9af7", [("Odoo", 0), ("Apache", 60), ("Nginx", 120),
                                 ("Linux", 180), ("Firebase", 240), ("Git", 300)]),
]

STYLE = (
    "<style>"
    ".p{transform-box:fill-box;transform-origin:center;animation:pu 4s ease-out infinite}"
    ".p2{animation-delay:2s}"
    "@keyframes pu{0%{transform:scale(1);opacity:.5}80%,100%{transform:scale(1.9);opacity:0}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    "</style>"
)

GRAD = (
    '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0%" stop-color="#7aa2f7"><animate attributeName="stop-color" '
    'values="#7aa2f7;#bb9af7;#7dcfff;#7aa2f7" dur="9s" repeatCount="indefinite"/></stop>'
    '<stop offset="100%" stop-color="#bb9af7"><animate attributeName="stop-color" '
    'values="#bb9af7;#7dcfff;#7aa2f7;#bb9af7" dur="9s" repeatCount="indefinite"/></stop>'
    "</linearGradient></defs>"
)


def item(name, ang, r, dur, reverse, accent):
    w = len(name) * 7 + 20
    a_to = ang - 360 if reverse else ang + 360
    c_to = -a_to
    return (
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'from="{ang} {C} {C}" to="{a_to} {C} {C}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g transform="translate({C} {C - r})">'
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'from="{-ang} 0 0" to="{c_to} 0 0" dur="{dur}s" repeatCount="indefinite"/>'
        f'<rect x="{-w / 2}" y="-11" width="{w}" height="22" rx="11" fill="#24283b" '
        f'stroke="{accent}" stroke-opacity="0.5"/>'
        f'<text y="4" text-anchor="middle" font-size="11" font-weight="700" '
        f'fill="{accent}">{name}</text>'
        f"</g></g></g>"
    )


parts = [
    f'<svg width="{S}" height="{S}" viewBox="0 0 {S} {S}" xmlns="http://www.w3.org/2000/svg" '
    f"font-family=\"'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif\" role=\"img\" "
    f'aria-label="Stack de TenebrisOne orbitando">',
    STYLE,
    GRAD,
]
for r, _, _, _, _ in RINGS:
    parts.append(
        f'<circle cx="{C}" cy="{C}" r="{r}" fill="none" stroke="#565f89" '
        f'stroke-opacity="0.35" stroke-dasharray="3 7"/>'
    )
parts += [
    f'<circle class="p" cx="{C}" cy="{C}" r="52" fill="none" stroke="#7aa2f7" stroke-width="1.5"/>',
    f'<circle class="p p2" cx="{C}" cy="{C}" r="52" fill="none" stroke="#bb9af7" stroke-width="1.5"/>',
    f'<circle cx="{C}" cy="{C}" r="52" fill="#1a1b27" stroke="url(#g)" stroke-width="1.5"/>',
    f'<text x="{C}" y="{C - 2}" text-anchor="middle" font-size="26" font-weight="800" fill="url(#g)">CR</text>',
    f'<text x="{C}" y="{C + 20}" text-anchor="middle" font-size="10.5" '
    f"font-family=\"ui-monospace,'Courier New',monospace\" fill=\"#565f89\">TenebrisOne</text>",
]
for r, dur, rev, accent, items in RINGS:
    for name, ang in items:
        parts.append(item(name, ang, r, dur, rev, accent))
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))
print(f"Órbita generada en {OUT}")
