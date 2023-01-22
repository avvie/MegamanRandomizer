import binascii
import random
import shutil

#Original weapon bytes
Vanilla_Weapons = [0x20, 0x10, 0x02, 0x40, 0x04, 0x08]
print("Vanilla Weapons",Vanilla_Weapons)

#The shuffled weapon bytes
New_Weapons = []
Megaman_Default = [0x2c, 0x11]

#to do: make palette file that python can load from longer list
primaryPal_Megaman = [0x2c, 0x11, 0x30, 0x00, 0x30, 0x12, 0x30, 0x19, 0x28, 0x16, 0x38, 0x00, 0x30, 0x17, 0x2C, 0x11]
print(primaryPal_Megaman)

Megaman_Default_Offsets = [0xCB1, 0xCE1, 0xDDD, 0x4CB1, 0x4CE1, 0X4D9B, 0x8CB1, 0x8CE1, 0xCCB1, 0xCCE1, 
0x10CB1, 0x10ce1, 0x14cb1, 0x1D485, 0x1D493, 0x14CE1]#Megamans stage default palette values we need to overwrite
                                                      #Dear god why are there so many

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
    
#Generate Megaman Default Palette
Megaman_Default_New = paletteGenerator(0x2c, 0x11)


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

###Fixed MegaMans sprite reverting to 2c 11 when dying in boss rooms
file.seek(0x1C29B)
file.write(int.to_bytes(Megaman_Default_New[0])) #replaces a lda #$2c with our new palette
file.seek(0x1C2A0)
file.write(int.to_bytes(Megaman_Default_New[1])) #replaces a lda #$11 with our new palette

for offset in Megaman_Default_Offsets: #Writes our megaman palette to palette tables
    file.seek(offset)
    file.write(int.to_bytes(Megaman_Default_New[0]))
    file.write(int.to_bytes(Megaman_Default_New[1]))

file.seek(0x1D487)#MM palette offset
x = 2 #hack to skip the buster palette we just wrote
while x < 15: 
    Generated_Palettes = paletteGenerator(primaryPal_Megaman[x],primaryPal_Megaman[(x+1)])
    file.write(int.to_bytes(Generated_Palettes[0]))
    file.write(int.to_bytes(Generated_Palettes[1]))
    print("Writing Palettes ",Generated_Palettes)
    x += 2

file.close()

#add header for proper booting
header = bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x08\x20\x00\x00\x07\x00\x00\x00\x01')
with open("MMRando.nes",'r+b') as contents:
      save = contents.read()
with open("MMRando.nes",'w+b') as contents:
      contents.write(header)
with open("MMRando.nes",'a+b') as contents:
      contents.write(save)