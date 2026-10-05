import urllib.request
import json
import re

URL = "https://api.github.com/users/HafizRP/repos?sort=updated&per_page=12"
headers = {"User-Agent": "GitHub-Action-Script"}

req = urllib.request.Request(URL, headers=headers)
with urllib.request.urlopen(req) as resp:
    repos = json.load(resp)

# Exclude current profile repo, forks, and repos without clear context
filtered = []
for r in repos:
    name = r.get("name", "")
    if name.lower() in ["hafizrp", "hafizrp.github.io", "testo-new"]:
        continue
    if r.get("fork"):
        continue
    filtered.append(r)
    if len(filtered) == 5:
        break

rows = ["| Repository | Description | Primary Stack | Stars | Updates |",
        "| :--- | :--- | :--- | :---: | :---: |"]

for r in filtered:
    name = r.get("name")
    url = r.get("html_url")
    desc = r.get("description") or "Personal project repository"
    # Clean markdown pipe
    desc = desc.replace("|", "/")
    lang = r.get("language") or "Code"
    stars = r.get("stargazers_count", 0)
    updated = r.get("pushed_at", "")[:10]
    rows.append(f"| [**{name}**]({url}) | {desc} | `{lang}` | ⭐ {stars} | `{updated}` |")

table_content = "\n".join(rows)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

pattern = r"<!-- REPOS-START -->[\s\S]*?<!-- REPOS-END -->"
replacement = f"<!-- REPOS-START -->\n{table_content}\n<!-- REPOS-END -->"

updated_readme = re.sub(pattern, replacement, readme)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_readme)

print("README.md successfully updated with live API repositories.")
