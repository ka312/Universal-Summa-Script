import pkg_resources
import subprocess
import sys

def get_installed_packages():
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def check_and_install_requirements():
    required_packages = {
        'flask': '2.0.1',
        'openai': '1.3.0',
        'yt-dlp': '2023.11.16',
        'pydub': '0.25.1',
        'ffmpeg-python': '0.2.0',
        'python-dotenv': '0.19.0'
    }
    
    installed_packages = get_installed_packages()
    packages_to_install = []
    
    print("\nChecking installed packages...")
    for package, version in required_packages.items():
        if package in installed_packages:
            print(f"✓ {package} is already installed (version {installed_packages[package]})")
        else:
            print(f"✗ {package} needs to be installed (required version {version})")
            packages_to_install.append(f"{package}=={version}")
    
    if packages_to_install:
        print("\nInstalling missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages_to_install)
            print("\nAll missing packages have been installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"\nError installing packages: {e}")
    else:
        print("\nAll required packages are already installed!")

if __name__ == "__main__":
    check_and_install_requirements()
