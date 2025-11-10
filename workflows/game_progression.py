"""Game progression steps and execution"""

import time
import threading
from macros import *


def get_game_steps():
    """Get the complete list of game progression steps
    
    Returns:
        list: List of (description, function, coords, sleep_duration) tuples
    """
    steps = [
        ('Login', tap_macro, (640, 560), 5),
        ('Guest Account', tap_macro, (840, 285), 6),
        ('Confirm', tap_macro, (895, 520), 8),
        ('Confirm Guest', tap_macro, (630, 615), 8),
        ('Confirm Server', tap_macro, (625, 495), 5),
        ('Choose Voice', tap_macro, (625, 360), 3),
        ('Confirm Voice', tap_macro, (625, 495), 10),
        ('Confirm Download', tap_macro, (860, 500), 60),
        ('Settings', tap_macro, (1205, 560), 10),
        ('Choose Detail 1', tap_macro, (1020, 275), 7),
        ('Low Detail 1', tap_macro, (1030, 380), 5),
        ('Choose Detail 2', tap_macro, (1020, 330), 3),
        ('Low Detail 2', tap_macro, (1030, 430), 5),    
        ('Choose Detail 3', tap_macro, (1020, 385), 3),
        ('Low Detail 3', tap_macro, (1030, 485), 5),
        ('Choose Detail 4', tap_macro, (1020, 440), 3),
        ('Low Detail 4', tap_macro, (1030, 540), 5),
        ('Choose Detail 5', tap_macro, (1020, 495), 3),
        ('Low Detail 5', tap_macro, (1030, 595), 5),
        ('Apply', tap_macro, (1120, 645), 5),
        ('Sound', tap_macro, (60, 235), 6),
        ('Mute', tap_macro, (1200, 165), 3),
        ('Close Settings', tap_macro, (1200, 60), 10)
    ]
    
    return steps


def execute_macro_steps(guest_data, steps, log_func, pause_event):
    """Execute macro steps for all accounts in parallel
    
    Args:
        guest_data: List of (instance_name, guest_name) tuples
        steps: List of macro steps to execute
        log_func: Logging function
        pause_event: Threading event for pause control
    """
    for log_text, action_func, coords, sleep_duration in steps:
        pause_event.wait()
        log_func(log_text)

        if action_func == "input_name":
            # Special case for name input
            for instance_name, guest_name in guest_data:
                pause_event.wait()
                input_macro(instance_name, guest_name)
                log_func(f"[{instance_name}] Input guest name: {guest_name}")
        else:
            # Normal actions with threading
            threads = []
            for instance_name, _ in guest_data:
                pause_event.wait()
                if coords is not None:
                    t = threading.Thread(target=action_func, args=(instance_name, *coords))
                else:
                    t = threading.Thread(target=action_func, args=(instance_name,))
                t.start()
                threads.append(t)

            # Wait for all threads
            for t in threads:
                t.join()

        # Sleep with pause checking
        for _ in range(sleep_duration):
            pause_event.wait()
            time.sleep(1)