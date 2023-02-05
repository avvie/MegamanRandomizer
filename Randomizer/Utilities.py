import os.path

def AddHeader(header, __output_file):
    with open(__output_file,'r+b') as contents:
        save = contents.read()
    with open(__output_file,'w+b') as contents:
        contents.write(header)
    with open(__output_file,'a+b') as contents:
        contents.write(save)

# Gets the path to a valid file passed in arguments, positionally after param
def GetValidFileFromParameter(paramList, param, default = None, check_existence = True):
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
           "-w:\t Do NOT randomize weapon drops. Default: Weapons WILL get randomized\n" +
           "-p:\t Do NOT randomize pallete drops. Default: Palletes WILL get randomized\n" +
           "-roll:\t Applies Roll-Chan graphics patch (Credit:\t ZYNK). Defualt: Off\n")

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
