# Development Workflow Guide

## 🌿 Branch Strategy

Your repository now has two branches:

### `main` Branch (Production)
- **Purpose**: Production-ready code only
- **Deployment**: Automatically deployed to Google Cloud Run
- **Protection**: Should only receive code via Pull Requests from `development`
- **URL**: https://accessadvisr-932375520212.us-central1.run.app/

### `development` Branch (Active Development)
- **Purpose**: All new features and changes
- **Testing**: Test locally before merging to `main`
- **Current Branch**: ✅ You are here now!

---

## 📋 Daily Workflow

### 1. **Start Working (Always on development branch)**

```bash
# Make sure you're on development branch
git checkout development

# Get latest changes (if working with others)
git pull origin development
```

### 2. **Make Your Changes**

Edit any files you want:
- Add new features
- Fix bugs
- Update documentation
- Modify templates, views, models, etc.

### 3. **Test Locally**

```bash
# Run the development server
source venv/bin/activate
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and verify everything works.

### 4. **Commit Your Changes**

```bash
# See what files changed
git status

# Add files to commit
git add .

# Commit with a descriptive message
git commit -m "feat: Add new accessibility filter feature"
```

**Commit Message Conventions:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic change)
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 5. **Push to GitHub**

```bash
# Push to development branch
git push origin development
```

**Important**: This pushes to the `development` branch on GitHub, **NOT** to production!

---

## 🚀 Deploying to Production

When you're ready to deploy your changes to the live site:

### Option 1: Using GitHub (Recommended)

1. **Go to GitHub**: https://github.com/TeddyJubu/Accessadvisr
2. **Click "Pull Requests"** tab
3. **Click "New Pull Request"**
4. **Set**:
   - Base: `main` (where changes will go)
   - Compare: `development` (where changes come from)
5. **Review the changes** in the diff view
6. **Click "Create Pull Request"**
7. **Add a description** of what changed
8. **Click "Merge Pull Request"** when ready
9. **Delete the branch** (optional, or keep it for future PRs)

### Option 2: Using Command Line

```bash
# Switch to main branch
git checkout main

# Merge development into main
git merge development

# Push to GitHub
git push origin main

# Switch back to development
git checkout development
```

### Step 3: Deploy to Google Cloud Run

After merging to `main`, deploy to production:

```bash
# Make sure you're on main branch
git checkout main

# Deploy to Cloud Run
gcloud run deploy accessadvisr \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PRODUCTION=True,DEBUG=False,DJANGO_SECRET_KEY=access-advisr-prod-secret-9a7b1,GOOGLE_MAPS_BROWSER_KEY=AIzaSyDHcj7wVmd4QzftOAniu-BWQbmPpUBHDs4,GOOGLE_MAPS_SERVER_KEY=AIzaSyBjsGX8c9Ic-QQoaA5jzdhv-r9j6QOHsUY \
  --add-cloudsql-instances accessadvisr-prod-9a7b1:us-central1:accessadvisr-db \
  --project accessadvisr-prod-9a7b1

# Switch back to development
git checkout development
```

---

## 🔍 Checking Your Current Branch

```bash
# See which branch you're on
git branch

# See all branches (local and remote)
git branch -a
```

The branch with `*` is your current branch.

---

## 🛡️ Branch Protection (Optional but Recommended)

To prevent accidental pushes to `main`:

1. Go to: https://github.com/TeddyJubu/Accessadvisr/settings/branches
2. Click **"Add rule"**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (if working with a team)
5. Click **"Create"**

This ensures all changes to `main` go through Pull Requests.

---

## 📊 Workflow Diagram

```
development branch (your daily work)
    │
    │ (make changes, test locally)
    │
    ├─ git add .
    ├─ git commit -m "message"
    ├─ git push origin development
    │
    │ (when ready for production)
    │
    ├─ Create Pull Request on GitHub
    │   OR
    ├─ git checkout main
    ├─ git merge development
    ├─ git push origin main
    │
    ├─ Deploy to Cloud Run
    │
    └─ git checkout development (back to work!)
```

---

## 🎯 Quick Reference

### Common Commands

```bash
# Check current branch
git branch

# Switch to development
git checkout development

# Switch to main
git checkout main

# Create a new feature branch (advanced)
git checkout -b feature/new-feature

# See what changed
git status
git diff

# Undo uncommitted changes
git checkout -- filename.py

# See commit history
git log --oneline
```

### Current Status

- ✅ **Current Branch**: `development`
- ✅ **Production Branch**: `main`
- ✅ **Remote Repository**: https://github.com/TeddyJubu/Accessadvisr
- ✅ **Live Site**: https://accessadvisr-932375520212.us-central1.run.app/

---

## 💡 Best Practices

1. **Always work on `development`** - Never commit directly to `main`
2. **Test before merging** - Run the app locally and verify everything works
3. **Write clear commit messages** - Future you will thank you
4. **Commit often** - Small, focused commits are better than large ones
5. **Pull before push** - If working with others, always `git pull` first
6. **Review your changes** - Use `git diff` before committing
7. **Keep branches in sync** - Regularly merge `main` into `development` if others are deploying

---

## 🆘 Troubleshooting

### "I'm on the wrong branch!"

```bash
# Switch to development
git checkout development
```

### "I committed to main by accident!"

```bash
# If you haven't pushed yet
git reset --soft HEAD~1  # Undo last commit, keep changes
git checkout development
git add .
git commit -m "your message"
```

### "I want to discard all my changes"

```bash
git checkout -- .  # Discard all uncommitted changes
```

### "I need to see what's different between branches"

```bash
git diff main..development
```

---

## 🎓 Next Steps

1. **Make a test change** to verify the workflow:
   ```bash
   # Edit any file (e.g., README.md)
   git add .
   git commit -m "test: Verify development workflow"
   git push origin development
   ```

2. **Check GitHub** to see your commit on the `development` branch

3. **When ready**, create a Pull Request to merge to `main`

4. **After merging**, deploy to Cloud Run

---

**You're all set!** 🎉

Your changes on the `development` branch will stay local/on GitHub until you explicitly merge them to `main` and deploy to Cloud Run.
