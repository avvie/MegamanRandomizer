from BaseClasses.GeneratorBase import *


class WeaknessGenerator(GeneratorBase):
    #                    C  I  B  F  E  G
    BossWeaponIndexes = [1, 2, 3, 4, 5, 6]
    DamageTableOffset = 0x1FDEE
    # Each boss has its own Damage chart that is 8 bytes long. The index points to the corresponding weapon (PCIBFEGM)
    # And the value is how much damage that weapon does.
    # For Example: Cutman's vanilla damage chart
    #  P  C  I  B  F  E  G  M
    # [3, 1, 0, 2, 3, 1, 14 0]
    DamageCharts = []  # Damage charts that ultimately get written to rom

    def __init__(self, file, params = None):
        super().__init__(file, params)

    # Generates a 6 x 8 byte long damage chart for the main Robot bosses.
    # Each boss has an 8 byte list. Each index corresponds to a weapon, with the value being how much damage it does.
    # For each chart, most weapons have a 50/50 chance to deal 0 or 1 damage (Buster is always set to 1)
    # Then a weapon is randomly chosen to be the major weakness, and a second weapon is chosen to be the minor weakness
    # Major weakness is simply a nickname for the most damaging weapon in a particular chart(typically 4 damage)
    # Minor weakness is simply a nickname for the second most damaging weapon in a particular chart (typically 2 damage)
    # Each boss' damage chart should have a major weakness unique to that boss, and a minor weakness
    # The minor weakness should just be different from the major weakness
    def __Generate(self):
        # Choosing a random boss weapon for the major weakness
        while len(self.BossWeaponIndexes) > 0:  # Counting down to 0 as we remove options from the list
            newdamagechart = self.__damagechartGenerator()
            remainingoptions = len(self.BossWeaponIndexes)

            # Get the index of the random weapon we're going to assign 4 damage to
            randomweaponindex = random.randrange(remainingoptions)
            majorweaknessindex = self.BossWeaponIndexes[randomweaponindex]

            newdamagechart[majorweaknessindex] = 4
            self.BossWeaponIndexes.pop(randomweaponindex)  # Remove for each robot to have a unique major weakness

            # Choosing a boss weapon for the minor weakness
            if len(self.BossWeaponIndexes) > 0:
                randomweaponindex = random.randrange(len(self.BossWeaponIndexes))
                minorweakness = self.BossWeaponIndexes[randomweaponindex]
                newdamagechart[minorweakness] = 2
            else:  # Give a minor weakness to buster if were out of boss weapons
                newdamagechart[0] = 3  # Buster can't be a major weakness, let's give it a small buff in damage
            self.DamageCharts.append(newdamagechart)

    # For logic, we need to shuffle the order of lists to randomize the buster minor weakness
    # Also only certain boss rooms have throwable blocks to utilize the weakness to Gutsman's weapon
    # Logic sets the damage chart with a major weakness to Gutsman's weapon to a boss fight with throwable blocks
    # Lastly, as there's only two throwable blocks - Buff Gutsman's weapon to deal 14 damage to kill a boss in two hits
    def __Logic(self):
        random.shuffle(self.DamageCharts)  # Shuffles the order of lists without shuffling the lists' contents

        original_index = 0
        for chart in self.DamageCharts:
            # Check if Gutsman's weapon is the most damaging weapon in a chart
            if chart[6] > 3:  # Damage chart has a major weakness to Gutsman's wepaon
                chart[6] = 14  # As mentioned before, buff damage to defeat a boss in only two hits
                new_index = random.choice([0, 4, 5])  # These are the boss rooms that have throwable blocks

                # Swap the original damage chart with a Gutsman weakness (original_index)
                # With a randomly chosen index of 0, 4, or 5 (Cut, Elec, or Guts. They all have throwable blocks)
                damagechart_with_gutsmanweakness = self.DamageCharts[original_index]
                damagechart_with_throwableblocks = self.DamageCharts[new_index]

                # Swap the two charts
                self.DamageCharts[original_index] = damagechart_with_throwableblocks
                self.DamageCharts[new_index] = damagechart_with_gutsmanweakness

                break
            else:
                original_index = original_index + 1

    def __Write(self):
        print("Weakness table", self.DamageCharts)
        self.file.seek(self.DamageTableOffset)
        for damagecharts in self.DamageCharts:
            for damagevalues in damagecharts:
                self.file.write(int.to_bytes(damagevalues))

    @staticmethod
    def __damagechartGenerator():
        damagechart = []
        for damageindex in range(8):
            damagevalue = random.choice([0, 1])
            damagechart.append(damagevalue)
        # Hardcode Buster to always do 1 damage, Ice 0 Damage, and Magnet 0 damage
        damagechart[0] = 1  # Buster
        damagechart[4] = 0  # Ice always does 0 damage in Vanilla except to Fireman where it does 4
        damagechart[7] = 0  # Magnet creates platforms and isn't intended to deal damage
        return damagechart[:]

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Logic()
        self.__Write()
