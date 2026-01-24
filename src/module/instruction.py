from PIL import Image
import numpy as np
import configparser

def make_instruction(path2image):
    img = Image.open(path2image).convert("RGB")
    binary_2D_image = picture_to_array(img)
    print_2D_array(binary_2D_image)
    instruction = prepare_instruction(binary_2D_image)
    print(' P = pusta linia')
    print(' N = nowa linia')
    print(' R = głowica jedzie w prawo')
    print(' L = głowica jedzie w lewo')
    print(' K = koniec pliku')
    print(instruction)
    return instruction

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
    print("1. Oznaczenie pustych lini i prawo lewo.")
    instruction = set_dir(binary_array)
    print("2. Dodanie znaku końca pracy")
    instruction.append("K") # znak końca pliku
    print("3. Usunięcie niepotrzebnych pixeli")
    instruction = remove_unnecessary_pixels(instruction)
    print("4. dodanie wszedzie znacznika następnej linii")
    instruction = add_next_line_mark(instruction)
    print("5. Usuwanie zer pomiedzy pustymi liniami")
    print(remove_0_between_empty_lines(instruction))
    instruction = remove_0_between_empty_lines(instruction)
    print("6. Usuniecie zbędnej końcówki przed znakiem końca pracy")
    while instruction[-2] == 0 or instruction[-2] == 'N':
        instruction.pop(-2)
    print("8. Dodanie znaku dluzszego dzialania przy starcie linii")
    for i, mark in enumerate(instruction):
        if i == 0 or mark == 'K':
            pass
        else:
            if instruction[i-1] != 1  and instruction[i] == 1:
                if instruction[i-1] == 2:
                    pass
                else:
                    instruction[i] = 2
    return instruction


def set_dir(binary_array):
    instruction = []
    kierunek = False # w lewo to ujemny czyli *False*, a w prawo to dodatni, czyli *True*
    for line in binary_array: # sprawdzamy czy całą linia jest pusta. Jeżeli tak to oznaczamy jako 'N' = Następna
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
    return instruction

def remove_0_between_empty_lines(instruction):
    NN = 1
    while NN > 0:
        NN = 0
        N_after_N_list = find_multiple_n_starts(instruction)
        print(N_after_N_list)
        for i in N_after_N_list:
            try:
                if instruction[i[0]-1] == 0 and instruction[i[0]+i[1]+1] == 0:
                    instruction.pop(i[0]+i[1]+1)
                    instruction.pop(i[0]-1)
                    NN = NN + 1
                    print(NN)
            except Exception as e:
                print(e)
    return instruction

def remove_unnecessary_pixels(instruction):
    flag = True
    while flag:
        quantity = 0
        indices = [i for i, item in enumerate(instruction) if item in ('R', 'L')]
        indices.reverse()
        dlugosc = len(indices)
        for index in indices:
            if instruction[index-1] == 0 and instruction[index+1] == 0:
                instruction.pop(index+1)
                instruction.pop(index-1)
                quantity = quantity + 1
        if quantity == 0:
            flag = False
    return instruction
    
def add_next_line_mark(instruction):
    indices = [i for i, item in enumerate(instruction) if item in ('R', 'L')]
    indices.reverse()
    for index in indices:
        instruction.insert(index, 'N')
    if instruction[0] == 'N' and instruction[1] == 'N':
        instruction.pop(0)
    return instruction

def find_multiple_n_starts(seq):
    indices_n_start = []
    i = 0
    while i < len(seq):
        # Sprawdzamy czy to litera 'N'
        if isinstance(seq[i], str) and seq[i] == 'N':
            # Zliczamy wszystkie kolejne N
            n_count = 1
            j = i + 1
            while j < len(seq) and isinstance(seq[j], str) and seq[j] == 'N':
                n_count += 1
                j += 1
            # Jeśli 2 lub więcej N, dodajemy do wyniku
            if n_count >= 2:
                indices_n_start.append((i, n_count))
            # Przeskakujemy całą sekwencję N
            i = j
        else:
            i += 1
    
    return indices_n_start
