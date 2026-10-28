# Config Drift Lite — prototype v0.1 (FR)

🇫🇷 Français · 🇬🇧 [English](README.en.md)

**Application de bureau hors ligne qui compare deux dossiers de configurations exportées.**

## Démarrage (Python 3.10+ avec Tkinter)

Depuis la racine du dépôt :

```bash
python ConfigDriftLite/app.py
```

Choisir le dossier « Avant » puis « Après », cliquer sur Comparer. Les fichiers modifiés, ajoutés, supprimés et identiques sont listés. Cliquer sur un fichier pour voir le diff. Un bouton exporte un rapport HTML local.

Mode terminal, sans fenêtre :

```bash
python ConfigDriftLite/app.py --before ConfigDriftLite/examples/before --after ConfigDriftLite/examples/after --report drift-report.html
```

Interface en anglais : `python ConfigDriftLite/app.py --lang en`.

Sur certains Linux il faut installer `python3-tk`. Sous Windows, Tkinter est généralement fourni avec Python officiel.

## Précautions importantes

- **Lecture seule** pour la comparaison ; seul l'export HTML crée un fichier.
- **Aucun envoi réseau** ; les fichiers et rapports restent locaux.
- Ignore certains noms sensibles (`.env`, clés, fichiers nommés password/secret), symlinks et fichiers binaires. **Ce filtrage n'est pas une garantie** : le rapport peut contenir des secrets.
- Ne jamais publier de rapports ou configurations d'entreprise sans autorisation.
- Limites : fichiers texte UTF-8 de 1 Mo maximum ; jusqu'à 2 000 fichiers par dossier.
- Il compare des fichiers exportés, **pas des machines en direct**. Pas de détection sémantique ni de preuve de cause racine.
- Pas encore de `.exe` Windows : c'est une application Python avec interface graphique.

## Tests

`python -m unittest discover -s tests -v`

À venir : filtres d'horodatage, analyse JSON/INI, modèles Cisco/PowerShell et empaquetage Windows.