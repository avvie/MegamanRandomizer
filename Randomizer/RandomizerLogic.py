import shutil
import sys

from Generators.MusicGenerator import MusicGenerator
from Generators.PaletteGenerator import PaletteGenerator
from Generators.WeaponGenerator import WeaponGenerator
from Offsets import Megaman_Default
from Patches.AmmoRefilOnDeath import AmmoRefilOnDeath
from Patches.BombBuff import BombBuff
from Patches.IPSPatcher import IPSPatcher
from Patches.QualityOfLifePatches import QualityOfLifePatches
from Utilities import AddHeader, headers, ParamExistsInArgs, ListIntersection, qolPatches, GetHeader, StripHeader, \
    WriteBuffer


class RandomizerLogic:
    def __init__(self):
        self.file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file is not None:
            self.file.close()

    def prepare_output_file(self, input_file, output_file):
        self.write_stripped_output_file(input_file, output_file)

        try:
            self.file = open(output_file, "r+b")
        except Exception as e:
            print(e.with_traceback())

    def Run(self, args, input_file, output_file):

        self.prepare_output_file(input_file, output_file)

        generator_list = []
        patch_list = []
        ips_patches = []
        self.handle_generator_args(generator_list, args, self.file)
        self.handle_patch_args(patch_list, args, self.file)

        (patch_list, ips_patches) = self.separate_patchers(patch_list, ips_patches)
        self.apply_ips_patches(ips_patches)
        self.apply_patches(patch_list)
        self.apply_generators(generator_list)

        # Assume headerless and add header
        AddHeader(headers[0], output_file)

    def apply_generators(self, generator_list):
        for generator in generator_list:
            generator.Randomize()

    def apply_patches(self, patch_list):
        for patch in patch_list:
            patch.Patch()

    def apply_ips_patches(self, ips_patches):
        for patch in ips_patches:
            patch.Patch()

    def separate_patchers(self, patch_list, ips_list):
        for patcher in patch_list:
            if patcher is IPSPatcher:
                ips_list.append(patcher)
        out_list = [i for i in patch_list if i not in ips_list]
        return out_list, ips_list

    def handle_patch_args(self, PatchList, args, file):
        if ParamExistsInArgs(args, '+roll'):
            PatchList.append(IPSPatcher(file, "ROLLCHAN.ips"))
        if not ParamExistsInArgs(args, '-qol') and len(ListIntersection(args, qolPatches)) == 0:
            PatchList.append(QualityOfLifePatches(file))

        elif not ParamExistsInArgs(args, '-a'):
            PatchList.append(AmmoRefilOnDeath(file))

        elif not ParamExistsInArgs(args, '-b'):
            PatchList.append(BombBuff(file))

    def handle_generator_args(self, GeneratorList, args, file):
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
