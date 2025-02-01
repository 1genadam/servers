import os
import sys
import subprocess
from typing import Optional

def git_pull(repo_url: str, branch: str = "main", target_dir: Optional[str] = None) -> bool:
    """
    Pull code from a specific branch of a repository
    
    Args:
        repo_url (str): URL of the repository
        branch (str): Branch name (default: main)
        target_dir (str): Target directory for clone/pull (default: current directory)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
            os.chdir(target_dir)

        if not os.path.exists('.git'):
            # Clone if repository doesn't exist
            subprocess.run(['git', 'clone', '-b', branch, repo_url, '.'], check=True)
        else:
            # Fetch and checkout if repository exists
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            subprocess.run(['git', 'checkout', branch], check=True)
            subprocess.run(['git', 'pull', 'origin', branch], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pull code from any git repository and branch')
    parser.add_argument('repo_url', help='URL of the git repository')
    parser.add_argument('--branch', '-b', default='main', help='Branch to pull (default: main)')
    parser.add_argument('--dir', '-d', help='Target directory (default: current directory)')
    
    args = parser.parse_args()
    success = git_pull(args.repo_url, args.branch, args.dir)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()