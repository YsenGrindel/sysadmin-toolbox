# Publishing to GitHub

**Languages / Langues:** 🇬🇧 English · 🇫🇷 [Français](PUBLISHING.md)

## Option A — GitHub website

1. Sign in to [GitHub](https://github.com) and select **New repository**.
2. Name it `sysadmin-toolbox`. Choose **Public** for an open portfolio, or **Private** if needed.
3. Do **not** initialize it with a README, `.gitignore`, or license; these files already exist here.
4. Use **uploading an existing file** to upload the *contents* of the `sysadmin-toolbox` folder, including `.github`.
5. Check that no sensitive information is included before committing.

For multiple folders or hidden files, the Git CLI is usually easier.

## Option B — Git CLI

Create an **empty** GitHub repository first, then inside the extracted `sysadmin-toolbox` folder:

```bash
git init -b main
git add .
git commit -m "Initial toolbox: network, Windows, Linux, AD and security"
git remote add origin https://github.com/YsenGrindel/sysadmin-toolbox.git
git push -u origin main
```

Authenticate using Git Credential Manager, the browser, or SSH. **Never place a password or access token in repository files.**

## Option C — through ChatGPT's GitHub connection

First create an **empty** `sysadmin-toolbox` repository at [GitHub New Repository](https://github.com/new), without a README, `.gitignore`, or license. Then return to the connected ChatGPT conversation and request to publish the files to that existing repository. The currently available connector can modify accessible repositories, but cannot create the initial repository itself.

## Before publishing

- Review the README and all scripts.
- Keep example data fictional (`example.local`).
- Test Python and Bash; validate PowerShell on Windows, and Active Directory actions only in an isolated lab.
- Never commit data or logs from an employer, internship, or customer.