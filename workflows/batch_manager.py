"""Batch preparation and execution"""

import os
import time
import threading

from random import randint

from macros.game_actions import clone_instance, launch_instance

from utils.instance_manager import install_apk_threaded, generate_guest_name
from utils.paths import PACKAGE_NAME
from utils.file_manager import backup_account_data, push_assets

from .game_progression import get_game_steps, execute_macro_steps
from .account_setup import validate_accounts

def prepare_batch(batch_num, instances_per_batch, base_instance, log_func):
    """Prepare a batch of instances
    
    Args:
        batch_num: Batch number
        instances_per_batch: Number of instances in this batch
        base_instance: Base name for instances
        log_func: Logging function
        
    Returns:
        list: List of created instance names
    """
    instance_names = []
    unique_num = randint(0, 1000)

    for i in range(instances_per_batch):
        # Create unique instance name
        new_name = f"{base_instance}-{(batch_num - 1) * instances_per_batch + i + 1}-{unique_num}"
        
        # Create instance
        # log_func(f"📦 Creating new instance: {new_name}")
        # os.system(f'ldconsole add --name {new_name} --resolution 1280,720,240')

        # Enable ADB debug
        # log_func(f"🔧 Enabling ADB Debug for {new_name}")
        # adb_debugger()

        log_func(f"Cloned instance: {new_name}")
        clone_instance(base_instance, new_name)

        # Launch instance
        log_func(f"🚀 Launching {new_name}")
        launch_instance(new_name)
        
        instance_names.append(new_name)
    
    return instance_names

def run_all_batches(base_instance, total_accounts, instances_per_batch, log_func, pause_event):
    """
    Run all batches sequentially
    
    Args:
        base_instance: Base name for instances
        total_accounts: Total number of accounts to create
        instances_per_batch: Number of instances per batch
        guest_name: Prefix for guest names
        log_func: Logging function
        pause_event: Threading event for pause control
    """

    total_batches = total_accounts // instances_per_batch
    guest_index = 1

    for batch in range(1, total_batches + 1):
        log_func(f"🚀 Starting batch {batch}")
        run_batch(batch, instances_per_batch, log_func, base_instance, pause_event)
        guest_index += instances_per_batch

def run_batch(batch_num, instances_per_batch, log_func, base_instance, pause_event):
    """Run a complete batch workflow
    
    Args:
        batch_num: Batch number
        instances_per_batch: Number of instances in batch
        log_func: Logging function
        base_instance: Base instance name
        pause_event: Threading event for pause control
    """
    # Prepare instances
    instance_names = prepare_batch(batch_num, instances_per_batch, base_instance, log_func)
    log_func(f"🛠️ Prepared batch {batch_num} with {len(instance_names)} instances")

    if instances_per_batch > 5:
        time.sleep(240)
    elif instances_per_batch > 3:
        time.sleep(150)
    else:
        time.sleep(100)


    # Generate guest data
    guest_data = []
    for i, instance_name in enumerate(instance_names):
        guest_name = generate_guest_name()
        guest_data.append((instance_name, guest_name))
        log_func(f"[{instance_name}] Guest: {guest_name}")

    # Install APKs
    # apk_dir = APK_DIR
    # 
    # apk_files = [
    #     "com.smilegate.chaoszero.stove.google.apk",
    #     "config.arm64_v8a.apk",
    #     "config.xhdpi.apk",
    #     "config.en.apk"
    # ]
    # 
    # apk_paths = " ".join([f"{apk_dir}/{apk}" for apk in apk_files])
    # 
    # install_apk_threaded(instance_names, apk_paths, log_func)
    # time.sleep(10)

    # Clear app data
    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell pm clear {PACKAGE_NAME}"')

    # Push external assets
    threads = []

    for instance_name, _ in guest_data:
        t = threading.Thread(target=push_assets, args=(instance_name,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    log_func("All external assets pushed to all instances.")

    # Launch game
    for instance_name, _ in guest_data:
        os.system(
            f'ldconsole.exe adb --name "{instance_name}" '
            f'--command "shell monkey -p {PACKAGE_NAME} '
            f'-c android.intent.category.LAUNCHER 1"'
        )
        log_func(f"[{instance_name}] - Launched Chaos Zero Nightmare")
    time.sleep(70)

    # Execute game steps
    steps = get_game_steps()
    execute_macro_steps(guest_data, steps, log_func, pause_event)

    # Validate accounts
    validate_accounts(guest_data, log_func)

    log_func(f"✅ Batch {batch_num} completed")