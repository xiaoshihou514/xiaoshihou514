import os
import subprocess
import json
import datetime
from pathlib import Path

# -------------- Config --------------
USERNAME = os.environ.get("USERNAME", "")
GIT_USERNAME = os.environ.get("GIT_USERNAME", "")
REPOS_DIR = Path("temp")
OUTPUT_DIR = Path("recent")
OUTPUT_DIR.mkdir(exist_ok=True)

# Optional: languages mapping for file extension -> language
with open("languages.json") as f:
    LANGUAGES_JSON = json.load(f)

EXT_LANG = {}
for lang_key, data in LANGUAGES_JSON["languages"].items():
    for ext in data.get("extensions", []):
        EXT_LANG[ext.lower()] = data.get(
            "name", lang_key
        )  # Use 'name' if present, otherwise key

# Time window
since_dt = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=30)
since_str = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# -------------- Helpers --------------
def get_language(filename: str):
    _, ext = os.path.splitext(filename)
    return EXT_LANG.get(ext[1:])

def git_commits(repo_path: Path):
    """Return list of commit SHAs by USERNAME in last 30 days"""
    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        f"--since={since_str}",
        f"--author={USERNAME}",
        "--pretty=format:%H",
    ]
    handle = subprocess.run(cmd, capture_output=True, text=True)
    if handle.returncode != 0:
        print(f"Git log failed for {repo_path}")
        return []
    result = handle.stdout.strip().splitlines()
    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        f"--since={since_str}",
        f"--author={GIT_USERNAME}",
        "--pretty=format:%H",
    ]
    handle = subprocess.run(cmd, capture_output=True, text=True)
    if handle.returncode != 0:
        print(f"Git log failed for {repo_path}")
        return []
    return result + handle.stdout.strip().splitlines()


def git_commit_stats(repo_path: Path, sha: str):
    """Return list of (additions, deletions, filename) for a commit"""
    cmd = ["git", "-C", str(repo_path), "show", "--numstat", "--format=", sha]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Git show failed for {sha} in {repo_path}")
        return []

    stats = []
    for line in result.stdout.splitlines():
        parts = line.strip().split("\t")
        if len(parts) != 3:
            continue
        added, deleted, filename = parts
        try:
            added = int(added)
            deleted = int(deleted)
        except ValueError:
            continue
        stats.append((added, deleted, filename))
    return stats


# -------------- Main --------------
for repo_path in REPOS_DIR.iterdir():
    if not repo_path.is_dir():
        continue
    repo_name = repo_path.name
    print(f"Processing...")

    commits = git_commits(repo_path)
    if not commits:
        continue

    # Aggregate LOC per language
    lang_totals = {}
    for sha in commits:
        for added, deleted, filename in git_commit_stats(repo_path, sha):
            lang = get_language(filename)
            if lang:
                lang_totals[lang] = lang_totals.get(lang, 0) + added + deleted

    # Skip repos with no LOC changes
    if not lang_totals:
        continue

    # Write per-repo JSON
    output_file = OUTPUT_DIR / f"{USERNAME}_{repo_name}.json"
    with open(output_file, "w") as f:
        json.dump(
            {
                "repo": repo_name,
                "since": since_str,
                "loc_changed_per_language": lang_totals,
            },
            f,
            indent=2,
        )

print("Done. Data written to recent/*.json")
