"""Regenerates the README's SVG header and language donuts, in light and dark variants.

Counts come from the GitHub API; update the DATA blocks below and re-run:
    python3 assets/generate_cards.py
"""
import math

FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, Helvetica, Arial, sans-serif'

# Desaturated but hue-distinct, so each language stays readable in both themes.
COLORS = {
    "TypeScript":       "#4C7FBE",
    "Jupyter Notebook": "#C4703F",
    "Python":           "#7FA65C",
    "JavaScript":       "#C2A44B",
}

THEMES = {
    "dark":  dict(bg="#0d1117", border="#262c36", fg="#e6edf3", muted="#8b949e", faint="#6e7681"),
    "light": dict(bg="#ffffff", border="#d8dee4", fg="#1f2328", muted="#59636e", faint="#818b98"),
}

W, H = 400, 190
CX, CY, RO, RI = 312, 108, 56, 33


def donut(data, total, t):
    out, ang = [], 0.0
    for name, v in data:
        sweep = v / total * 360
        a0, a1 = ang, ang + sweep
        large = 1 if sweep > 180 else 0
        p = lambda r, a: (CX + r * math.cos(math.radians(a - 90)),
                          CY + r * math.sin(math.radians(a - 90)))
        x0, y0 = p(RO, a0); x1, y1 = p(RO, a1); x2, y2 = p(RI, a1); x3, y3 = p(RI, a0)
        out.append(f'    <path d="M {x0:.2f} {y0:.2f} A {RO} {RO} 0 {large} 1 {x1:.2f} {y1:.2f} '
                   f'L {x2:.2f} {y2:.2f} A {RI} {RI} 0 {large} 0 {x3:.2f} {y3:.2f} Z" '
                   f'fill="{COLORS[name]}" stroke="{t["bg"]}" stroke-width="2.5" />')
        ang = a1
    return out


def card(stem, title, subtitle, data, total, unit):
    for theme, t in THEMES.items():
        rows = []
        for i, (name, v) in enumerate(data):
            y = 62 + i * 26
            rows.append(
                f'  <circle cx="34" cy="{y + 5}" r="5" fill="{COLORS[name]}" />'
                f'<text x="50" y="{y + 9}" class="label">{name}</text>'
                f'<text x="214" y="{y + 9}" class="value">{v}</text>')
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">Donut chart of {unit.lower()} per language, one distinct color each.</desc>
  <style>
    .title {{ font: 600 15px {FONT}; fill: {t["fg"]}; }}
    .subtitle {{ font: 400 11px {FONT}; fill: {t["faint"]}; }}
    .label {{ font: 400 12.5px {FONT}; fill: {t["muted"]}; }}
    .value {{ font: 500 12.5px {FONT}; fill: {t["fg"]}; text-anchor: end; }}
    .big {{ font: 600 22px {FONT}; fill: {t["fg"]}; text-anchor: middle; }}
    .unit {{ font: 400 8.5px {FONT}; fill: {t["faint"]}; text-anchor: middle; letter-spacing: 1.2px; }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}" />
  <text x="28" y="32" class="title">{title}</text>
  <text x="28" y="48" class="subtitle">{subtitle}</text>
{chr(10).join(rows)}
  <g>
{chr(10).join(donut(data, total, t))}
    <circle cx="{CX}" cy="{CY}" r="{RI - 2}" fill="{t["bg"]}" />
    <text x="{CX}" y="{CY + 1}" class="big">{total}</text>
    <text x="{CX}" y="{CY + 15}" class="unit">{unit}</text>
  </g>
</svg>
'''
        open(f"assets/{stem}-{theme}.svg", "w").write(svg)


def header():
    for theme, t in THEMES.items():
        rule = COLORS["TypeScript"]
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="112" viewBox="0 0 840 112" role="img" aria-labelledby="t">
  <title id="t">Swarnim Mandal — AI engineer</title>
  <style>
    .name {{ font: 600 34px {FONT}; fill: {t["fg"]}; letter-spacing: -0.4px; }}
    .role {{ font: 400 15px {FONT}; fill: {t["muted"]}; }}
  </style>
  <rect width="840" height="112" fill="{t["bg"]}" />
  <rect x="40" y="30" width="3" height="52" rx="1.5" fill="{rule}" />
  <text x="62" y="58" class="name">Swarnim Mandal</text>
  <text x="64" y="82" class="role">AI engineer — end-to-end machine learning systems</text>
</svg>
'''
        open(f"assets/header-{theme}.svg", "w").write(svg)


header()

card("languages-by-repo", "Languages by repository",
     "Primary language across 13 public repos",
     [("TypeScript", 4), ("Python", 4), ("Jupyter Notebook", 3), ("JavaScript", 2)], 13, "REPOS")

card("languages-by-commit", "Languages by commit",
     "Commits grouped by each repo's primary language",
     [("TypeScript", 32), ("Jupyter Notebook", 7), ("Python", 6), ("JavaScript", 2)], 47, "COMMITS")
