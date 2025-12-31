# opens .bin files and 
# highlight the bits that have changed
# between two files

from pathlib import Path
from colored import fg, bg, attr
import os, sys, argparse

RED = '\033[91m'
RESET = '\033[0m'

def display(file):
    f = open(file,'rb')
    basename = os.path.basename(file)
    f_bytes = f.read()
    f_list = []
    
    #copy data from File 1 into a list
    for i in range(len(f_bytes)):
        f_list.append(f_bytes[i])
        
    print("\n")
    print(f"File: {RED}{basename}{RESET}") 
    print(f"Size: {RED}{len(f_bytes)} bytes {RESET}")
                
    for column in range(len(f_bytes)): 
        if column >= 1 and column % 8 == 0 and column != len(f_bytes):
            print("|", end = " ")
        if column % 16 == 0:
            print(f"\n0x{column:08x}:", end = " ")
        print(f"0x{f_list[column]:02x}", end = " ")
        
    f.close()
    print("\n")

def backup(file):
    path = os.path.splitext(file)
    with open(file, 'rb') as src, open(f'{path[0]}.tmp', 'wb') as dst:
        nbytes = src.read()
        for byte in src:
            print(f"{byte}")
            dst.write(byte) 
            
    print("\n")
    print(f"{RED}{len(nbytes)} bytes {RESET}saved to {path[0]}.tmp")
    print("\n")
    #display(file)
    src.close()
    dst.close()
    
def main():
    parser = argparse.ArgumentParser(description=f"USAGE: binreader.py [filename]")
    parser.add_argument("filename", help="The path to the input file for processing.")
    parser.add_argument('--verbose', '-s', action='store_true', help='Save data to .tmp file')
    
    args = parser.parse_args()
    
    fpath = args.filename
    if args.verbose:
        if os.path.isfile(fpath):
            ext = os.path.splitext(fpath)[-1].lower()
            if ext == ".bin":
                backup(fpath)
            else:    
                print(f"{RED}.bin FILES ONLY{RESET}")
                
    else:
        if os.path.isfile(fpath):
            ext = os.path.splitext(fpath)[-1].lower()
            if ext == ".bin":
                display(fpath)
            else:    
                print(f"{RED}.bin FILES ONLY{RESET}")
        
if __name__ == "__main__":
    main()       
    
    