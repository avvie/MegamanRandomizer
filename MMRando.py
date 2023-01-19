import binascii
import random
import shutil
import argparse
import Data
import Offsets


settings = argparse.ArgumentParser()

settings.add_argument("--skipweapons", help="Skips weapon randomization",  action="store_true", default=False)
settings.add_argument("--skipcolors", help="Skip color randomization", action="store_true", default=False)

args = settings.parse_args()

##Byte writing testing
filecopy = shutil.copyfile("./Mega Man (USA).nes", "./MMRando.nes")

file = open("MMRando.nes", "r+b")

def patcher(offset, data):
    file.seek(offset)
    file.write(int.to_bytes(data))
    
def paletteGenerator(color1, color2):
        
    print("palette", color1, color2)
    palette_offset = color1 - color2
    print("offset", palette_offset)

    r_high = random.randint(1, 2)
    r_low = random.randrange(13)
    print(r_high, r_low)
    new_paletteh = (r_high * 16) + r_low
    new_palettel = new_paletteh - palette_offset
    
    if new_palettel < 0:
        new_palettel = new_palettel ^ -56

    if new_palettel == new_paletteh:
        new_paletteh -= 16
        
    
    rando_palette = [new_paletteh, new_palettel]
    return rando_palette    

if args.skipweapons == False:
    Weapons = Data.Vanilla_Weapons
    random.shuffle(Weapons)
    for x in range(5):
        patcher(Offsets.WeaponReward + x, Weapons[x])
        patcher(Offsets.BossDefeated + x, Weapons[x])
    patcher(Offsets.Gutsman_ClearPatch, Weapons[5])
    print("randomized weapons", Weapons)
    
if args.skipcolors == False:
    Default_Pal = paletteGenerator(0x2c, 0x11)
    for x in Offsets.Megaman_DefaultPal:
        patcher(x, Default_Pal[0])
        file.write(int.to_bytes(Default_Pal[1])) #hack for writing two values based off one offset. TO DO: Expand patcher for support
    
    for x in range(2, 7, 2):
        Weapon_Pal = paletteGenerator(Data.primaryPal_Megaman[x], Data.primaryPal_Megaman[x+1])
        patcher(Offsets.Megaman_WeaponPal + x, Weapon_Pal[0])
        file.write(int.to_bytes(Weapon_Pal[1])) #hack for writing two values based off one offset. TO DO: Expand patcher for support
    
    patcher(Offsets.Bossroom_PalPatch[0], Default_Pal[0])
    patcher(Offsets.Bossroom_PalPatch[1], Default_Pal[1])


file.close()

#add header for proper booting
header = bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x08\x20\x00\x00\x07\x00\x00\x00\x01')
with open("MMRando.nes",'r+b') as contents:
      save = contents.read()
with open("MMRando.nes",'w+b') as contents:
      contents.write(header)
with open("MMRando.nes",'a+b') as contents:
      contents.write(save)