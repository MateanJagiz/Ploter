import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import numpy as np
import json
import argparse

parser = argparse.ArgumentParser(description="Opis")
parser.add_argument("input", type=str, help="Obraz")

args = parser.parse_args()

print("Obraz:", args.input)

# Obróbka obrazu 

# ---- 1. Wczytanie PNG ----
img = Image.open(args.input).convert("RGB")

# ---- 2. Zamiana na NumPy array ----
arr = np.array(img)
#print(arr)

binary_array = []

lines_quantity = 0
pixels_quantity = 0

# brakuje 2 rzeczy: 
# 1 - usuwanie zbędnych zer jeżeli w następnej linijce jest mniej pixeli i głowiaca zamiast dojechać do końca i wrócić, powinna od razu zejść do następnej lini.
# 2 - dodawanie zer jeżeli następna linia jest dłuższa niż poprzednia.

print(' N = pusta linia')
print(' P = głowica jedzie w prawo')
print(' L = głowica jedzie w lewo')
print(' K = koniec pliku')


for line in arr:
    lines_quantity+=1
    empty_line_watcher = 0
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
            empty_line_watcher += 1 


    if empty_line_watcher == 0: # sprawdzamy czy całą linia jest pusta. Jeżeli tak to oznaczamy jako 'N'
        for i in range(pixels_quantity_in_line):
            linia.pop()
        linia.append("N")
        lines_quantity-=1
    else:
        if lines_quantity % 2 == 0 or lines_quantity == 0: # sprawdzamy czy linia jest parzysta czy nie. jeżeli jest to po jej skończeniu zmienia się kierunek na prawy. Domyślnie urządzenie zaczyna jechać w lewo.
            for mark in linia:
                binary_array.append(mark)
                print(mark, end='')
            binary_array.append("R")
        else:
            linia.reverse()
            for mark in linia:
                binary_array.append(mark)
                print(mark, end='')
            binary_array.append("L")
    print('')


# Usuwamy ostatni element

try: 
    binary_array.pop()
except IndexError as e:
    #print(binary_array)
    print(e)

# Oznaczamy zakończenie pliku
binary_array.append("K")
    
print("lines = ", lines_quantity)
print("pixels = ", pixels_quantity)
print(binary_array)

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
