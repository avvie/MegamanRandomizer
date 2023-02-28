from BaseClasses.GeneratorBase import *

class WeaponGenerator(GeneratorBase):
    #Original weapon bytes
    #Cut, Ice, Bomb, Fire, Elec, Guts
    Weapon_Rewards = [0x20, 0x10, 0x02, 0x40, 0x04, 0x08]
    Rewards_Table_Offset = 0x1C148
    Boss_Defeated_Table_Offset = 0x1BFCC
    Gutsman_Specific_Fix_Offset = 0x1B69E
    Weakness_Table_Offset = 0x1FDEE
    Weakness_Table = []
    Rewards_Table = []
    #This may be dumb to use
    #converts which index is the major weakness at the corrosponding reward value
    Weakness_Reward_Dict = {1: 0x20, 2: 0x10, 3: 0x02, 4: 0x40, 5: 0x04, 6: 0x08}
    def __init__(self, file, params = None):
        super().__init__(file, params)
    def __CreateWeaknessChart(self):
        #Get the 6 x 8 byte chart for the weakness table
        self.file.seek(self.Weakness_Table_Offset)
        for list in range(6):
            weakness = []
            for bytes in range(8):
                byte = int.from_bytes(self.file.read(1))
                weakness.append(byte)
            self.Weakness_Table.append(weakness)
        print(self.Weakness_Table)
    def __Organize(self):
        #For each list in Weakness Chart
        #Find the index of the major weakness
        for weaknesslist in self.Weakness_Table:
            rewardlist = self.Weapon_Rewards[:]
            sortedlist = weaknesslist[:]
            sortedlist.sort() #sets major weakness to the last index
            #now that we know the major weakness index, we can temporerly remove it from the rewards
            #and assign a random one
            #sense we're modifying lists we need to go by value instead of index

            #Find the weakness index in the original list using the sorted one
            #The major weakness will be index 7 in the sorted list
            weakness_index = weaknesslist.index(sortedlist[7])
            #Convert from weakness index to weapon reward
            major_weakness_weapon = self.Weakness_Reward_Dict[weakness_index]
            print("Major weakness", major_weakness_weapon)
            #Temporily remove the major weakness
            #As another option may have removed it we can use try and skip it if it's already removed
            try:
                rewardlist.pop(rewardlist.index(major_weakness_weapon))
            except ValueError:
                pass #already removed

            try:
                reward = random.choice(rewardlist)
            except IndexError: #Last weapon available was the major weakness, which was removed
                #Lets just swap the last two weaknesses?
                prev_reward = self.Rewards_Table[4]
                new_reward = major_weakness_weapon
                self.Rewards_Table[4] = new_reward
                self.Rewards_Table.append(prev_reward)
            else:
            #Remove reward from options
                self.Weapon_Rewards.pop(self.Weapon_Rewards.index(reward))
                self.Rewards_Table.append(reward)
            print("rewards table ", self.Rewards_Table)


    def __Generate(self):
        self.__CreateWeaknessChart()
        self.__Organize()

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        #self.__Write()