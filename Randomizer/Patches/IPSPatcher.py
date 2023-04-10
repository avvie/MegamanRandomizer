from pathlib import Path
from BaseClasses.PatchBase import *

class IPSPatcher(PatchBase):
    
    def __init__(self, file, params=None):
        super().__init__(file, params)        
        
    def __GetFile(self):
        self.ips_folder = Path("IPSFiles/")
        self.patch_file = self.ips_folder / self.params
        self.ips_file = open(self.patch_file, "r+b")
    
    def __Write(self):
        record = bytes()
        self.ips_file.seek(5) #skip past "PATCH" string header in the ips file
        while record != bytes(b'EOF'): #Checks for string "EOF" (end of file) that ends an ips file
            record = bytes(self.ips_file.read(3))
            offset = (int.from_bytes(record, 'big')) - 0x10 #Subtracting the header size
            size = int.from_bytes(self.ips_file.read(2))

            if size != 0:           
                patchbytes = self.ips_file.read(size)
                self.file.seek(offset)
                self.file.write(patchbytes)
                
            else: 
                rle_size = int.from_bytes(self.ips_file.read(2))
                value = self.ips_file.read(1)
                self.file.seek(offset)
                while rle_size > 0:
                    self.file.write(value)
                    rle_size = rle_size - 1

        self.ips_file.close()

    def Patch(self):
        super().Patch()
        self.__GetFile()
        self.__Write()

###Credit https://zerosoft.zophar.net/ips.php ZeroSoft for ips file format specification