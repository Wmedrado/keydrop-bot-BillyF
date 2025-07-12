import os


def main() -> int:
    ref = os.environ.get("GITHUB_REF", "")
    event = os.environ.get("GITHUB_EVENT_NAME", "")
    if event == "push" and ref == "refs/heads/main":
        print("Direct pushes to main are not allowed")
        return 1
    print("Branch check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
