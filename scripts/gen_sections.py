#!/usr/bin/env python3
"""Genera cabeceras de sección SVG animadas para el README de TenebrisOne.

Cada cabecera: número editorial fantasma, icono flotante en caja glass con
anillo degradado, título con degradado vivo, subrayado que se dibuja y un
cometa que recorre la línea. Fondo transparente (tema claro y oscuro).
"""
import html
import os

from tokens import FONT, MONO, PALETTE, REDUCED, flow_gradient, glow_filter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "sections")

P = PALETTE

SECTIONS = [
    ("sobre-mi", "🚀", "Sobre mí"),
    ("stack", "🧰", "Stack Tecnológico"),
    ("destacados", "⭐", "Proyectos Destacados"),
    ("proyectos", "📂", "Todos mis proyectos"),
    ("actividad", "📊", "Mi actividad en GitHub"),
    ("culebrita", "🐍", "La culebrita se come mis commits"),
    ("logros", "🏆", "Logros Destacados"),
    ("contacto", "📫", "¿Hablamos?"),
]

W, H = 900, 76

STYLE = (
    "<style>"
    ".box{transform-box:fill-box;transform-origin:center;animation:fl 3s ease-in-out infinite alternate}"
    "@keyframes fl{to{transform:translateY(-5px)}}"
    ".ttl{opacity:0;transform:translateX(-16px);animation:in .6s cubic-bezier(.22,1,.36,1) .1s forwards}"
    ".num{opacity:0;animation:nin .8s ease .25s forwards}"
    "@keyframes nin{to{opacity:1}}"
    "@keyframes in{to{opacity:1;transform:none}}"
    ".ul{transform:scaleX(0);transform-box:fill-box;transform-origin:0 50%;"
    "animation:gr .7s cubic-bezier(.22,1,.36,1) .45s forwards}"
    "@keyframes gr{to{transform:scaleX(1)}}"
    ".comet{animation:cm 5s cubic-bezier(.45,.05,.55,.95) 1.2s infinite}"
    "@keyframes cm{0%{transform:translateX(0)}100%{transform:translateX(806px)}}"
    + REDUCED
    + "@media (prefers-reduced-motion:reduce){.ttl,.num{opacity:1!important;transform:none!important}"
    ".ul{transform:none!important}.comet{opacity:0!important}}"
    "</style>"
)


def section(idx, slug, icon, title):
    tw = round(len(title) * 14.8) + 10
    num = f"{idx:02d}"
    defs = (
        "<defs>"
        + flow_gradient("g")
        + glow_filter("gw", 3)
        + '<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{P["cyan"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{P["cyan"]}" stop-opacity=".8"/></linearGradient>'
        "</defs>"
    )
    svg = (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="{FONT}" role="img" aria-label="{html.escape(title)}">'
        f"{STYLE}{defs}"
        # número editorial fantasma a la derecha
        f'<text class="num" x="{W - 6}" y="52" text-anchor="end" font-size="46" font-weight="900" '
        f'font-family="{MONO}" fill="none" stroke="{P["muted"]}" stroke-opacity=".45" '
        f'stroke-width="1.1" letter-spacing="2">{num}</text>'
        # caja glass del icono con anillo degradado
        f'<g class="box"><rect x="8" y="12" width="46" height="46" rx="13" fill="{P["glass"]}" '
        f'stroke="url(#g)" stroke-width="1.6"/>'
        f'<text x="31" y="45" text-anchor="middle" font-size="24">{icon}</text></g>'
        # título con degradado vivo
        f'<text class="ttl" x="70" y="44" font-size="28" font-weight="800" '
        f'fill="url(#g)">{html.escape(title)}</text>'
        # línea base + subrayado + cometa
        f'<rect x="70" y="62" width="{W - 80}" height="1.5" fill="{P["violet"]}" opacity="0.18"/>'
        f'<rect class="ul" x="70" y="60" width="{tw}" height="4.5" rx="2.25" fill="url(#g)"/>'
        f'<g class="comet"><rect x="26" y="61.6" width="48" height="1.8" rx="0.9" fill="url(#trail)"/>'
        f'<circle cx="74" cy="62.5" r="3" fill="{P["cyan"]}" filter="url(#gw)"/></g>'
        "</svg>"
    )
    with open(os.path.join(OUT, f"{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


os.makedirs(OUT, exist_ok=True)
for i, s in enumerate(SECTIONS, start=1):
    section(i, *s)
print(f"{len(SECTIONS)} cabeceras generadas en {OUT}")
