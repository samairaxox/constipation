# 🐙 Team Git Workflow

This document outlines the branching strategy and collaboration rules for our hackathon team.

## 🌿 Branching Strategy

We use a feature-branch workflow. **Do not push directly to `main`.**

### 🛡️ Main Branch (`main`)
- Contains production-ready code.
- **Protected**: No direct pushes.
- Updated only via Pull Requests (PRs).

### 🏗️ Integration Branch (`architect-main-integration`)
- **Owner**: Architect / Team Lead
- **Purpose**: Merging all modules, shared configurations, and final routing.
- **Upstream**: All feature branches merge here before going to `main`.

### 🎨 Frontend Branch (`frontend-ui-dashboard`)
- **Scope**: React app, Components, UI styling, Widgets.
- **Path**: `frontend/`

### ⚙️ Backend Branch (`backend-api-agents`)
- **Scope**: FastAPI routes, Database integration, API logic.
- **Path**: `backend/`

### 🧠 AI Branch (`data-ai-models`)
- **Scope**: AI Agents, LLM integration, Data pipelines.
- **Path**: `agents/`

---

## 🔄 Daily Workflow

### 1️⃣ Start Your Shift
Always pull the latest changes before starting.

```bash
# Switch to your branch
git checkout <your-branch-name>

# Pull latest changes from remote
git pull origin <your-branch-name>

# (Optional) Merge updates from main if needed
git merge main
```

### 2️⃣ Development Cycle
Work on your code, save, and test.

```bash
# Check changed files
git status

# Stage changes
git add .

# Commit with a clear message
git commit -m "feat: added new chart component"
```

### 3️⃣ Push Changes
Sync your work with the team.

```bash
# Push to your specific branch
git push origin <your-branch-name>
```

---

## 🤝 Making a Pull Request (PR)

1. Go to GitHub.
2. Switch to your branch.
3. Click **"Compare & pull request"**.
4. Set base branch to `architect-main-integration` (or `main` if ready).
5. Add reviewers from the team.
6. Merge only after approval!

---

## 🆘 Emergency Commands

**Mistake in commit?** (Soft reset - keeps changes)
```bash
git reset --soft HEAD~1
```

**Discard local changes?** (Dangerous!)
```bash
git checkout .
```

**Switch branch?**
```bash
git checkout <branch_name>
```

Happy Coding! 🚀
