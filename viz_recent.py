#!/usr/bin/env python3
import json
import glob

# ---------- helpers ----------


def fmt_lines(n):
    """Format LOC as 1k, 1.2k, etc."""
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def trunc(s, n=12):
    """Truncate name to max n chars."""
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------- load colors ----------

with open("colors.json") as f:
    colors = json.load(f)

# ---------- load recent data ----------

skip_langs = {
    "JSON",
    "HTML",
    "SVG",
    "YAML",
    "TOML",
    "Plain Text",
    "XML",
    "MDX",
    "INI",
    "TSX",
    "ReStructuredText",
}

lang_totals = {}

for path in glob.glob("recent/*.json"):
    with open(path) as f:
        data = json.load(f)
        per_lang = data.get("loc_changed_per_language", {})
        for lang, loc in per_lang.items():
            if lang in skip_langs:
                continue
            lang_totals[lang] = lang_totals.get(lang, 0) + loc

if not lang_totals:
    raise SystemExit("No recent data found")

# Convert to list of dicts
lang_stats = []
total_lines = sum(lang_totals.values())

for lang, lines in lang_totals.items():
    lang_stats.append(
        {
            "name": lang,
            "lines": lines,
            "percent": lines / total_lines * 100,
            "color": colors.get(lang, {}).get("color", "#888888"),
        }
    )

# Sort descending by lines
lang_stats.sort(key=lambda x: x["lines"], reverse=True)

# ---------- SVG setup ----------

width = 800
bar_height = 50
gap = 30
stats_gap = 30
circle_radius = 6
text_line_height = 20
height = bar_height + gap + ((len(lang_stats) + 2) // 3) * text_line_height + 50

svg_lines = [
    f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
]

# Draw horizontal stacked bar
x = 10
y = 40
for lang in lang_stats:
    bar_width = width * lang["percent"] / 100
    svg_lines.append(
        f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{lang["color"]}"/>'
    )
    x += bar_width

# Draw language stats below (3 per line) with colored circle
y_stats = y + bar_height + stats_gap
count = 0
x_text = 10
for lang in lang_stats:
    # circle
    svg_lines.append(
        f'<circle cx="{x_text + circle_radius}" cy="{y_stats - 4}" r="{circle_radius}" fill="{lang["color"]}" />'
    )
    # text
    name = trunc(lang["name"])
    lines_str = fmt_lines(lang["lines"])
    text = f"{name} ({lines_str} lines, {lang['percent']:.1f}%)"
    svg_lines.append(
        f'<text x="{x_text + 2 * circle_radius + 5}" y="{y_stats}" font-size="15" font-family="sans-serif" fill="#FFF">{text}</text>'
    )

    count += 1
    if count % 3 == 0:
        y_stats += text_line_height
        x_text = 10
    else:
        x_text += 250

svg_lines.append("</svg>")

# Write SVG
with open("recent.svg", "w") as f:
    f.write("\n".join(svg_lines))

print(
    f"Recent LOC total (excluding skipped languages): {total_lines}"
)
print("SVG generated: recent.svg")
