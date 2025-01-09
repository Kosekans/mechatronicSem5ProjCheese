import os
import sys
import subprocess
import socket
import json
#automatically install required packages commented out for now, it doesn't work
#instead of <"updateSuccessful": updateSuccessful> its set to True for now
def setup():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_dir = os.path.join(base_dir, 'config')
    
    internetConnection = check_internet_connection()
    updateSuccessful = False
    if internetConnection:
        updateSuccessful = update_repository()
        '''
        if updateSuccessful:
            if not installSystemPackages():
                return False
            if not installPythonPackages():
                return False
        '''
    config_path = os.path.join(config_dir, 'setup_status.json')
    status = {
        "internetConnection": internetConnection,
        "updateSuccessful": True #updateSuccessful
    }
    with open(config_path, 'w') as config_file:
        json.dump(status, config_file)
    
    return True

def check_internet_connection():
    try:
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

def installSystemPackages():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        system_req_path = os.path.join(base_dir, 'config', 'requirementsSystem.txt')
        
        if not os.path.exists(system_req_path):
            print(f"System requirements file not found at: {system_req_path}")
            return False
    
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "--fix-broken", "install", "-y"])
        
        with open(system_req_path) as f:
            packages = [line.strip() for line in f if line.strip()]
        
        package_list = " ".join(packages)
        subprocess.check_call(f"sudo apt install -y {package_list}", shell=True)
            
        print("System packages installed successfully")
        return True
    except Exception as e:
        print(f"Failed to install system packages: {e}")
        return False

def installPythonPackages():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        requirements_path = os.path.join(base_dir, 'config', 'requirementsPython.txt')
        
        if not os.path.exists(requirements_path):
            print(f"Python requirements file not found at: {requirements_path}")
            return False

        subprocess.check_call(["sudo", "python3", "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call(["sudo", "python3", "-m", "pip", "install", "-r", requirements_path])
        
        print("Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python packages: {e}")
        return False

if __name__ == "__main__":
    success = setup()
    sys.exit(0 if success else 1)