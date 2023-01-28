from Generators.PaletteGenerator import PaletteGenerator
from Generators.WeaponGenerator import WeaponGenerator
import binascii
import random
import shutil

filecopy = shutil.copyfile("./Mega Man (USA).nes", "./MMRando.nes")

file = open("MMRando.nes", "r+b")

#please name this more concretely
Megaman_Default = [0x2c, 0x11]

##Byte writing testing
filecopy = shutil.copyfile("./Mega Man (USA).nes", "./MMRando.nes")

file = open("MMRando.nes", "r+b")

GeneratorList = []
GeneratorList.append(WeaponGenerator(file))
GeneratorList.append(PaletteGenerator(file, Megaman_Default))

for generator in GeneratorList:
    generator.Randomize()

file.close()

#add header for proper booting
header = bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x08\x20\x00\x00\x07\x00\x00\x00\x01')
with open("MMRando.nes",'r+b') as contents:
      save = contents.read()
with open("MMRando.nes",'w+b') as contents:
      contents.write(header)
with open("MMRando.nes",'a+b') as contents:
      contents.write(save)