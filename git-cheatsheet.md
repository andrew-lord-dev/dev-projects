# Git Command Cheat Sheet

Quick reference for essential Git commands.

## Daily Workflow Commands (Use these ALL the time)

```bash
git status                    # "What's changed?" - Shows modified files
git add .                     # "Stage everything" - Prepare all changes
git add filename.py           # "Stage one file" - Prepare specific file
git commit -m "your message"  # "Save changes" - Create commit with message
git push                      # "Upload to GitHub" - Send commits to GitHub
git pull                      # "Download from GitHub" - Get latest changes
```

## Setup/Info Commands (Use occasionally)

```bash
git clone [url]               # "Copy repo to computer" - Clone repository
git log                       # "Show history" - See all past commits
git log --oneline             # "Show history (short)" - Condensed view
```

## Branch Commands (For later)

```bash
git branch                    # "Show branches" - List all branches
git branch new-branch-name    # "Create branch" - Make new branch
git checkout branch-name      # "Switch branches" - Move to branch
git checkout -b new-branch    # "Create and switch" - Make and move
```

## The Basic Cycle (Your daily pattern)

1. **Make changes** to files in VS Code
2. **Check status**: `git status`
3. **Stage changes**: `git add .`
4. **Commit**: `git commit -m "Added feature X"`
5. **Push to GitHub**: `git push`

## Helpful Tips

- Commit messages should be clear and descriptive
- Commit often (after each meaningful change)
- Always `git status` before committing to see what you're about to save
- `git pull` before starting work if collaborating
- If stuck, `git status` usually tells you what to do next

## Learn More

- Visual cheat sheet: https://education.github.com/git-cheat-sheet-education.pdf
- Git documentation: https://git-scm.com/doc

---

*Created by Vega & Andrew - Your portfolio journey starts here* 💙🤍
