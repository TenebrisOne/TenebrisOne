#!/usr/bin/env python3
"""Genera images/hero.svg: portada animada del README.

Auroras difuminadas a la deriva, campo de estrellas, estrellas fugaces,
suelo de rejilla estilo synthwave, nombre con degradado vivo + resplandor
y una terminal glass con efecto de tipeo. Motion tokens de tokens.py.
"""
import os

from tokens import (FONT, MONO, PALETTE, REDUCED, TW_STYLE, blur_filter,
                    flow_gradient, glow_filter, stars)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "hero.svg")

W, H = 960, 320
P = PALETTE

STYLE = (
    "<style>"
    ".fu{opacity:0;transform:translateY(16px);animation:fu .7s cubic-bezier(.22,1,.36,1) forwards}"
    "@keyframes fu{to{opacity:1;transform:none}}"
    ".d1{animation-delay:.1s}.d2{animation-delay:.25s}.d3{animation-delay:.4s}"
    ".d4{animation-delay:.55s}.d5{animation-delay:.68s}.d6{animation-delay:.8s}"
    ".t{transform:scaleX(0);transform-box:fill-box;transform-origin:0 50%}"
    ".t1{animation:ty .5s steps(8) 1s forwards}"
    ".t2{animation:ty .8s steps(30) 1.7s forwards}"
    ".t3{animation:ty .6s steps(13) 2.7s forwards}"
    ".t4{animation:ty .9s steps(34) 3.5s forwards}"
    "@keyframes ty{to{transform:scaleX(1)}}"
    ".cur{opacity:0;animation:bl 1.1s steps(1) 4.6s infinite}"
    "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
    + TW_STYLE +
    ".au1{animation:au1 16s ease-in-out infinite alternate}"
    "@keyframes au1{to{transform:translate(70px,26px)}}"
    ".au2{animation:au2 20s ease-in-out infinite alternate}"
    "@keyframes au2{to{transform:translate(-60px,20px)}}"
    ".au3{animation:au3 13s ease-in-out infinite alternate}"
    "@keyframes au3{to{transform:translate(40px,-24px)}}"
    ".glow{animation:gl 5s ease-in-out infinite}"
    "@keyframes gl{0%,100%{stroke-opacity:.3}50%{stroke-opacity:.9}}"
    ".st1{animation:sh1 11s linear 2s infinite}"
    "@keyframes sh1{0%{transform:translate(-140px,20px);opacity:0}"
    "2%{opacity:1}9%{transform:translate(1060px,240px);opacity:0}"
    "100%{transform:translate(1060px,240px);opacity:0}}"
    ".st2{animation:sh2 15s linear 7s infinite}"
    "@keyframes sh2{0%{transform:translate(1100px,10px);opacity:0}"
    "2%{opacity:1}8%{transform:translate(-160px,190px);opacity:0}"
    "100%{transform:translate(-160px,190px);opacity:0}}"
    ".flt{animation:flt 6s ease-in-out infinite alternate}"
    "@keyframes flt{to{transform:translateY(-7px)}}"
    ".scan{animation:scan 7s linear infinite}"
    "@keyframes scan{0%{transform:translateX(-960px)}100%{transform:translateX(960px)}}"
    + REDUCED +
    "@media (prefers-reduced-motion:reduce){.t{transform:scaleX(1)!important}"
    ".cur{opacity:1!important}.st1,.st2{opacity:0!important}}"
    "</style>"
)


def defs():
    typ_masks = "".join(
        f'<mask id="m{i}"><rect class="t t{i}" x="{x}" y="{y}" width="{w}" height="18" fill="#fff"/></mask>'
        for i, (x, y, w) in enumerate(
            [(580, 116, 95), (580, 140, 250), (580, 168, 135), (580, 192, 300)], start=1
        )
    )
    return (
        "<defs>"
        + flow_gradient("g1")
        + flow_gradient("g2", [P["violet"], P["pink"], P["cyan"]], dur=10)
        + glow_filter("glow2", 6)
        + blur_filter("soft", 34)
        + '<linearGradient id="ss" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>'
        '<linearGradient id="gridfade" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".45" stop-color="#fff" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>'
        '<mask id="gridm"><rect x="0" y="248" width="960" height="72" fill="url(#gridfade)"/></mask>'
        '<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".05"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="hc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17"/></clipPath>'
        + typ_masks
        + "</defs>"
    )


def auroras():
    return (
        '<g clip-path="url(#hc)">'
        f'<ellipse class="au1" cx="180" cy="60" rx="230" ry="120" fill="{P["violet"]}" opacity=".17" filter="url(#soft)"/>'
        f'<ellipse class="au2" cx="760" cy="40" rx="260" ry="110" fill="{P["cyan"]}" opacity=".13" filter="url(#soft)"/>'
        f'<ellipse class="au3" cx="500" cy="290" rx="300" ry="120" fill="{P["pink"]}" opacity=".10" filter="url(#soft)"/>'
        "</g>"
    )


def star_field():
    coords = [
        (60, 36, 0), (140, 70, 1.1), (250, 30, 2.2), (330, 88, 0.6),
        (420, 44, 1.7), (505, 26, 0.3), (700, 36, 2.6), (800, 60, 1.3),
        (880, 28, 0.9), (930, 90, 2.0), (540, 66, 1.5), (905, 170, 0.4),
        (45, 150, 2.4), (935, 250, 1.0),
    ]
    return '<g clip-path="url(#hc)">' + stars(coords) + "</g>"


def shooting_stars():
    line = '<line x1="0" y1="0" x2="95" y2="21" stroke="url(#ss)" stroke-width="2" stroke-linecap="round"/>'
    return (
        '<g clip-path="url(#hc)">'
        f'<g class="st1" opacity="0">{line}</g>'
        f'<g class="st2" opacity="0"><line x1="95" y1="0" x2="0" y2="14" stroke="url(#ss)" stroke-width="2" stroke-linecap="round"/></g>'
        "</g>"
    )


def grid_floor():
    parts = ['<g clip-path="url(#hc)"><g mask="url(#gridm)">']
    # verticales convergiendo hacia el punto de fuga (480, 180)
    for k in range(-10, 11):
        xt, xb = 480 + k * 30, 480 + k * 105
        parts.append(
            f'<line x1="{xt}" y1="252" x2="{xb}" y2="322" stroke="{P["violet"]}" '
            f'stroke-opacity=".22" stroke-width="1"/>'
        )
    # horizontales con espaciado creciente
    for y in (256, 262, 270, 280, 293, 308):
        parts.append(
            f'<line x1="0" y1="{y}" x2="960" y2="{y}" stroke="{P["cyan"]}" '
            f'stroke-opacity=".16" stroke-width="1"/>'
        )
    parts.append("</g>")
    # horizonte brillante
    parts.append(
        f'<line x1="24" y1="250" x2="936" y2="250" stroke="url(#g1)" '
        f'stroke-width="1.6" opacity=".75" filter="url(#glow2)"/>'
    )
    parts.append('<rect class="scan" x="0" y="248" width="300" height="72" fill="url(#shine)"/>')
    parts.append("</g>")
    return "".join(parts)


def chip(x, y, label, color):
    w = round(len(label) * 8.2) + 30
    return (
        f'<g><rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{P["glass"]}" '
        f'stroke="{color}" stroke-opacity=".65"/>'
        f'<circle cx="{x + 14}" cy="{y + 13}" r="3" fill="{color}"/>'
        f'<text x="{x + 24}" y="{y + 17.5}" font-size="11.5" font-weight="700" '
        f'letter-spacing=".8" fill="{color}">{label}</text></g>',
        w,
    )


def left_block():
    parts = [
        f'<text class="fu d1" x="48" y="102" font-size="17" fill="{P["body"]}">👋 ¡Hola! Soy</text>',
        f'<text class="fu d2" x="46" y="150" font-size="46" font-weight="800" '
        f'fill="url(#g1)" filter="url(#glow2)">Cristian Ruiz</text>',
        f'<text class="fu d3" x="48" y="182" font-size="15.5" font-family="{MONO}" '
        f'fill="{P["cyan"]}">~ @TenebrisOne</text>',
    ]
    x = 48
    for i, (label, color) in enumerate(
        [("FULLSTACK DEV", P["cyan"]), ("ODOO · ERP", P["violet"]), ("VPS LINUX", P["pink"])]
    ):
        c, w = chip(x, 205, label, color)
        parts.append(f'<g class="fu d{4 + i}">{c}</g>')
        x += w + 10
    return "".join(parts)


def terminal():
    tx, ty, tw, th = 565, 74, 352, 156
    mono = f'font-family="{MONO}" font-size="12.5"'
    return (
        f'<g class="fu d3">'
        f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{P["glass"]}" '
        f'stroke="{P["border"]}" opacity=".92"/>'
        f'<rect x="{tx}" y="{ty}" width="{tw}" height="30" rx="12" fill="{P["surface"]}"/>'
        f'<rect x="{tx}" y="{ty + 18}" width="{tw}" height="12" fill="{P["surface"]}"/>'
        f'<circle cx="{tx + 18}" cy="{ty + 15}" r="4.5" fill="{P["red"]}"/>'
        f'<circle cx="{tx + 34}" cy="{ty + 15}" r="4.5" fill="{P["amber"]}"/>'
        f'<circle cx="{tx + 50}" cy="{ty + 15}" r="4.5" fill="{P["green"]}"/>'
        f'<text x="{tx + tw / 2}" y="{ty + 19}" text-anchor="middle" {mono} '
        f'fill="{P["muted"]}">cristian@tenebris: ~</text>'
        f'<text x="{tx + 16}" y="{ty + 55}" {mono} fill="{P["green"]}" mask="url(#m1)">$ whoami</text>'
        f'<text x="{tx + 16}" y="{ty + 79}" {mono} fill="{P["body"]}" mask="url(#m2)">'
        f'&#187; fullstack developer &#183; Colombia</text>'
        f'<text x="{tx + 16}" y="{ty + 107}" {mono} fill="{P["green"]}" mask="url(#m3)">$ stack --list</text>'
        f'<text x="{tx + 16}" y="{ty + 131}" {mono} fill="{P["cyan"]}" mask="url(#m4)">'
        f'&#187; php &#183; python &#183; odoo &#183; mysql &#183; vps</text>'
        f'<rect class="cur" x="{tx + 16}" y="{ty + 138}" width="8" height="14" fill="{P["cyan"]}"/>'
        f"</g>"
    )


svg = (
    f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
    f'font-family="{FONT}" role="img" '
    f'aria-label="Cristian Ruiz — TenebrisOne · Desarrollador Fullstack · Odoo · VPS">'
    + STYLE
    + defs()
    + f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="{P["bg_deep"]}" stroke="{P["border"]}"/>'
    + auroras()
    + star_field()
    + grid_floor()
    + shooting_stars()
    + f'<rect class="glow" x="2.5" y="2.5" width="{W - 5}" height="{H - 5}" rx="16" '
    f'fill="none" stroke="url(#g1)" stroke-width="1.6"/>'
    + f'<rect x="30" y="0" width="900" height="4" rx="2" fill="url(#g1)"/>'
    + left_block()
    + terminal()
    + "</svg>"
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Héroe generado en {OUT}")
