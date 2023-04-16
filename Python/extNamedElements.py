import json
import re
import inspect
# import copy

class Pars:
	'''
		This wrapper is a wild ride

		The purpose of this is to make it easy to work with both td.Par and td.ParGroup objects
		from a single interface. This Par object is what is stored as the value in the named_parameters dictionary.

		The reason both are wrapped is really just because it's easier to wrap anything Par-like

		When the Par object is retrieved, it is called (see def Pars() below), it calls the __call__ method
		If it wraps a single td.Par object, it simple returns that object,
		and users can interact with it generally how they would a normal parameter
		EXCEPT that to assign a value, they must explicitly call the .val attribute (this it is retrieved through a function call)

		If it wraps a td.ParGroup object, then Par returns its self. Unlike regular ParGroup objects, the user can access attributes
		So, for a radius parameter, users can call Par.radx, Par.rady, etc. 
		They can also assign the way they normally would, e.g. Par.radx = 1.0

		Users can also assign multiple values at once through the .vals attribute, e.g. Par.vals = [1.1, 2.4, 1.1]
	'''
	def __init__(self, name, parameter):

		self.name = name
		self.parameter = parameter
		self.children = {}
		if isinstance(self.parameter, ParGroup):
			# print(parameter.val)

			self._vals = []

			for i in range(len(self.parameter.val)):
				p_name = self.parameter[i].name
				p_val = self.parameter[i].val
				setattr(self, p_name, self.parameter[i] )

				self.children.update({self.parameter[i].name:self.parameter[i]})
				self._vals.append(self.parameter[i])


				# setattr(self, p_name, self.parameter[i])
				# setattr(self, p_name, property(self._get_par_val(p_name), self._set_par_val(p_name, p_val)))
	def __setattr__(self, name, value):
		if inspect.stack()[1].function == '__init__':
			super.__setattr__(self, name, value)
		else:
			if name in self.children.keys():
				self.children[name].val = value
		
	def _set_par_val(self, par_name, par_val):
		self.children[par_name] = par_val
	
	def _get_par_val(self, par_name):
		return self.children[par_name]
	
	def __call__(self):

		if isinstance(self.parameter, Par):
			return self.parameter
		else:
			return self

	def __getitem__(self, _name):
		return self.children[_name]

	@property
	def vals(self):
		print("vals")
		self._values = self._vals
		return self._values
	
	@vals.setter
	def set_vals(self, value):
		print("setting value")
		if not isinstance(value, list):
			print("not")
			raise ValueError("Input value must be a list")
		
		if len(value) != len(self._vals):
			raise ValueError("Input list length is bad")
		
		for val, par in zip(value, self._vals):
			print(par)
			print(type(par))
			par.val = val
	
	# @vals.getterY
	# def vals(self):
	# 	print("getting vals")
	# 	return [i.val for i in self._vals]

	@property
	def valid(self):
		return self._valid

	@valid.getter
	def valid(self):
		return self.parameter.valid


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
	@property
	def Test(self):
		print("HELLO TEST")
	
	@Test.setter
	def Test(self, value):
		print("HELLO {}".format(value))
	# def __getattr__(self,_attrib):
	# 	pass
		# Ops and Par allow the user to get the path to the operator by calling its name
	def Ops(self, op_name):
			# called to access an operator object via op.NAPs.Ops(op_name).<attribute> | <method>
		try:
			return self.named_operators[op_name]
		except:
			return None
		
	def Pars(self, par_name):
		try:
			return self.named_parameters[par_name]()#self.named_parameters[par_name]
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
	
	def validateParameterAddition(self):
		if self.name in self.named_parameters:
			message = f'The name `{self.name}` already exists.'
			ui.messageBox("ERROR: Duplicate Par Names", message, buttons=["OK"])
			return False
		
		if re.match(self.validName, self.name):
			return True
		else:
			message = "Par names can only contain letters, numberes and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid Par Name", message, buttons=["OK"])
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
		
		self.namedOperatorsDAT.replaceRow(op_curr_name, self.name, entireRow=False)
		operator = self.named_operators.pop(op_curr_name)
		self.named_operators[self.name] = operator

	def NameParameter(self, parameter, name):
		self.parameter = parameter
		self.name = name

		valid = self.validateParameterAddition()

		if valid:
				# add to dict and update table for user viewability AND to populate menu
			self.named_parameters.update({name:parameter})
			self.namedParametersDAT.appendRow([name, parameter.owner])
			return 1
		
		else:
			return -1

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
		
		valid = self.validateParameterAddition()

		if not valid:
			return -1
		
		
		# first add the par group
		# should add the owner object to dictionary, and owner path to DAT

		newPAR = Pars(self.name, self.parameter)

		self.named_parameters.update({self.name:newPAR})
		self.namedParametersDAT.appendRow([self.name, self.parameter.owner])
		'''
		self.named_parameters.update({self.name:self.parameter})
		self.namedParametersDAT.appendRow([self.name, self.parameter.owner])
		'''

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
	def RenameParameter(self, par_curr_name, par_new_name):
		# get the parameter object from dictionary

		self.name = par_new_name
		valid = self.validateOperatorAddition()

		if not valid:
			return
		
		self.namedParametersDAT.replaceRow(par_curr_name, self.name, entireRow=False)
		parameter = self.named_parameters.pop(par_curr_name)
		self.named_parameters[self.name] = parameter

	def DeleteNamedParameter(self, par_name):
			# IF name exists, remove from dict, remove from table DAT
		if par_name in self.named_parameters:
			self.named_parameters.pop(par_name)
			self.namedParametersDAT.deleteRow(par_name)
			return 0
		else:
			return -1
