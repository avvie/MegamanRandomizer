import hashlib
import os
import sys

from Randomizer import Randomizer
from RandomizerFlagLogic import RandomizerFlagLogic
from Utilities import ParamExistsInArgs, PrintHelp, GetValidFileFromParameter, max_image_file_size, \
    supported_md5_input_checksums


class ConsoleInterface:

    def __init__(self, argv_, flag_logic=None):
        self.argv_ = argv_
        self.flag_logic = flag_logic
        if self.flag_logic is None:
            self.flag_logic = RandomizerFlagLogic

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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

        try:
            with Randomizer(self.flag_logic) as rando:
                rando.Run(args, input_file, output_file)
        except Exception as e:
            print(e.with_traceback())
            print("\n\nERROR: Creating rom failed\n")

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

