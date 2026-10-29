# SysAdmin Toolbox 🧰

**Languages / Langues:** 🇬🇧 English · 🇫🇷 [Français](README.md)

Five open-source tools for systems and network administrators. Each script remains usable from a terminal and also offers a **Windows double-click launcher**.

> Work in progress: lab validation required before professional use. Review the code and obtain permission before running scripts on third-party machines.

## Easy downloads: one ZIP per tool

Each ZIP includes **the .cmd launcher and the associated .ps1, .py or .sh script**, together in the same directory. Extract **all** the files, then double-click `Lancer-….cmd`.

| Tool | Download ZIP | Double-click | Requirements |
|---|---|---|---|
| Windows HealthCheck | [Windows-HealthCheck.zip](downloads/Windows-HealthCheck.zip) | `Lancer-Windows-HealthCheck.cmd` | Windows + PowerShell |
| Security Baseline Checker | [Security-BaselineChecker.zip](downloads/Security-BaselineChecker.zip) | `Lancer-Security-BaselineChecker.cmd` | Windows + PowerShell |
| AD Bulk User Creation | [AD-BulkUserCreation.zip](downloads/AD-BulkUserCreation.zip) | `Lancer-AD-BulkUserCreation.cmd` | Dry run by default; isolated AD lab required for actual provisioning |
| Network Doctor | [Network-Doctor.zip](downloads/Network-Doctor.zip) | `Lancer-Network-Doctor.cmd` | Windows + Python 3 |
| Linux HealthCheck | [Linux-HealthCheck.zip](downloads/Linux-HealthCheck.zip) | `Lancer-Linux-HealthCheck.cmd` | Windows with WSL/Linux installed; otherwise run .sh on Linux |

Alternatively, select **Code → Download ZIP** to get the whole repository. The launchers are also in `PowerShell/`, `Python/` and `Bash/`; a global **`Lancer-Toolbox.cmd`** menu is at the project root.

**Important:** ZIPs are snapshots of their scripts; download the latest version after changes. A restrictive PowerShell execution policy may prevent a script from running. The launchers keep the terminal open so you can read any error; they do not silently disable those protections.

## Included tools

| Source | Function | Side effects |
|---|---|---|
| [Windows-HealthCheck.ps1](PowerShell/Windows-HealthCheck.ps1) | Windows memory, disks, services, BitLocker; clear OK / WARNING / PROBLEM / NOT CHECKED status and optional JSON | Read-only |
| [Security-BaselineChecker.ps1](PowerShell/Security-BaselineChecker.ps1) | Indicative firewall, Defender, BitLocker, UAC checks | Read-only |
| [AD-BulkUserCreation.ps1](PowerShell/AD-BulkUserCreation.ps1) | CSV-based AD creation. Actual changes require `-Apply` and PowerShell confirmation in a separate manual run | **Double-click always dry run** |
| [network_doctor.py](Python/network_doctor.py) | IPv4, gateway, external TCP, DNS and target port troubleshooting hypotheses | Network probes |
| [linux-healthcheck.sh](Bash/linux-healthcheck.sh) | Linux resources, disk usage, systemd and SSH inspection | Read-only |

Launchers do not automatically request elevated rights. Results may be unavailable due to permissions or host policy.

## Terminal usage

```powershell
.\PowerShell\Windows-HealthCheck.ps1 -Language en -OutputPath .\health.json
.\PowerShell\Security-BaselineChecker.ps1
.\PowerShell\AD-BulkUserCreation.ps1 -CsvPath .\examples\ad-users.example.csv
python Python/network_doctor.py --host example.com --port 443 --json
```

On Linux: `bash Bash/linux-healthcheck.sh`. Network Doctor creates diagnostic network connections; proxies, ICMP filtering and network restrictions may cause false negatives. **Never commit passwords, keys, tokens, internship data, employer configurations or customer logs.**

Only run real AD provisioning with `-Apply` **manually in an isolated lab** after carefully checking the CSV; the double-click launcher never enables `-Apply`.

## Quality and contribution

- Python tests: `python -m unittest discover -s tests -v`.
- GitHub Actions checks Bash syntax.
- PowerShell and AD scripts still require real Windows/lab testing.
- [Contributing](CONTRIBUTING.en.md) · [Publishing](PUBLISHING.en.md) · [MIT License](LICENSE).

## Future ideas

**Incident Timeline**, **ChangeGuard** and **Port Story** are not yet implemented.
