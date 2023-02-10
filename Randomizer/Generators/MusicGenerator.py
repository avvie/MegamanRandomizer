from BaseClasses.GeneratorBase import *

class MusicGenerator(GeneratorBase):
    
    def __init__(self, file, params = None):
        super().__init__(file, params)


    def __Generate(self):
        self.stage_music_table = [0x05,0x0f,0x08,0x07,0x09,0x0a,0x0c,0x0c,0x10,0x10,0x10,0x0e]
        random.shuffle(self.stage_music_table)
        
    def __Write(self):
        self.file.seek(0x15394)
        for song in self.stage_music_table:
            self.file.write(int.to_bytes(song))
        
    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()