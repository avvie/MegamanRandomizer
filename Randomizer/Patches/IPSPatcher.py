from pathlib import Path
from BaseClasses.PatchBase import *

class IPSPatcher(PatchBase):
    
    def __init__(self, file, params = None):
        super().__init__(file, params)        
        
    def __GetFile()
    IPS_Folder = Path("./IPSFiles/")
    PatchFile = IPS_Folder / params
    IPSFile = open(PatchFile)
    
    def __Write(self):
    Offset = 0
    Size = 0
    RLE_Size = 0
    Value = 0
    End_of_file_Checker = bytes(b'/x00')
    x = 0
    self.IPSFile.seek(5) #Skip past header
    while End_of_file_Checker != bytes(b'EOF'):
        # print("Patch offset: " ,PatchOffset)
        # self.IPSFile.seek(PatchOffset)
        Record = bytes(self.IPSFile.read(3))
        End_of_file_Checker = Record
        Offset = int.from_bytes(Record, 'big')
        # print("Read ROM offset " , Offset, "at patch offset ", PatchOffset)
        # PatchOffset = PatchOffset+3 #we read 3 bytes and move the offset accordingly
    
        Size = int.from_bytes(self.IPSFile.read(2))
        # PatchOffset = (PatchOffset+2)

        if Size != 0:           
            PatchBytes = self.IPSFile.read(Size)
            self.file.seek(Offset)
            self.file.write(PatchBytes)
        else: 
            # print("RLE patch")
            RLE_Size = int.from_bytes(self.IPSFile.read(2))
            Value = self.IPSFile.read(1)
            # PatchOffset = PatchOffset + 3
            # print("RLE Size ", RLE_Size, "Byte to write ", Value, "at offset ", PatchOffset)
            self.file.seek(Offset)
            while RLE_Size > 0:
                self.file.write(Value)
                RLE_Size = RLE_Size - 1
    self.IPSFile.close()

    def Patch(self):
        super().Patch()
        self.__GetFile()
        self.__Write()
