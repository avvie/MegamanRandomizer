from BaseClasses.PatchBase import *

class IPS(PatchBase):
    PatchFile = open(file("./IPS/ROLLCHAN.ips"))
    
    def __init__(self, file, params = None):
        super().__init__(file, params)
        
    def Patch(self):
        super().Patch()
        self.__Write()
        
    def __Write(self):
    Offset = 0
    Size = 0
    RLE_Size = 0
    Value = 0
    End_of_file_Checker = bytes(b'/x00')
    x = 0
    PatchFile.seek(5)
    while End_of_file_Checker != bytes(b'EOF'):
        # print("Patch offset: " ,PatchOffset)
        # PatchFile.seek(PatchOffset)
        Record = bytes(PatchFile.read(3))
        End_of_file_Checker = Record
        Offset = int.from_bytes(Record, 'big')
        # print("Read ROM offset " , Offset, "at patch offset ", PatchOffset)
        # PatchOffset = PatchOffset+3 #we read 3 bytes and move the offset accordingly
    
        Size = int.from_bytes(PatchFile.read(2))
        # PatchOffset = (PatchOffset+2)

        if Size != 0:
            if Size == 1:
                print("Sketchy patch at patchoffset ", PatchOffset, "writing to ", Offset, " Offset")
            # PatchOffset = PatchOffset + Size #read 2 bytes and move the offset accordingly then move forward how many bytes we've written
            PatchBytes = PatchFile.read(Size)
            RomFile.seek(Offset)
            RomFile.write(PatchBytes)
        else:
            # print("RLE patch")
            RLE_Size = int.from_bytes(PatchFile.read(2))
            Value = PatchFile.read(1)
            # PatchOffset = PatchOffset + 3
            # print("RLE Size ", RLE_Size, "Byte to write ", Value, "at offset ", PatchOffset)
            RomFile.seek(Offset)
            while RLE_Size > 0:
                RomFile.write(Value)
                RLE_Size = RLE_Size - 1
