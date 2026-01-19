"""
Setup verification script for Movie Recommendation System
Checks if all dependencies are installed and data files are present
"""

import sys
import os


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'scipy': 'scipy'
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is NOT installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them using: pip install -r requirements.txt")
        return False
    
    return True


def check_data_files():
    """Check if data files exist."""
    data_dir = "data"
    required_files = ["movies.csv", "ratings.csv"]
    
    if not os.path.exists(data_dir):
        print(f"❌ Data directory '{data_dir}' does not exist")
        return False
    
    print(f"✅ Data directory '{data_dir}' exists")
    
    missing_files = []
    for filename in required_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ {filename} exists ({file_size:,} bytes)")
        else:
            print(f"❌ {filename} is missing")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n⚠️  Missing data files: {', '.join(missing_files)}")
        print("Please download the MovieLens dataset and place the files in the data/ directory.")
        print("See data/README.md for instructions.")
        return False
    
    return True


def check_project_structure():
    """Check if project structure is correct."""
    required_dirs = ["recommender"]
    required_files = ["main.py", "requirements.txt", "README.md"]
    
    all_good = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' is missing")
            all_good = False
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ File '{file_name}' exists")
        else:
            print(f"❌ File '{file_name}' is missing")
            all_good = False
    
    # Check recommender module files
    recommender_files = [
        "__init__.py",
        "data_loader.py",
        "content_based.py",
        "collaborative.py",
        "utils.py"
    ]
    
    for file_name in recommender_files:
        filepath = os.path.join("recommender", file_name)
        if os.path.exists(filepath):
            print(f"✅ File 'recommender/{file_name}' exists")
        else:
            print(f"❌ File 'recommender/{file_name}' is missing")
            all_good = False
    
    return all_good


def main():
    """Run all verification checks."""
    print("="*60)
    print("Movie Recommendation System - Setup Verification")
    print("="*60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Data Files", check_data_files),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        result = check_func()
        results.append((name, result))
    
    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to use the recommendation system.")
        print("\nQuick start:")
        print("  python main.py --method content --movie \"Toy Story\"")
        print("  python main.py --method collaborative --user-id 1")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == '__main__':
    main()
