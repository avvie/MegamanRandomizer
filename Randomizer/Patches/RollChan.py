from Patches.IPSPatcher import IPSPatcher


class RollChanPatch(IPSPatcher):
    def __init__(self, file, params=None):
        super().__init__(file, "ROLLCHAN.ips")

    def Patch(self):
        super().Patch()

