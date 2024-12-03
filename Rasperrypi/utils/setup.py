import os
import sys
import subprocess
import socket
import shutil
import filecmp
import json

def install_requirementsB():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        system_req_path = os.path.join(base_dir, 'config', 'requirementsB.txt')
        
        if os.path.exists(system_req_path):
            with open(system_req_path) as f:
                packages = [line.strip() for line in f if line.strip()]
            
            # Force architecture for Raspberry Pi
            subprocess.check_call(["sudo", "dpkg", "--add-architecture", "armhf"])
            subprocess.check_call(["sudo", "apt", "update"])
            
            # Install each package with explicit confirmation
            for package in packages:
                try:
                    subprocess.check_call(["sudo", "apt", "install", "-y", "--fix-missing", package])
                except subprocess.CalledProcessError:
                    print(f"Failed to install {package}, continuing...")
                    continue
        print("System requirements installed")
        return True
    except Exception as e:
        print(f"Failed to install system requirements: {e}")
        return False

def install_requirements():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        requirements_path = os.path.join(base_dir, 'config', 'requirements.txt')
        
        if not os.path.exists(requirements_path):
            print(f"Requirements file not found at: {requirements_path}")
            return False

        # Install globally with sudo to ensure proper permissions
        subprocess.check_call(["sudo", sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call(["sudo", sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", requirements_path])
        print("Python requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False

def setup():
    # Get correct config path (one level up from utils)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_dir = os.path.join(base_dir, 'config')
    
    # Update the repository to the latest version
    internetConnection: bool = check_internet_connection()
    updateSuccessful: bool = False
    if internetConnection:
        updateSuccessful = update_repository()
        if updateSuccessful and requirements_changed():
            # Install system packages first
            if not install_requirementsB():
                print("Failed to install system requirements")
                return False
            # Then install Python packages
            if not install_requirements():
                print("Failed to install Python requirements")
                return False
            save_requirements()
            
    config_path = os.path.join(config_dir, 'setup_status.json')
    status = {
        "internetConnection": internetConnection,
        "updateSuccessful": updateSuccessful
    }
    with open(config_path, 'w') as config_file:
        json.dump(status, config_file)

def check_internet_connection():
    try:
        # Connect to a well-known host (Google DNS) to check for internet connection
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        print("Internet connection found")
        return True
    except OSError:
        print("No internet connection found")
        return False

def update_repository():
    try:
        subprocess.check_call(["git", "pull"])
        print("Repository updated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to update repository: {e}")
        return False

def requirements_changed():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    current_requirements = os.path.join(base_dir, 'config', 'requirements.txt')
    saved_requirements = os.path.join(base_dir, 'config', 'requirements_saved.txt')
    
    if not os.path.exists(saved_requirements):
        return True
    
    return not filecmp.cmp(current_requirements, saved_requirements, shallow=False)

def save_requirements():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    current_requirements = os.path.join(base_dir, 'config', 'requirements.txt')
    saved_requirements = os.path.join(base_dir, 'config', 'requirements_saved.txt')
    shutil.copyfile(current_requirements, saved_requirements)

if __name__ == "__main__":
    setup()