import sys
import json
import argparse
from tqdm import tqdm
from src.module.utils import *

# ==================================    ACT    ==================================

class Plot:
    def __init__(self):
        self.ploter = Ploter()
        self.ploter.start_default_position()

    def start_plot(self, instruction_data):
        pbar = tqdm(total=len(instruction_data), desc="Postęp")  # Szacunkowe total, dostosuj dynamicznie
        try:
            for mark in instruction_data:
                match mark:
                    case 'S':
                        #print('Stop')
                        self.ploter.stop_after_line_end()
                    case 'N':
                        #print('Nowa linia')
                        self.ploter.new_line()
                    case 'L':
                        #print('W lewo')
                        self.ploter.cd_left()
                    case 'R':
                        #print('W prawo')
                        self.ploter.cd_right()
                    case 'K':
                        #print('Koniec!')
                        self.ploter.end()
                    case 0:
                        #print('Wyłącz laser, Szybko omiń')
                        self.ploter.empty_step()
                    case 1:
                        #print('Utrzymaj laser, przytrzymaj króciutko, po czym zrób krok')
                        self.ploter.active_step()
                    case 2:
                        #print('Włącz LASER i przytrzymaj chwilę dłużej, po czym zrób krok')
                        self.ploter.first_pixel()
                    case _:
                        print(f"Nie ma takiego znaku: \'{mark}\'")
                pbar.update(1)  # Aktualizuj o 1 krok
        
        except KeyboardInterrupt:
            print("\nEmergency shutdown!")
            self.ploter.end_default_position()
            self.ploter.safe_mode()
            sys.exit(0)
            
        except Exception as e:    
            print(f"\nNieoczekiwany błąd: {e}")
            self.ploter.end_default_position()
            self.ploter.safe_mode()
    
        pbar.close()
    # =================================    ASSERT    ================================
    
    def server_plot(self, instruction_name):
        with open(f"./instructions/{instruction_name}", 'r', encoding='utf-8') as f:
            data = json.load(f)
        instruction = data["steps"]
        inst_len = len(instruction)/100

        try:
            for i, mark in enumerate(instruction):
                match mark:
                    case 'S':
                        print('Stop')
                        self.ploter.stop_after_line_end()
                    case 'N':
                        print('Nowa linia')
                        yield i/inst_len
                        self.ploter.new_line()
                    case 'L':
                        print('W lewo')
                        self.ploter.cd_left()
                    case 'R':
                        print('W prawo')
                        self.ploter.cd_right()
                    case 'K':
                        print('Koniec!')
                        self.ploter.end()
                    case 0:
                        print('Wyłącz laser, Szybko omiń')
                        self.ploter.empty_step()
                    case 1:
                        print('Utrzymaj laser, przytrzymaj króciutko, po czym zrób krok')
                        self.ploter.active_step()
                    case 2:
                        print('Włącz LASER i przytrzymaj chwilę dłużej, po czym zrób krok')
                        self.ploter.first_pixel()
                    case _:
                        print(f"Nie ma takiego znaku: \'{mark}\'")
           
        except Exception as e:    
            print(f"\nNieoczekiwany błąd: {e}")
            self.ploter.end_default_position()
            self.ploter.safe_mode()
    
        f.close()
        self.ploter.end_default_position()
        self.ploter.safe_mode()
#GPIO.cleanup()


if __name__ == "__main__":
    plot = Plot()
    instruction_data = []
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
    instruction_data = data["steps"]
    plot.start_plot(instruction_data)
