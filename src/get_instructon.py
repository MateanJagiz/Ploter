#import os
#import argparse
#from module.instruction import make_instruction as make
#from module.utils import *
#from pathlib import Path
#
#instruction = []
#try:
#    print("Parsing Opis")
#    parser = argparse.ArgumentParser(description="Opis")
#    print("Parsing Obraz")
#    parser.add_argument("input", type=str, help="Obraz")
#    print("Parseing Args")
#    args = parser.parse_args()
#    print("Image path")
#    image_path = args.input
#except Exception as e:
#    print('problem to get image path')
#    print(e)
#
#print("Użyty obraz: ",image_path)
#print("Making Image:")
#
#try:
#    instruction = make(image_path)
#except Exception as e:
#    print("Problem to get instruction")
#    print(e)
#
#image_path_2= Path(image_path)
#filename = image_path_2.stem 
#filename_path = image_path_2.parents[1]
#
#instruction_file = filename_path + '/' + 'instructions' + filename + '.ins'
#with open(instruction_file, 'w', encoding='utf-8') as f:
#    f.write(instruction)


import os
import argparse
import sys
import json
from pathlib import Path
from module.instruction import make_instruction as make
from module.utils import *

def main():
    parser = argparse.ArgumentParser(description="Parse image to instructions")
    parser.add_argument("input", type=str, help="Path to input image")
    args = parser.parse_args()
    
    image_path = Path(args.input).resolve()  # Resolve for safety
    if not image_path.exists():
        print(f"Error: {image_path} not found")
        sys.exit(1)
    
    print(f"Using image: {image_path}")
    
    try:
        instruction = make(str(image_path))  # make expects string?
    except Exception as e:
        print(f"Problem making instruction: {e}")
        sys.exit(1)
    
    # Fixed path logic
    filename = image_path.stem  # 'PTFP_001'
    output_dir = image_path.parents[1] / 'instructions'  # /home/user/instructions
    output_dir.mkdir(exist_ok=True)  # Create if missing
    
    instruction_file = output_dir / f'{filename}.ins'
    
    json_data = {"steps": instruction}
    try:
        with open(instruction_file.with_suffix('.json'), 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Saved to: {instruction_file}")
    except IOError as e:
        print(f"Write error: {e}")

if __name__ == "__main__":
    main()

