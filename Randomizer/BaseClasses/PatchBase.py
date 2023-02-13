from BaseClasses.BaseTargetOp import BaseTargetOp


class PatchBase(BaseTargetOp):
	def __init__(self, file, params):
		super().__init__(file, params)

	def Patch(self):
		pass
