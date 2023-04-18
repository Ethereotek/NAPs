import json
import re
import inspect
# import copy


class Pars:
	'''

	'''
	def __init__(self, name: str, parameter):

		self.name = name
		self.parameter = parameter
		self.children = {}			# if td.ParGroup, the individual td.Par's
		# self._val

			# mode-specific read-only states
			# if ro_EXPORT == True, parameter is read-only when par mode is set to Expression
		self.ro_EXPORT = False
		self.ro_EXPRESSION = False
		self.ro_BIND = False
		self.ro_CONSTANT = False
		self._ro_ANY = False

		if isinstance(self.parameter, ParGroup): 
			# This handles accessing child Par objects and their values
			self._vals = []

			for i in range(len(self.parameter.val)):
				self.children.update({self.parameter[i].name:self.parameter[i]})
				self._vals.append(self.parameter[i])
	
		# using square brackets to get/set td.Par members
	def __getitem__(self, _name: str):
			# returns the td.Par object
		if not _name in self.children.keys():
			raise AttributeError(f'{_name} is not a Named Parameter')
			
		return self.children[_name]

	def __setitem__(self, _name: str, _value):

		if not _name in self.children.keys():
			raise AttributeError(f'{_name} is not a Named Parameter')
		
			# check if read-only
		parmode = self.children[_name].mode.name
		readonly = getattr(self, 'ro_' + parmode)

		if readonly or self._ro_ANY:
			raise TypeError(f'{_name} is a read-only parameter')

		self.children[_name].val = _value
	
	def setSelectiveReadOnly(self, ro_modes: dict[str,bool]):
		# set multiple mode-based read-only attributes with a dict
		for key, val in ro_modes.items():
			if key == "any":
				self._ro_ANY = val
			else:
				ro_mode = 'ro_' + key.upper()
				setattr(self, ro_mode, val)

	@property
	def ro_ANY(self):
		return self._ro_ANY
	
	@ro_ANY.setter
	def ro_ANY(self, value: bool):
		if not type(value) == bool:
			raise TypeError('Read Only descriptions must be of type <bool>')
		self._ro_ANY = value

		op("named_pars_list").par.reset.pulse()

	@property
	def vals(self):
		return self._vals
	
	@vals.setter
	def vals(self, value: list):

		# if not isinstance(value, list):
		# 	raise ValueError("Input value must be a list.")
		
		if len(value) != len(self._vals):
			raise ValueError("Input list length is bad.")
		
		for par in self._vals:
			parmode = par.mode.name
			readonly = getattr(self, 'ro_' + parmode)
			if readonly:
				raise TypeError(f'At least one member of {self.name} is a read-only parameter.')
		
		if self._ro_ANY:
			raise TypeError(f'{self.name} is a read-only parameter')
		
		for val, par in zip(value, self._vals):
			par.val = val

	@property
	def val(self):
		return self.parameter.eval()
	
	@val.setter
	def val(self, value):
			# get mode of parameter
			# and get the corresponding ro_ attribute
		parmode = self.parameter.mode.name
		readonly = getattr(self, 'ro_' + parmode)

			# if the mode or any mode is readonly, raise exception
		if readonly or self._ro_ANY:
			raise TypeError(f'{self.name} is a read-only parameter')
		else:
			self.parameter.val = value

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

	def Ops(self, op_name):
			# called to access an operator object via op.NAPs.Ops(op_name).<attribute> | <method>
		try:
			return self.named_operators[op_name]
		except:
			return None
		
	def Pars(self, par_name):
		try:
			return self.named_parameters[par_name]
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

		ParsWrapper = Pars(self.name, self.parameter)
		ro_modes = {
				"any" : self.owner.par.Ropars.val,
				"expression" : self.owner.par.Roexpression.val,
				"export" : self.owner.par.Roexport.val
				}


		ParsWrapper.setSelectiveReadOnly(ro_modes)
		# if self.owner.par.Ropars:
		# 	ParsWrapper.ro_ANY = True

		self.named_parameters.update({self.name:ParsWrapper})
		self.namedParametersDAT.appendRow([self.name, self.parameter.owner])

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
