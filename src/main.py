#import RPi.GPIO as GPIO
import enum
from time import sleep
import json
import argparse
import pdb
from module.instruction import make_instruction as make


# ======  ASSERTION  ======

# Ustawienia GPIO
#
#ENA = 6
#DIR = 13
#PUL = 26
#
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#
#GPIO.setup(ENA, GPIO.OUT)
#GPIO.output(ENA, GPIO.LOW)
#
#GPIO.setup(DIR, GPIO.OUT)
#GPIO.output(DIR, GPIO.LOW)
#
#GPIO.setup(PUL, GPIO.OUT)
#GPIO.output(PUL, GPIO.LOW)
#
## uruchomienie  plotera
#GPIO.output(DIR, GPIO.HIGH)
#GPIO.output(ENA, GPIO.LOW)
#



# =========  ACT  =========

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
        case 'L':
            print('W lewo')
        case 'R':
            print('W prawo')
        case 'K':
            print('Koniec!')
        case 0:
            print('Wyłącz laser, Szybko omiń')
        case 1:
            print('Utrzymaj laser, przytrzymaj króciutko, po czym zrób krok')
        case 2:
            print('Włącz LASER i przytrzymaj chwilę dłużej, po czym zrób krok')
        case _:
            print(f"Nie ma takiego znaku: \"{mark}\"")

#for j in range(10):
#    for i in range(200):
#        print(i)
#        GPIO.output(PUL, GPIO.HIGH)
#        sleep(0.001)
#        GPIO.output(PUL, GPIO.LOW)
#        sleep(0.001)
#    sleep(1)
#
#GPIO.cleanup()
