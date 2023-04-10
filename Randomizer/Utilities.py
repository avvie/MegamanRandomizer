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
           "+weakness:\tRandomizes weaknesses of the main 6 Robots: Default Off \n" +
           "+damagetoboss:\tRandomizes damage dealt to main 6 Robots excluding weaknesses: Default Off \n" +
           "+music:\tShuffle stage music. Default: Music WILL NOT get randomized\n" +
           "\nGame Patches\n"+
           "+stageclear:\tMega Man now fires his newly obtained weapon upon clearing the stage: Default: Off\n" +
           "+weaknessviz:\tMarks levels on stage select based on if you have that bosses weakness: Default Off\n" +
           "\tRed for not having it, Green for having it, Black for level completed\n" +
           "+roll:\tApplies Roll-Chan graphics patch (Credit:\t ZYNK). Defualt: Off\n" +
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


