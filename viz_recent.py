#!/usr/bin/env python3
import json
import glob
from config import SKIP_LANGS
from utils import generate_svg

# ---------- load colors ----------

with open("colors.json") as f:
    colors = json.load(f)

# ---------- load recent data ----------

skip_langs = SKIP_LANGS

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
total_lines = sum(lang_totals.values())
lang_stats = []

for lang, lines in lang_totals.items():
    lang_stats.append(
        {
            "name": lang,
            "lines": lines,
            "percent": lines / total_lines * 100,
            "color": colors.get(lang, {}).get("color", "#000000"),
        }
    )

# Sort descending by lines
lang_stats.sort(key=lambda x: x["lines"], reverse=True)

# Generate SVG
generate_svg(lang_stats, "recent.svg", total_lines, "Recent Code Lines by Language")
