#import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import numpy as np
import json
import argparse
import pdb

parser = argparse.ArgumentParser(description="Opis")
parser.add_argument("input", type=str, help="Obraz")

args = parser.parse_args()

print("Użyty obraz: ", args.input)

# brakuje 2 rzeczy: 
# 1 - usuwanie zbędnych zer jeżeli w następnej linijce jest mniej pixeli i głowiaca zamiast dojechać do końca i wrócić, powinna od razu zejść do następnej lini.
# 2 - dodawanie zer jeżeli następna linia jest dłuższa niż poprzednia.

print(' N = pusta linia')
print(' P = głowica jedzie w prawo')
print(' L = głowica jedzie w lewo')
print(' K = koniec pliku')


def picture_to_array(image):
    binary_array = []
    pixels_quantity = 0
    lines_quantity = 0
    arr = np.array(image)

    for line in arr:
        lines_quantity+=1
        pixels_quantity_in_line = 0
        linia = [] #lista do tymczasowego zapisu dla pixeli w lini
    
        for pixel in line:
            pixels_quantity+=1
            pixels_quantity_in_line+=1
            suma = int(pixel[0]) + int(pixel[1]) + int(pixel[2])
            if suma > 500:
                linia.append(0)
            else:
                linia.append(1)
        binary_array.append(linia)
    print('ilość lini = ', len(binary_array))

    return binary_array

def print_2D_array(array):
    for line in array:
        for item in line:
            if item == 0:
                print('•', end = '')
            else:
                print('■', end = '')
        print('')

def prepare_instruction(binary_array):
    marks_quantity = 0
    instruction = []

    kierunek = False # w lewo to ujemny czyli *False*, a w prawo to dodatni, czyli *True*
    #pdb.set_trace()
    for i, line in enumerate(binary_array): # sprawdzamy czy całą linia jest pusta. Jeżeli tak to oznaczamy jako 'N' = Next, Następna
        try:
            suma_lini = sum(line) 
            if suma_lini == 0:
                instruction.append("N")
            else:
                if kierunek == True:
                    instruction.append("R")
                elif kierunek == False:
                    instruction.append("L")
                    line.reverse()
                for mark in line:
                    instruction.append(mark)
                kierunek = not kierunek
        except:
            print("EXCEPTION!!!")
    
    try: 
       instruction.pop() # Usuwamy zbedne dane z końca
    except IndexError as e:
        pass
    instruction.append("K") # znak końca pliku
    return instruction

def remove_unnecessary_pixels(instruction):
    flag = True
    while flag:
        quantity = 0
        indices = [i for i, item in enumerate(instruction) if item in ('R', 'L')]
        for index in indices:
            if instruction[index-1] == 0 and instruction[index+1] == 0:
                instruction.pop(index-1)
                instruction.pop(index)
                quantity = quantity + 1
        if quantity == 0:
            flag = False 
    print(instruction)
        # Oznaczamy zakończenie pliku

# ---- Tworzenie obrazu ----

img = Image.open(args.input).convert("RGB")
binary_2D_image = picture_to_array(img)
print_2D_array(binary_2D_image)
instruction = prepare_instruction(binary_2D_image)
remove_unnecessary_pixels(instruction)

# ---- 3. Rozpoczęcie druk ----

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
