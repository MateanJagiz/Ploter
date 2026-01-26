import RPi.GPIO as GPIO
import sys
import json
from time import sleep
import argparse
from module.instruction import make_instruction as make
from module.utils import *

# ==================================  ARRANGE  ==================================

# ==================================    ACT    ==================================

default_position()

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

try:
    for mark in instruction:
        match mark:
            case 'N':
                print('Nowa linia')
                new_line()
            case 'L':
                print('W lewo')
                cd_left()
            case 'R':
                print('W prawo')
                cd_right()
            case 'K':
                print('Koniec!')
                end()
            case 0:
                print('Wyłącz laser, Szybko omiń')
                empty_step()
            case 1:
                print('Utrzymaj laser, przytrzymaj króciutko, po czym zrób krok')
                active_step()
            case 2:
                print('Włącz LASER i przytrzymaj chwilę dłużej, po czym zrób krok')
                first_pixel()
            case _:
                print(f"Nie ma takiego znaku: \"{mark}\"")
except KeyboardInterrupt:
    print("\nEmergency shutdown!")
    default_position()
    safe_mode()
    sys.exit(0)
    
except Exception as e:    
    print(f"\nNieoczekiwany błąd: {e}")
    safe_mode()

#GPIO.cleanup()
