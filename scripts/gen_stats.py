#!/usr/bin/env python3
"""Genera images/stats.svg e images/top-langs.svg con datos reales de GitHub.

Sustituye a github-readme-stats (instancia pública caída). Usa la API
pública de GitHub (con GITHUB_TOKEN opcional para la Action) y el calendario
de contribuciones. Estilo «Aurora Nocturna» de tokens.py, autocontenido.
"""
import datetime
import json
import os
import re
import urllib.request

from tokens import (FONT, MONO, PALETTE, REDUCED, blend, flow_gradient,
                    glow_filter)

USER = "TenebrisOne"
IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
P = PALETTE

# colores linguist de GitHub; acento aurora como respaldo
LANG_COLORS = {
    "PHP": "#4F5D95", "Python": "#3572A5", "JavaScript": "#f1e05a",
    "HTML": "#e34c26", "CSS": "#663399", "Hack": "#878787",
    "Shell": "#89e051", "TypeScript": "#3178c6", "Blade": "#f7523f",
    "SCSS": "#c6538c", "Vue": "#41b883", "Dockerfile": "#384d54",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "stats-gen"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def contributions():
    page = get(f"https://github.com/users/{USER}/contributions")
    m = re.search(r"([\d.,]+)\s+contributions?\s+in the last year", page)
    return m.group(1).replace(",", ".") if m else "—"


def fetch_data():
    user = json.loads(get(f"https://api.github.com/users/{USER}"))
    repos = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"))
    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    langs = {}
    for r in own:
        try:
            for lang, size in json.loads(get(r["languages_url"])).items():
                langs[lang] = langs.get(lang, 0) + size
        except Exception:
            pass
    return {
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "repos": user.get("public_repos", len(own)),
        "stars": stars,
        "langs": langs,
        "contrib": contributions(),
    }


W, H = 495, 195

STYLE = (
    "<style>"
    ".fu{opacity:0;transform:translateY(10px);animation:fu .6s cubic-bezier(.22,1,.36,1) forwards}"
    "@keyframes fu{to{opacity:1;transform:none}}"
    ".bar{transform:scaleX(0);transform-box:fill-box;transform-origin:0 50%;"
    "animation:gr .9s cubic-bezier(.22,1,.36,1) .5s forwards}"
    "@keyframes gr{to{transform:scaleX(1)}}"
    ".glowc{animation:gp 5s ease-in-out infinite}"
    "@keyframes gp{0%,100%{opacity:.55}50%{opacity:1}}"
    ".shine{animation:sweep 6s cubic-bezier(.4,0,.2,1) 1.5s infinite}"
    "@keyframes sweep{0%{transform:translateX(0)}26%{transform:translateX(760px)}"
    "100%{transform:translateX(760px)}}"
    + REDUCED
    + "@media (prefers-reduced-motion:reduce){.fu{opacity:1!important;transform:none!important}"
    ".bar{transform:none!important}.shine{opacity:0!important}}"
    "</style>"
)


def frame(title, accent):
    return (
        "<defs>"
        + flow_gradient("g")
        + flow_gradient("gb", [accent, P["border"], accent], dur=6)
        + glow_filter("gw", 4)
        + f'<radialGradient id="rg" gradientUnits="userSpaceOnUse" cx="70" cy="0" r="280">'
        f'<stop offset="0" stop-color="{accent}" stop-opacity=".2"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".06"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="cp"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13"/></clipPath>'
        "</defs>"
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="{P["glass"]}"/>'
        f'<g clip-path="url(#cp)"><rect class="glowc" x="0" y="0" width="{W}" height="{H}" fill="url(#rg)"/></g>'
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none" '
        f'stroke="url(#gb)" stroke-width="1.5"/>'
        f'<text class="fu" x="22" y="34" font-size="16" font-weight="800" fill="url(#g)">{title}</text>'
    )


SHINE = (
    '<g clip-path="url(#cp)"><g transform="rotate(16)">'
    '<rect class="shine" x="-170" y="-140" width="90" height="460" fill="url(#sh)"/>'
    "</g></g>"
)


def svg_open(label):
    return (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="{FONT}" role="img" aria-label="{label}">'
    )


def gen_stats(d):
    tiles = [
        ("⭐", "Estrellas", d["stars"], P["amber"]),
        ("📦", "Repos públicos", d["repos"], P["cyan"]),
        ("👥", "Seguidores", d["followers"], P["violet"]),
        ("🤝", "Siguiendo", d["following"], P["pink"]),
    ]
    parts = [
        svg_open(f"Estadísticas de GitHub de {USER}"),
        STYLE,
        frame(f"⚡ {USER} en GitHub", P["cyan"]),
        # bloque izquierdo: contribuciones del último año
        f'<text class="fu" style="animation-delay:.2s" x="22" y="108" font-size="44" '
        f'font-weight="800" fill="url(#g)" filter="url(#gw)">{d["contrib"]}</text>',
        f'<text class="fu" style="animation-delay:.3s" x="22" y="132" font-size="12" '
        f'fill="{P["body"]}">contribuciones en el último año</text>',
        f'<text class="fu" style="animation-delay:.4s" x="22" y="168" font-size="11" '
        f'font-family="{MONO}" fill="{P["muted"]}">actualizado a diario 🤖</text>',
    ]
    # cuadrícula 2×2 de tiles a la derecha
    tx, ty, tw, th, gap = 268, 52, 100, 58, 10
    for i, (icon, label, value, color) in enumerate(tiles):
        x = tx + (i % 2) * (tw + gap)
        y = ty + (i // 2) * (th + gap)
        parts.append(
            f'<g class="fu" style="animation-delay:{0.25 + i * 0.12:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="10" '
            f'fill="{blend(color, 0.08, P["glass"])}" stroke="{color}" stroke-opacity=".35"/>'
            f'<text x="{x + 12}" y="{y + 24}" font-size="13">{icon}</text>'
            f'<text x="{x + 34}" y="{y + 26}" font-size="17" font-weight="800" '
            f'fill="{P["title"]}">{value}</text>'
            f'<text x="{x + 12}" y="{y + 44}" font-size="9.5" letter-spacing=".3" '
            f'fill="{P["body"]}">{label}</text></g>'
        )
    parts += [SHINE, "</svg>"]
    with open(os.path.join(IMG, "stats.svg"), "w", encoding="utf-8") as f:
        f.write("".join(parts))


def gen_langs(d):
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
    rest = total - sum(v for _, v in top)
    items = [(k, v / total * 100) for k, v in top]
    if rest > 0:
        items.append(("Otros", rest / total * 100))
    parts = [
        svg_open(f"Lenguajes más usados por {USER}"),
        STYLE,
        frame("🧪 Lenguajes más usados", P["violet"]),
        f'<rect x="22" y="52" width="{W - 44}" height="12" rx="6" fill="{P["surface"]}"/>',
    ]
    # barra apilada
    x = 22.0
    bw = W - 44
    for i, (name, pct) in enumerate(items):
        seg = bw * pct / 100
        color = LANG_COLORS.get(name, [P["cyan"], P["violet"], P["pink"]][i % 3])
        parts.append(
            f'<rect class="bar" style="animation-delay:{0.4 + i * 0.1:.2f}s" '
            f'x="{x:.1f}" y="52" width="{max(seg, 2):.1f}" height="12" '
            f'{"rx=\"6\"" if len(items) == 1 else ""} fill="{color}"/>'
        )
        x += seg
    # recorte redondeado de la barra
    parts.append(
        f'<rect x="22" y="52" width="{bw}" height="12" rx="6" fill="none" '
        f'stroke="{P["glass"]}" stroke-width="3"/>'
    )
    # leyenda en 2 columnas
    lx, ly, col_w, row_h = 22, 92, (W - 44) // 2, 26
    for i, (name, pct) in enumerate(items):
        cx = lx + (i % 2) * col_w
        cy = ly + (i // 2) * row_h
        color = LANG_COLORS.get(name, [P["cyan"], P["violet"], P["pink"]][i % 3])
        ptxt = f"{pct:.1f}".replace(".", ",") + " %"
        parts.append(
            f'<g class="fu" style="animation-delay:{0.5 + i * 0.1:.2f}s">'
            f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{color}"/>'
            f'<text x="{cx + 18}" y="{cy}" font-size="12.5" font-weight="600" '
            f'fill="{P["title"]}">{name}</text>'
            f'<text x="{cx + col_w - 24}" y="{cy}" text-anchor="end" font-size="12" '
            f'font-family="{MONO}" fill="{P["body"]}">{ptxt}</text></g>'
        )
    parts += [SHINE, "</svg>"]
    with open(os.path.join(IMG, "top-langs.svg"), "w", encoding="utf-8") as f:
        f.write("".join(parts))


data = fetch_data()
gen_stats(data)
gen_langs(data)
print(f"stats.svg y top-langs.svg generados: {data['repos']} repos, "
      f"{data['stars']} estrellas, {len(data['langs'])} lenguajes")
