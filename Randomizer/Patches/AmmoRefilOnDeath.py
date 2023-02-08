from BaseClasses.PatchBase import *

class AmmoRefilOnDeath(PatchBase):
    Health_Refill_On_Death_Offset = (0x1512C)
    Health_Refill_On_Death_Hijack = [0x4c, 0x76, 0xBF] #Replaces health refill with a jump
                                                       #to free space
    Free_Space_Offset = (0x17F76) #Free space offset
    Ammo_Refills_On_Death = [0xA9, 0x1C, 0xA2, 0x07, 0x95, 0x6A, 
    0xCA, 0x10, 0xFB, 0x4C, 0x30, 0x91] #New assembly for refilling health and ammo
    
    def __init__(self, file, params = None):
        super().__init__(file, params)

    def Patch(self):
        super().Patch()
        self.__Write()
        
    def __Write(self):
        #Ammo Refill
        self.file.seek(self.Health_Refill_On_Death_Offset) #boss defeated offset
        
        for x in self.Health_Refill_On_Death_Hijack:
            self.file.write(int.to_bytes(x))
        
        self.file.seek(self.Free_Space_Offset)
        
        for x in self.Ammo_Refills_On_Death:
            self.file.write(int.to_bytes(x))
