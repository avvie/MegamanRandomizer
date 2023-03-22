from Patches.IPSPatcher import IPSPatcher


class StageClearCutscene(IPSPatcher):
    def __init__(self, file, params=None):
        super().__init__(file, "STAGECLEARCUTSCENE.ips")

    def Patch(self):
        super().Patch()