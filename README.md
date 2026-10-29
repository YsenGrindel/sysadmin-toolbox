# SysAdmin Toolbox 🧰

**Langues / Languages :** 🇫🇷 Français · 🇬🇧 [English](README.en.md)

Cinq outils open source pour l'administration systèmes et réseaux. Les scripts restent séparés et utilisables en ligne de commande, mais ils proposent aussi des **lanceurs Windows par double-clic**.

> Version de travail : à tester en laboratoire avant une utilisation professionnelle. Les scripts publiés peuvent contenir des erreurs. Ne pas les utiliser sur des machines tierces sans autorisation.

## Téléchargement facile : fichier ZIP par outil

Chaque archive contient **le lanceur .cmd et le script nécessaire (.ps1, .py ou .sh)**, dans le même dossier. Décompresser **tous** les fichiers, puis double-cliquer sur le fichier `Lancer-….cmd`.

| Outil | Télécharger (ZIP) | Lanceur à double-cliquer | Conditions |
|---|---|---|---|
| Windows HealthCheck | [Windows-HealthCheck.zip](downloads/Windows-HealthCheck.zip) | `Lancer-Windows-HealthCheck.cmd` | Windows + PowerShell |
| Security Baseline Checker | [Security-BaselineChecker.zip](downloads/Security-BaselineChecker.zip) | `Lancer-Security-BaselineChecker.cmd` | Windows + PowerShell |
| AD Bulk User Creation | [AD-BulkUserCreation.zip](downloads/AD-BulkUserCreation.zip) | `Lancer-AD-BulkUserCreation.cmd` | Simulation par défaut ; lab AD requis pour de vraies créations |
| Network Doctor | [Network-Doctor.zip](downloads/Network-Doctor.zip) | `Lancer-Network-Doctor.cmd` | Windows + Python 3 |
| Linux HealthCheck | [Linux-HealthCheck.zip](downloads/Linux-HealthCheck.zip) | `Lancer-Linux-HealthCheck.cmd` | Windows avec WSL/Linux installé ; sinon lancer le .sh sur Linux |

Autre possibilité : **Code → Download ZIP** sur cette page GitHub, puis extraire l'ensemble du dépôt. Tu trouveras les mêmes lanceurs dans les dossiers `PowerShell/`, `Python/` et `Bash/`, et le menu global **`Lancer-Toolbox.cmd`** à la racine.

**Important :** les ZIP sont des copies datées des scripts à leur publication. En cas de mises à jour, télécharger à nouveau la dernière version. Les scripts PowerShell peuvent être bloqués par une politique d'exécution : les lanceurs conservent la fenêtre ouverte afin de lire l'erreur, mais ne désactivent pas cette protection.

## Ce que font les outils

| Script source | Fonction | Effet |
|---|---|---|
| [Windows-HealthCheck.ps1](PowerShell/Windows-HealthCheck.ps1) | Diagnostic Windows : mémoire, disques, services, BitLocker ; verdicts OK / ATTENTION / PROBLÈME / NON ÉVALUÉ ; export JSON optionnel | Lecture seule |
| [Security-BaselineChecker.ps1](PowerShell/Security-BaselineChecker.ps1) | Indicateurs de sécurité : pare-feu, Defender, BitLocker, UAC | Lecture seule |
| [AD-BulkUserCreation.ps1](PowerShell/AD-BulkUserCreation.ps1) | Prévisualise la création d'utilisateurs depuis un CSV. Modifie AD seulement avec `-Apply` et confirmations, depuis PowerShell ouvert manuellement | **Simulation au double-clic** |
| [network_doctor.py](Python/network_doctor.py) | Teste IP, passerelle, TCP externe, DNS et port cible ; propose une hypothèse de diagnostic | Requêtes réseau de diagnostic |
| [linux-healthcheck.sh](Bash/linux-healthcheck.sh) | Affiche état du système Linux, ressources, disque, systemd et SSH | Lecture seule |

Le menu/lanceur **ne demande pas les droits administrateur automatiquement**. Des contrôles peuvent être marqués indisponibles selon le poste, les droits ou la politique en vigueur.

## Utilisation avancée en terminal

```powershell
.\PowerShell\Windows-HealthCheck.ps1 -Language fr -OutputPath .\health.json
.\PowerShell\Windows-HealthCheck.ps1 -Language en -Pause
.\PowerShell\Security-BaselineChecker.ps1
.\PowerShell\AD-BulkUserCreation.ps1 -CsvPath .\examples\ad-users.example.csv
python Python/network_doctor.py --host example.com --port 443 --json
```

Sous Linux : `bash Bash/linux-healthcheck.sh`. Network Doctor effectue des requêtes réseau et ses tests sont indicatifs (proxy, ICMP filtré et restrictions réseau peuvent conduire à de faux négatifs). **Ne jamais mettre de mots de passe, clés, jetons, fichiers internes de stage ou logs clients sur GitHub.**

Pour la création AD réelle, sur un **laboratoire isolé et après vérification du CSV uniquement**, lancer manuellement le script avec `-Apply` depuis une console appropriée. Ne pas utiliser le lanceur à cette fin.

## Fiabilité et contribution

- Tests Python : `python -m unittest discover -s tests -v`.
- Vérification syntaxique Bash dans GitHub Actions.
- Les scripts PowerShell/AD doivent encore être validés sur Windows et en laboratoire.
- [Contribuer](CONTRIBUTING.md) · [Publication](PUBLISHING.md) · [Licence MIT](LICENSE).

## Pistes de futurs outils

**Incident Timeline**, **ChangeGuard** et **Port Story**. Ces idées ne sont pas encore implémentées.
