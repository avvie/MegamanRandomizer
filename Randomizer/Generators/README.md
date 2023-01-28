
# Generators

Generator classes are defined to randomize different parts of the game

## How to make a generator

Define the static parameters of the generator and initialize the base class through the init
Pass any parameters/data that you want in the class in the params variable.

```python
#Original weapon bytes
    Vanilla_Weapons = [0x20, 0x10, 0x02, 0x40, 0x04, 0x08]
    Weapons_Write_Offset = 0x1C148
    Boss_Defeated_Weapon_Write_Offset = 0x1BFCC
    Gutsman_Specific_Fix_Write_Offset = 0x1B69E

    def __init__(self, file, params = None):
        super().__init__(file, params)

```
Define internally how the generation and the writing of the file is going to happen.
The main randomizer class will call the Randomize() function, so make sure to override it,
in case the inheritance goes deeper make sure you call the super class Randomize function.

```python
    def Randomize(self):
        super().Randomize()
        self.__Generate()
        self.__Write()
```