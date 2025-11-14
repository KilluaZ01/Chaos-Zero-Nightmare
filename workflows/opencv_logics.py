import os
import time

from macros.basic_actions import swipe_macro, tap_macro

from utils.screenshot_utils import check_template, find_coordinates, find_all_coordinates
from utils.paths import TEMPLATE_DIR

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

    coords = find_coordinates(instance_name, template_path, threshold=0.8)
    if coords:
        x, y = coords
        tap_macro(instance_name, x, y)
        return True
    else:
        tap_macro(instance_name, 322, 366)
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

    for i in range(10):
        if check_template(instance_name, template_path, threshold=0.8):
            break

        tap_macro(instance_name, 1155, 45)
        time.sleep(2)

        tap_macro(instance_name, 1155, 45)
        time.sleep(4)
    
def summoning_1x(instance_name, *args):
    template_path = f"{TEMPLATE_DIR}/summon_1x_checker.png"

    for i in range(10):
        if check_template(instance_name, template_path, threshold=0.8):
            break

        tap_macro(instance_name, 1155, 45)
        time.sleep(2)

        tap_macro(instance_name, 660, 1)
        time.sleep(4)

def summoning_till_empty(instance_name, *args):
    template_path_empty = f"{TEMPLATE_DIR}/summon_empty.png"
    
    for i in range(10):
        if check_template(instance_name, template_path_empty, threshold=0.8):
            print("No more summons available.")
            break
        else:
            tap_macro(instance_name, 844, 658)
            time.sleep(2)
            summoning_1x(instance_name)
            tap_macro(instance_name, 1141, 663)

