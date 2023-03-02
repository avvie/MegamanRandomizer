from BaseClasses.GeneratorBase import *

class WeaponGenerator(GeneratorBase):
    #Original weapon reward bytes
    #Cut, Ice, Bomb, Fire, Elec, Guts
    Weapon_Rewards = [0x20, 0x10, 0x02, 0x40, 0x04, 0x08]
    Rewards_Table_Offset = 0x1C148
    Boss_Defeated_Table_Offset = 0x1BFCC
    Gutsman_Specific_Fix_Offset = 0x1B69E
    Damage_Table_Offset = 0x1FDEE
    DamageLists = []
    Rewards_Table = []
    #This may be dumb to use
    #Converts index of most damaging weapon to the corrosponding weapon reward
    DamageIndex_to_Reward_Dict = {1: 0x20, 2: 0x10, 3: 0x02, 4: 0x40, 5: 0x04, 6: 0x08}
    def __init__(self, file, params = None):
        super().__init__(file, params)

    def __Logic(self):
        #For each boss damage list in the Damage Chart
        #Find the index of the weapon that does the most damage to that boss and exclude it as an option
        #Then give a random reward from valid options
        for damagelist in self.DamageLists:
            rewardlist = self.Weapon_Rewards[:] #A copy makes it easier to temporarly remove a reward

            sorted_damagelist = damagelist[:]
            sorted_damagelist.sort() #sets highest damage value to the last (7th) index

            # Weakness is just a nick name for the weapon that does the most damage
            #Find the highest value's index from the original damage list


            excluded_index = damagelist.index(sorted_damagelist[7])
            #Convert from damage index to weapon reward
            excluded_award = self.DamageIndex_to_Reward_Dict[excluded_index]
            print("Major weakness", excluded_award)

            #Remove the excluded reward as an option from the temporary list
            #The reward may have already been assigned to another boss - use try to see
            try:
                rewardlist.pop(rewardlist.index(excluded_award))
            except ValueError:
                pass #already removed

            #Assign a random reward from remaining options
            try:
                reward = random.choice(rewardlist)
            except IndexError: #Last reward available has been excluded
                #Lets just swap the excluded reward with the previous one
                prev_reward = self.Rewards_Table[4]
                self.Rewards_Table[4] = excluded_award
                self.Rewards_Table.append(prev_reward)
            else:
            #Remove chosen reward from future options
                self.Weapon_Rewards.pop(self.Weapon_Rewards.index(reward))
                self.Rewards_Table.append(reward)
            print("rewards table ", self.Rewards_Table)


    def __Generate(self):
        self.__ReadDamageChart()
        self.__Logic()

    def __Write(self):
        self.file.seek(self.Rewards_Table_Offset)
        for reward in self.Rewards_Table:
            self.file.write(int.to_bytes(reward))

        self.file.seek(self.Boss_Defeated_Table_Offset)
        for reward in self.Rewards_Table:
            self.file.write(int.to_bytes(reward))

        self.file.seek(self.Gutsman_Specific_Fix_Offset)  # Gutsman drawn sprite works differently on the level select
        self.file.write(int.to_bytes(self.Rewards_Table[5]))


    def __ReadDamageChart(self):
        #Get the 6 x 8 damage chart
        self.file.seek(self.Damage_Table_Offset)
        for damagelists in range(6):
            damagelist = []
            for damagevalues in range(8):
                damage = int.from_bytes(self.file.read(1))
                damagelist.append(damage)
            self.DamageLists.append(damagelist)
        print(self.DamageLists)

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()