class RandomizerFlagLogic:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def apply_randomizer_logic_flags(self, generator_list, patch_list, ips_patches_list):
        if self.NameTester('RollChanPatch', patch_list) and \
                self.NameTester('PaletteGenerator', generator_list):
            print("Character patches currently lack palette Randomization support\n" +
                  "Removing randomized palettes")
            self.RemoveFromList('PaletteGenerator', generator_list)

        if self.NameTester('StageClearCutscene', patch_list) and \
                self.NameTester('WeaponGenerator', generator_list):
            generator_list[self.ReturnIndex('WeaponGenerator', generator_list)].StageClearCutscene = True

        if self.NameTester('WeaknessVisualizer', patch_list) and \
                self.NameTester('WeaponGenerator', generator_list):
            generator_list[self.ReturnIndex('WeaponGenerator', generator_list)].WeaknessVisualizer = True

        if self.NameTester('WeaknessVisualizer', patch_list) and \
                self.NameTester('WeaknessGenerator', generator_list):
            generator_list[self.ReturnIndex('WeaknessGenerator', generator_list)].WeaknessVisualizer = True

    def ParamTester(self, objectotest, listtocheck):
        for objects in listtocheck:
            if objectotest in objects.params:
                return True

    def NameTester(self, name, list):
        for objects in list:
            if objects.__class__.__name__ == name:
                return True

    def RemoveFromList(self, classname, _list):
        for classes in _list:
            if classes.__class__.__name__ == classname:
                _list.pop(_list.index(classes))

    def ReturnIndex(self, classname, _list):
        for classes in _list:
            if classes.__class__.__name__ == classname:
                return _list.index(classes)
