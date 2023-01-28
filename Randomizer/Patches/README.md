
# Patchers

Patch classes are intended to make singular, non random, changes to the games code.

## How to make a patcher

Define the static parameters of the patcher and initialize the base class through the init
Pass any parameters/data that you want in the class in the params variable.

Define internally how the patching and the writing of the file is going to happen.
The main Patcher class will call the Patch() function, so make sure to override it,
in case the inheritance goes deeper make sure you call the super class Patch function.

```python
    def Patch(self):
        super().Patch()
        self.__PatchLogc()
        self.__Write()
```