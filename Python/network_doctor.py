#!/usr/bin/env python3
"""Diagnostic IPv4 / gateway / TCP / DNS. Observations are hypotheses."""
from __future__ import annotations
import argparse
import json
import platform
import re
import socket
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Results:
    local_ipv4: Optional[str]
    gateway: Optional[str]
    gateway_ping: Optional[bool]
    external_tcp: bool
    dns_resolution: bool
    target_tcp: bool
    target: str
    target_port: int
    diagnosis: str

def local_ipv4():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("192.0.2.1", 9))
            ip = sock.getsockname()[0]
            return None if ip.startswith("127.") else ip
    except OSError:
        return None

def detect_gateway():
    system = platform.system()
    try:
        if system == "Windows":
            out = subprocess.run(["route", "print", "-4"], capture_output=True, text=True, timeout=4, check=False).stdout
            m = re.search(r"(?m)^\s*0\.0\.0\.0\s+0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)\s+", out)
        elif system == "Linux":
            out = subprocess.run(["ip", "-4", "route", "show", "default"], capture_output=True, text=True, timeout=4, check=False).stdout
            m = re.search(r"\bdefault via (\d+\.\d+\.\d+\.\d+)", out)
        elif system == "Darwin":
            out = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True, timeout=4, check=False).stdout
            m = re.search(r"\bgateway:\s*(\d+\.\d+\.\d+\.\d+)", out)
        else:
            return None
        return m.group(1) if m else None
    except (OSError, subprocess.TimeoutExpired):
        return None

def gateway_ping(address, timeout):
    if not address:
        return None
    if platform.system() == "Windows":
        command = ["ping", "-n", "1", "-w", str(max(1, round(timeout * 1000))), address]
    else:
        command = ["ping", "-c", "1", address]
    try:
        return subprocess.run(command, capture_output=True, timeout=timeout+2, check=False).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return None

def tcp_check(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

def dns_check(host):
    try:
        return bool(socket.getaddrinfo(host, None))
    except (socket.gaierror, OSError):
        return False

def classify(local, gateway, ping_ok, tcp_ok, dns_ok, target_ok):
    if not local:
        return "Aucune adresse IPv4 locale détectée : contrôler l'interface et la configuration IP."
    if tcp_ok and not dns_ok:
        return "Accès TCP externe OK, DNS KO : examiner les serveurs DNS et la résolution de noms."
    if not tcp_ok and ping_ok is False:
        return "Passerelle injoignable en ICMP et TCP externe KO : vérifier le réseau local (ICMP peut être filtré)."
    if not tcp_ok:
        return "Échec du test TCP externe : vérifier route par défaut, filtrage, proxy ou connectivité WAN."
    if not target_ok:
        return "Connectivité externe disponible, mais service cible injoignable : vérifier hôte/port/filtrage."
    if gateway is None:
        return "Tests externes OK ; passerelle non détectée automatiquement."
    if ping_ok is False:
        return "Tests externes OK ; ping de passerelle KO (ICMP probablement filtré)."
    return "Tests réussis. Aucun problème détecté par ces vérifications limitées."

def run(timeout, host, port, internet_ip):
    local = local_ipv4()
    gateway = detect_gateway()
    ping = gateway_ping(gateway, timeout)
    external = tcp_check(internet_ip, 443, timeout)
    dns = dns_check(host)
    target = tcp_check(host, port, timeout) if dns else False
    return Results(local, gateway, ping, external, dns, target, host, port, classify(local, gateway, ping, external, dns, target))

def main():
    p = argparse.ArgumentParser(description="Network Doctor - IPv4/TCP/DNS")
    p.add_argument("--host", default="example.com")
    p.add_argument("--port", type=int, default=443)
    p.add_argument("--internet-ip", default="1.1.1.1")
    p.add_argument("--timeout", type=float, default=2)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if not (1 <= args.port <= 65535 and 0 < args.timeout <= 30):
        p.error("Invalid port or timeout.")
    r = run(args.timeout, args.host, args.port, args.internet_ip)
    if args.json:
        print(json.dumps(asdict(r), indent=2, ensure_ascii=False))
    else:
        print("\nNETWORK DOCTOR — diagnostic limité IPv4/TCP/DNS\n")
        for key,value in asdict(r).items():
            print(f"  {key}: {value}")
    return 0 if r.external_tcp and r.dns_resolution and r.target_tcp else 1

if __name__ == "__main__":
    sys.exit(main())
