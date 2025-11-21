"""Game-specific actions"""

import os
import time

from macros.basic_actions import input_macro, tap_macro
from utils.screenshot_utils import check_template, find_coordinates
from utils.paths import MAIN_PATH, LUCK_NAME, PACKAGE_NAME, TEMPLATE_DIR

def launch_instance(instance_name):
    """Launch the LDPlayer instance"""
    os.system(f'ldconsole.exe launch --name "{instance_name}"')

def clone_instance(source_instance, target_instance):
    """Clone an LDPlayer instance"""
    os.system(f'ldconsole.exe copy --name "{target_instance}" --from "{source_instance}"')

def close_instance(instance_name):
    """Close the LDPlayer instance"""
    os.system(f'ldconsole.exe quit --name {instance_name}')

def delete_instance(instance_name):
    """Delete the LDPlayer instance"""
    os.system(f'ldconsole.exe remove --name {instance_name}')
    
def close_game(instance_name, *args):
    """Force close the game application
    
    Args:
        instance_name: Name of the LDPlayer instance
    """
    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell am force-stop com.skystone.silverblood.us"')

def open_luck(instance_name, luck_key, *args):
    """Launch the luck application
    
    Args:
        instance_name: Name of the LDPlayer instance
    """
    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p {LUCK_NAME} -c android.intent.category.LAUNCHER 1"')
    time.sleep(18)

    tap_macro(instance_name, 500, 270)
    time.sleep(5)

    for i in range(16):
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell input keyevent DEL"')

    input_macro(instance_name, luck_key)
    time.sleep(6)

    tap_macro(instance_name, 230, 350)      # Done
    time.sleep(3)

    tap_macro(instance_name, 582, 821)
    time.sleep(4)

    tap_macro(instance_name, 545, 733)
    time.sleep(14)

    tap_macro(instance_name, 32, 254)
    time.sleep(3)

    tap_macro(instance_name, 32, 356)
    time.sleep(3)

    tap_macro(instance_name, 364, 886)
    time.sleep(6)

    tap_macro(instance_name, 545, 733)
    time.sleep(10)

    template_path = f"{TEMPLATE_DIR}/luck_checker.png"
    for i in range(3):
        if check_template(instance_name, template_path, threshold=0.8):
            tap_macro(instance_name, 545, 733)
            time.sleep(10)
            break
        else:
            time.sleep(5)

    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1"')
    time.sleep(20)

def open_game(instance_name, *args):
    """Launch the game application
    
    Args:
        instance_name: Name of the LDPlayer instance
    """
    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1"')

def tap_if_regular_summon(instance_name, *args):
    """Check for regular summon banner and tap if found
    
    Args:
        instance_name: Name of the LDPlayer instance
    """
    from .basic_actions import tap_macro
    
    template_path = f"{MAIN_PATH}templates/regular_summon_template.png"
    print(f"[{instance_name}] 📸 Taking screenshot to detect regular summon...")

    match_coords = find_coordinates(instance_name, template_path)
    if match_coords:
        x, y = match_coords
        print(f"[{instance_name}] 🎯 Found regular summon at ({x}, {y}) — tapping")
        tap_macro(instance_name, x, y)
    else:
        print(f"[{instance_name}] ❌ Could not find regular summon banner")