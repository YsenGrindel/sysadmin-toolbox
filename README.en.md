# SysAdmin Toolbox 🧰

**Languages / Langues:** 🇬🇧 English (this document) · 🇫🇷 [Français](README.md)

**Open-source toolbox for systems and network technicians** — small, documented scripts designed to grow over time. Initial work-in-progress release (`v0.1.0`), **must be validated in a lab before professional use**.

## Five starter tools

| Script | Purpose | Changes system state? | Status |
|---|---|---|---|
| [`Python/network_doctor.py`](Python/network_doctor.py) | Detect local IPv4 and gateway; test external TCP, DNS and a target service | No; network probes only | Diagnostic logic has unit tests |
| [`PowerShell/Windows-HealthCheck.ps1`](PowerShell/Windows-HealthCheck.ps1) | Windows health summary: OK / WARNING / PROBLEM / NOT CHECKED, plus JSON export | No | Needs Windows testing |
| [`PowerShell/AD-BulkUserCreation.ps1`](PowerShell/AD-BulkUserCreation.ps1) | CSV-based AD user provisioning, simulation by default | **Yes, only with `-Apply` and confirmation** | Needs isolated AD lab testing |
| [`Bash/linux-healthcheck.sh`](Bash/linux-healthcheck.sh) | Resource, disk, systemd and SSH status | No | Bash syntax checked automatically |
| [`PowerShell/Security-BaselineChecker.ps1`](PowerShell/Security-BaselineChecker.ps1) | Indicative Windows firewall, Defender, BitLocker and UAC checks | No | Needs Windows testing |

## Quick start

### Network Doctor (Python 3.9+)

```bash
python Python/network_doctor.py
python Python/network_doctor.py --host example.com --port 443 --json
python -m unittest discover -s tests -v
```

By default, Network Doctor probes TCP connectivity to `1.1.1.1:443` and resolves `example.com`. **It makes outgoing network requests.** Firewalls, proxies and ICMP filtering can create false negatives. Its diagnosis is a *hypothesis*, **not proof of the root cause**.

CLI output is currently in French; structured output is available with `--json`. English CLI output is planned for a later version.

### Linux HealthCheck

```bash
bash Bash/linux-healthcheck.sh
```

### Windows HealthCheck (PowerShell)

**Windows double-click:** open `PowerShell/Lancer-Windows-HealthCheck.cmd`. The console will **wait for a keypress**, even after an execution error, so the result stays readable. This launcher does not silently bypass the PowerShell execution policy.

Alternatively, start PowerShell yourself, then run:

```powershell
.\PowerShell\Windows-HealthCheck.ps1 -Language en
.\PowerShell\Windows-HealthCheck.ps1 -Language fr -Pause
```

The `-Pause` option waits for Enter after a normal run. If you get an execution policy error, read and trust the script before unblocking it; don't disable security policies globally.

```powershell
.\PowerShell\Windows-HealthCheck.ps1
.\PowerShell\Windows-HealthCheck.ps1 -OutputPath .\health.json
```

The script prints clear OK / WARNING / PROBLEM / NOT CHECKED statuses and a summary. Bilingual output:

```powershell
.\PowerShell\Windows-HealthCheck.ps1 -Language en -OutputPath .\health.json
```

Default disk/memory thresholds are indicative (warning below 15%, problem below 5%). It does not claim full Windows health or security; unavailable checks are marked NOT CHECKED.

### Security Baseline Checker (PowerShell)

```powershell
.\PowerShell\Security-BaselineChecker.ps1
```

### AD Bulk User Creation (isolated lab only)

```powershell
# Dry run: creates nothing
.\PowerShell\AD-BulkUserCreation.ps1 -CsvPath .\examples\ad-users.example.csv

# Only after adapting the CSV to your lab domain:
.\PowerShell\AD-BulkUserCreation.ps1 -CsvPath .\examples\ad-users.example.csv -Apply
```

The example CSV uses a **fictional domain** (`example.local`) and must not be applied as-is. Prerequisites for `-Apply`: the `ActiveDirectory` PowerShell module, sufficient permissions and a reachable domain controller. PowerShell confirmation is required. The initial password is requested securely at runtime, never included in the CSV. **Never commit passwords, recovery keys, tokens, or real organizational data.**

## Quality and limitations

- Scripts are deliberately small and readable; Python needs no third-party packages.
- Windows / AD scripts require manual validation on suitable lab systems before deployment.
- Checks are not substitutes for monitoring, backups or a professional security audit.
- GitHub Actions checks Python unit tests and Bash syntax on pushes and pull requests.
- Do not run unreviewed scripts on production machines.

## Roadmap: more original tools

1. **Incident Timeline** — reconstruct a symptom timeline from sanitized exported logs.
2. **ChangeGuard** — preview likely impacts and plan rollback before routine changes.
3. **Port Story** — explain DNS/TCP/routing test results in plain language.
4. **[Config Drift Lite](ConfigDriftLite/README.en.md)** — **available desktop prototype** for comparing two local directories, viewing line-by-line diffs and exporting an offline HTML report.

The other three ideas are not implemented yet.

### Config Drift Lite (Python 3.10+ with Tkinter)

```bash
python ConfigDriftLite/app.py
```

Docs: [English](ConfigDriftLite/README.en.md) · [Français](ConfigDriftLite/README.md). Offline and read-only; reports may contain confidential information.

## Contribute and publish

See [CONTRIBUTING.en.md](CONTRIBUTING.en.md) for contribution guidance and [PUBLISHING.en.md](PUBLISHING.en.md) for publication steps.

## License

MIT — see [LICENSE](LICENSE).