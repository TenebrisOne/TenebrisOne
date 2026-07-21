#!/usr/bin/env python3
"""Genera cabeceras de sección SVG animadas para el README de TenebrisOne.

Cada cabecera: icono flotante, título con degradado vivo (SMIL), subrayado
que se dibuja al cargar y una chispa que recorre la línea en bucle.
Fondo transparente: funciona en tema claro y oscuro de GitHub.
"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "sections")

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

W, H = 900, 64

STYLE = (
    "<style>"
    ".ic{transform-box:fill-box;transform-origin:center;animation:fl 2.6s ease-in-out infinite alternate}"
    "@keyframes fl{to{transform:translateY(-6px)}}"
    ".ttl{opacity:0;transform:translateX(-14px);animation:in .6s cubic-bezier(.22,1,.36,1) .1s forwards}"
    "@keyframes in{to{opacity:1;transform:none}}"
    ".ul{transform:scaleX(0);transform-box:fill-box;transform-origin:0 50%;"
    "animation:gr .7s cubic-bezier(.22,1,.36,1) .5s forwards}"
    "@keyframes gr{to{transform:scaleX(1)}}"
    ".spark{animation:sp 4.5s ease-in-out 1.2s infinite alternate}"
    "@keyframes sp{to{transform:translateX(772px)}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}"
    ".ttl{opacity:1!important;transform:none!important}.ul{transform:none!important}}"
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


def section(slug, icon, title):
    tw = round(len(title) * 16.2) + 8
    svg = (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f"font-family=\"'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif\" role=\"img\" "
        f'aria-label="{html.escape(title)}">'
        f"{STYLE}{GRAD}"
        f'<text class="ic" x="6" y="44" font-size="32">{icon}</text>'
        f'<text class="ttl" x="56" y="44" font-size="30" font-weight="800" '
        f'fill="url(#g)">{html.escape(title)}</text>'
        f'<rect x="56" y="54" width="832" height="1.5" fill="#7aa2f7" opacity="0.18"/>'
        f'<rect class="ul" x="56" y="52" width="{tw}" height="4.5" rx="2.25" fill="url(#g)"/>'
        f'<g class="spark"><circle cx="60" cy="55" r="7" fill="#7dcfff" opacity="0.25"/>'
        f'<circle cx="60" cy="55" r="3" fill="#7dcfff"/></g>'
        "</svg>"
    )
    with open(os.path.join(OUT, f"{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


os.makedirs(OUT, exist_ok=True)
for s in SECTIONS:
    section(*s)
print(f"{len(SECTIONS)} cabeceras generadas en {OUT}")
