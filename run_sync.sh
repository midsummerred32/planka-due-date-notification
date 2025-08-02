
#!/bin/bash

# Planka Task Checker - Sync and Run Script
# This script ensures the local repository is in sync with GitHub before running the task checker

set -e  # Exit on any error

echo "🔄 Starting Planka Task Checker sync and run process..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please initialize git first."
    exit 1
fi

# Fetch latest changes from remote
echo "📡 Fetching latest changes from GitHub..."
git fetch origin

# Get current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $CURRENT_BRANCH"

# Check if we have uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes. Stashing them..."
    git stash push -m "Auto-stash before sync - $(date)"
    STASHED=true
else
    STASHED=false
fi

# Check if there are any changes to pull
CHANGES_AVAILABLE=$(git rev-list HEAD...origin/$CURRENT_BRANCH --count)

if [ "$CHANGES_AVAILABLE" -gt 0 ]; then
    echo "🔄 Found $CHANGES_AVAILABLE new commit(s) on GitHub"
    
    # Pull latest changes
    echo "⬇️  Pulling latest changes from origin/$CURRENT_BRANCH..."
    if git pull origin "$CURRENT_BRANCH"; then
        echo "✅ Successfully synced with GitHub"
        echo ""
        echo "🚨 IMPORTANT: New changes have been pulled from GitHub!"
        echo "   Please rerun this script to ensure you're using the latest version:"
        echo "   ./run_sync.sh"
        echo ""
        
        # Restore stashed changes if any
        if [ "$STASHED" = true ]; then
            echo "🔄 Restoring your stashed changes..."
            if git stash pop; then
                echo "✅ Stashed changes restored successfully"
            else
                echo "⚠️  Warning: Could not restore stashed changes automatically"
                echo "   Run 'git stash list' and 'git stash pop' manually if needed"
            fi
        fi
        
        exit 2  # Exit with code 2 to indicate updates were pulled
    else
        echo "❌ Failed to pull changes from GitHub"
        if [ "$STASHED" = true ]; then
            echo "🔄 Restoring your stashed changes..."
            git stash pop
        fi
        exit 1
    fi
else
    echo "✅ Already up to date with GitHub"
fi

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    echo "🔄 Restoring your stashed changes..."
    if git stash pop; then
        echo "✅ Stashed changes restored successfully"
    else
        echo "⚠️  Warning: Could not restore stashed changes automatically"
        echo "   Run 'git stash list' and 'git stash pop' manually if needed"
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create one based on .env.example"
    echo "   Copy .env.example to .env and configure your settings"
    exit 1
fi

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "📦 Found uv package manager, ensuring dependencies are synced..."
    uv sync
    echo "🚀 Running Planka task checker with uv..."
    uv run python main.py
else
    echo "⚠️  uv not found, falling back to python3..."
    echo "🚀 Running Planka task checker..."
    python3 main.py
fi

echo "✅ Planka task checker completed successfully!"
