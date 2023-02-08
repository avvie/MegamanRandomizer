from BaseClasses.PatchBase import *

class QualityOfLifePatches(PatchBase):
    Health_Refill_On_Death_Offset = (0x1512C)
    Health_Refill_On_Death_Hijack = [0x4c, 0x76, 0xBF] #Replaces health refill with a jump
                                                       #to free space
    Free_Space_Offset = (0x17F76) #Free space offset
    Ammo_Refills_On_Death = [0xA9, 0x1C, 0xA2, 0x07, 0x95, 0x6A, 
    0xCA, 0x10, 0xFB, 0x4C, 0x30, 0x91] #New assembly for refilling health and ammo
    
    Bomb_Full_Shot_Timer_Offset = (0x164b3) #timer until the shot is considered completed
    Bomb_Explosion_Timer_Offsets = [0x1648A, 0x162cA] #timer until the bomb explodes
    
    # Full Shot Timer is essentially the total time from firing until the explosion dissapears
    # and the player can fire again. While the explosion timer is how long until the bomb explodes
    # The game loads a universal shot timer and does a CMP of values. Here we are overwriting
    # the compares to lower numbers to make the bomb shots similar to vanilla while completing 
    # more quickly
    
    Bomb_Full_Shot_Timer = (0x55)
    Bomb_Explosion_Timer = (0x47)
    
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
            
        #Quicker Bombs
        self.file.seek(self.Bomb_Full_Shot_Timer_Offset)
        self.file.write(int.to_bytes(self.Bomb_Full_Shot_Timer))
        
        for offset in self.Bomb_Explosion_Timer_Offsets:
            self.file.seek(offset)
            self.file.write(int.to_bytes(self.Bomb_Explosion_Timer))
            
            #TO DO: also add bomb improvement patch