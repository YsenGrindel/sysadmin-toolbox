#!/usr/bin/env bash
# Linux HealthCheck — lecture seule, aucune modification de configuration.
set -u

printf '\n=== Linux HealthCheck ===\nDate : %s\nHôte : %s\n' "$(date -Is)" "$(hostname)"
printf '\n--- Système ---\n'
if command -v uptime >/dev/null 2>&1; then uptime -p 2>/dev/null || uptime; fi
if command -v uname >/dev/null 2>&1; then uname -sr; fi
printf '\n--- Stockage (/) ---\n'
df -h / 2>&1
printf '\n--- Mémoire ---\n'
if command -v free >/dev/null 2>&1; then free -h; else echo 'free indisponible'; fi
printf '\n--- Services systemd en échec ---\n'
if command -v systemctl >/dev/null 2>&1; then
    systemctl --failed --no-pager --no-legend 2>&1 || echo 'Impossible de lire systemd'
    printf '\n--- Service SSH ---\n'
    for service in ssh sshd; do
        if systemctl list-unit-files "${service}.service" --no-legend 2>/dev/null | grep -q "${service}.service"; then
            printf '%s : %s\n' "$service" "$(systemctl is-active "${service}.service" 2>/dev/null || true)"
        fi
    done
else
    echo 'systemd indisponible sur ce système'
fi
printf '\nFin du contrôle. Ce rapport ne constitue pas un audit de sécurité.\n'
