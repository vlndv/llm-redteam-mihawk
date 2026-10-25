import json
import sys

with open(sys.argv[1]) as f:
    results = json.load(f)

for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"--- [{status}] {r['id']} ---")
    print("ATTACK:", r["prompt"])
    print("REPLY: ", r["reply"])
    print()