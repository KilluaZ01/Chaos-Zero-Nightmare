"""File and data management utilities"""

import os
import json
import subprocess
from datetime import datetime

from utils.paths import ASSETS_DIR

MAIN_PATH = "D:/Silver_Blood_Bot/"

def get_persistent_path(filename, subdir=None):
    """Get persistent file path in AppData
    
    Args:
        filename: Name of the file
        subdir: Optional subdirectory
        
    Returns:
        str: Full file path
    """
    base_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'ChaosZeroNightmare')
    if subdir:
        base_dir = os.path.join(base_dir, subdir)
    os.makedirs(base_dir, exist_ok=True)
    
    file_path = os.path.join(base_dir, filename)
    
    # Create empty batches.json if it doesn't exist
    if filename == "batches.json" and not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
        print(f"✅ Created empty {filename} at {file_path}")
    
    return file_path

def push_assets(instance_name):
    """Push specified assets to device using adb
    
    Args:
        instance_name: Name of the instance
    """

    push_cmd = (
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command "push {ASSETS_DIR} /sdcard/temp_extracted"'
    )
    
    move_cmd = (
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command "shell su -c \'cp -r /sdcard/temp_extracted/* /storage/emulated/0/Android/data/\'"'
    )

    r1 = subprocess.run(push_cmd, shell=True)
    if r1.returncode != 0:
        print(f"[{instance_name}] ❌ Failed to push external data.")
        return False, None
    
    r2 = subprocess.run(move_cmd, shell=True)
    if r2.returncode != 0:
        print(f"[{instance_name}] ❌ Failed to move external data.")
        return False, None
    
    print(f"[{instance_name}] ✅ Successfully pushed external data.")
    return True, None

def save_account_metadata(account):
    """Save account metadata to batches.json
    
    Args:
        account: Dictionary containing account information
    """
    accounts_file = get_persistent_path("batches.json")

    # Load existing accounts
    if os.path.exists(accounts_file):
        with open(accounts_file, "r", encoding="utf-8") as f:
            try:
                all_accounts = json.load(f)
            except json.JSONDecodeError:
                all_accounts = []
    else:
        all_accounts = []

    # Append new account
    all_accounts.append(account)

    # Save back
    with open(accounts_file, "w", encoding="utf-8") as f:
        json.dump(all_accounts, f, indent=2)

    print(f"✅ Account metadata saved for {account['instance_name']}")

def backup_account_data(instance_name, guest_name, log_func):
    """Create and save account backup
    
    Args:
        instance_name: Name of the instance
        guest_name: Guest account name
        log_func: Logging function
        
    Returns:
        tuple: (success: bool, backup_filename: str)
    """
    account_dir = f"{MAIN_PATH}accounts"
    os.makedirs(account_dir, exist_ok=True)

    safe_guest = guest_name
    safe_inst = instance_name
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_filename = f"{safe_guest}_{safe_inst}_{ts}.tar.gz"
    backup_path = os.path.join(account_dir, backup_filename)

    # Create tar backup
    make_tar_cmd = (
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command "shell su -c \'cd /data/data && '
        f'tar -czf /sdcard/{backup_filename} com.skystone.silverblood.us\'"'
    )
    
    pull_tar_cmd = (
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command "pull /sdcard/{backup_filename} {backup_path}"'
    )
    
    clean_tar_cmd = (
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command "shell rm /sdcard/{backup_filename}"'
    )

    r1 = subprocess.run(make_tar_cmd, shell=True)
    if r1.returncode != 0:
        log_func(f"[{instance_name}] ❌ Failed to create internal backup tar.")
        return False, None
    
    r2 = subprocess.run(pull_tar_cmd, shell=True)
    if r2.returncode != 0:
        log_func(f"[{instance_name}] ❌ Failed to pull backup from device.")
        return False, None
    
    subprocess.run(clean_tar_cmd, shell=True)
    log_func(f"[{instance_name}] 💾 Saved internal backup -> {backup_path}")
    
    return True, backup_filename