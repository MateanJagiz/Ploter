import RPi.GPIO as GPIO
from time import sleep
import argparse
#from module.instruction import make_instruction as make
from module.utils import *

# ==================================  ARRANGE  ==================================

# ==================================    ACT    ==================================

default_position()

instruction = []
try:
    parser = argparse.ArgumentParser(description="Opis")
    parser.add_argument("input", type=str, help="Obraz")
    args = parser.parse_args()
    image_path = args.input
    print("Użyty obraz: ",image_path)
    instruction = make(image_path)
except Exception as e:
    print('SOMETHING IS NO YES')
    print(e)


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


# ===================================  ASSERT  ==================================

#GPIO.cleanup()
