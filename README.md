# NAPs - Named Operators & Parameters for TouchDesigner

## Introduction

NAPs provides similar functionality as TD's built in `Global OP Shortcuts` for any family of operators as well as for parameters. You simply create a short alias for the operator/parameter, then you can access it from anywhere in your network via `op.NAPs.OPS("your_op_name")` or `op.NAPs.PARS("your_par_name")`. The "named" operator/parameter terminology is inspired by Q-Sys Named Components and Named Controls which allow users to access those elements externally, and, in fact, using NAPs allows users an easy way to expose operators and parameters to remote applications.

## Using NAPs
### **Adding Operators**
Navigate to `NAPs/Build/NamedElements.tox` and drag and drop the tox into your network; it's ready to use. There are two ways to add operators:   
1. Make the NAPs Component viewer active, then drag and drop your operator into the panel. You will be prompted to give your operator a name. Operator names can only contain letters, numbers and underscores, and cannot start with a number; they must also be unique. A popup will inform you if these criteria are not met.
2. Using the `NameOperator()` method:   

		op.NAPs.NameOperator(op("path/to/example/constant"), "my_constant")
	
	Your name will be validated against the same criteria as drag and drop.   

### **Accessing Operators***
You will be able to access your operator and interact with it the same way you would using TD's built in `op()` call, except NAPs uses `OPS()`:   

	op.NAPs.OPS("my_constant").par.value0
	op.NAPs.OPS("my_constant").bypass = True

	const = op.NAPs.OPS("my_constant")
	const[0]
	const["chan1"]

	# or consider a table
	table = op.NAPs.OPS("my_table")
	table[0,0]
	table.appendRow([0,1,2])

It's important to note that if you move the operator to a different part of the network, you will have to readd it to the NAPs module. If an operator is deleted from the network, NAPs will not sense this. However, you can use the `Purge` parameter to clear all deleted operators. 

### **Deleting and Renaming Operators**
You can delete operators from NAPs using the `delete` button in the interface, or with an API call:   

	op.NAPs.DeleteNamedOperator("my_constant")

You can also rename an operator from the interface by double clicking on its name or using an API call:   
	
	op.NAPs.RenameOperator("my_table", "MyTable")

### **Adding Parameters**
Add parameters is almost identical adding operators, except that the Python call would be `NameParameter()`. ParGroups, however, must be drag-dropped.

### **Accessing Parameters**
The method for accessing parameters is similar to operators, but is unique in its behavior. There is admittedly some weirdness here in order to make ParGroups play nice, and to actually extend the functional interaction with ParGroups by wrapping them in a `PAR` object. 

For parameters: 

	rad_x = op.NAPs.PARS("rad_x")
		# print the value of `radx`
	print(rax_x) 

		# updating the value
	rad_x.val = 1.3

Note, however, that you cannot assign a value without accessing the `.val` attribute first. This is because the parameter is accessed through a function call. 

		# incorrect:
	op.NAPs.PARS("rad_x") = 0.5

		# correct:
	op.NAPs.PARS("rad_x").val = 0.5

When working with the td.ParGroup object, you can access all its children parameteres by their typical names. For example, if you were to add the `radius` group: 

	radius = op.NAPs.PARS("radius")
	radx = radius.radx
	rady = radius.rady
	radz = radius.radz

		# updating value is a little smooter here
	
	radius.radx = 1.0 	# perfectly legal

You're also able to update all the children at once through the `.vals` attribute: 

	radius = op.NAPs.PARS("radius")
	radius.vals = [0.1, 0.5, 0.5]

### **Parameters**

#### - **Initialize Page**


`Init Named Operators` -> clears the named_operators dictionary of `{name:operator}` pairs

`Init Named Parameters` -> clears the named_parameters dictionary of `{name:parameter}` pairs

The component's parameters are sparse. The two most important are `Purge`, as mentioned, and `Init Named Operators`, which will simply clear the entire dictionary of `{name:operator}` pairs.

All names are also added to a drop-down menu called in the `Operator` parameter. The `Path` parameter will reflect the full path to your selected operator. This is one easy way to get the path to your named operator, if so desired.

Note, however, that NAPs stores the actual operator object, so anything you can do with the `op()` call, you should be able to do with the `OPS` call, including retrieving the full path.