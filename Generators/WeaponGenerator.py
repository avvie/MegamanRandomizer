from BaseClasses.GeneratorBase import *

class WeaponGenerator(GeneratorBase):
    #Original weapon bytes
    Vanilla_Weapons = [0x20, 0x10, 0x02, 0x40, 0x04, 0x08]
    Weapons_Write_Offset = 0x1C148
    Boss_Defeated_Weapon_Write_Offset = 0x1BFCC
    Gutsman_Specific_Fix_Write_Offset = 0x1B69E

    def __init__(self, file, params = None):
        super().__init__(file, params)

    def ShuffleWeapons(self):
        New_Weapons = []
        #byte shuffle loop
        while (len(self.Vanilla_Weapons) > 0):
            length = len(self.Vanilla_Weapons)
            r = random.randrange(length)
            print("rng",r)
            newByte = self.Vanilla_Weapons[r]
            New_Weapons.append(newByte)
            self.Vanilla_Weapons.pop(r)
        return New_Weapons

    def __Generate(self):
        self.shuffled_weapons = self.ShuffleWeapons()
        print("Randomized Weapons: ",self.shuffled_weapons)

    def __Write(self):
        self.file.seek(self.Weapons_Write_Offset) #weapons offset
        for x in self.shuffled_weapons:
            self.file.write(int.to_bytes(x))
        #####fixes incorrect level beaten graphics on stage select
        self.file.seek(self.Boss_Defeated_Weapon_Write_Offset) #boss defeated offset
        for x in self.shuffled_weapons:
            self.file.write(int.to_bytes(x))

        self.file.seek(self.Gutsman_Specific_Fix_Write_Offset) #Gutsman drawn sprite works differently on the level select
        self.file.write(int.to_bytes(self.shuffled_weapons[5])) #This patches a CMP call of 08 (Gutsman's usual reward) with the new reward assigned to GM

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()