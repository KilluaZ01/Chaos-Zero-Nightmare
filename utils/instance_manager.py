"""LDPlayer instance management utilities"""

import os
import subprocess
import threading
import time
from random import randint
from utils.paths import CONFIG_PATH

def adb_debugger():
    """Enable ADB debugging for the specified instance
    """

    for filename in os.listdir(CONFIG_PATH):
        if filename.startswith("leidian") and filename.endswith(".config") and filename != "leidians.config":
            file_path = os.path.join(CONFIG_PATH, filename)
            # print(f"Processing {filename}...")

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Skip if adbDebug already present
            if '"basicSettings.adbDebug"' in content:
                # print("  ADB already enabled, skipping.")
                continue

            # Split into lines without extra empty ones
            lines = [line.rstrip() for line in content.splitlines()]

            new_lines = []
            adb_added = False
            for line in lines:
                new_lines.append(line)
                if '"propertySettings.macAddress"' in line and not adb_added:
                    new_lines.append('    "basicSettings.adbDebug": 1,')
                    new_lines.append('    "basicSettings.rootMode": true,')
                    adb_added = True

            if adb_added:
                # Join with CRLF, remove consecutive blank lines
                clean_content = []
                prev_blank = False
                for line in new_lines:
                    if line.strip() == "":
                        if prev_blank:
                            continue
                        prev_blank = True
                    else:
                        prev_blank = False
                    clean_content.append(line)

                new_content = "\r\n".join(clean_content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                # print("  adbDebug added.")
            else:
                # print("  macAddress not found — skipped.")
                pass
            
def is_process_running(process_name):
    """Check if a process is currently running
    
    Args:
        process_name: Name of the process to check
        
    Returns:
        bool: True if process is running, False otherwise
    """
    try:
        output = subprocess.check_output(
            f'tasklist /FI "IMAGENAME eq {process_name}"',
            shell=True
        ).decode()
        return process_name.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False


def generate_guest_name():
    """
        Generate a random guest name
    """
    guest_list = ["Alph", "Brav", "Char", "Delt", "Echo", "Fot",
                  "Golf", "Hote", "Indi", "Juli", "Kilo", "Lima"]
    
    guest_name = f"{guest_list[randint(0, len(guest_list) - 1)]}{randint(100, 999)}"

    return guest_name

def install_apk_threaded(instance_names, apk_paths, log_func, timeout=200, max_retries=3):
    """Install APKs on multiple instances using threading
    
    Args:
        instance_names: List of instance names
        apk_paths: Space-separated APK file paths
        log_func: Logging function
        timeout: Installation timeout in seconds
        max_retries: Maximum number of retry attempts
    """
    def install_apk(instance_name):
        for attempt in range(1, max_retries + 1):
            command = f'ldconsole.exe adb --name "{instance_name}" --command "install-multiple {apk_paths}"'
            try:
                subprocess.run(command, shell=True, timeout=timeout)
                print(f"[{instance_name}] APK installed successfully on attempt {attempt}.")
                return
            except subprocess.TimeoutExpired:
                print(f"[{instance_name}] APK install timed out on attempt {attempt}. Retrying...")
            except Exception as e:
                print(f"[{instance_name}] APK install failed: {e}. Retrying...")
            time.sleep(3)

        print(f"[{instance_name}] APK install failed after {max_retries} attempts.")

    threads = []
    for instance_name in instance_names:
        t = threading.Thread(target=install_apk, args=(instance_name,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()