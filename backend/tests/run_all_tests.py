"""
Run all tests and generate coverage report
"""
import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests with pytest"""
    print("=" * 60)
    print("Running Test Suite")
    print("=" * 60)
    
    test_dir = Path(__file__).parent
    
    try:
        result = subprocess.run(
            ["pytest", str(test_dir), "-v", "--tb=short"],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠ pytest not found. Install with: pip install pytest")
        return False

def run_with_coverage():
    """Run tests with coverage report"""
    print("=" * 60)
    print("Running Tests with Coverage")
    print("=" * 60)
    
    test_dir = Path(__file__).parent
    project_root = test_dir.parent
    
    try:
        result = subprocess.run(
            [
                "pytest",
                str(test_dir),
                "--cov", str(project_root),
                "--cov-report", "term-missing",
                "--cov-report", "html",
                "-v"
            ],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print("\n✓ Coverage report generated in htmlcov/")
        
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠ pytest-cov not found. Install with: pip install pytest-cov")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        success = run_with_coverage()
    else:
        success = run_tests()
    
    sys.exit(0 if success else 1)

