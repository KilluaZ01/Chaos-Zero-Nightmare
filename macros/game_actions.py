"""Game-specific actions"""

import os
from utils.screenshot_utils import find_coordinates
from utils.paths import MAIN_PATH

def launch_instance(instance_name):
    """Launch the LDPlayer instance"""
    os.system(f'ldconsole.exe launch --name "{instance_name}"')

def close_instance(instance_name):
    """Close the LDPlayer instance"""
    os.system(f'ldconsole.exe quit --name "{instance_name}"')

def delete_instance(instance_name):
    """Delete the LDPlayer instance"""
    os.system(f'ldconsole.exe delete --name "{instance_name}" --force')

def close_game(instance_name, *args):
    """Force close the game application
    
    Args:
        instance_name: Name of the LDPlayer instance
    """
    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell am force-stop com.skystone.silverblood.us"')

def open_game(instance_name, *args):
    """Launch the game application
    
    Args:
        instance_name: Name of the LDPlayer instance
    """
    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')

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