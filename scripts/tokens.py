#!/usr/bin/env python3
"""Design tokens compartidos para todos los SVG del README de TenebrisOne.

Paleta «Aurora Nocturna»: fondo espacial profundo con acentos neón.
Única fuente de verdad: colores, tipografía, radios y motion tokens.
"""

PALETTE = {
    # superficies
    "bg": "#0d1226",        # fondo de paneles
    "bg_deep": "#0a0e1f",   # fondo héroe / footer
    "surface": "#161c38",   # tarjetas internas / chips
    "glass": "#10162e",     # paneles translúcidos
    "border": "#272f55",    # bordes
    # texto
    "title": "#e6ebff",
    "body": "#a3aed6",
    "muted": "#5d6791",
    # acentos neón
    "cyan": "#5ee7ff",
    "violet": "#9d7bff",
    "pink": "#ff6ac2",
    "green": "#57e6a8",
    "amber": "#ffc24b",
    "orange": "#ff9e64",
    "red": "#ff7a93",
}

# trío principal para degradados
TRIO = [PALETTE["cyan"], PALETTE["violet"], PALETTE["pink"]]

FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif"
MONO = "ui-monospace,'Cascadia Code','Courier New',monospace"

# motion tokens
EASE = "cubic-bezier(.22,1,.36,1)"      # entradas
EASE_SOFT = "ease-in-out"                # bucles ambientales
DUR_IN = ".6s"                           # entrada
DUR_AMBIENT = 8                          # segundos, ciclos de color

RADIUS = {"panel": 18, "card": 14, "chip": 8, "pill": 999}

REDUCED = (
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}"
    ".fu,.in{opacity:1!important;transform:none!important}}"
)


def flow_gradient(gid, colors=None, dur=DUR_AMBIENT, x2="1", y2="0"):
    """Degradado lineal cuyos stops rotan de color en bucle (SMIL)."""
    colors = colors or TRIO
    n = len(colors)
    stops = []
    for i, c in enumerate(colors):
        cycle = ";".join(colors[i:] + colors[:i] + [c])
        offset = round(i / (n - 1) * 100) if n > 1 else 0
        stops.append(
            f'<stop offset="{offset}%" stop-color="{c}">'
            f'<animate attributeName="stop-color" values="{cycle}" '
            f'dur="{dur}s" repeatCount="indefinite"/></stop>'
        )
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
        + "".join(stops)
        + "</linearGradient>"
    )


def glow_filter(fid="glow", dev=5):
    """Filtro de resplandor: blur + gráfica original encima."""
    return (
        f'<filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%">'
        f'<feGaussianBlur stdDeviation="{dev}" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f"</filter>"
    )


def blur_filter(fid="soft", dev=40):
    return (
        f'<filter id="{fid}" x="-80%" y="-80%" width="260%" height="260%">'
        f'<feGaussianBlur stdDeviation="{dev}"/></filter>'
    )


def blend(fg, alpha, bg=None):
    """Mezcla un color con el fondo para simular transparencia sólida."""
    bg = bg or PALETTE["bg"]
    f = [int(fg[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(
        f"{round(alpha * fc + (1 - alpha) * bc):02x}" for fc, bc in zip(f, b)
    )


def stars(coords, cls="tw", color=None, rmin=1.0, rmax=1.8):
    """Campo de estrellas parpadeantes. coords: [(x, y, fase)]."""
    color = color or PALETTE["title"]
    out = []
    for i, (x, y, phase) in enumerate(coords):
        r = rmin + (rmax - rmin) * ((i * 7) % 5) / 4
        out.append(
            f'<circle class="{cls}" style="animation-delay:{phase}s" '
            f'cx="{x}" cy="{y}" r="{r:.1f}" fill="{color}"/>'
        )
    return "".join(out)


TW_STYLE = (
    ".tw{animation:tw 3.4s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:.1}50%{opacity:.9}}"
)
