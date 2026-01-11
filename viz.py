import json

# Load data
with open("stats.json") as f:
    stats = json.load(f)  # output of tokei -o json

with open("colors.json") as f:
    colors = json.load(f)

# Set languages to skip
skip_langs = {"Total", "JSON", "HTML", "Markdown"}

# Compute totals and percentages
total_lines = 0
lang_stats = []

for lang, data in stats.items():
    if lang in skip_langs:
        continue

    code = data.get("code", 0)
    comments = data.get("comments", 0)
    lines = code + comments
    if lines == 0:
        continue

    total_lines += lines
    lang_stats.append({"name": lang, "lines": lines})

# Sort descending by lines
lang_stats.sort(key=lambda x: x["lines"], reverse=True)

# Calculate percentages and assign colors
for l in lang_stats:
    l["percent"] = l["lines"] / total_lines * 100
    l["color"] = colors.get(l["name"], {}).get("color", "#888888")

# SVG setup
width = 800
bar_height = 50
gap = 30
stats_gap = 20
height = bar_height + gap + ((len(lang_stats) + 2) // 3) * 20 + 50  # +50 for top padding

# Start SVG
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
    x += bar_width  # move to next segment

# Draw language stats below (3 per line)
y_stats = y + bar_height + stats_gap
count = 0
x_text = 10
for lang in lang_stats:
    text = f'{lang["name"]} ({lang["lines"]} lines, {lang["percent"]:.1f}%)'
    svg_lines.append(
        f'<text x="{x_text}" y="{y_stats}" font-size="15" font-family="sans-serif" fill="#000">{text}</text>'
    )
    count += 1
    if count % 3 == 0:
        y_stats += 20  # next line
        x_text = 10
    else:
        x_text += 250  # adjust spacing between columns

svg_lines.append("</svg>")

# Write SVG
with open("all.svg", "w") as f:
    f.write("\n".join(svg_lines))

print(f"Total lines (excluding skipped languages): {total_lines}")
print("SVG generated: tokei_horizontal.svg")
