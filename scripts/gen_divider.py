#!/usr/bin/env python3
"""Genera images/divider.svg: separador con haz de energía y cometa.

Línea base tenue, haz degradado que respira, cometa con estela cruzando
en bucle y destellos parpadeantes. Fondo transparente (tema claro/oscuro).
"""
import os

from tokens import PALETTE, REDUCED, TW_STYLE, flow_gradient, glow_filter, stars

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "divider.svg")

W, H = 960, 48
P = PALETTE
CY = 24  # eje vertical del haz

STYLE = (
    "<style>"
    ".beam{animation:br 5s ease-in-out infinite}"
    "@keyframes br{0%,100%{opacity:.45}50%{opacity:1}}"
    ".comet{animation:cm 6s cubic-bezier(.45,.05,.55,.95) infinite}"
    "@keyframes cm{0%{transform:translateX(-80px)}100%{transform:translateX(1040px)}}"
    ".dia{transform-box:fill-box;transform-origin:center;animation:rot 9s linear infinite}"
    "@keyframes rot{to{transform:rotate(360deg)}}"
    + TW_STYLE
    + REDUCED
    + "@media (prefers-reduced-motion:reduce){.comet{opacity:0!important}}"
    "</style>"
)

DEFS = (
    "<defs>"
    + flow_gradient("g")
    + glow_filter("gw", 3)
    + '<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{P["cyan"]}" stop-opacity="0"/>'
    f'<stop offset="1" stop-color="{P["cyan"]}" stop-opacity=".85"/></linearGradient>'
    "</defs>"
)

svg = (
    f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
    f'role="img" aria-label="">'
    + STYLE
    + DEFS
    # línea base tenue de borde a borde
    + f'<line x1="0" y1="{CY}" x2="{W}" y2="{CY}" stroke="{P["muted"]}" stroke-opacity=".3" stroke-width="1"/>'
    # haz degradado que respira
    + f'<line class="beam" x1="120" y1="{CY}" x2="{W - 120}" y2="{CY}" stroke="url(#g)" '
    f'stroke-width="2.2" stroke-linecap="round" filter="url(#gw)"/>'
    # cometa con estela
    + f'<g class="comet"><rect x="-64" y="{CY - 1.2}" width="64" height="2.4" rx="1.2" fill="url(#trail)"/>'
    f'<circle cx="0" cy="{CY}" r="3.4" fill="{P["cyan"]}" filter="url(#gw)"/></g>'
    # diamante central girando
    + f'<g class="dia"><rect x="{W / 2 - 5}" y="{CY - 5}" width="10" height="10" rx="2" '
    f'fill="{P["bg"]}" stroke="url(#g)" stroke-width="1.6"/></g>'
    # destellos
    + stars([(200, 12, 0.4), (430, 38, 1.6), (620, 10, 0.9), (790, 36, 2.3)], color=P["violet"])
    + "</svg>"
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Divisor generado en {OUT}")
