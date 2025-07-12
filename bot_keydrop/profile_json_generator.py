import os
import re
import json
import sys
from typing import List, Dict

from bot_keydrop.utils.cli_sanitizer import sanitize_cli_args


def create_profiles_json(
    profiles_dir: str = "bot_keydrop/profiles",
    output_file: str = "profiles.json",
    default_proxy: str = "",
) -> List[Dict[str, str]]:
    """Generate a JSON file with profile data.

    Each profile directory should follow the pattern ``bot_<id>_<browser>``.

    Args:
        profiles_dir: Directory containing profile folders.
        output_file: Path to save the generated JSON.
        default_proxy: Proxy value to assign to profiles (optional).

    Returns:
        List with the profile dictionaries generated.
    """
    profiles = []
    pattern = re.compile(r"bot_(\d+)_(\w+)")

    for entry in os.scandir(profiles_dir):
        if entry.is_dir():
            match = pattern.match(entry.name)
            if match:
                bot_id, browser = match.groups()
                profiles.append(
                    {"bot_id": int(bot_id), "browser": browser, "proxy": default_proxy}
                )

    profiles.sort(key=lambda x: x["bot_id"])

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

    return profiles


if __name__ == "__main__":
    import argparse

    sanitize_cli_args(sys.argv[1:])
    parser = argparse.ArgumentParser(description="Generate profile data JSON")
    parser.add_argument(
        "--dir", default="bot_keydrop/profiles", help="Profiles directory"
    )
    parser.add_argument("--output", default="profiles.json", help="Output JSON path")
    parser.add_argument("--proxy", default="", help="Default proxy value")

    args = parser.parse_args()

    created = create_profiles_json(args.dir, args.output, args.proxy)
    print(f"Generated {len(created)} profiles in {args.output}")
