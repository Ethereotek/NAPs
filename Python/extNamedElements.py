import json
import re
# import copy

class PAR:

	def __init__(self, name, parameter):
		self.name = name
		self.parameter = parameter
		self.children = {}
		if isinstance(self.parameter, ParGroup):
			# print(parameter.val)

			self._group = []
			for i in range(len(self.parameter.val)):
				self.children.update({self.parameter[i].name:self.parameter[i]})
				self._group.append(self.parameter[i])

		
	def __call__(self):
		return self.parameter


	# def __getattr__(self, _name):
	# 	print(_name)
	# 	return self.children[_name]
	def __getitem__(self, _name):
		return self.children[_name]

	@property
	def group(self):
		return self._group
	
	@group.setter
	def group(self, value):
		if not isinstance(value, list):
			return Exception
		
		if len(value) != len(self._group):
			return Exception
		
		for val, par in zip(value, self._group):
			par.val = val

# class Test:
# 	def __init__(self, name, parameter):
# 		self.name = name
# 		self.parameter = parameter
# 		self.children = {}

# 		if isinstance(self.parameter, ParGroup):
# 			self._group = []
# 			for i in range(len(self.parameter.val)):
# 				self.children.update({self.parameter[i].name:self.parameter[i]})
# 				self._group.append(self.parameter[i])
# 	def __call__(self):
# 		return self.parameter
	
# 	def __getitem__(self, _name):
# 		return self.children
# 	@property
# 	def group(self):
# 		return self._group
	
# 	@group.setter
# 	def group(self, value):
# 		if not isinstance(value, list):
# 			return Exception
		
# 		if len(value) != len(self._group):
# 			return Exception
		
# 		for val, par in zip(value, self._group):
# 			par.val = val
	

class NamedElements:
    
	def __init__(self, owner):
		# print("init NamedElements extension")

		self.owner = owner
		self.parent_storage = op.NAPs.storage

			# if named_ops/pars storage dicts don't exist,
			# the extension will create them
		try:
			self.named_operators = op.NAPs.storage["named_operators"]
		except KeyError:
			op.NAPs.storage.update({"named_operators":{}})
			self.named_operators = op.NAPs.storage["named_operators"]
		
		try:
			self.named_parameters = op.NAPs.storage["named_parameters"]
		except KeyError:
			op.NAPs.storage.update({"named_parameters":{}})
			self.named_parameters = op.NAPs.storage["named_parameters"]

			##
		self.validName = r'^[A-z][A-z_0-9]*$'	# regex for testing op/par name validity
		self.namedOperatorsDAT = op("named_operators")
		self.namedParametersDAT = op("named_parameters")
	

		# OPS and PAR allow the user to get the path to the operator by calling its name
	def OPS(self, op_name):
			# called to access an operator object via op.NAPs.OPS(op_name).<attribute> | <method>
		try:
			return self.named_operators[op_name]
		except:
			return None
		
	def PARS(self, par_name):
		try:
			return self.named_parameters[par_name]#self.named_parameters[par_name]
		except:
			return None

		# clear the op/par dicts and associated tables
	def InitNamedOperatorsDict(self):
		op.NAPs.storage["named_operators"].clear()
		self.namedOperatorsDAT.clear()
	
	def InitNamedParametersDict(self):
		op.NAPs.storage["named_parameters"].clear()
		self.namedParametersDAT.clear()
	
	def validateOperatorAddition(self):

		if self.name in self.named_operators:
			message = f'The name `{self.name}` already exists.'
			ui.messageBox("ERROR: Duplicate OP Names", message, buttons=["OK"])
			return False

			# check if name is valid pattern
		if re.match(self.validName, self.name):
			return True
		else:
				# inform user via a popup message box
			message = "OP names can only contain letters, numbers and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid Operator Name",message, buttons=["OK"])
			return False
	
	def validParameterAddition(self):
		if self.name in self.named_parameters:
			message = f'The name `{self.name}` already exists.'
			ui.messageBox("ERROR: Duplicate PAR Names", message, buttons=["OK"])
			return False
		
		if re.match(self.validName, self.name):
			return True
		else:
			message = "PAR names can only contain letters, numberes and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid PAR Name", message, buttons=["OK"])
			return False

	def NameOperator(self, operator, name):
		self.operator = operator
		self.name = name

		valid = self.validateOperatorAddition()

		if valid:
				# add to dict and update table for user viewability AND to populate menu
			self.named_operators.update({name:operator})
			self.namedOperatorsDAT.appendRow([name, operator.path])
			return 1
		
		else:
			return -1

	def addOperatorFromPopup(self, args):
			# args is passed in from the popDialog function

			# operator is reference to operator object

		self.operator = args["details"]["operator"]
		self.name = args["enteredText"]
		button = args["button"]

		if button != "OK":
			print("Goodbye")
			return -1
		
			# it's possible to call self.NameOperator here instead
			# and pass the return up the stack, for now this is easier to understand
		valid = self.validateOperatorAddition()

		if valid:
			self.named_operators.update({self.name:self.operator})
			self.namedOperatorsDAT.appendRow([self.name, self.operator.path])
			return 1
		else:
			return -1

	def DeleteNamedOperator(self, op_name):
			# IF name exists, remove from dict, remove from table DAT
		if op_name in self.named_operators:
			self.named_operators.pop(op_name)
			self.namedOperatorsDAT.deleteRow(op_name)
			return 0
		else:
			return -1

	def RenameOperator(self, op_curr_name, op_new_name):
		# get the operator object from dictionary
		# `args` is a dictionary normally passed from the PopDialog to AddNamedOperator
		# this is needed just to make it all work with the PopDialog
		# This will likely be replaced with a better function that 
		# handles all the logic itself instead of calling Add/Delete functions
		# operator = self.named_operators[op_curr_name]
		self.name = op_new_name
		valid = self.validateOperatorAddition()

		if not valid:
			return
		
		self.namedOperatorsDAT.replaceRow(op_curr_name, [self.name], entireRow=False)
		operator = self.named_operators.pop(op_curr_name)
		self.named_operators[self.name] = operator
		# args = {
		# 	"details":{
		# 		"operator":operator
		# 	},
		# 	"enteredText":op_new_name,
		# 	"button":"OK"
		# }

		# self.AddNamedOperator(args)

		# self.DeleteNamedOperator(op_curr_name)

	def AddNamedParameter(self, args):
		parameter = args["details"]["parameter"]
		name = args["enteredText"]

		if name in self.named_parameters:
			message = f'The name `{name}` already exists.'
			ui.messageBox("ERROR: Duplicate Par Names", message, buttons=["OK"])
			return -1

		if re.match(self.validName, name):
			self.named_parameters.update({name:parameter})
			self.namedParametersDAT.appendRow([name, ""])
			return 0
		else:
			message = "Par names can only contain letters, numbers and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid Parameter Name",message, buttons=["OK"])
			return -1

	
	# def parseParGroup(self):
	def addParameterFromPopup(self, args):
		self.parameter = args["details"]["parameter"]
		self.name = args["enteredText"]
		button = args["button"]

		if button != "OK":
			return -1
		
		valid = self.validParameterAddition()

		if not valid:
			return -1
		
		
		# first add the par group
		# should add the owner object to dictionary, and owner path to DAT

		newPAR = PAR(self.name, self.parameter)
		print(self.parameter.owner)
		self.named_parameters.update({self.name:newPAR})
		self.namedParametersDAT.appendRow([self.name, self.parameter.owner])



		# then add each par in the group
		'''
		if isinstance(self.parameter, ParGroup):
			# print(parameter.val)
			for i in range(len(self.parameter.val)):
				param = self.parameter[i]
				name = copy.copy(self.name)
				name += ("_" + param.name)
				self.named_parameters.update({name:newPAR})
				print(self.named_parameters[name])
				self.namedParametersDAT.appendRow([name, self.parameter.owner])
			print("pargroup")
		'''
		# if valid:
		# 	self.named_parameters.update({name:self.parameter})
		# 	self.namedParametersDAT.appendRow([name])
		# 	return 1
		# else:
		# 	return -1

