from BaseClasses.GeneratorBase import *


class DamageToBossGenerator(GeneratorBase):
    # Each boss has its own Damage chart that is 8 bytes long. The index points to the corresponding weapon (PCIBFEGM)
    # And the value is how much damage that weapon does.
    # For Example: Cutman's vanilla damage chart
    #  P  C  I  B  F  E  G  M
    # [3, 1, 0, 2, 3, 1, 14 0]
    ReadDamageCharts = []
    NewDamageCharts = []
    DamageTableOffset = 0x1FDEE

    def __init__(self, file, params = None):
        super().__init__(file, params)

    def __Logic(self):
        # For each boss generate a randomized damage chart
        # While leaving the major and minor weaknesses
        # (The most damaging, and second most damaging values)
        for chart in self.ReadDamageCharts:
            # Find the major weakness index and value
            sortedchart = chart[:]
            sortedchart.sort()
            highestdamageindex = chart.index(sortedchart[7])
            highestdamagevalue = sortedchart[7]
            minorweaknessindex = chart.index(sortedchart[6])
            minorweaknessvalue = sortedchart[6]
            # Create new chart
            generatedchart = self.__damagechartGenerator()
            # Restore original weakness damage
            generatedchart[highestdamageindex] = highestdamagevalue
            generatedchart[minorweaknessindex] = minorweaknessvalue
            self.NewDamageCharts.append(generatedchart)


    def __Generate(self):
        self.__ReadDamageChart()
        self.__Logic()


    def __Write(self):
        self.file.seek(self.DamageTableOffset)
        for damagecharts in self.NewDamageCharts:
            for damagevalues in damagecharts:
                self.file.write(int.to_bytes(damagevalues))
    @staticmethod
    def __damagechartGenerator():
        damagechart = []
        for damageindex in range(8):
            damagevalue = random.choice([0, 1])
            damagechart.append(damagevalue)
        # Hardcode Buster to always do 1 damage, Ice 0 Damage, and Magnet 0 damage
        damagechart[0] = random.choice([1, 2])  # Buster
        damagechart[4] = 0  # Ice always does 0 damage in Vanilla except to Fireman where it does 4
        damagechart[7] = 0  # Magnet creates platforms and isn't intended to deal damage
        return damagechart[:]

    def __ReadDamageChart(self):
        # Get the 6 x 8 damage chart
        self.file.seek(self.DamageTableOffset)
        for damagelists in range(6):
            damagelist = []
            for damagevalues in range(8):
                damage = int.from_bytes(self.file.read(1))
                damagelist.append(damage)
            self.ReadDamageCharts.append(damagelist)

    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()