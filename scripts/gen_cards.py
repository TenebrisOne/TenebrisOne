#!/usr/bin/env python3
"""Genera tarjetas SVG uniformes para los proyectos del README de TenebrisOne.

Diseño «Aurora Nocturna» (tokens.py): superficie glass, borde degradado
animado, resplandor de esquina tintado por categoría, píldora de categoría,
badge de visibilidad con halo, chips de stack y barrido de brillo.
Grid 8pt, radius 14, tipografía system-ui.
"""
import html
import os

from tokens import FONT, PALETTE, blend, flow_gradient, glow_filter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "cards")

P = PALETTE

ACCENTS = {
    "plataformas": P["cyan"],
    "integraciones": P["violet"],
    "herramientas": P["pink"],
}

CAT_LABEL = {
    "plataformas": "PLATAFORMA WEB",
    "integraciones": "INTEGRACIÓN · AUTOMATIZACIÓN",
    "herramientas": "APP · HERRAMIENTA",
}

W, H = 420, 190
PAD = 20

PROJECTS = [
    # (slug, nombre, categoria, publico, descripcion, [stack])
    ("mja-manager", "MJA_Manager", "plataformas", False,
     "Plataforma interna de Legado de Honor: afiliados, cuotas, pagos, servicios, procesos y documentos, con autenticación, auditoría y panel administrativo.",
     ["PHP", "MySQL"]),
    ("mja-landing", "mja-landing", "plataformas", False,
     "Landing page de la plataforma MJA, puerta de entrada y presentación del producto.",
     ["HTML", "CSS"]),
    ("gestion-terranova", "gestion_terranova", "plataformas", False,
     "Gestión integral de una empresa de venta de lotes: clientes, propiedades, ventas y procesos administrativos. Migración de Excel a plataforma estructurada.",
     ["PHP", "MySQL"]),
    ("kryon", "Kryon", "plataformas", False,
     "Kanban multiempresa para proyectos y sprints: autenticación, multitenencia, selector de empresa y UI en modo oscuro.",
     ["Multitenant", "Kanban"]),
    ("auto-msn-crm", "Auto_msn_CRM", "plataformas", False,
     "CRM para gestión y automatización de clientes: contactos, comunicaciones y seguimiento de procesos comerciales.",
     ["CRM", "Automatización"]),
    ("si-pos", "SI-POS", "plataformas", False,
     "Sistema de facturación de punto de venta para gestión ágil de ventas, inventarios y reportes.",
     ["PHP", "MySQL", "JS"]),
    ("azaroth", "Azaroth", "plataformas", False,
     "App para crear y administrar rifas; organiza cada sorteo y genera boletos listos para impresión.",
     ["PHP"]),
    ("rifa-sanroque", "rifa-sanroque", "plataformas", False,
     "Rifa profesional con reservas temporales y pagos PSE, dashboard de API para control de stock, gestión de clientes y confirmación automatizada.",
     ["PHP", "MySQL", "PSE"]),
    ("registro-contactos", "registro_contactos", "plataformas", False,
     "Formulario web para registrar terceros y centralizar su información de contacto.",
     ["Web"]),
    ("senaparking", "SENAParking", "plataformas", True,
     "Gestión del parqueadero del SENA: ingreso/salida de vehículos, administración de usuarios e historial de movimientos.",
     ["PHP", "MySQL", "Bootstrap"]),
    ("excel-terceros-odoo", "excel-terceros-odoo", "integraciones", True,
     "Sincroniza empresas y empleados con Odoo desde Excel/JSON: valida NIT colombiano con cálculo de DV, resuelve Many2one y crea o actualiza vía JSON-RPC.",
     ["Python", "Flask", "Odoo"]),
    ("pricelist", "pricelist", "integraciones", True,
     "Genera listas de precios profesionales en PDF desde Odoo por XML-RPC. Filtros por fechas, categorías, marcas y favoritos; diseño con ReportLab.",
     ["Python", "Odoo", "ReportLab"]),
    ("webhook-uvt-iva", "webhook_uvt_iva", "integraciones", False,
     "Recibe webhooks de Odoo y ajusta el IVA (0% o 19%) en ventas y compras según precio y topes de UVT en Colombia para computadores y móviles.",
     ["Python", "Flask", "Odoo"]),
    ("webhook-scrap", "webhook_scrap", "integraciones", False,
     "Consulta información empresarial del RUES por la API de Socrata y enriquece los registros de terceros en Odoo.",
     ["Python", "Odoo", "Socrata"]),
    ("search-linkedin", "Search_linkedIn", "integraciones", False,
     "Busca perfiles de LinkedIn con Google Custom Search desde webhooks de Odoo y actualiza el registro vía JSON-RPC. Corre sobre PM2 + Nginx.",
     ["Python", "Flask", "PM2"]),
    ("instagram-odoo-msn", "instagram_odoo_msn", "integraciones", False,
     "Webhook entre Instagram y Odoo: recibe mensajes y eventos, los procesa y los envía al ERP para centralizar contactos y conversaciones.",
     ["Python", "Odoo"]),
    ("servientrega-script", "Servientrega_script", "integraciones", False,
     "Scripts de integración con Servientrega para optimizar procesos operativos, manejo de datos y tareas de envíos y logística.",
     ["Python"]),
    ("scrpt-whatsapp", "Scrpt_whatsapp", "herramientas", True,
     "Envía uno o varios mensajes a uno o varios contactos de WhatsApp de forma automatizada.",
     ["Python"]),
    ("asadero-bar-mamonas", "asadero-bar-mamonas", "herramientas", True,
     "Sitio web responsive para restaurante, enfocado en visibilidad y pedidos online. Desplegado en Firebase Hosting.",
     ["HTML", "CSS", "Bootstrap"]),
    ("nextqr", "NextQR", "herramientas", True,
     "App estática para generar códigos QR y de barras, sin dependencias de servidor.",
     ["HTML", "JS"]),
    ("conversorimg-py", "ConversorImg_py", "herramientas", True,
     "App de escritorio para convertir imágenes entre PNG, JPG, JPEG, WEBP, BMP, GIF e ICO.",
     ["Python", "Tkinter"]),
]


def wrap(text, max_chars=60, max_lines=3):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        cand = f"{cur} {w_}".strip()
        if len(cand) <= max_chars:
            cur = cand
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max_chars - 1].rstrip(" ,.;") + "…"
    return lines


def chip(x, y, label, accent):
    tw = round(len(label) * 6.2) + 18
    return (
        f'<rect x="{x}" y="{y}" width="{tw}" height="22" rx="11" fill="{P["surface"]}" '
        f'stroke="{accent}" stroke-opacity=".4"/>'
        f'<text x="{x + tw / 2}" y="{y + 15}" text-anchor="middle" font-size="10.5" '
        f'font-weight="600" fill="{accent}">{html.escape(label)}</text>',
        tw,
    )


def badge(publico):
    label = "PÚBLICO" if publico else "PRIVADO"
    color = P["green"] if publico else P["amber"]
    tw = round(len(label) * 6.6) + 26
    x = W - PAD - tw
    return (
        f'<rect x="{x}" y="{14}" width="{tw}" height="18" rx="9" '
        f'fill="{blend(color, 0.14, P["glass"])}" stroke="{color}" stroke-opacity=".35"/>'
        f'<circle class="halo" cx="{x + 11}" cy="23" r="3" fill="none" '
        f'stroke="{color}" stroke-width="1.5"/>'
        f'<circle class="dot" cx="{x + 11}" cy="23" r="3" fill="{color}"/>'
        f'<text x="{x + 18}" y="27" font-size="9.5" font-weight="700" '
        f'letter-spacing="0.5" fill="{color}">{label}</text>'
    )


STYLE = (
    "<style>"
    ".cat{opacity:0;transform:translateX(-10px);animation:in .5s ease .25s forwards}"
    ".ttl{opacity:0;transform:translateY(8px);animation:in .5s ease .38s forwards}"
    ".bdg{opacity:0;animation:in .5s ease .5s forwards}"
    ".ln{opacity:0;transform:translateY(6px);animation:in .45s ease forwards}"
    ".chp{opacity:0;transform:translateY(10px);animation:in .4s cubic-bezier(.22,1,.36,1) forwards}"
    "@keyframes in{to{opacity:1;transform:none}}"
    ".dot{animation:pulse 2.6s ease-in-out 1.4s infinite}"
    "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}"
    ".halo{transform-box:fill-box;transform-origin:center;opacity:0;"
    "animation:halo 2.6s ease-out 1.4s infinite}"
    "@keyframes halo{0%{opacity:.7;transform:scale(1)}70%,100%{opacity:0;transform:scale(2.4)}}"
    ".glowc{animation:gp 5s ease-in-out infinite}"
    "@keyframes gp{0%,100%{opacity:.55}50%{opacity:1}}"
    ".shine{animation:sweep 6s cubic-bezier(.4,0,.2,1) 1.2s infinite}"
    "@keyframes sweep{0%{transform:translateX(0)}26%{transform:translateX(640px)}"
    "100%{transform:translateX(640px)}}"
    ".arr{animation:arr 1.8s ease-in-out infinite}"
    "@keyframes arr{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}"
    ".pt{transform-box:fill-box;transform-origin:center;animation:pt 5s ease-in-out infinite alternate}"
    "@keyframes pt{to{transform:translateY(-8px)}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}"
    ".cat,.ttl,.bdg,.ln,.chp{opacity:1!important;transform:none!important}"
    ".halo,.shine{opacity:0!important}}"
    "</style>"
)


def defs(accent):
    return (
        "<defs>"
        f'<clipPath id="cp"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13"/></clipPath>'
        + flow_gradient("gb", [accent, P["border"], accent], dur=6)
        + f'<radialGradient id="rg" gradientUnits="userSpaceOnUse" cx="60" cy="0" r="250">'
        f'<stop offset="0" stop-color="{accent}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="#fff" stop-opacity="0.07"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        "</linearGradient>"
        + glow_filter("gw", 2.5)
        + "</defs>"
    )


SHINE = (
    '<g clip-path="url(#cp)"><g transform="rotate(16)">'
    '<rect class="shine" x="-150" y="-120" width="90" height="440" fill="url(#sh)"/>'
    "</g></g>"
)


def cat_pill(cat, accent):
    label = CAT_LABEL[cat]
    tw = round(len(label) * 6.0) + 20
    return (
        f'<rect x="{PAD}" y="13" width="{tw}" height="20" rx="10" '
        f'fill="{blend(accent, 0.13, P["glass"])}"/>'
        f'<text x="{PAD + tw / 2}" y="26.5" text-anchor="middle" font-size="9.5" '
        f'font-weight="700" letter-spacing="1" fill="{accent}">{html.escape(label)}</text>'
    )


def particles(accent):
    pts = [(392, 62, 0), (376, 96, 1.6), (398, 128, 0.8)]
    return "".join(
        f'<circle class="pt" style="animation-delay:{d}s" cx="{x}" cy="{y}" r="2" '
        f'fill="{accent}" opacity=".35"/>'
        for x, y, d in pts
    )


def card(slug, name, cat, publico, desc, stack):
    accent = ACCENTS[cat]
    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="{FONT}" role="img" aria-label="{html.escape(name)}">',
        STYLE,
        defs(accent),
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="{P["glass"]}"/>',
        f'<g clip-path="url(#cp)"><rect class="glowc" x="0" y="0" width="{W}" height="{H}" '
        f'fill="url(#rg)"/></g>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none" '
        f'stroke="url(#gb)" stroke-width="1.5"/>',
        cat_pill(cat, accent),
        f'<g class="bdg">{badge(publico)}</g>',
        f'<text class="ttl" x="{PAD}" y="60" font-size="18" font-weight="700" '
        f'fill="{P["title"]}">{html.escape(name)}</text>',
        particles(accent),
    ]
    for i, line in enumerate(wrap(desc)):
        parts.append(
            f'<text class="ln" style="animation-delay:{0.55 + i * 0.12:.2f}s" '
            f'x="{PAD}" y="{84 + i * 17}" font-size="12" '
            f'fill="{P["body"]}">{html.escape(line)}</text>'
        )
    x = PAD
    for j, s in enumerate(stack):
        c, tw = chip(x, H - PAD - 22, s, accent)
        parts.append(f'<g class="chp" style="animation-delay:{0.85 + j * 0.1:.2f}s">{c}</g>')
        x += tw + 8
    if publico:
        parts.append(
            f'<g class="chp" style="animation-delay:1.1s"><text class="arr" x="{W - PAD - 14}" '
            f'y="{H - PAD - 6}" font-size="14" font-weight="700" fill="{accent}" '
            f'filter="url(#gw)">❯</text></g>'
        )
    parts.append(SHINE)
    parts.append("</svg>")
    svg = "".join(parts)
    with open(os.path.join(OUT, f"{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    return slug


os.makedirs(OUT, exist_ok=True)
for p in PROJECTS:
    card(*p)
print(f"{len(PROJECTS)} tarjetas generadas en {OUT}")
