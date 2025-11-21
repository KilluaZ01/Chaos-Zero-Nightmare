"""Account setup and validation"""

import os
from datetime import datetime

from utils.file_manager import save_account_metadata, backup_account_data
from utils.screenshot_utils import check_template
from utils.paths import SCREENSHOT_DIR_FINAL, TEMPLATE_DIR, SCREENSHOT_DIR

from macros.game_actions import close_instance, delete_instance
from macros.basic_actions import input_macro


import time

def setup_guest_accounts(guest_data, log_func):
    """Input guest names for all accounts
    
    Args:
        guest_data: List of (instance_name, guest_name) tuples
        log_func: Logging function
    """
    for instance_name, guest_name, luck_code in guest_data:
        input_macro(instance_name, guest_name)
        log_func(f"[{instance_name}] Input guest name: {guest_name}")


def validate_accounts(guest_data, log_func):
    """Validate accounts and save successful ones
    
    Args:
        guest_data: List of (instance_name, guest_name, luck_code) tuples
        log_func: Logging function
        
    Returns:
        tuple: (valid_instances, valid_guest_names)
    """
    template_path = f"{TEMPLATE_DIR}/validate_end.png"
    final_dir = SCREENSHOT_DIR_FINAL
    valid_instances = []
    valid_guest_names = []

    for instance_name, guest_name, luck_code in guest_data:
        log_func(f"[{instance_name}] Taking screenshot for {guest_name}")

        if check_template(instance_name, template_path, final_dir, threshold=0.80):
            log_func(f"[{instance_name}] ✅ Successfully reached login reward screen.")

            # Backup account data
            success, backup_filename = backup_account_data(instance_name, guest_name, log_func)
            
            if success:
                # Save metadata
                save_account_metadata({
                    "instance_name": instance_name,
                    "guest_name": guest_name,
                    "backup_file": backup_filename,
                    "login_day": 1,
                    "last_login": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Active"
                })

                valid_instances.append(instance_name)
                valid_guest_names.append(guest_name)
        else:
            log_func(f"[{instance_name}] ❌ Failed to reach reward screen. Closing and deleting.")

            # Cleanup screenshots
            for day_file in os.listdir(SCREENSHOT_DIR):
                if day_file.startswith(instance_name):
                    try:
                        os.remove(os.path.join(SCREENSHOT_DIR, day_file))
                    except Exception as e:
                        pass
            
            for day_file in os.listdir(SCREENSHOT_DIR_FINAL):
                if day_file.startswith(instance_name):
                    try:
                        os.remove(os.path.join(SCREENSHOT_DIR_FINAL, day_file))
                    except Exception as e:
                        pass

            close_instance(instance_name)
            time.sleep(10)
            delete_instance(instance_name)

    # Cleanup valid instances
    for instance_name in valid_instances:
        log_func(f"[{instance_name}] Closing & deleting instance")
        try:
            close_instance(instance_name)
        except Exception:
            pass
        time.sleep(8)
        delete_instance(instance_name)

    return valid_instances, valid_guest_names