import hashlib
import os
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
from Utilities import ParamExistsInArgs, PrintHelp, GetValidFileFromParameter, max_image_file_size, \
    supported_md5_input_checksums, GetHeader, headers, StripHeader, WriteBuffer, ListIntersection, qolPatches, AddHeader


class ConsoleInterface:

    def __init__(self, argv_):
        self.argv_ = argv_

    @staticmethod
    def help_and_exit(args):
        if ParamExistsInArgs(args, '-h'):
            PrintHelp()
            sys.exit(0)

    def main(self,):
        # Get console arguments passed
        args = self.argv_
        input_file = "./Mega Man (USA).nes"
        output_file = "./MMRando.nes"
        ConsoleInterface.help_and_exit(args)
        # Get input file path passed into the app, or default
        input_file = GetValidFileFromParameter(args, '-i', input_file)
        # Get output file path passed into the app, or default
        output_file = GetValidFileFromParameter(args, '-o', output_file, False)

        if not self.validate_input(input_file):
            sys.exit(1)

        self.write_stripped_output_file(input_file, output_file)

        try:
            file = open(output_file, "r+b")
        except Exception as e:
            print(e.with_traceback())
        finally:
            file.close()

        try:
            self.apply_all(args, file, output_file)
        except Exception as e:
            print(e.with_traceback())
            print("\n\nERROR: Creating rom failed\n")

    def apply_all(self, args, file, output_file):
        generator_list = []
        patch_list = []
        ips_patches = []
        self.handle_generator_args(generator_list, args, file)
        self.handle_patch_args(patch_list, args, file)

        (patch_list, ips_patches) = self.separate_patchers(patch_list, ips_patches)
        for patch in ips_patches:
            patch.Patch()
        for patch in patch_list:
            patch.Patch()
        for generator in generator_list:
            generator.Randomize()
        
        # Assume headerless and add header
        AddHeader(headers[0], output_file)

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

    def validate_input(self, input_file):
        if not os.path.exists(input_file):
            print("Input file not found, define an input file")

            # Check for checksum
        if os.path.getsize(input_file) >= max_image_file_size:
            print("File too big")
            return False
        try:
            file = open(input_file, "rb")
            checksum = str(hashlib.md5(file.read()).hexdigest())
        except OSError as e:
            print(e.with_traceback())
        finally:
            file.close()

        if checksum not in supported_md5_input_checksums:
            print("Input file md5 checksum not supported " + checksum)

        return True

