import json
import sys

files = sys.argv[1:]

all_results = {}
for filename in files:
    with open(filename) as f:
        all_results[filename] = json.load(f)

lines = ["# LLM Red-Team Report", ""]

# Overall scores
lines.append("## Overall")
lines.append("")
lines.append("| Model file | Resisted | Total |")
lines.append("|---|---|---|")
for filename, results in all_results.items():
    passed = sum(r["passed"] for r in results)
    lines.append(f"| {filename} | {passed} | {len(results)} |")

# Scores by category
categories = sorted({r["category"] for results in all_results.values() for r in results})
lines.append("")
lines.append("## By category")
lines.append("")
lines.append("| Category | " + " | ".join(all_results.keys()) + " |")
lines.append("|---|" + "---|" * len(all_results))
for category in categories:
    row = [category]
    for results in all_results.values():
        in_cat = [r for r in results if r["category"] == category]
        passed = sum(r["passed"] for r in in_cat)
        row.append(f"{passed}/{len(in_cat)}")
    lines.append("| " + " | ".join(row) + " |")

# Failures
lines.append("")
lines.append("## Failures")
for filename, results in all_results.items():
    lines.append("")
    lines.append(f"### {filename}")
    for r in results:
        if not r["passed"]:
            lines.append(f"- **{r['id']}** ({r['category']}): `{r['prompt']}`")

with open("REPORT.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
print("\nSaved REPORT.md")