from Generators.PaletteGenerator import PaletteGenerator
import binascii
import random
import shutil

filecopy = shutil.copyfile("./Mega Man (USA).nes", "./MMRando.nes")

file = open("MMRando.nes", "r+b")

#Original weapon bytes
Vanilla_Weapons = [0x20, 0x10, 0x02, 0x40, 0x04, 0x08]
print("Vanilla Weapons",Vanilla_Weapons)

#The shuffled weapon bytes
New_Weapons = []
Megaman_Default = [0x2c, 0x11]

#byte shuffle loop
while (len(Vanilla_Weapons) > 0):
    length = len(Vanilla_Weapons)
    r = random.randrange(length)
    print("rng",r)
    newByte = Vanilla_Weapons[r]
    New_Weapons.append(newByte)
    Vanilla_Weapons.pop(r)
  
    
# print("Weapons1",Vanilla_Weapons)
print("Randomized Weapons",New_Weapons)

##Byte writing testing
filecopy = shutil.copyfile("./Mega Man (USA).nes", "./MMRando.nes")

file = open("MMRando.nes", "r+b")

file.seek(0x1C148) #weapons offset
for x in New_Weapons:
    file.write(int.to_bytes(x))
#####fixes incorrect level beaten graphics on stage select
file.seek(0x1BFCC) #boss defeated offset
for x in New_Weapons:
    file.write(int.to_bytes(x))
    
file.seek(0x1B69E) #Gutsman drawn sprite works differently on the level select
file.write(int.to_bytes(New_Weapons[5])) #This patches a CMP call of 08 (Gutsman's usual reward) with the new reward assigned to GM

p = PaletteGenerator(file, Megaman_Default)
p.Randomize()

file.close()

#add header for proper booting
header = bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x08\x20\x00\x00\x07\x00\x00\x00\x01')
with open("MMRando.nes",'r+b') as contents:
      save = contents.read()
with open("MMRando.nes",'w+b') as contents:
      contents.write(header)
with open("MMRando.nes",'a+b') as contents:
      contents.write(save)