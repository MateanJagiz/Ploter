import json
import argparse
import configparser

config = configparser.ConfigParser()
config.read('config.ini')  

time_step_arm = config.getfloat('device', 'time_step_arm')
time_step_trollay = config.getfloat('device', 'time_step_trollay')
time_wait_1_active_pixel = config.getfloat('device', 'time_wait_1_active_pixel')
time_wait_n_active_pixel = config.getfloat('device', 'time_wait_n_active_pixel')
trolley_steps_on_move = config.getint('device', 'trolley_steps_on_move')
arm_steps_on_move = config.getint('device', 'arm_steps_on_move')

def format_time(seconds):
    if seconds == 0:
        return "0s"
    parts = []
    units = [("d", 86400), ("g", 3600), ("min", 60), ("s", 1)]
    for unit, div in units:
        amount = int(seconds // div)
        if amount > 0:
            parts.append(f"{amount}{unit}")
            seconds %= div
    return " ".join(parts)

instruction = []
try:
    parser = argparse.ArgumentParser(description="Opis")
    parser.add_argument("input", type=str, help="Instrukcja")
    args = parser.parse_args()
    instruction_path = args.input
    with open(instruction_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print("Problem to get instruction")
    print(e)

instruction = data["steps"]

time = 0.0
for mark in instruction:
    match mark:
        case 'N':
            time += time_step_trollay * 2 * trolley_steps_on_move
        case 'L':
            pass
        case 'R':
            pass
        case 'K':
            time += 5
        case 0:
            time += time_step_arm * 2 * arm_steps_on_move
        case 1:
            time += time_step_arm * 2 * arm_steps_on_move
            time += time_wait_n_active_pixel
        case 2:
            time += time_step_arm * 2 * arm_steps_on_move
            time += time_wait_1_active_pixel
        case _:
            print(f"Nie ma takiego znaku: \"{mark}\"")

print(format_time(time))

