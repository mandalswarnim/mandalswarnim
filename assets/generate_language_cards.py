import math

# Shared, deliberately distinct palette so a language keeps the same color in both cards.
COLORS = {
    "TypeScript":       "#3178C6",  # blue
    "Jupyter Notebook": "#DA5B0B",  # orange
    "Python":           "#8CC84B",  # green
    "JavaScript":       "#F1E05A",  # yellow
}

W, H = 400, 200
CX, CY, RO, RI = 318, 112, 58, 34

def arcs(data, total):
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
                   f'fill="{COLORS[name]}" stroke="#0d1117" stroke-width="2" />')
        ang = a1
    return out

def card(path, title, subtitle, data, total, center_label):
    legend = []
    for i, (name, v) in enumerate(data):
        y = 66 + i * 27
        pct = round(v / total * 100)
        legend.append(
            f'  <rect x="28" y="{y}" width="11" height="11" rx="2" fill="{COLORS[name]}" />'
            f'<text x="47" y="{y + 10}" class="label">{name}</text>'
            f'<text x="218" y="{y + 10}" class="value">{v}</text>'
            f'<text x="224" y="{y + 10}" class="pct">{pct}%</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">Donut chart of {center_label.lower()} with a distinct color per language.</desc>
  <style>
    .title {{ font: 600 17px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #58a6ff; }}
    .subtitle {{ font: 400 10.5px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #77909c; }}
    .label {{ font: 400 12.5px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #c9d1d9; }}
    .value {{ font: 600 12.5px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #c9d1d9; text-anchor: end; }}
    .pct {{ font: 400 11px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #8b949e; }}
    .center-top {{ font: 700 24px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #c9d1d9; text-anchor: middle; }}
    .center-bottom {{ font: 400 9px "Segoe UI", Ubuntu, "Helvetica Neue", Sans-Serif; fill: #8b949e; text-anchor: middle; letter-spacing: 1px; }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="#0d1117" stroke="#30363d" />
  <text x="28" y="34" class="title">{title}</text>
  <text x="28" y="50" class="subtitle">{subtitle}</text>
{chr(10).join(legend)}
  <g>
{chr(10).join(arcs(data, total))}
    <circle cx="{CX}" cy="{CY}" r="{RI - 2}" fill="#0d1117" />
    <text x="{CX}" y="{CY - 2}" class="center-top">{total}</text>
    <text x="{CX}" y="{CY + 14}" class="center-bottom">{center_label}</text>
  </g>
</svg>
'''
    open(path, "w").write(svg)

card("assets/top-languages-by-repo.svg",
     "Top Languages by Repo",
     "Primary language across 13 public repos",
     [("TypeScript", 4), ("Python", 4), ("Jupyter Notebook", 3), ("JavaScript", 2)], 13, "REPOS")

card("assets/top-languages-by-commit.svg",
     "Top Languages by Commit",
     "47 commits grouped by each repo's primary language",
     [("TypeScript", 32), ("Jupyter Notebook", 7), ("Python", 6), ("JavaScript", 2)], 47, "COMMITS")
