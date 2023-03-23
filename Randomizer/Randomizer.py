import shutil
import sys

from Generators.WeaknessGenerator import WeaknessGenerator
from Generators.DamageToBossGenerator import DamageToBossGenerator
from Generators.MusicGenerator import MusicGenerator
from Generators.PaletteGenerator import PaletteGenerator
from Generators.WeaponGenerator import WeaponGenerator
from Patches.StageClearCutscene import StageClearCutscene
from Patches.WeaknessVisualizer import WeaknessVisualizer
from Patches.RollChan import RollChanPatch
from Offsets import Megaman_Default
from Patches.AmmoRefilOnDeath import AmmoRefilOnDeath
from Patches.BombBuff import BombBuff
from Patches.IPSPatcher import IPSPatcher
from Patches.QualityOfLifePatches import QualityOfLifePatches
from RandomizerFlagLogic import RandomizerFlagLogic
from Utilities import __add_header__, headers, ParamExistsInArgs, ListIntersection, qolPatches, GetHeader, StripHeader, \
    WriteBuffer


class Randomizer:
    def __init__(self, FlagLogic):
        self.file = None
        self.flag_logic = FlagLogic

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file is not None:
            self.file.close()

    def Run(self, args, input_file, output_file):

        self.__prepare_output_file__(input_file, output_file)

        generator_list = []
        patch_list = []
        ips_patches_list = []
        self.__handle_generator_args__(generator_list, args, self.file)
        self.__handle_patch_args__(patch_list, args, self.file)

        (patch_list, ips_patches_list) = self.__separate_patchers__(patch_list, ips_patches_list)

        with self.flag_logic() as flag_logic:
            flag_logic.apply_randomizer_logic_flags(generator_list, patch_list, ips_patches_list)

        self.__apply_ips_patches__(ips_patches_list)
        self.__apply_patches__(patch_list)
        self.__apply_generators__(generator_list)
        self.file.close()
        # Assume headerless and add header
        __add_header__(headers[0], output_file)

    def __prepare_output_file__(self, input_file, output_file):
        self.write_stripped_output_file(input_file, output_file)

        try:
            self.file = open(output_file, "r+b")
        except Exception as e:
            print(e.with_traceback())

    def __apply_generators__(self, generator_list):
        for generator in generator_list:
            generator.Randomize()

    def __apply_patches__(self, patch_list):
        for patch in patch_list:
            patch.Patch()

    def __apply_ips_patches__(self, ips_patches):
        for patch in ips_patches:
            patch.Patch()

    def __separate_patchers__(self, patch_list, ips_list):
        for patcher in patch_list:
            if patcher is IPSPatcher:
                ips_list.append(patcher)
        out_list = [i for i in patch_list if i not in ips_list]
        return out_list, ips_list

    def __handle_patch_args__(self, PatchList, args, file):
        if ParamExistsInArgs(args, '+roll'):
            PatchList.append(RollChanPatch(file))

        if ParamExistsInArgs(args, '+stageclear'):
            PatchList.append(StageClearCutscene(file))

        if ParamExistsInArgs(args, '+weaknessviz'):
            PatchList.append(WeaknessVisualizer(file))

        if not ParamExistsInArgs(args, '-qol') and len(ListIntersection(args, qolPatches)) == 0:
            PatchList.append(QualityOfLifePatches(file))

        elif not ParamExistsInArgs(args, '-a'):
            PatchList.append(AmmoRefilOnDeath(file))

        elif not ParamExistsInArgs(args, '-b'):
            PatchList.append(BombBuff(file))

    def __handle_generator_args__(self, GeneratorList, args, file):
        if ParamExistsInArgs(args, '+damage'):
            GeneratorList.append(DamageToBossGenerator(file))
        if ParamExistsInArgs(args, '+weakness'):
            GeneratorList.append(WeaknessGenerator(file))
        if not ParamExistsInArgs(args, '-w'):
            GeneratorList.append(WeaponGenerator(file))
        if not ParamExistsInArgs(args, '-p'):
            GeneratorList.append(PaletteGenerator(file, Megaman_Default))
        if ParamExistsInArgs(args, '+music'):
            GeneratorList.append(MusicGenerator(file))

    def write_stripped_output_file(self, input_file, output_file):
        try:
            if GetHeader(input_file) in headers:
                headerless_buffer = StripHeader(input_file)
                WriteBuffer(output_file, headerless_buffer)
            else:
                # Assume headerless and whatever happens
                shutil.copyfile(input_file, output_file)
        except Exception as e:
            print(e.with_traceback())
            sys.exit(1)
