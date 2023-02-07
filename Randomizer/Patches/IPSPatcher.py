from pathlib import Path
from BaseClasses.PatchBase import *

class IPSPatcher(PatchBase):
    
    def __init__(self, file, params = None):
        super().__init__(file, params)        
        
    def __GetFile(self):
        self.IPS_Folder = Path("IPSFiles/")
        self.PatchFile = self.IPS_Folder / self.params
        self.IPSFile = open(self.PatchFile, "r+b")
    
    def __Write(self):
        record = bytes()
        self.IPSFile.seek(5) #skip past PATCH string header in the ips file
        while record != bytes(b'EOF'): #Checks for the EOF (end of file) string that ends an ips file
            record = bytes(self.IPSFile.read(3))
            end_of_file_checker = record
            offset = (int.from_bytes(record, 'big')) - 0x10 #Subtracting the header size
            size = int.from_bytes(self.IPSFile.read(2))


            if size != 0:           
                PatchBytes = self.IPSFile.read(size)
                self.file.seek(offset)
                self.file.write(PatchBytes)
            else: 
                rle_size = int.from_bytes(self.IPSFile.read(2))
                value = self.IPSFile.read(1)
                self.file.seek(offset)
                while rle_size > 0:
                    self.file.write(value)
                    rle_size = rle_size - 1
        self.IPSFile.close()

    def Patch(self):
        super().Patch()
        self.__GetFile()
        self.__Write()
###Credit https://zerosoft.zophar.net/ips.php ZeroSoft for ips file format specification