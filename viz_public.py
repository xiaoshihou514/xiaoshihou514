import json
from config import SKIP_LANGS
from utils import generate_svg

# Load data
with open("stats_public.json") as f:
    stats = json.load(f)  # output of tokei -o json

with open("colors.json") as f:
    colors = json.load(f)

# Set languages to skip
skip_langs = SKIP_LANGS.union({
    "Total",
    "JavaScript",
    "CSS",
    "Perl",
    "Markdown",
    "TypeScript",
})

# Minimum LOC to display
min_lines = 100

# Compute totals and percentages
total_lines = 0
lang_stats = []

for lang, data in stats.items():
    if lang in skip_langs:
        continue

    code = data.get("code", 0)
    comments = data.get("comments", 0)
    lines = code + comments
    if lines < min_lines:
        continue  # skip small languages

    total_lines += lines
    lang_stats.append({"name": lang, "lines": lines})

# Sort descending by lines
lang_stats.sort(key=lambda x: x["lines"], reverse=True)

# Calculate percentages and assign colors
for l in lang_stats:
    l["percent"] = l["lines"] / total_lines * 100
    l["color"] = colors.get(l["name"], {}).get("color", "#000000")

# Generate SVG
generate_svg(lang_stats, "public.svg", total_lines, "Public Code Lines by Language")

print(
    f"Total lines (excluding skipped languages and small langs < {min_lines} LOC): {total_lines}"
)
