#!/usr/bin/env python3
"""Genera images/footer.svg: cierre del README.

Olas aurora con degradados vivos, campo de estrellas, CTA con resplandor
y corazón latiendo. Paleta y motion tokens de tokens.py.
"""
import os

from tokens import (FONT, PALETTE, REDUCED, TW_STYLE, flow_gradient,
                    glow_filter, stars)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "footer.svg")

W, H = 960, 190
P = PALETTE

STYLE = (
    "<style>"
    ".w1{animation:mv 11s linear infinite}"
    ".w2{animation:mv 17s linear infinite reverse}"
    ".w3{animation:mv 25s linear infinite}"
    "@keyframes mv{to{transform:translateX(-480px)}}"
    ".fu{opacity:0;transform:translateY(12px);animation:fu .8s cubic-bezier(.22,1,.36,1) .15s forwards}"
    ".fu2{animation-delay:.45s}"
    "@keyframes fu{to{opacity:1;transform:none}}"
    ".beat{transform-box:fill-box;transform-origin:center;animation:beat 1.6s ease-in-out infinite}"
    "@keyframes beat{0%,100%{transform:scale(1)}12%{transform:scale(1.3)}24%{transform:scale(1)}"
    "36%{transform:scale(1.2)}48%{transform:scale(1)}}"
    ".star{transform-box:fill-box;transform-origin:center;animation:spin 7s ease-in-out infinite}"
    "@keyframes spin{0%,100%{transform:rotate(-12deg) scale(1)}50%{transform:rotate(12deg) scale(1.18)}}"
    + TW_STYLE
    + REDUCED
    + "</style>"
)


def wave(cls, y, color, opacity):
    return (
        f'<g class="{cls}"><path d="M0 {y} Q120 {y - 22} 240 {y} T480 {y} T720 {y} '
        f'T960 {y} T1200 {y} T1440 {y} V{H} H0 Z" fill="{color}" opacity="{opacity}"/></g>'
    )


svg = (
    f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
    f'font-family="{FONT}" role="img" '
    f'aria-label="⭐ ¿Te gustó algún proyecto? ¡Dale una estrella! Hecho con amor en Colombia — TenebrisOne">'
    + STYLE
    + "<defs>"
    + flow_gradient("g")
    + glow_filter("gw", 4)
    + "</defs>"
    + stars(
        [(80, 30, 0.2), (200, 62, 1.4), (330, 22, 2.5), (620, 58, 0.8),
         (760, 24, 1.9), (900, 48, 0.5), (480, 14, 2.9)],
        color=P["violet"],
    )
    + f'<g class="fu"><text class="star" x="322" y="46" font-size="22">⭐</text>'
    f'<text x="352" y="46" font-size="22" font-weight="800" fill="url(#g)" filter="url(#gw)">'
    f"¿Te gustó algún proyecto?</text></g>"
    + f'<text class="fu" x="480" y="76" text-anchor="middle" font-size="15" '
    f'fill="{P["body"]}">¡Dale una estrella! Me ayuda a seguir construyendo cosas útiles.</text>'
    + f'<g class="fu fu2">'
    f'<text x="447" y="104" text-anchor="end" font-size="13.5" fill="{P["muted"]}">Hecho con</text>'
    f'<text class="beat" x="455" y="104" font-size="14" fill="{P["pink"]}">❤</text>'
    f'<text x="474" y="104" font-size="13.5" fill="{P["muted"]}">en Colombia — TenebrisOne</text></g>'
    + wave("w3", 128, P["pink"], 0.16)
    + wave("w2", 140, P["violet"], 0.22)
    + wave("w1", 152, P["cyan"], 0.20)
    + "</svg>"
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Footer generado en {OUT}")
