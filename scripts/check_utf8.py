from pathlib import Path


TEXT_EXTENSIONS = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".md",
    ".txt",
    ".toml",
}

TEXT_NAMES = {
    ".env",
    ".gitignore",
    ".python-version",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".agents",
    ".codex",
    "vector_db",
    "logs",
}

MOJIBAKE_TOKENS = [
    "\u951b",
    "\u9356",
    "\u7487",
    "\u93b4",
    "\u6d93",
    "\u7027",
    "\u9425",
    "\u93c6",
    "\u68ab",
    "\u95c2",
    "\ufffd",
]


def should_check(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in TEXT_NAMES


def main() -> int:
    failed = False

    for path in Path(".").rglob("*"):
        if not path.is_file() or not should_check(path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            failed = True
            print(f"UTF-8 decode failed: {path} ({exc})")
            continue

        hits = [token for token in MOJIBAKE_TOKENS if token in text]
        if hits:
            failed = True
            escaped = ", ".join(token.encode("unicode_escape").decode() for token in hits)
            print(f"Possible mojibake: {path} ({escaped})")

    if failed:
        return 1

    print("UTF-8 check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
