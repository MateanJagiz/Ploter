import RPi.GPIO as GPIO
import sys
import json
import time
import argparse
from tqdm import tqdm
from module.instruction import make_instruction as make
from module.utils import *

# ==================================  ARRANGE  ==================================

ploter = Ploter()
ploter.default_position()

instruction = []
data = {}
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

pbar = tqdm(total=len(instruction), desc="Postęp")  # Szacunkowe total, dostosuj dynamicznie



# ==================================    ACT    ==================================

try:
    for mark in instruction:
        match mark:
            case 'N':
                #print('Nowa linia')
                ploter.new_line()
            case 'L':
                #print('W lewo')
                ploter.cd_left()
            case 'R':
                #print('W prawo')
                ploter.cd_right()
            case 'K':
                #print('Koniec!')
                ploter.end()
            case 0:
                #print('Wyłącz laser, Szybko omiń')
                ploter.empty_step()
            case 1:
                #print('Utrzymaj laser, przytrzymaj króciutko, po czym zrób krok')
                ploter.active_step()
            case 2:
                #print('Włącz LASER i przytrzymaj chwilę dłużej, po czym zrób krok')
                ploter.first_pixel()
            case _:
                print(f"Nie ma takiego znaku: \"{mark}\"")
        pbar.update(1)  # Aktualizuj o 1 krok

except KeyboardInterrupt:
    print("\nEmergency shutdown!")
    ploter.default_position()
    ploter.safe_mode()
    sys.exit(0)
    
except Exception as e:    
    print(f"\nNieoczekiwany błąd: {e}")
    ploter.safe_mode()

# =================================    ASSERT    ================================

pbar.close()
#GPIO.cleanup()
