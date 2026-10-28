# Publier le dépôt sur GitHub

**Langues / Languages :** 🇫🇷 Français · 🇬🇧 [English](PUBLISHING.en.md)

## Option A — depuis l'interface web

1. Se connecter à https://github.com et cliquer sur **New repository**.
2. Nommer le dépôt `sysadmin-toolbox`, choisir **Public** pour un portfolio ouvert (ou **Private** si nécessaire).
3. Ne pas ajouter de README ni de licence lors de la création (ils existent déjà ici).
4. Cliquer sur **uploading an existing file**, puis importer **le contenu** du dossier `sysadmin-toolbox` (dossiers cachés compris, notamment `.github`).
5. Vérifier qu'aucune donnée confidentielle n'est présente, puis valider le commit.

L'interface web n'est pas toujours pratique pour importer de nombreux dossiers : l'option B est plus fiable.

## Option B — depuis un terminal Git

Créer un dépôt **vide** sur https://github.com/new (sans README ni licence), puis, dans le dossier extrait `sysadmin-toolbox` :

```bash
git init -b main
git add .
git commit -m "Initial toolbox: network, Windows, Linux, AD and security"
git remote add origin https://github.com/TON-COMPTE/sysadmin-toolbox.git
git push -u origin main
```

Remplacer `TON-COMPTE` par son identifiant GitHub. GitHub utilise une authentification moderne (navigateur/Git Credential Manager ou clé SSH) ; **ne jamais coller son mot de passe ni un token dans les fichiers du dépôt**.

## Avant la publication

- Relire le README et le code.
- Garder les exemples fictifs (domaine `example.local`).
- Tester Python et Bash ; tester PowerShell sur Windows et AD uniquement en lab.
- Ne jamais committer de données ou journaux provenant d'un employeur, d'un stage ou d'un client.

## Option C — avec ChatGPT connecté à GitHub

Créer un dépôt **vide** nommé `sysadmin-toolbox` sur [GitHub New Repository](https://github.com/new) : **ne pas** cocher « Add a README », `.gitignore` ni licence. Une fois créé, revenir dans la conversation pour demander l’ajout des fichiers à ce dépôt. Cette connexion peut écrire dans un dépôt existant autorisé, mais ne crée pas le dépôt via l’outil actuellement disponible.