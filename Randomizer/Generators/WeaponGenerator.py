from BaseClasses.GeneratorBase import *

class WeaponGenerator(GeneratorBase):
    #Original weapon bytes

    Rewards_Table_Offset = 0x1C148
    Boss_Defeated_Table_Offset = 0x1BFCC
    Gutsman_Specific_Fix_Offset = 0x1B69E
    Weakness_Table_Offset = 0x1FDEE
    Weakness_Table = []
    Rewards_Table = []
    def __init__(self, file, params = None):
        super().__init__(file, params)
    def __Generate(self):
        #Get the 8 x 8 byte chart for the weakness table
        self.file.seek(self.Weakness_Table_Offset)
        for list in range(7):
            weakness = []
            for bytes in range(7):
                byte = int.from_bytes(self.file.read(1))
                weakness.append(byte)
            self.Weakness_Table.append(weakness)
        print(self.Weakness_Table)
    #def __Logic(self):


    def Randomize(self):
        super().Randomize()
        self.__Generate()
        #self.__Write()