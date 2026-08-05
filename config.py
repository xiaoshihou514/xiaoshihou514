import os
from pathlib import Path

# -------------- Config --------------
USERNAME = os.environ.get("USERNAME", "")
GIT_USERNAME = os.environ.get("GIT_USERNAME", "")
REPOS_DIR = Path("temp")
OUTPUT_DIR = Path("recent")
OUTPUT_DIR.mkdir(exist_ok=True)

# Languages to skip in visualization
SKIP_LANGS = {
    "JSON",
    "HTML",
    "SVG",
    "YAML",
    "TOML",
    "Plain Text",
    "Markdown",
    "XML",
    "MDX",
    "INI",
    "TSX",
    "ReStructuredText",
}
