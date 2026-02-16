#!/usr/bin/env python3
"""
GitHub Push Automation Script
Automatically pushes local projects to GitHub without using the web interface.
"""

import os
import subprocess
import sys
from datetime import datetime


def run_command(command, check=True, capture_output=False):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e.stderr if capture_output else str(e)}")
        return None


def is_git_initialized():
    """Check if the current directory is a git repository."""
    return os.path.isdir('.git')


def get_user_input():
    """Get repository details from user."""
    print("\n=== GitHub Repository Setup ===\n")
    
    repo_name = input("Enter repository name: ").strip()
    if not repo_name:
        print("Repository name cannot be empty!")
        sys.exit(1)
    
    description = input("Enter repository description (optional): ").strip()
    if not description:
        description = "Created via automated script"
    
    visibility = input("Make repository public or private? (public/private) [private]: ").strip().lower()
    if visibility not in ['public', 'private']:
        visibility = 'private'
    
    return repo_name, description, visibility


def initialize_and_push_new_repo(repo_name, description, visibility):
    """Initialize git, create GitHub repo, and push."""
    print("\n🚀 Initializing new repository...\n")
    
    # Initialize git
    print("📦 Initializing git...")
    if not run_command("git init"):
        return False
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists('.gitignore'):
        print("📝 Creating basic .gitignore...")
        with open('.gitignore', 'w') as f:
            f.write("# Python\n__pycache__/\n*.py[cod]\n*.so\n.Python\nvenv/\nENV/\n\n")
            f.write("# Java\ntarget/\n*.class\n*.jar\n*.war\n\n")
            f.write("# IDE\n.idea/\n.vscode/\n*.swp\n*.swo\n\n")
            f.write("# OS\n.DS_Store\nThumbs.db\n")
    
    # Add all files
    print("➕ Adding files to git...")
    if not run_command("git add ."):
        return False
    
    # Create initial commit
    commit_message = f"Initial commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"💾 Creating commit: {commit_message}")
    if not run_command(f'git commit -m "{commit_message}"'):
        return False
    
    # Rename branch to main if needed
    print("🌿 Setting branch to main...")
    run_command("git branch -M main")
    
    # Create GitHub repository using gh CLI
    print(f"\n🌐 Creating GitHub repository '{repo_name}'...")
    visibility_flag = "--public" if visibility == "public" else "--private"
    gh_command = f'gh repo create {repo_name} {visibility_flag} --source=. --description "{description}" --push'
    
    result = run_command(gh_command, capture_output=True)
    if result and result.returncode == 0:
        print(f"\n✅ Repository created and pushed successfully!")
        print(f"🔗 Repository URL: https://github.com/$(gh api user --jq .login)/{repo_name}")
        return True
    else:
        print("\n❌ Failed to create repository. Make sure GitHub CLI is installed and authenticated.")
        print("Run 'gh auth login' to authenticate.")
        return False


def push_existing_repo():
    """Push uncommitted changes to existing repository."""
    print("\n🔄 Existing repository detected...\n")
    
    # Check if there are any changes
    status = run_command("git status --porcelain", capture_output=True)
    if not status or not status.stdout.strip():
        print("✨ No changes to commit. Repository is up to date!")
        
        # Try to push anyway in case there are unpushed commits
        print("\n📤 Checking for unpushed commits...")
        result = run_command("git push", check=False, capture_output=True)
        if result and result.returncode == 0:
            print("✅ All commits are synced with remote!")
        else:
            print("ℹ️  Nothing to push or no remote configured.")
        return True
    
    # Add all changes
    print("➕ Adding changes...")
    if not run_command("git add ."):
        return False
    
    # Create commit with timestamp
    commit_message = f"Update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"💾 Creating commit: {commit_message}")
    if not run_command(f'git commit -m "{commit_message}"'):
        return False
    
    # Push to main branch
    print("📤 Pushing to GitHub...")
    result = run_command("git push origin main", check=False, capture_output=True)
    
    if result and result.returncode == 0:
        print("\n✅ Changes pushed successfully!")
        return True
    else:
        # Try without specifying origin main
        print("⚠️  Trying alternative push method...")
        result = run_command("git push", check=False, capture_output=True)
        if result and result.returncode == 0:
            print("\n✅ Changes pushed successfully!")
            return True
        else:
            print("\n❌ Failed to push. Error:")
            print(result.stderr if result else "Unknown error")
            return False


def main():
    """Main execution function."""
    print("╔════════════════════════════════════════════╗")
    print("║   GitHub Auto-Push Script                 ║")
    print("╚════════════════════════════════════════════╝")
    
    # Check if gh CLI is installed
    gh_check = run_command("which gh", check=False, capture_output=True)
    if not gh_check or not gh_check.stdout.strip():
        print("\n⚠️  Warning: GitHub CLI (gh) not found!")
        print("Install it from: https://cli.github.com/")
        print("After installation, run: gh auth login")
        sys.exit(1)
    
    if is_git_initialized():
        # Repository already exists, just push changes
        success = push_existing_repo()
    else:
        # New repository, get details and initialize
        repo_name, description, visibility = get_user_input()
        success = initialize_and_push_new_repo(repo_name, description, visibility)
    
    if success:
        print("\n🎉 All done!\n")
    else:
        print("\n😞 Operation failed. Please check the errors above.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
