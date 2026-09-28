import re
from typing import Dict, Any, List


def test_regex(pattern: str, text: str) -> Dict[str, Any]:
    print("\n🔬 \033[1;36mAERO REGEX TESTER & PARSER\033[0m")
    print("═" * 58)
    print(f" • Pattern: \033[1;33m{pattern}\033[0m")
    print(f" • Target:  {text}")
    print("─" * 58)

    try:
        compiled = re.compile(pattern)
    except re.error as e:
        print(f"❌ \033[1;31mRegex Syntax Error:\033[0m {e}")
        print("═" * 58 + "\n")
        return {"valid": False, "error": str(e), "matches": []}

    matches = []
    for m in compiled.finditer(text):
        match_info = {
            "span": m.span(),
            "match": m.group(0),
            "groups": m.groups(),
            "groupdict": m.groupdict(),
        }
        matches.append(match_info)

    if not matches:
        print("❌ \033[1;33mNo matches found.\033[0m")
    else:
        print(f"\033[1;32m✔ Found {len(matches)} match(es):\033[0m")
        for idx, match in enumerate(matches, 1):
            print(f" Match #{idx}: '\033[1;32m{match['match']}\033[0m' at span {match['span']}")
            if match["groups"]:
                print(f"   - Groups:    {match['groups']}")
            if match["groupdict"]:
                print(f"   - Named:     {match['groupdict']}")

    print("═" * 58 + "\n")
    return {"valid": True, "error": None, "matches": matches}
