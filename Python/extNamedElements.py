import json
import re

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
		
	def PAR(self, par_name):
		pass

		# clear the op/par dicts and associated tables
	def InitNamedOperatorsDict(self):
		op.NAPs.storage["named_operators"].clear()
		self.namedOperatorsDAT.clear()
	
	def InitNamedParametersDict(self):
		op.NAPs.storage["named_parameters"].clear()
		self.namedParametersDAT.clear()
	
	def AddNamedOperator(self, args):
			# args is passed in from the popDialog function

			# operator is reference to operator object

		operator = args["details"]["operator"]
		name = args["enteredText"]
		button = args["button"]

			# if the name is empty, or button pressed was not "OK", return function
		if not name:
			print("empty name")
			return -1
		
		if button != "OK":
			print("Goodbye")
			return -1
		
			# otherwise:
			# check if name already exists
		if name in self.named_operators:
			message = f'The name `{name}` already exists.'
			ui.messageBox("ERROR: Duplicate OP Names", message, buttons=["OK"])
			return -1

			# check if name is valid pattern
		if re.match(self.validName, name):

				# add to dict and update table for user viewability AND to populate menu
			self.named_operators.update({name:operator})
			self.namedOperatorsDAT.appendRow([name, operator.path])
			return 0
		else:
				# inform user via a popup message box
			message = "OP names can only contain letters, numbers and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid Operator Name",message, buttons=["OK"])
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
		operator = self.named_operators[op_curr_name]
		args = {
			"details":{
				"operator":operator
			},
			"enteredText":op_new_name,
			"button":"OK"
		}

		self.AddNamedOperator(args)
		self.DeleteNamedOperator(op_curr_name)

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

		
