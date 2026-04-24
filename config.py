import os
from pathlib import Path

# -------------- Config --------------
USERNAME = os.environ.get("USERNAME", "")
GIT_USERNAME = os.environ.get("GIT_USERNAME", "")
REPOS_DIR = Path("temp")
OUTPUT_DIR = Path("recent")
OUTPUT_DIR.mkdir(exist_ok=True)

# Define agents to detect
AGENTS = {
    "copilot": "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
    "trae": "Co-authored-by: TRAE <trae@example.com>"
}

# Create output directories for each agent
for agent in AGENTS:
    agent_output_dir = Path(f"recent_{agent}")
    agent_output_dir.mkdir(exist_ok=True)

# Languages to skip in visualization
SKIP_LANGS = {
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

# Agent colors for visualization
AGENT_COLORS = {
    "copilot": "#FF6B6B",  # Red
    "trae": "#4ECDC4",  # Teal
    "default": "#45B7D1"  # Blue
}
