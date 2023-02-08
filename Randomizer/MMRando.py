from pickle import TRUE
from Generators.PaletteGenerator import PaletteGenerator
from Generators.WeaponGenerator import WeaponGenerator
from Patches.IPSPatcher import IPSPatcher
from Patches.QualityOfLifePatches import QualityOfLifePatches
from Patches.AmmoRefilOnDeath import AmmoRefilOnDeath
from Patches.BombBuff import BombBuff
from Utilities import *
import hashlib
import shutil
import sys
import os.path
from Offsets import *

# Get console arguments passed
args = sys.argv[1:]
input_file = "./Mega Man (USA).nes"
output_file = "./MMRando.nes"

if ParamExistsInArgs(args, '-h'):
    PrintHelp()
    sys.exit(0)

# Get input file path passed into the app, or default
input_file = GetValidFileFromParameter(args, '-i', input_file)
# Get output file path passed into the app, or default
output_file = GetValidFileFromParameter(args, '-o', output_file, False)

try:
    # Check for checksum
    if os.path.getsize(input_file) >= max_image_file_size:
        print("File too big")
        sys.exit(0)
    
    file = open(input_file, "rb")
    checksum = str(hashlib.md5(file.read()).hexdigest())
    file.close()

    if checksum not in supported_md5_input_checksums:
        print("Input file md5 checksum not supported " + checksum)
        sys.exit(0)
        
    if GetHeader(input_file) in headers:
        headerless_buffer = StripHeader(input_file)
        WriteBuffer(output_file, headerless_buffer)
    else:
        # Assume headerless and whatever happens 
        shutil.copyfile(input_file, output_file)

    file = open(output_file, "r+b")
    # This pattern is getting out of control in the main script.. needz 
    # the refactoring kittens
    GeneratorList = []
    if not ParamExistsInArgs(args, '-w'):
        GeneratorList.append(WeaponGenerator(file))
    if not ParamExistsInArgs(args, '-p'):
        GeneratorList.append(PaletteGenerator(file, Megaman_Default))
    
    for generator in GeneratorList:
        generator.Randomize()
        
    PatchList = []
    if ParamExistsInArgs(args, '+roll'):
        PatchList.append(IPSPatcher(file, "ROLLCHAN.ips"))
        
    if not ParamExistsInArgs(args, '-qol') and len(ListIntersection(args, qolPatches)) == 0:
        PatchList.append(QualityOfLifePatches(file))
    
    elif not ParamExistsInArgs(args, '-a'):
        PatchList.append(AmmoRefilOnDeath(file))

    elif not ParamExistsInArgs(args, '-b'):
        PatchList.append(BombBuff(file))

    for patch in PatchList:
        patch.Patch()
    # end of litterbox
except Exception as e:
    print(e.with_traceback())
finally:
    file.close()

# Assume headerless and add header
AddHeader(headers[0], output_file)