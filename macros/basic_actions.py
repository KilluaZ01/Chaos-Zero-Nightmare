"""Basic tap and swipe actions"""

import os

def tap_macro(instance_name, x, y):
    """Perform a tap action on the specified instance
    
    Args:
        instance_name: Name of the LDPlayer instance
        x: X coordinate
        y: Y coordinate
    """
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input tap {x} {y}"'
    os.system(tap_command)


def swipe_macro(instance_name, x1, y1, x2, y2):
    """Perform a swipe action on the specified instance
    
    Args:
        instance_name: Name of the LDPlayer instance
        x1, y1: Starting coordinates
        x2, y2: Ending coordinates
    """
    swipe_command = f'ldconsole.exe adb --name {instance_name} --command "shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000"'
    os.system(swipe_command)

def input_macro(instance_name, name):
    """Input text into the specified instance
    
    Args:
        instance_name: Name of the LDPlayer instance
        name: Text to input
    """
    input_command = f'ldconsole.exe adb --name {instance_name} --command "shell input text {name}"'
    os.system(input_command)