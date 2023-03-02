from BaseClasses.GeneratorBase import *


class WeaknessGenerator(GeneratorBase):
    WeaknessByteIndex = [1, 2, 3, 4, 5, 6]
    DamageTableOffset = 0x1FDEE
    # P C I B F E G M
    DamageChart = [1, 0, 0, 0, 0, 0, 0, 0]  # preset default values
    DamageLists = []

    def __init__(self, file, params = None):
        super().__init__(file, params)

    def __Generate(self):
        while len(self.WeaknessByteIndex) > 0:  # Counting down to 0 as we remove options frm the list
            currentchart = self.DamageChart[:]
            length = len(self.WeaknessByteIndex)

            # Get the byte offset that we're going to set to 4
            r = random.randrange(length)  # From the list of remaining values
            majorweakness = self.WeaknessByteIndex[r]  # Get the offset we'll set to 4

            currentchart[majorweakness] = 4
            self.WeaknessByteIndex.pop(r)  # Remove that as a major weakness so each robot is unique

            if len(self.WeaknessByteIndex) > 0:
                r = random.randrange(len(self.WeaknessByteIndex))
                minorweakness = self.WeaknessByteIndex[r]
                currentchart[minorweakness] = 2
            else:
                currentchart[0] = 3  # Gives a buster weakness if were out of boss weapons
            self.DamageLists.append(currentchart)

    # Here we shuffle the list order - this shuffles it from the last boss to any random one
    # Next we find where the Gutsman weakness is (it's the 7th byte in a chart)
    # Then we swap the index with the Gutsman weakness with a randomly chosen boss that has throwable blocks

    def __Logic(self):
        random.shuffle(self.DamageLists)  # Shuffles the lists without shuffling the lists' contents

        original_index = 0
        for damagevalue in self.DamageLists:
            # Checks if the major weakness in assigned to Gutsman
            if damagevalue[6] > 3:  # Has a major weakness to Gutsman
                new_index = random.choice([0, 4, 5])  # These are the boss rooms that have throwable blocks

                # we want to swap the original list with Gutsman weakness (original_index)
                # with the randomly chosen index of 0, 4, or 5 (Cut, Elec, or Guts)
                list_with_gutsman_weakness = self.DamageLists[original_index]
                list_to_swap = self.DamageLists[new_index]

                # Swap the two lists
                self.DamageLists[original_index] = list_to_swap
                self.DamageLists[new_index] = list_with_gutsman_weakness

                break
            else:
                original_index = original_index + 1

    def __Write(self):
        print("Weakness table", self.DamageLists)
        self.file.seek(self.DamageTableOffset)
        for damagelist in self.DamageLists:
            for damagebytes in damagelist:
                self.file.write(int.to_bytes(damagebytes))

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Logic()
        self.__Write()
