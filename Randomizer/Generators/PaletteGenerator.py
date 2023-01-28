from BaseClasses.GeneratorBase import *

class PaletteGenerator(GeneratorBase):
    # P C I B F E G M Weapon Palettes for Mega Man
    #TODO: make palette file that python can load from longer list
    primaryPal_Megaman = [0x2c, 0x11, 0x30, 0x00, 0x30, 0x12, 0x30, 0x19, 0x28, 0x16, 0x38, 0x00, 0x30, 0x17, 0x2C, 0x11] 
    
    #Megamans stage default palette values we need to overwrite
    #Dear god why are there so many
    Megaman_Default_Offsets = [0xCB1, 0xCE1, 0xDDD, 0x4CB1, 0x4CE1, 0X4D9B, 0x8CB1, 0x8CE1, 0xCCB1, 0xCCE1, 0x10CB1, 0x10ce1, 0x14cb1, 0x1D485, 0x1D493, 0x14CE1]


    def __init__(self, file, params = None):
        super().__init__(file, params)

    def __palletteGenerator(self, color1, color2):
        palette_offset = color1 - color2

        r_high = random.randint(1, 2)
        r_low = random.randrange(13)
        new_paletteh = (r_high * 16) + r_low
        new_palettel = new_paletteh - palette_offset
    
        if new_palettel < 0:
            new_palettel = new_palettel ^ -56

        if new_palettel == new_paletteh:
            new_paletteh -= 16
        return [new_paletteh, new_palettel]

    def __Generate(self):
        color1 = self.params[0]
        color2 = self.params[1]
        self.rando_palette = self.__palletteGenerator(color1, color2)

    def __Write(self):
        ###Fixed MegaMans sprite reverting to 2c 11 when dying in boss rooms
        self.file.seek(0x1C29B)
        self.file.write(int.to_bytes(self.rando_palette[0])) #replaces a lda #$2c with our new palette
        self.file.seek(0x1C2A0)
        self.file.write(int.to_bytes(self.rando_palette[1])) #replaces a lda #$11 with our new palette

        for offset in self.Megaman_Default_Offsets: #Writes our megaman palette to palette tables
            self.file.seek(offset)
            self.file.write(int.to_bytes(self.rando_palette[0]))
            self.file.write(int.to_bytes(self.rando_palette[1]))

        self.file.seek(0x1D487)#MM palette offset
        x = 2 #hack to skip the buster palette we just wrote
        while x < 15: 
            Generated_Palettes = self.__palletteGenerator(self.primaryPal_Megaman[x],self.primaryPal_Megaman[(x+1)])
            self.file.write(int.to_bytes(Generated_Palettes[0]))
            self.file.write(int.to_bytes(Generated_Palettes[1]))
            x += 2

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()




    #TODO
    #Add fun presets
    #Add stage palettes for shuffling stage colors
