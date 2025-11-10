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
        ('Agreed!', tap_macro, (496, 601), 1),
        ('Terms and Condition! - Done', tap_macro, (820, 600), 4),
        ('Guest', tap_macro, (493, 531), 20),

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