from utils.paths import SCREENSHOT_DIR
import os
import subprocess
import cv2
from random import randint

def take_screenshot(instance_name, filename=None):
    if filename is None:
        filename = f"{instance_name}_{randint(1000, 9999)}.png"

    remote_path = "/sdcard/result.png"
    local_path = os.path.join(SCREENSHOT_DIR, filename)

    # Step 1: Take screenshot inside emulator
    screencap_cmd = [
        "ldconsole.exe", "adb", 
        "--name", instance_name,
        "--command", f"shell screencap -p {remote_path}"
    ]
    result1 = subprocess.run(screencap_cmd, capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"[{instance_name}] ❌ Error during screencap: {result1.stderr.strip()}")
        return None

    # Step 2: Pull screenshot
    pull_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f'pull {remote_path} "{local_path}"'
    ]
    result2 = subprocess.run(pull_cmd, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"[{instance_name}] ❌ Error during pull: {result2.stderr.strip()}")
        return None

    return local_path

def check_template(instance_name, template_path, threshold=0.8):
    screenshot_path = take_screenshot(instance_name)
    if not screenshot_path:
        return False

    img = cv2.imread(screenshot_path, 0)
    template = cv2.imread(template_path, 0)

    if img is None or template is None:
        return False

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    os.remove(screenshot_path)
    return max_val >= threshold

def find_coordinates(instance_name, template_path, threshold=0.8):
    screenshot_path = take_screenshot(instance_name)
    img = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if img is None:
        print(f"❌ Failed to read screenshot: {screenshot_path}")
        return None

    if template is None:
        print(f"❌ Failed to read template: {template_path}")
        return None

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    os.remove(screenshot_path)  # Clean up screenshot file

    if max_val >= threshold:
        center_x = max_loc[0] + template.shape[1] // 2
        center_y = max_loc[1] + template.shape[0] // 2  
        return center_x, center_y
    else:
        return None
    
