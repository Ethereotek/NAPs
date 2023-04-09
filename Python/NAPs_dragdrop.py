# callbacks for when associated Panel is being dropped on

import re
import inspect

named_operators = op("NAPs/named_operators")	# table to add alias/op to

validName = r'^[A-z_][A-z_0-9]*$' # pattern to validate alias string

# def popDialogCallback(args):
# 	name = args["enteredText"]
# 	storage = args["details"][0]
# 	operator = args["details"][1]

# 	# validate callback
# 	if re.match(validName, name):
# 		storage.update({name:operator})
# 		named_operators.appendRow([name, ""])
# 		return 0
# 	else:
# 		message = "OP names can only contain letters, numbers and underscores, and cannot start with a number.\nPlease enter a different name."
# 		ui.messageBox("ERROR: Invalid Shortcut",message, buttons=["OK"])
# 		return -1

# namedOpCallback = op.NAPs.AddNamedOperator
namedOpCallback = op.NAPs.ext.NamedElements.addOperatorFromPopup
namedParCallback = op.NAPs.AddNamedParameter


def onHoverStartGetAccept(comp, info):
	"""
	Called when comp needs to know if dragItems are acceptable as a drop.

	Args:
		comp: the panel component being hovered over
		info: A dictionary containing all info about hover, including:
			dragItems: a list of objects being dragged over comp
			callbackPanel: the panel Component pointing to this callback DAT

	Returns:
		True if comp can receive dragItems
	"""
	#debug('\nonHoverStartGetAccept comp:', comp.path, '- info:\n', info)
	return True # accept what is being dragged

def onHoverEnd(comp, info):
	"""
	Called when dragItems leave comp's hover area.

	Args:
		comp: the panel component being hovered over
		info: A dictionary containing all info about hover, including:
			dragItems: a list of objects being dragged over comp
			callbackPanel: the panel Component pointing to this callback DAT
	"""
	#debug('\nonHoverEnd comp:', comp.path, '- info:\n', info)

def onDropGetResults(comp, info):
	
	dragItem = info["dragItems"][0]
	# print(isinstance(dragItem, OP))
	dragItem_mro = inspect.getmro(dragItem.__class__)
	if OP in dragItem_mro:
		# print("op in mro")
		operator = dragItem
		op.TDResources.PopDialog.OpenDefault(
			title="Add named operator",
			text="Name: ",
			details = {"operator":operator},
			textEntry=True,
			buttons=["OK", "Cancel"],
			enterButton=1,
			escButton=2,
			callback=namedOpCallback
		)
		# print("called add")
	elif Par in dragItem_mro:
		param = dragItem
		op.TDResources.PopDialog.OpenDefault(
			title="Add named parameter",
			text = "Name: ",
			details = {"parameter":param},
			textEntry = True,
			buttons = ["OK", "Cancel"],
			callback = namedParCallback
		)
		# print(param)
		# print("par in mro")
	
	elif ParGroup in dragItem_mro:
		print("pargroup in mro")
	else:
		print(False)

		# get the operator object from drag items
		# open a dialog box and prompt user to enter alias
		# pass operator object and parent storage to callback
	#operator = info["dragItems"][0]


	# op.TDResources.PopDialog.OpenDefault(
	# 	title="Add named operator",
	# 	text="Name: ",
	# 	details = [comp.storage["named_operators"], operator],
	# 	textEntry=True,
	# 	buttons=["OK", "Cancel"],
	# 	callback=popDialogCallback
	# )

	"""
	Called when comp receives a drop of dragItems. This will only be called if
	onHoverStartGetAccept has returned True for these dragItems.

	Args:
		comp: the panel component being dropped on
		info: A dictionary containing all info about drop, including:
			dragItems: a list of objects being dropped on comp
			callbackPanel: the panel Component pointing to this callback DAT

	Returns:
		A dictionary of results with descriptive keys. Some possibilities:
			'droppedOn': the object receiving the drop
			'createdOPs': list of created ops in order of drag items
			'dropChoice': drop menu choice selected
			'modified': object modified by drop
	"""
	# debug('\nonDropGetResults comp:', comp.path, '- info:\n', info)
	return

# callbacks for when associated Panel is being dragged

def onDragStartGetItems(comp, info):
	"""
	Called when information about dragged items is required.

	Args:
		comp: the panel clicked on to start drag
		info: A dictionary containing all info about drag
			callbackPanel: the panel Component pointing to this callback DAT

	Returns:
		A list of dragItems: [object1, object2, ...]
	"""
	dragItems = [comp] # drag the comp itself
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	return dragItems

def onDragEnd(comp, info):
	"""
	Called when a drag action ends.

	Args:
		comp: the panel clicked on to start drag
		info: A dictionary containing all info about drag, including:
			accepted: True if the drag was accepted, False if not
			dropResults: a dict of drop results. This is the return value of 
				onDropGetResults
			dragItems: the original dragItems for the drag
			callbackPanel: the panel Component pointing to this callback DAT
	"""
	#debug('\nonDragEnd comp:', comp.path, '- info:\n', info)
	
