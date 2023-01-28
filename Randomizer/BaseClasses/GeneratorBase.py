from BaseClasses.BaseTargetOp import BaseTargetOp
import random

class GeneratorBase(BaseTargetOp):
	def __init__(self, file, params):
		super().__init__(file, params)

	def Randomize(self):
		pass