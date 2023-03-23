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
    ReadDamageCharts = []
    StageSelectPatch = bool

    def __init__(self, file, params = None):
        super().__init__(file, params)

    # Generates a 6 x 8 byte long damage chart for the main Robot bosses.
    # Each boss has an 8 byte list. Each index corresponds to a weapon, with the value being how much damage it does.
    # Then a weapon is randomly chosen to be the major weakness, and a second weapon is chosen to be the minor weakness
    # Major weakness is simply a nickname for the most damaging weapon in a particular chart(typically 4 damage)
    # Minor weakness is simply a nickname for the second most damaging weapon in a particular chart (typically 2 damage)
    # Each boss' damage chart should have a major weakness unique to that boss, and a minor weakness
    # The minor weakness should just be different from the major weakness
    def __Generate(self):
        self.__ReadDamageChart()
        random.shuffle(self.ReadDamageCharts)  # Shuffles the order of lists without shuffling the lists' contents

        original_index = 0
        for chart in self.ReadDamageCharts:
            # Check if Gutsman's weapon is the most damaging weapon in a chart
            if chart[6] > 3:  # Damage chart has a major weakness to Gutsman's wepaon
                chart[6] = 14  # As mentioned before, buff damage to defeat a boss in only two hits
                new_index = random.choice([0, 4, 5])  # These are the boss rooms that have throwable blocks

                # Swap the original damage chart with a Gutsman weakness (original_index)
                # With a randomly chosen index of 0, 4, or 5 (Cut, Elec, or Guts. They all have throwable blocks)
                damagechart_with_gutsmanweakness = self.ReadDamageCharts[original_index]
                damagechart_with_throwableblocks = self.ReadDamageCharts[new_index]

                # Swap the two charts
                self.ReadDamageCharts[original_index] = damagechart_with_throwableblocks
                self.ReadDamageCharts[new_index] = damagechart_with_gutsmanweakness

                break
            else:
                original_index = original_index + 1
        print(self.ReadDamageCharts)
    def __Write(self):
        self.file.seek(self.DamageTableOffset)
        for damagecharts in self.ReadDamageCharts:
            for damagevalues in damagecharts:
                self.file.write(int.to_bytes(damagevalues))

    def __ReadDamageChart(self):
        # Get the 6 x 8 damage chart
        self.file.seek(self.DamageTableOffset)
        for damagelists in range(6):
            damagelist = []
            for damagevalues in range(8):
                damage = int.from_bytes(self.file.read(1))
                damagelist.append(damage)
            self.ReadDamageCharts.append(damagelist)
        print("Read damage charts ", self.ReadDamageCharts)


    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()
