from BaseClasses.GeneratorBase import *

class WeaknessGenerator(GeneratorBase):
    WeaknessByteOffset = [1, 2, 3, 4, 5, 6]
    DamageTable = 0x1FDEE
    # P C I B F E G M
    WeaknessChart = [1, 0, 0, 0, 0, 0, 0, 0]  # preset default values
    WeaknessList = []

    def __init__(self, file, params = None):
        super().__init__(file, params)


    def __Generate(self):
        while len(self.WeaknessByteOffset) > 0:
            currentchart = self.WeaknessChart[:]
            length = len(self.WeaknessByteOffset)

            # Get the byte offset that we're going to set to 4
            r = random.randrange(length)  # From the list of remaining values
            majorweakness = self.WeaknessByteOffset[r]  # Get the offset well set to 4

            currentchart[majorweakness] = 4
            self.WeaknessByteOffset.pop(r)  # Remove that as a major weakness so each robot is unique

            if len(self.WeaknessByteOffset) > 0:
                r = random.randrange(len(self.WeaknessByteOffset))
                minorweakness = self.WeaknessByteOffset[r]
                currentchart[minorweakness] = 2
            else:
                currentchart[0] = 3 #Gives a buster weakness if were out of boss weapons
            self.WeaknessList.append(currentchart)
        self.__Organize()

    #Here we shuffle the list order - this shuffles it from the last boss to any random one
    #Next we find where the Gutsman weakness is (it's the 7th byte in a chart)
    #Then we swap the index with the Gutsman weakness with a randomly chosen boss that has throwable blocks
    def __Organize(self):
        random.shuffle(self.WeaknessList) #Shuffles the lists without shuffling the lists' contents

        original_index = 0
        for weaknesses in self.WeaknessList:
            # Checks if the major weakness in assigned to Gutsman
            if weaknesses[6] > 3: #Has a major weakness to Gutsman
                new_index = random.choice([0, 4, 5]) #These are the boss rooms that have throwable blocks

                # we want to swap the original list with Gutsman weakness (original_index)
                # with the randomly chosen index of 0, 4, or 5 (Cut, Elec, or Guts)
                oldgutsman_weakness_value = self.WeaknessList[original_index]
                newgutsman_weakness_value = self.WeaknessList[new_index]

                # Move the original values to the randomly chosen index
                self.WeaknessList.insert(new_index, oldgutsman_weakness_value)

                # Remove the extra copy
                self.WeaknessList.pop(new_index + 1)
                # Replace the values from the randomly chosen index into the index original_index was at
                self.WeaknessList.insert(original_index, newgutsman_weakness_value)
                # Delete the extra
                self.WeaknessList.pop(original_index + 1)
                # Add extra damage for Gutsman weakness
                self.WeaknessList[new_index][6] += 10
                break
            else:
                original_index = original_index + 1

    def __Write(self):
        print("Weakness table", self.WeaknessList)
        self.file.seek(self.DamageTable)
        for list in self.WeaknessList:
            for bytes in list:
                self.file.write(int.to_bytes(bytes))







    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()