import os.path

def __add_header__(header, __output_file):
    with open(__output_file,'r+b') as contents:
        save = contents.read()
    with open(__output_file,'w+b') as contents:
        contents.write(header)
    with open(__output_file,'a+b') as contents:
        contents.write(save)


# Gets the path to a valid file passed in arguments, positionally after param
def GetValidFileFromParameter(paramList: object, param: object, default: object = None, check_existence: object = True) -> object:
    if param in paramList:
        i = paramList.index(param)
        if i+1 < len(paramList):
            if os.path.exists(paramList[i+1]) or not check_existence:
                local = paramList[i+1]
                return local
    return default


def ParamExistsInArgs(paramList, param):
    if param in paramList:
        return True
    return False


def PrintHelp():
    print ("Help menu for MegamanRandomizer:\n\n" +
           "-i [filePath]:\t Set a specific input file path. Default: ./Mega Man (USA).nes\n" +
           "-o [filePath]:\t Set a specific output file path. Default: ./MMRando.nes\n" +
           "\nRandomizer Options:\n" +
           "-w:\tDo NOT randomize weapon drops. Default: Weapons WILL get randomized\n" +
           "-p:\tDo NOT randomize  color palettes. Default: Palettes WILL get randomized\n" +
           "+weakness\t Randomizes new damage charts for the main 6 bosses with with classic MM styled weaknesses \n" +
           "+music:\tShuffle stage music. Default: Music WILL NOT get randomized\n" +
           "+stageclear:\t Mega Man now fires his new obtained weapon upon clearing the stage. Default: Off\n" +
           "\nGame Patches\n"+
           "+roll:\t Applies Roll-Chan graphics patch (Credit:\t ZYNK). Defualt: Off\n" +
           "-qol:\tDo NOT apply Quality of Life patch. Default: Patch WILL be applied\n" +
           "\tQuality of life buffs bomb weapon and refills ammo upon death\n"+
           "\n\tDisable individual patches from QoL set:\n\n"+
           "\t-a:\tDo NOT apply ammo refill patch\n"+
           "\t-b:\tDo Not apply bomb timer buff patch\n"+
           "\n"
           )


qolPatches = ['-a', '-b']


def ListIntersection(a, b):
    return list(set(a) & set(b))


supported_md5_input_checksums = ["4de82cfceadbf1a5e693b669b1221107", "4d4ffdfe7979b5f06dec2cf3563440ad"]


max_image_file_size = 150*1024


headers = [
    bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x08\x20\x00\x00\x07\x00\x00\x00\x01'),
    bytes(b'\x4E\x45\x53\x1A\x08\x00\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    ]


def GetHeader(__filename):
    with open(__filename,'rb') as contents:
        # Header is in the first 16 bytes
        return contents.read(16)


def StripHeader(path):
    with open(path,'rb') as contents:
        buffer = contents.read()[16:]
    return buffer


def WriteBuffer(path, buffer):
    if os.path.exists(path):
        os.remove(path)
    with open(path,'+bw') as contents:
        contents.write(buffer)


