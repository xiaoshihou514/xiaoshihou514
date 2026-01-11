import json
import glob
import hashlib

# ---------- helpers ----------

def fmt_lines(n: int) -> str:
    """Format LOC as 1k, 1.2k, etc."""
    if n < 1000:
        return str(n)
    v = n / 1000
    return f"{int(v)}k" if v.is_integer() else f"{v:.1f}k"

def trunc(s: str, n=12) -> str:
    """Truncate name to max n chars."""
    return s if len(s) <= n else s[: n - 1] + "…"

def color_for(name: str) -> str:
    """Deterministic color per language."""
    h = hashlib.md5(name.encode()).hexdigest()
    return f"#{h[:6]}"

# ---------- load data ----------

lang_totals = {}

for path in glob.glob("recent/*.json"):
    with open(path) as f:
        data = json.load(f)
        per_lang = data.get("loc_changed_per_language", {})
        for lang, loc in per_lang.items():
            if loc <= 0:
                continue
            lang_totals[lang] = lang_totals.get(lang, 0) + loc

if not lang_totals:
    raise SystemExit("No recent data found")

# Convert to list of dicts
entries = []
for lang, lines in lang_totals.items():
    entries.append({
        "name": lang,
        "lines": lines,
        "color": color_for(lang)
    })

# Sort descending by lines
entries.sort(key=lambda x: x["lines"], reverse=True)
total_lines = sum(e["lines"] for e in entries)

for e in entries:
    e["percent"] = e["lines"] / total_lines * 100

# ---------- SVG layout ----------

width = 800
bar_height = 40
stats_gap = 25
row_height = 20
cols = 3

height = (
    40
    + bar_height
    + stats_gap
    + ((len(entries) + cols - 1) // cols) * row_height
    + 20
)

svg = [
    f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
    '<style>text{font-family:sans-serif}</style>',
]

# ---------- stacked bar ----------

x = 10
y = 30

for e in entries:
    w = width * e["percent"] / 100
    svg.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{bar_height}" fill="{e["color"]}"/>'
    )
    x += w

# ---------- stats text ----------

y_text = y + bar_height + stats_gap
x_start = 10
x_gap = width // cols

for i, e in enumerate(entries):
    col = i % cols
    row = i // cols

    x = x_start + col * x_gap
    y_pos = y_text + row * row_height

    name = trunc(e["name"])
    lines = fmt_lines(e["lines"])

    # color dot
    svg.append(
        f'<circle cx="{x}" cy="{y_pos - 4}" r="5" fill="{e["color"]}"/>'
    )

    svg.append(
        f'<text x="{x + 10}" y="{y_pos}" font-size="13" fill="#fff">'
        f'{name} ({lines}, {e["percent"]:.1f}%)'
        f'</text>'
    )

svg.append("</svg>")

# ---------- write ----------

with open("recent.svg", "w") as f:
    f.write("\n".join(svg))

print(f"Recent LOC total (all languages): {total_lines}")
print("SVG generated: recent.svg")
