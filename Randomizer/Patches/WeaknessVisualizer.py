from Patches.IPSPatcher import IPSPatcher


class WeaknessVisualizer(IPSPatcher):
    def __init__(self, file, params=None):
        super().__init__(file, "WEAKNESSVISUALIZER.ips")

    def Patch(self):
        super().Patch()
