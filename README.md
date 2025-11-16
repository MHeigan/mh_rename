# mh_rename

**Version:** 2025-11-16  •  **Author:** Martin Heigan  •  **Suite:** mh_tools

Rename and Renumber Image Sequences

**License:** CC BY-NC-ND 4.0 (see LICENSE.rtf)

---
## 🎛️ Tool Usage & Overview
mh_tools • All-in-One Git + README + LFS — User Manual

Version: {{today}}

Overview

This tool unifies everyday Git + GitHub tasks for your scripting projects:

README & Docs generation (manual import to docs/ and Markdown extraction from .docx)

Repository & remote management (create repo via PAT, set origin to SSH, Quick Commit, Stash/Pop, Pull --rebase, Push, Force push with lease)

Ignore & LFS controls (preset ignores, ffmpeg/ toggle, custom file/folder ignore picker, optional .git/info/exclude, enable Git LFS for media)

Backup Files tab (preserves original path structure inside project/backup/)

History Cleanup (purge >100 MB blobs with git-filter-repo, then force push)

Utilities (Test SSH, Repair origin→SSH & push, Create venv, Init repo, Load SSH key console, Open docs/, Force SSH everywhere)

The GUI is centered and contained in a labeled frame named mh_tool. Default size is 1200×660 (min width 1200 to avoid button cropping).

What’s New in This Version

Quick Commit detects a clean tree and shows the last commit hash when there’s nothing to commit.

Automatic Force SSH everywhere before push/force-push/repair/set-origin (prevents HTTPS credential prompts).

Public/Private visibility toggle when creating a GitHub repository via PAT.

README tab: generate, preview, and commit README; attach manual (.docx), setup PDF, and other docs to docs/.

Ignore & LFS: add custom files/folders to .gitignore via pickers; optionally mirror to .git/info/exclude (local only).

Backup tab: add files/folders to back up into project/backup/ with original project-relative paths preserved.

History Cleanup: purge >100 MB blobs with git-filter-repo and then force push main.

Utilities: Test SSH, Repair origin→SSH & Push, Create venv + install requirements, Init repo, load SSH key console.

Typical Workflow (Day-to-Day Updates)

Open your project folder at the top of the GUI.

(Optional) In README & Docs: Preview/Generate README or Generate → Stage & Commit.

In Repo & Remote: Quick Commit (stage all) → enter a concise message.

Push main. If rejected (remote ahead), choose Pull (rebase) or Force push with lease.

If large binaries appear (>100 MB), use History Cleanup → Purge >100 MB & Force Push.

In Backup: Sync backup to project for .spec / .bat / icons, preserving project-relative paths.

Tabs & Controls — README & Docs

Repository Name / Description → used in README.md.

Manual (.docx): copied to docs/; Markdown headings are extracted and embedded into README (link to the .docx is kept).

Attachments (docs/): copied to docs/ and linked in README.

Setup PDF: optional; included in docs/ and linked.

Buttons:

Preview README: show generated Markdown.

Generate README: write README.md (and copy docs).

Generate README → Stage & Commit: commits README and docs immediately.

Docs ▸ Open folder: opens docs/ in your OS file manager.

Tabs & Controls — Repo & Remote

Username/Org + Repository Name → used for SSH origin URL and for PAT repo creation.

Visibility: Private/Public when creating repo via PAT.

Personal Access Token (repo scope): only required for Create Repo on GitHub (via PAT). Regular pushes use SSH.

Use SSH for push (recommended): prevents Windows Credential Manager loops.

Buttons:

Create Repo on GitHub (via PAT): create remote repository via API.

Set origin → SSH: sets origin to git@github.com:<user>/<repo>.git and configures Windows OpenSSH.

Quick Commit (stage all): stages everything; if tree is clean, shows last commit hash; else prompts for message and commits.

Stash / Stash Pop: save/restore WIP before pull --rebase if necessary.

Pull (rebase): integrates remote changes while keeping a linear history.

Force push (lease): safe overwrite when history changed locally; uses --force-with-lease.

Push main: standard push; if rejected, app offers Pull (rebase) or Force push (lease).

Open repo on GitHub: opens https://github.com/<user>/<repo>.

Tabs & Controls — Ignore & LFS

Ignore ffmpeg/ folder: toggles ffmpeg/ in .gitignore.

Enable Git LFS for media: enables LFS and tracks typical media patterns (EXR/MOV/MP4/TIF/WAV/JPG/PNG/TIFF).

Custom ignores: add files/folders (converted to project-relative patterns) to .gitignore.

Also add to .git/info/exclude: mirrors the same patterns locally (never pushed).

Buttons:

Apply .gitignore rules: appends rules and stages .gitignore.

Enable LFS (track media): runs git lfs track and commits .gitattributes if needed.

Edit .gitignore: quick editor.

Tabs & Controls — Backup Files

Add Files… / Add Folder…: choose items to copy to project/backup/.

Preserve original path structure: items inside the project mirror to backup/<relative_path>.

External items (outside project) go to backup/_external/.

Ensure backup/ is tracked: updates .gitignore to allow backup/**.

Auto-commit backup during README commit (optional).

Buttons:

Sync backup to project

Open backup folder

Tabs & Controls — History Cleanup

Purge >100 MB & Force Push: uses git-filter-repo to remove blobs >100 MB across history, expires reflog, runs aggressive GC, then force pushes main.

Use when GitHub rejects pushes due to large file history (e.g., ffmpeg.exe, big EXRs).

Requires: pip install git-filter-repo.

Tabs & Controls — Utilities

Test SSH: ssh -T git@github.com and report result (“successfully authenticated”).

Repair origin → SSH & Push: convert origin to SSH, use Windows OpenSSH, push.

Create venv & install requirements: create .venv and install requirements.txt if present.

Init repo (.git): git init, set branch main.

Load SSH key (opens console): elevated PowerShell starts ssh-agent and runs ssh-add ~/.ssh/id_ed25519.

Force SSH everywhere: sets global HTTPS→SSH rewrite for GitHub and updates repo origin to SSH; verifies with ls-remote.

Short Guide: Push an Updated Version

Update code/docs locally.

(Optional) README: Generate README → Stage & Commit.

Quick Commit → message.

Push main. If rejected, Pull (rebase) or Force push (lease).

If GitHub rejects due to large files: History Cleanup → Purge >100 MB & Force Push.

SSH & Origin Notes

The app enforces SSH for pushes to avoid Credential Manager prompts.

Force SSH everywhere sets a global Git rewrite from https://github.com/ to ssh://git@github.com/ and updates origin.

Use Load SSH key if ssh-add -l shows no identities.

Appendix A — GitHub Setup (Windows)

Ensure OpenSSH Client is installed and Git is in PATH.

Generate a key:
ssh-keygen -t ed25519 -C "you@example.com"

Start + load agent (PowerShell as Admin):
Set-Service ssh-agent -StartupType Automatic; Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519

Test:
ssh -T git@github.com → “Hi <user>! You’ve successfully authenticated…”

Set origin SSH:
git remote set-url origin git@github.com:<user>/<repo>.git

## 📂 Attached Docs
- [mh_tools_all_in_one_manual.docx](docs/mh_tools_all_in_one_manual.docx)
- [mh_Rename_User_Manual.docx](docs/mh_Rename_User_Manual.docx)

## 🧭 Appendix A — GitHub Setup (Windows)

**SSH quick check**
1) Load key: `ssh-add %USERPROFILE%\\.ssh\id_ed25519`
2) Test: `ssh -T git@github.com`  →  “successfully authenticated”
3) Ensure remote uses SSH:
   `git remote set-url origin git@github.com:<user>/<repo>.git`


—

_README generated by mh_tools All-in-One GUI_
