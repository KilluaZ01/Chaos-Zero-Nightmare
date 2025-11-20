import os
import time

from macros.basic_actions import swipe_macro, tap_macro

from utils.screenshot_utils import check_template, find_coordinates, find_all_coordinates, match_in_roi, take_screenshot
from utils.paths import SCREENSHOT_DIR_FINAL, TEMPLATE_DIR

def check_if_glitch(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/wait.png"

    if check_template(instance_name, template_path, threshold=0.8):
        tap_macro(instance_name, 530, 460)
        time.sleep(2)

def watch_again(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/watch_again_button.png"

    if check_template(instance_name, template_path, threshold=0.8):
        tap_macro(instance_name, 51, 32)
        time.sleep(2)

        tap_macro(instance_name, 1180, 360)
    else:
        pass

def find_research(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/research_card.png"
    template_path_horse = f"{TEMPLATE_DIR}/horse.png"
    template_path_judge = f"{TEMPLATE_DIR}/judge.png"
    template_path_perse = f"{TEMPLATE_DIR}/perse.png"

    coords = find_coordinates(instance_name, template_path, threshold=0.8)
    if coords:
        x, y = coords
        tap_macro(instance_name, x, y)
        time.sleep(2)
        tap_macro(instance_name, 1141, 663)
        time.sleep(4)
        tap_macro(instance_name, 1141, 663)
        time.sleep(4)
        tap_macro(instance_name, 1141, 663)
        time.sleep(4)
        return True   
    else:
        sub_coords = find_coordinates(instance_name, template_path_horse, threshold=0.8)
        if sub_coords:
            x, y = sub_coords
            tap_macro(instance_name, x, y)
            time.sleep(2)
            tap_macro(instance_name, 1141, 663)
            time.sleep(4)
            return True
        else:
            sub_coords_2 = find_coordinates(instance_name, template_path_judge, threshold=0.7)
            if sub_coords_2:
                x, y = sub_coords_2
                tap_macro(instance_name, x, y)
                time.sleep(2)
                tap_macro(instance_name, 1141, 663)
                time.sleep(4)
                return True
            else:
                sub_coords_3 = find_coordinates(instance_name, template_path_perse, threshold=0.6)
                if sub_coords_3:
                    x, y = sub_coords_3
                    tap_macro(instance_name, x, y)
                    time.sleep(2)
                    tap_macro(instance_name, 1141, 663)
                    time.sleep(4)
                    return True
                else:
                    tap_macro(instance_name, 322, 366)
                    time.sleep(2)
                    tap_macro(instance_name, 1141, 663)
                    time.sleep(4)
                    return False
    
def check_start(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/start_button.png"

    for i in range(10):
        if check_template(instance_name, template_path, threshold=0.8):
            print('Download completed.')
            return True
        else:
            print(f'[{i}] Retrying to check start button...')
            time.sleep(30)

def check_battle_finish(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/battle_finish_button.png"

    for i in range(5):
        if check_template(instance_name, template_path, threshold=0.8):
            return True
        else:
            print(f'[{i}] Checking for battle finish...')
            time.sleep(20)

def find_char1(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/character_1.png"

    coords = find_coordinates(instance_name, template_path, threshold=0.8)
    if coords:
        x, y = coords
        tap_macro(instance_name, x, y)
        return True
    else:
        return False

def find_char2(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/character_2.png"

    coords = find_coordinates(instance_name, template_path, threshold=0.8)
    if coords:
        x, y = coords
        tap_macro(instance_name, x, y)
        return True
    else:
        return False
    
def find_attacking_points(instance_name):
    coords = find_all_coordinates(instance_name, f"{TEMPLATE_DIR}/enemy_symbol.png")

    OFF_X = 20
    OFF_Y = 60

    attacking_points = [(x + OFF_X, y + OFF_Y) for x, y in coords]
    return attacking_points

def random_hit_logic(instance_name, Attacking_Points):
    x, y = Attacking_Points
    swipe_macro(instance_name, 640, 594, x, y, 1500)
    time.sleep(3)
    swipe_macro(instance_name, 720, 592, x, y, 1500)
    time.sleep(3)
    swipe_macro(instance_name, 640, 594, x, y, 1500)
    time.sleep(3)
    swipe_macro(instance_name, 720, 592, x, y, 1500)
    time.sleep(3)
    swipe_macro(instance_name, 640, 594, x, y, 1500)
    time.sleep(6)

def fighting_logic(instance_name):
    while True:
        Enemy_Available = find_attacking_points(instance_name)
        if Enemy_Available:
            tap_macro(instance_name, 1142, 623)
            Attacking_Point = Enemy_Available[0]
            random_hit_logic(instance_name, Attacking_Point)
        else:
            print("No enemies found, ending fighting logic.")
            break

def fighting_logic_boss(instance_name):
    x = 962
    y = 314 
    while True:
        Enemy_Available = find_attacking_points(instance_name)
        if Enemy_Available:
            tap_macro(instance_name, 1142, 623)
            random_hit_logic(instance_name, (x, y))
        else:
            print("No enemies found, ending fighting logic.")
            break
        
def check_confirm(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/confirm_button.png"
    
    for i in range(5):
        if check_template(instance_name, template_path, threshold=0.8):
            return True
        else:
            time.sleep(10)

def claim_rewards(instance_name, *args):
    template_path_claim = f"{TEMPLATE_DIR}/claim_rewards_button.png"
    template_path_event = f"{TEMPLATE_DIR}/event_icon.png"

    coords = find_all_coordinates(instance_name, template_path_event, threshold=0.8)
    print(coords)
    for coord in coords:
        x, y = coord
        tap_macro(instance_name, x, y)
        time.sleep(2)

        claim_coords = find_coordinates(instance_name, template_path_claim, threshold=0.8)

        if claim_coords:
            tap_macro(instance_name, claim_coords[0], claim_coords[1])
            time.sleep(4)
            tap_macro(instance_name, 660, 1)
            time.sleep(2)
        else:
            pass

def summoning_rare(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/reward_confirm_button.png"

    for i in range(8):
        if check_template(instance_name, template_path, threshold=0.8):
            break

        tap_macro(instance_name, 1155, 45)
        time.sleep(2)

        tap_macro(instance_name, 1155, 45)
        time.sleep(4)
    
def summoning_1x(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/summon_1x_checker.png"

    for i in range(8):
        if check_template(instance_name, template_path, threshold=0.8):
            break

        tap_macro(instance_name, 1155, 45)
        time.sleep(2)

        tap_macro(instance_name, 660, 1)
        time.sleep(4)

def summoning_till_empty(instance_name, *args):
    template_path_empty = f"{TEMPLATE_DIR}/summon_empty.png"
    roi = (1050, 0, 1250, 100)
    
    for i in range(10):
        if match_in_roi(instance_name, template_path_empty, roi):
            print("No more summons available.")
            break
        else:
            tap_macro(instance_name, 844, 658) # Summon 1x Button
            time.sleep(2)
            summoning_1x(instance_name)

def summoning_till_10x(instance_name, *args):
    template_confirm_button = f"{TEMPLATE_DIR}/orange_confirm_button.png"
    
    for i in range(4):
        if check_template(instance_name, template_confirm_button, threshold=0.8):
            print("10x summon completed.")
            break
        else:
            summoning_rare(instance_name)
            tap_macro(instance_name, 1141, 663)
            time.sleep(4)
            tap_macro(instance_name, 1141, 663)
            time.sleep(4)

def summon_might(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/summon_might.png"

    if check_template(instance_name, template_path, threshold=0.8):
        tap_macro(instance_name, 500, 405)      # Do not
        time.sleep(2)
        tap_macro(instance_name, 906, 485)      # Confirm
    else:
        pass

def login_checker(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/login_checker.png"

    for i in range(6):
        if check_template(instance_name, template_path, threshold=0.8):
            pass
        else:
            time.sleep(10)

def final_screenshot(instance_name, *args):
    DIR = SCREENSHOT_DIR_FINAL
    FILENAME = f"{instance_name}_DAY1.png"
    take_screenshot(instance_name, DIR, FILENAME)

def validate_template(instance_name, template_path, threshold):
    path = f"{TEMPLATE_DIR}/{template_path}"
    valid = check_template(instance_name, path, threshold=threshold)
    return valid

def fighting_till_continue(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/continue_button.png"

    for i in range(6):
        swipe_macro(instance_name,640, 594, 914, 405, 1500)
        time.sleep(3)
        swipe_macro(instance_name, 720, 592, 914, 405, 1500)
        time.sleep(3)
        swipe_macro(instance_name, 640, 594, 914, 405, 1500)
        time.sleep(3)
        tap_macro(instance_name, 1142, 623)
        time.sleep(8)
        swipe_macro(instance_name, 720, 592, 914, 405, 1500)
        time.sleep(3)
        swipe_macro(instance_name, 640, 594, 914, 405, 1500)
        time.sleep(3)
        if check_template(instance_name, template_path, threshold=0.8):
            break        
        else:
            pass

def global_till_slide(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/slide.png"

    for i in range(3):
        tap_macro(instance_name, 660, 1)
        time.sleep(2)
        tap_macro(instance_name, 660, 1)
        time.sleep(2)
        if check_template(instance_name, template_path, threshold=0.8):
            break        
        else:
            pass

def if_continue(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/orange_confirm_button.png"
    
    coords = find_coordinates(instance_name, template_path, threshold=0.8)

    if coords:
        tap_macro(instance_name, coords[0], coords[1])
        time.sleep(2)
    else:
        pass