from ast import arg
from genericpath import isfile
from platform import architecture
from typing import final
from Generators.PaletteGenerator import PaletteGenerator
from Generators.WeaponGenerator import WeaponGenerator
from Utilities import *
import hashlib
import shutil
import sys
import os.path

# Get console arguments passed
args = sys.argv[1:]

input_file = "./Mega Man (USA).nes"
output_file = "./MMRando.nes"
supported_md5_input_checksums = ["4de82cfceadbf1a5e693b669b1221107"]

# Gets the path to a valid file passed in arguments, positionally after param
def GetValidFileFromParameter(paramList, param, default = None):
    if param in paramList:
        i = paramList.index(param)
        if i+1 < len(paramList):
            if os.path.exists(paramList[i+1]):
                local = paramList[i+1]
                paramList.remove(local)
                paramList.remove(param)
                print("return value:"+ local)
                return local
    return default

def ParamExistsInArgs(paramList, param):
    if param in paramList:
        return True
    return False

if ParamExistsInArgs(args, '-h'):
    PrintHelp()
    sys.exit(0)

# Get input file path passed into the app, or default
input_file = GetValidFileFromParameter(args, '-i', input_file)
# Get output file path passed into the app, or default
output_file = GetValidFileFromParameter(args, '-o', output_file)

#please name this more concretely
Megaman_Default = [0x2c, 0x11]

try:
    # Check for checksum
    if os.path.getsize(input_file) >= 150*1024:
        print("File too big")
        sys.exit(0)
    
    file = open(input_file, "rb")
    checksum = str(hashlib.md5(file.read()).hexdigest())
    file.close()

    if checksum not in supported_md5_input_checksums:
        print("Input file md5 checksum not supported " + checksum)
        sys.exit(0)

    # Make a copy of the original input file 
    filecopy = shutil.copyfile(input_file, output_file)

    file = open("MMRando.nes", "r+b")

    GeneratorList = []
    if not ParamExistsInArgs(args, '-w'):
        GeneratorList.append(WeaponGenerator(file))
    if not ParamExistsInArgs(args, '-p'):
        GeneratorList.append(PaletteGenerator(file, Megaman_Default))
    
    for generator in GeneratorList:
        generator.Randomize()
    
except Exception as e:
    print(e.with_traceback())
finally:
    file.close()


#add header for proper booting
header = bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x08\x20\x00\x00\x07\x00\x00\x00\x01')
with open("MMRando.nes",'r+b') as contents:
      save = contents.read()
with open("MMRando.nes",'w+b') as contents:
      contents.write(header)
with open("MMRando.nes",'a+b') as contents:
      contents.write(save)