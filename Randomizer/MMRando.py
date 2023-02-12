import sys

from ConsoleInterface import ConsoleInterface

if __name__ == "__main__":
    with ConsoleInterface(sys.argv[1:]) as program_entry:
        program_entry.main()

