# SysAdmin Toolbox 

**Langues / Languages :** 🇫🇷 Français (ce document) · 🇬🇧 [English](README.en.md)

**Boîte à outils open source pour techniciens systèmes et réseaux** — scripts simples, documentés et conçus pour évoluer. Première version de travail (`v0.1.0`), **à valider en lab avant usage professionnel**.

## Les cinq utilitaires

| Script | Fonction | Modification du système ? | État |
|---|---|---|---|
| [`Python/network_doctor.py`](Python/network_doctor.py) | Test IPv4 local, passerelle, TCP externe, DNS et service cible | Non, uniquement des connexions de test | Tests unitaires sur le diagnostic |
| [`PowerShell/Windows-HealthCheck.ps1`](PowerShell/Windows-HealthCheck.ps1) | Bilan Windows avec statuts OK / ATTENTION / PROBLÈME / NON ÉVALUÉ, résumé et JSON | Non | À tester sous Windows |
| [`PowerShell/AD-BulkUserCreation.ps1`](PowerShell/AD-BulkUserCreation.ps1) | Création AD CSV avec simulation par défaut | **Oui, uniquement avec `-Apply` et confirmation** | À tester en lab AD isolé |
| [`Bash/linux-healthcheck.sh`](Bash/linux-healthcheck.sh) | Ressources, espace disque, systemd et SSH | Non | Syntaxe validable automatiquement |
| [`PowerShell/Security-BaselineChecker.ps1`](PowerShell/Security-BaselineChecker.ps1) | Contrôles indicatifs pare-feu, Defender, BitLocker et UAC | Non | À tester sous Windows |

## Démarrage rapide

### Network Doctor (Python 3.9+)

```bash
python Python/network_doctor.py
python Python/network_doctor.py --host example.com --port 443 --json
python -m unittest discover -s tests -v
```

Il teste la connexion TCP vers `1.1.1.1:443` et résout `example.com` par défaut. **Des requêtes réseau sont effectuées**. Une restriction de pare-feu, un proxy ou ICMP désactivé peuvent provoquer des faux négatifs ; ce programme suggère une piste et **ne prouve pas la cause**.

### Linux HealthCheck

```bash
bash Bash/linux-healthcheck.sh
```

### Windows HealthCheck (PowerShell)

**Pour un lancement par double-clic sous Windows**, ouvre `PowerShell/Lancer-Windows-HealthCheck.cmd`. Le lanceur **attend une touche avant de fermer la fenêtre**, y compris en cas d'erreur de PowerShell. Il ne désactive pas silencieusement la politique d'exécution.

Sinon, ouvre toi-même PowerShell puis lance :

```powershell
.\PowerShell\Windows-HealthCheck.ps1 -Language fr
.\PowerShell\Windows-HealthCheck.ps1 -Language fr -Pause
```

L'option `-Pause` attend la touche Entrée à la fin d'une exécution normale. Si Windows bloque le script selon sa politique d'exécution, vérifie sa provenance avant de le débloquer, sans désactiver globalement les protections.

```powershell
.\PowerShell\Windows-HealthCheck.ps1
.\PowerShell\Windows-HealthCheck.ps1 -OutputPath .\health.json
```

Version bilingue et bilan lisible :

```powershell
.\PowerShell\Windows-HealthCheck.ps1 -Language fr
.\PowerShell\Windows-HealthCheck.ps1 -Language en -OutputPath .\health.json
```

Les seuils par défaut sont indicatifs (mémoire/disque : attention sous 15 %, problème sous 5 %). Ce n'est ni un diagnostic exhaustif ni une preuve que Windows est sécurisé. Statuts *NON ÉVALUÉ* si une information ne peut pas être lue ; BitLocker dépend de la politique du poste.

### Security Baseline Checker (PowerShell)

```powershell
.\PowerShell\Security-BaselineChecker.ps1
```

### AD Bulk User Creation (lab uniquement)

```powershell
# Simulation : ne crée rien
.\PowerShell\AD-BulkUserCreation.ps1 -CsvPath .\examples\ad-users.example.csv

# Seulement après avoir adapté le CSV au domaine de lab :
.\PowerShell\AD-BulkUserCreation.ps1 -CsvPath .\examples\ad-users.example.csv -Apply
```

Le CSV exemple utilise un **domaine fictif** (`example.local`) et ne doit pas être appliqué tel quel. Prérequis pour `-Apply` : module `ActiveDirectory`, droits nécessaires, contrôleur de domaine joignable. Une demande de confirmation est prévue. Le mot de passe initial est saisi en mode sécurisé au moment de l'exécution. **Aucun mot de passe, clé de récupération ou donnée d'organisation ne doit être ajouté au dépôt.**

## Qualité et limites

- Les scripts sont volontairement petits, lisibles et sans dépendances tierces pour la partie Python.
- Les scripts Windows/AD demandent des tests manuels dans des environnements adaptés avant déploiement.
- Les scripts de contrôle ne remplacent pas une supervision, une stratégie de sauvegarde ou un audit de sécurité.
- L'automatisation GitHub Actions teste la logique Python et la syntaxe Bash à chaque push.
- Ne pas exécuter des scripts non revus sur des machines de production.

## Feuille de route : les outils originaux

1. **Incident Timeline** — reconstituer une chronologie de symptômes à partir de journaux exportés (sans données sensibles).
2. **ChangeGuard** — prévisualiser l'impact et proposer un plan de retour arrière avant certaines modifications récurrentes.
3. **Port Story** — expliquer un diagnostic de connexion en langage compréhensible à partir d'observations (DNS/TCP/routage).
4. **[Config Drift Lite](https://github.com/YsenGrindel/Config-Drift-Lite)** — **prototype d'application graphique déjà disponible** pour comparer deux dossiers de configurations, visualiser les modifications et exporter un rapport HTML local.

Les trois autres outils originaux ne sont pas encore implémentés.

### Config Drift Lite (Python 3.10+ et Tkinter)

```bash
python ConfigDriftLite/app.py
```

Projet désormais indépendant : [dépôt GitHub Config Drift Lite](https://github.com/YsenGrindel/Config-Drift-Lite). Le dossier local de ce dépôt conserve une copie historique du prototype ; les évolutions se feront sur le dépôt dédié.

## Contribuer et publier

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour participer et [PUBLISHING.md](PUBLISHING.md) pour les étapes de publication.

## Licence

MIT — voir [LICENSE](LICENSE).
