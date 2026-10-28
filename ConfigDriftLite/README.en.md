# Config Drift Lite — v0.1 prototype (EN)

🇬🇧 English · 🇫🇷 [Français](README.md)

**Offline desktop app that compares two directories of exported configuration files.**

## Run (Python 3.10+ with Tkinter)

From the repository root:

```bash
python ConfigDriftLite/app.py
```

Choose the Before and After directories, then click Compare. Modified, added, removed and unchanged files appear in a list. Click a file to view its unified diff. You may export an offline HTML report.

Headless CLI mode:

```bash
python ConfigDriftLite/app.py --before ConfigDriftLite/examples/before --after ConfigDriftLite/examples/after --report drift-report.html
```

French is the default UI language; launch with `--lang en` for English.

Tkinter is usually included with official Windows Python, while some Linux distributions need `python3-tk`.

## Safety and limitations

- **Read-only** comparison; only HTML export writes a file.
- **No network upload**: all source files and reports stay local.
- Common secret-looking names (`.env`, keys, password/secret), symlinks and binary files are excluded. **Exclusion is not foolproof**: HTML reports may still contain secrets.
- Never publish employer/client configurations or reports without permission.
- Limits: UTF-8 text up to 1 MB per file and 2,000 files per snapshot.
- Compares exported text files, **not live machines**; does not infer the root cause or semantically normalize differences.
- Not yet a packaged Windows `.exe`; it is a Python desktop application.

## Tests

`python -m unittest discover -s tests -v`

Planned: timestamp filters, JSON/INI-aware diffs, Cisco/PowerShell templates and Windows packaging.