# 🚀 Team Onboarding & Git Instructions

Welcome to the team! Our hackathon repository is ready. Follow these steps to get started.

## 1️⃣ Cloning the Repository

Open your terminal and run:

```bash
git clone https://github.com/samairax/hackathon-repo.git
cd hackathon-repo
```
*(Replace the URL with the actual repo URL if different, but this is standard format)*

## 2️⃣ Fetching All Branches

Ensure you have all the latest branches from the team:

```bash
git fetch --all
```

## 3️⃣ Switching to Your Assigned Branch

Identify your role and switch to the corresponding branch:

| Role | Branch Name | Command |
|------|------------|---------|
| **Architect / Lead** | `architect-main-integration` | `git checkout architect-main-integration` |
| **Frontend Dev** | `frontend-ui-dashboard` | `git checkout frontend-ui-dashboard` |
| **Backend Dev** | `backend-api-agents` | `git checkout backend-api-agents` |
| **AI / Data Engineer** | `data-ai-models` | `git checkout data-ai-models` |

## 4️⃣ Daily Workflow (Commit & Push)

1. **Pull latest changes** (always do this first!):
   ```bash
   git pull origin <your-branch-name>
   ```

2. **Make your changes** in the code.

3. **Stage and Commit**:
   ```bash
   git add .
   git commit -m "feat: added login page layout"
   ```

4. **Push to GitHub**:
   ```bash
   git push origin <your-branch-name>
   ```

## ⚠️ Important Rules

- **NEVER push to `main` directly.**
- Work **ONLY** in your assigned branch.
- If you need to merge, open a **Pull Request (PR)** on GitHub.

Happy Hacking! 💻🔥
