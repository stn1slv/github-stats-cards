#!/usr/bin/env python3
"""
Installation and functionality verification script.
Run this after installing to verify everything works correctly.
"""

import sys
import subprocess
from pathlib import Path


def check_command(cmd: str, description: str, flag: str = "--version") -> bool:
    """Check if a command exists and can be run."""
    try:
        result = subprocess.run(
            [cmd, flag],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            print(f"✅ {description}: Available")
            return True
        else:
            print(f"❌ {description}: Error (exit code {result.returncode})")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ {description}: Not found or error ({type(e).__name__})")
        return False


def check_import(module: str, description: str) -> bool:
    """Check if a Python module can be imported."""
    try:
        __import__(module)
        print(f"✅ {description}: Importable")
        return True
    except ImportError as e:
        print(f"❌ {description}: {e}")
        return False


def check_file(filepath: Path, description: str) -> bool:
    """Check if a file exists."""
    if filepath.exists():
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Not found")
        return False


def main():
    """Run all verification checks."""
    print("🔍 GitHub Stats Card - Installation Verification\n")
    
    checks = []
    
    # Check Python version
    print("📦 Python Environment:")
    py_version = sys.version_info
    if py_version >= (3, 13):
        print(f"✅ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
        checks.append(True)
    else:
        print(f"❌ Python version: {py_version.major}.{py_version.minor}.{py_version.micro} (requires 3.13+)")
        checks.append(False)
    
    # Check commands
    print("\n🛠️  Command Line Tools:")
    checks.append(check_command("github-stats-card", "CLI tool", "--help"))
    checks.append(check_command("uv", "uv package manager", "--version"))
    
    # Check imports
    print("\n📚 Python Modules:")
    checks.append(check_import("src", "Main package"))
    checks.append(check_import("src.cli", "CLI module"))
    checks.append(check_import("src.fetcher", "Fetcher module"))
    checks.append(check_import("src.rank", "Rank module"))
    checks.append(check_import("src.stats_card", "Stats card module"))
    checks.append(check_import("requests", "requests library"))
    checks.append(check_import("click", "click library"))
    
    # Check files
    print("\n📄 Project Files:")
    base_path = Path(__file__).parent
    checks.append(check_file(base_path / "README.md", "README"))
    checks.append(check_file(base_path / "pyproject.toml", "pyproject.toml"))
    checks.append(check_file(base_path / "src" / "__init__.py", "Package init"))
    
    # Run quick test
    print("\n🧪 Quick Functionality Test:")
    try:
        from src.rank import calculate_rank
        result = calculate_rank(
            commits=1000,
            prs=100,
            issues=50,
            reviews=10,
            stars=200,
            followers=50,
        )
        if "level" in result and "percentile" in result:
            print(f"✅ Rank calculation: Works (Level: {result['level']})")
            checks.append(True)
        else:
            print("❌ Rank calculation: Invalid result")
            checks.append(False)
    except Exception as e:
        print(f"❌ Rank calculation: {e}")
        checks.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})")
        print("\n🎉 Installation verified successfully!")
        print("\nNext steps:")
        print("  1. Set GITHUB_TOKEN: export GITHUB_TOKEN=ghp_xxxxx")
        print("  2. Generate a card: github-stats-card -u yourusername -o stats.svg")
        print("  3. See QUICKSTART.md for more examples")
        return 0
    else:
        print(f"⚠️  Some checks failed ({passed}/{total})")
        print("\nPlease review the errors above and:")
        print("  1. Make sure you ran: uv pip install -e .")
        print("  2. Activate the virtual environment: source .venv/bin/activate")
        print("  3. Check Python version: python --version")
        return 1


if __name__ == "__main__":
    sys.exit(main())
