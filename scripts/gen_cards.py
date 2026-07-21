#!/usr/bin/env python3
"""Genera tarjetas SVG uniformes para los proyectos del README de TenebrisOne.

Design tokens (coherentes con el tema tokyonight de github-readme-stats):
  bg #1a1b27 · border #2f334d · title #c0caf5 · body #a9b1d6
  accents: plataformas #7aa2f7 · integraciones #bb9af7 · herramientas #7dcfff
  semantic: público #9ece6a · privado #e0af68
Grid 8pt, radius 8px (estilo modern), tipografía system-ui.
"""
import html
import os
import re

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "cards")

TOKENS = {
    "bg": "#1a1b27",
    "border": "#2f334d",
    "title": "#c0caf5",
    "body": "#a9b1d6",
    "chip_bg": "#24283b",
    "public": "#9ece6a",
    "private": "#e0af68",
    "font": "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif",
}

ACCENTS = {
    "plataformas": "#7aa2f7",
    "integraciones": "#bb9af7",
    "herramientas": "#7dcfff",
}

CAT_LABEL = {
    "plataformas": "PLATAFORMA WEB",
    "integraciones": "INTEGRACIÓN · AUTOMATIZACIÓN",
    "herramientas": "APP · HERRAMIENTA",
}

W, H = 420, 180
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
    tw = round(len(label) * 6.2) + 16
    return (
        f'<rect x="{x}" y="{y}" width="{tw}" height="22" rx="6" fill="{TOKENS["chip_bg"]}"/>'
        f'<text x="{x + tw / 2}" y="{y + 15}" text-anchor="middle" font-size="10.5" '
        f'font-weight="600" fill="{accent}">{html.escape(label)}</text>',
        tw,
    )


def blend(fg, alpha, bg="#1a1b27"):
    f = [int(fg[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(alpha * fc + (1 - alpha) * bc):02x}" for fc, bc in zip(f, b))


def badge(publico):
    label = "PÚBLICO" if publico else "PRIVADO"
    color = TOKENS["public"] if publico else TOKENS["private"]
    tw = round(len(label) * 6.6) + 26
    x = W - PAD - tw
    dot = (
        f'<circle class="halo" cx="{x + 11}" cy="23" r="3" fill="none" '
        f'stroke="{color}" stroke-width="1.5"/>'
        f'<circle class="dot" cx="{x + 11}" cy="23" r="3" fill="{color}"/>'
    )
    return (
        f'<rect x="{x}" y="14" width="{tw}" height="18" rx="9" fill="{blend(color, 0.12)}"/>'
        f"{dot}"
        f'<text x="{x + 18}" y="27" font-size="9.5" font-weight="700" '
        f'letter-spacing="0.5" fill="{color}">{label}</text>'
    )


STYLE = (
    "<style>"
    ".bar{transform:scaleY(0);transform-box:fill-box;transform-origin:center;"
    "animation:grow .55s cubic-bezier(.22,1,.36,1) .1s forwards,"
    "bpulse 3.4s ease-in-out 2.2s infinite}"
    "@keyframes grow{to{transform:scaleY(1)}}"
    "@keyframes bpulse{0%,100%{opacity:1}50%{opacity:.5}}"
    ".cat{opacity:0;transform:translateX(-10px);animation:in .5s ease .3s forwards}"
    ".ttl{opacity:0;transform:translateY(8px);animation:in .5s ease .4s forwards}"
    ".bdg{opacity:0;animation:in .5s ease .55s forwards}"
    ".ln{opacity:0;transform:translateY(6px);animation:in .45s ease forwards}"
    ".chp{opacity:0;transform:translateY(10px);animation:in .4s cubic-bezier(.22,1,.36,1) forwards}"
    "@keyframes in{to{opacity:1;transform:none}}"
    ".dot{animation:pulse 2.6s ease-in-out 1.4s infinite}"
    "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}"
    ".halo{opacity:0;animation:halo 2.6s ease-out 1.4s infinite}"
    "@keyframes halo{0%{opacity:.7;transform:scale(1)}70%,100%{opacity:0;transform:scale(2.4)}}"
    ".halo{transform-box:fill-box;transform-origin:center}"
    ".shine{animation:sweep 6s cubic-bezier(.4,0,.2,1) 1.2s infinite}"
    "@keyframes sweep{0%{transform:translateX(0)}26%{transform:translateX(640px)}100%{transform:translateX(640px)}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}"
    ".cat,.ttl,.bdg,.ln,.chp{opacity:1!important;transform:none!important}"
    ".bar{transform:none!important}.halo,.shine{opacity:0!important}}"
    "</style>"
)

DEFS = (
    '<defs>'
    f'<clipPath id="cp"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8"/></clipPath>'
    '<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
    '<stop offset="0.5" stop-color="#fff" stop-opacity="0.08"/>'
    '<stop offset="1" stop-color="#fff" stop-opacity="0"/>'
    '</linearGradient>'
    '</defs>'
)

SHINE = (
    '<g clip-path="url(#cp)"><g transform="rotate(16)">'
    '<rect class="shine" x="-150" y="-120" width="90" height="420" fill="url(#sh)"/>'
    '</g></g>'
)


def card(slug, name, cat, publico, desc, stack):
    accent = ACCENTS[cat]
    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="{TOKENS["font"]}" role="img" aria-label="{html.escape(name)}">',
        STYLE,
        DEFS,
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" '
        f'fill="{TOKENS["bg"]}" stroke="{TOKENS["border"]}"/>',
        f'<rect class="bar" x="0" y="16" width="3.5" height="{H - 32}" rx="1.75" fill="{accent}"/>',
        f'<text class="cat" x="{PAD}" y="28" font-size="10" font-weight="700" letter-spacing="1.2" '
        f'fill="{accent}">{html.escape(CAT_LABEL[cat])}</text>',
        f'<g class="bdg">{badge(publico)}</g>',
        f'<text class="ttl" x="{PAD}" y="56" font-size="17" font-weight="700" '
        f'fill="{TOKENS["title"]}">{html.escape(name)}</text>',
    ]
    for i, line in enumerate(wrap(desc)):
        parts.append(
            f'<text class="ln" style="animation-delay:{0.55 + i * 0.12:.2f}s" '
            f'x="{PAD}" y="{80 + i * 17}" font-size="12" '
            f'fill="{TOKENS["body"]}">{html.escape(line)}</text>'
        )
    x = PAD
    for j, s in enumerate(stack):
        c, tw = chip(x, H - PAD - 22, s, accent)
        parts.append(f'<g class="chp" style="animation-delay:{0.85 + j * 0.1:.2f}s">{c}</g>')
        x += tw + 8
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
