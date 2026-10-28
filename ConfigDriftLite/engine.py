"""Config Drift Lite: conservative, read-only comparison of two local text snapshots.

No network access. No secret collection. Never upload reports without reviewing them.
"""
from __future__ import annotations

from dataclasses import dataclass
from difflib import unified_diff
from fnmatch import fnmatch
from html import escape
import os
from pathlib import Path

MAX_FILE_BYTES = 1_000_000
MAX_FILES = 2000
IGNORED_DIRS = {
    ".git", ".svn", ".hg", ".venv", "venv", "node_modules",
    "__pycache__", ".ssh", "secrets", "private", "credentials",
}
IGNORED_FILES = (
    ".env", ".env.*", "*.pem", "*.key", "*.pfx", "*.p12", "*.kdbx",
    "id_rsa*", "id_ed25519*", "*password*", "*secret*",
    "*credential*", "shadow", "shadow-*", "*.sqlite", "*.db",
)


@dataclass(frozen=True)
class FileChange:
    path: str
    status: str
    before: str = ""
    after: str = ""

    def diff(self) -> str:
        if self.status == "unchanged":
            return ""
        return "".join(unified_diff(
            self.before.splitlines(keepends=True),
            self.after.splitlines(keepends=True),
            fromfile="avant/" + self.path if self.status != "added" else "/dev/null",
            tofile="apres/" + self.path if self.status != "removed" else "/dev/null",
            lineterm="\n",
        ))


@dataclass
class Comparison:
    before_dir: str
    after_dir: str
    changes: list[FileChange]
    skipped: list[str]

    def counts(self) -> dict[str, int]:
        return {kind: sum(c.status == kind for c in self.changes)
                for kind in ("modified", "added", "removed", "unchanged")}


def _ignored_file(name: str) -> bool:
    value = name.lower()
    return any(fnmatch(value, pattern) for pattern in IGNORED_FILES)


def scan(root: Path) -> tuple[dict[str, str], list[str]]:
    """Read non-sensitive-looking UTF-8 text files, ignoring links and binaries.

    Patterns are a safety aid, NOT a guarantee of secret detection.
    """
    if not root.is_dir():
        raise ValueError(f"Dossier introuvable / Missing directory: {root}")
    files: dict[str, str] = {}
    skipped: list[str] = []
    inspected = 0

    for folder, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs
                         if d.lower() not in IGNORED_DIRS
                         and not (Path(folder) / d).is_symlink())
        for name in sorted(names):
            path = Path(folder) / name
            relative = path.relative_to(root).as_posix()
            if _ignored_file(name):
                skipped.append(f"{relative} (excluded by name)")
                continue
            if path.is_symlink():
                skipped.append(f"{relative} (symbolic link)")
                continue
            if not path.is_file():
                continue
            inspected += 1
            if inspected > MAX_FILES:
                raise ValueError(f"Limite de {MAX_FILES} fichiers depassee / Too many files")
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    skipped.append(f"{relative} (too large)")
                    continue
                data = path.read_bytes()
                if b"\x00" in data:
                    skipped.append(f"{relative} (binary or unsupported encoding)")
                    continue
                files[relative] = data.decode("utf-8-sig")
            except (OSError, UnicodeError):
                skipped.append(f"{relative} (unreadable or not UTF-8)")
    return files, skipped


def compare(before_dir: str | Path, after_dir: str | Path) -> Comparison:
    before_root = Path(before_dir).expanduser().resolve()
    after_root = Path(after_dir).expanduser().resolve()
    if before_root == after_root:
        raise ValueError("Choisir deux dossiers differents / Choose two different folders")
    before, skipped_before = scan(before_root)
    after, skipped_after = scan(after_root)
    changes = []
    for path in sorted(set(before) | set(after)):
        if path not in before:
            status = "added"
        elif path not in after:
            status = "removed"
        elif before[path] == after[path]:
            status = "unchanged"
        else:
            status = "modified"
        changes.append(FileChange(path, status, before.get(path, ""), after.get(path, "")))
    return Comparison(
        str(before_root), str(after_root), changes,
        ["Before: " + entry for entry in skipped_before] +
        ["After: " + entry for entry in skipped_after],
    )


def html_report(result: Comparison) -> str:
    """Produce a self-contained local HTML report; content can be sensitive."""
    counts = result.counts()
    rows = []
    for change in result.changes:
        safe_name = escape(change.path)
        safe_status = escape(change.status)
        snippet = escape(change.diff())
        details = (f"<details><summary>View differences / Voir les differences</summary>"
                   f"<pre>{snippet}</pre></details>") if snippet else ""
        rows.append(f"<tr class='{safe_status}'><td>{safe_name}</td>"
                    f"<td>{safe_status}</td><td>{details}</td></tr>")
    skipped = "".join(f"<li>{escape(s)}</li>" for s in result.skipped)
    count_text = " | ".join(f"{key}: {value}" for key, value in counts.items())
    return ("""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Config Drift Lite - report</title><style>
body{font:15px system-ui,Arial;max-width:1100px;margin:2em auto;padding:0 1em;color:#192638}
h1{color:#174879}small{color:#58667c}table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #ddd;padding:10px;text-align:left;vertical-align:top}
.modified td:first-child{border-left:4px solid #e9a225}
.added td:first-child{border-left:4px solid #32a473}
.removed td:first-child{border-left:4px solid #d45555}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf2f7;padding:12px}
</style></head><body>"""
        f"<h1>Config Drift Lite</h1><p>{escape(count_text)}</p>"
        f"<p><b>Avant / Before:</b> {escape(result.before_dir)}<br>"
        f"<b>Apres / After:</b> {escape(result.after_dir)}</p>"
        "<p><small>Read-only comparison. Review before sharing: differences may contain sensitive data."
        " / Comparaison en lecture seule. Relire avant tout partage : donnees potentiellement sensibles.</small></p>"
        "<table><thead><tr><th>File / Fichier</th><th>Status</th><th>Diff</th></tr></thead><tbody>"
        + "".join(rows) + "</tbody></table>"
        "<h2>Ignored / Ignored files</h2><ul>" + skipped +
        "</ul></body></html>"
    )
