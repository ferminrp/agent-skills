"""xchart v2: gráficos estáticos para X/Twitter (reglas en references/charts.md).

    from xchart import figure, finish, label, stat, phone_sheet
    fig, ax = figure()                       # light (default): suelo gris claro + panel blanco
    ...plot con INK (grises) y UN acento...
    stat(fig, "+186 pb", "ley local vs NY")  # el único número grande
    finish(fig, title=..., subtitle=..., source=..., out="x.png")
    phone_sheet(["a.png", "b.png"], "phone-preview.png", width=390)
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

import os
HANDLE = os.environ.get("FINANZAS_AR_HANDLE", "")
DPI = 200
SIZES = {"landscape": (8.0, 4.5), "vertical": (5.4, 6.75), "square": (6.0, 6.0)}  # 1600x900, 1080x1350, 1200x1200

# Una familia neutra (5 tintas) + UN acento. Profundidad en oscuro = superficie más clara, no sombra.
THEMES = {
    "dark": dict(ground="#09090B", surface="#131519", raised="#1C1F25",
                 ink1="#2A2E36", ink2="#3D424C", ink3="#6B7280", ink4="#9CA3AF", ink5="#F4F4F5",
                 accent="#4EA8FF", accent_soft="#4EA8FF33"),
    # Recomendado (default): grises fríos sobre blanco, un acento azul. Contraste texto >= 4.5:1.
    "light": dict(ground="#F3F4F6", surface="#FFFFFF", raised="#F5F6F8",
                  ink1="#E8EAED", ink2="#C9CDD3", ink3="#6B7280", ink4="#4B5563", ink5="#111827",
                  accent="#1663D6", accent_soft="#1663D61F"),
}
T = THEMES["light"]
GUTTER = 0.035  # un solo gutter (fracción del ancho), usado en todos los bordes


# Carpetas donde buscar Pretendard (.otf/.ttf estáticos): env FINANZAS_AR_FONT_DIR primero
# (admite varias separadas por os.pathsep), después rutas conocidas. Si no hay, DejaVu Sans
# (viene con matplotlib).
FONT_DIRS = [d for d in os.environ.get("FINANZAS_AR_FONT_DIR", "").split(os.pathsep) if d] + [
    str(Path.home() / ".finanzas-ar" / "fonts"),
    "/usr/share/fonts/truetype/sand-box/custom/Pretendard",
]


def _font():
    for d in FONT_DIRS:
        p = Path(d).expanduser()
        if not p.is_dir():
            continue
        for f in [*p.glob("*.otf"), *p.glob("*.ttf")]:
            try: fm.fontManager.addfont(str(f))
            except Exception: pass
    return "Pretendard" if "Pretendard" in {f.name for f in fm.fontManager.ttflist} else "DejaVu Sans"
FONT = _font()


def figure(theme="light", size="landscape", plot_box=None):
    """Devuelve fig, ax. plot_box=[x0,y0,w,h] en fracciones de la figura (dentro del panel)."""
    global T
    T = THEMES[theme]
    plt.rcParams.update({
        "font.family": FONT, "font.size": 11,
        "figure.facecolor": T["ground"], "savefig.facecolor": T["ground"],
        "axes.facecolor": "none", "text.color": T["ink5"], "axes.labelcolor": T["ink3"],
        "xtick.color": T["ink3"], "ytick.color": T["ink3"],
        "xtick.labelsize": 12.5, "ytick.labelsize": 12.5, "axes.labelsize": 12,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.spines.bottom": False, "axes.grid": True, "axes.grid.axis": "y",
        "grid.color": T["ink1"], "grid.linewidth": 0.8, "axes.axisbelow": True,
        "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 7, "ytick.major.pad": 7,
    })
    fig = plt.figure(figsize=SIZES[size], dpi=DPI)
    w, h = SIZES[size]
    g = GUTTER; gy = g * w / h
    # panel ("poster"): un paso de superficie sobre el suelo, mismo gutter en los 4 lados (deja lugar al footer)
    fig._panel = (g, gy * 2.2, 1 - 2 * g, 1 - gy * 3.2)
    x0, y0, pw, ph = fig._panel
    fig.patches.append(FancyBboxPatch((x0, y0), pw, ph, boxstyle="round,pad=0,rounding_size=0.018",
                                      transform=fig.transFigure, fc=T["surface"], ec="none", zorder=-10))
    ax = fig.add_axes(plot_box or [x0 + 0.06, y0 + 0.10, pw - 0.10, ph * 0.62])
    return fig, ax


def finish(fig, title, subtitle="", source="", out="chart.png", handle=HANDLE):
    x0, y0, pw, ph = fig._panel
    pad = 0.03
    top = y0 + ph
    fig.text(x0 + pad, top - 0.055, title, fontsize=18, fontweight="bold", color=T["ink5"], va="top")
    if subtitle:
        fig.text(x0 + pad, top - 0.145, subtitle, fontsize=12, color=T["ink4"], va="top")
    yf = y0 / 2
    fig.text(x0, yf, source, fontsize=9.5, color=T["ink3"], va="center")
    fig.text(x0 + pw, yf, handle, fontsize=10, fontweight="bold", color=T["ink4"], va="center", ha="right")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def stat(fig, value, caption, x=None, y=None, ha="right"):
    """El único número grande, en el acento, arriba a la derecha del panel."""
    x0, y0, pw, ph = fig._panel
    x = x if x is not None else x0 + pw - 0.03
    y = y if y is not None else y0 + ph - 0.045
    fig.text(x, y, value, fontsize=30, fontweight="bold", color=T["accent"], va="top", ha=ha)
    fig.text(x, y - 0.115, caption, fontsize=11, color=T["ink4"], va="top", ha=ha)


def label(ax, x, y, text, color=None, dx=6, dy=0, **kw):
    """Etiqueta directa (en vez de leyenda)."""
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                color=color or T["ink4"], fontsize=kw.pop("fontsize", 11.5),
                va=kw.pop("va", "center"), **kw)


def phone_sheet(paths, out, width=390, gap=24, bg="#000000"):
    """Contact sheet a ancho de celular (cada imagen escalada a `width` px)."""
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in paths]
    ims = [im.resize((width, round(im.height * width / im.width)), Image.LANCZOS) for im in ims]
    H = sum(i.height for i in ims) + gap * (len(ims) + 1)
    sheet = Image.new("RGB", (width + 2 * gap, H), bg)
    yy = gap
    for im in ims:
        sheet.paste(im, (gap, yy)); yy += im.height + gap
    sheet.save(out)
    return out
