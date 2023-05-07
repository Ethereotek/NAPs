# NAPs - Named Operators & Parameters for TouchDesigner

## Introduction

NAPs provides similar functionality as TD's built in `Global OP Shortcuts` for any family of operators as well as for parameters. You simply create a short alias for the operator/parameter, then you can access it from anywhere in your network via `op.NAPs.Ops("your_op_name")` or `op.NAPs.Pars("your_par_name")`. The "named" operator/parameter terminology is inspired by Q-Sys Named Components and Named Controls which allow users to access those elements externally, and, in fact, using NAPs allows users an easy way to expose operators and parameters to remote applications.

## Using NAPs
### **Adding Operators**
Navigate to `NAPs/Build/NamedElements.tox` and drag and drop the tox into your network; it's ready to use. There are two ways to add operators:   
1. Make the NAPs Component viewer active, then drag and drop your operator into the panel. You will be prompted to give your operator a name. Operator names can only contain letters, numbers and underscores, and cannot start with a number; they must also be unique. A popup will inform you if these criteria are not met.
2. Using the `NameOperator()` method:   

		op.NAPs.NameOperator(op("path/to/operator"), "my_operator")
	
	Your name will be validated against the same criteria as drag and drop.   

### **Accessing Operators**
You will be able to access your operator and interact with it the same way you would using TD's built in `op()` call, except NAPs uses `Ops()`:   

	op.NAPs.Ops("my_constant").par.value0
	op.NAPs.Ops("my_constant").bypass = True

	const = op.NAPs.Ops("my_constant")
	const[0]
	const["chan1"]

	# or consider a table
	table = op.NAPs.Ops("my_table")
	table[0,0]
	table.appendRow([0,1,2])

It's important to note that if you move the operator to a different part of the network, you will have to re-add it to the NAPs module. If an operator is deleted from the network, NAPs will not sense this. However, you can use the `Purge` parameter to clear all deleted operators. 

### **Deleting and Renaming Operators**
You can delete operators from NAPs using the `delete` button in the interface, or with an API call:   

	op.NAPs.DeleteNamedOperator("my_constant")

You can also rename an operator from the interface by double clicking on its name or using an API call:   
	
	op.NAPs.RenameOperator("my_name", "MyNewName")

### **Adding Parameters**
Adding parameters is almost identical to adding operators, except that the Python call would be `NameParameter()`. ParGroups, however, must be drag-dropped.

### **Accessing Parameters**
The method for accessing parameters is similar to operators, but is unique in its behavior. There is admittedly some weirdness here in order to make ParGroups play nice, and to actually extend the functional interaction with both td.ParGroup's and td.Par's by wrapping them in a `Pars` object. 

For parameters: 

	rad_x = op.NAPs.Pars("rad_x")
		# print the value of `radx`
	print(rax_x.val) 

		# updating the value
	rad_x.val = 1.3

Note, however, that you are *not* interacting with an td.Par object. To access a parameter's `expr` attribute, for example, you must explicitly call via the `parameter` attribute, e.g.: 

	rad_x.parameter.expr
	rad_x.parameter.label 

When working with the td.ParGroup object, you can access all its children parameters by their typical names using squar-bracket notation. For example, if you were to add the `radius` group: 

	radius = op.NAPs.Pars("radius")
	radx = radius["radx"]
	rady = radius["rady"]
	radz = radius["radz"]

		# updating the value is a little smoother here
	
	radius["radx"] = 1.0 	# perfectly legal

Note that the square-bracket does return the `td.Par` object.

You're also able to update all the children at once through the `.vals` attribute: 

	radius = op.NAPs.Pars("radius")
	radius.vals = [0.1, 0.5, 0.5]

### **Parameters**

#### - **Initialize Page**


`Init Named Operators` -> clears the named_operators dictionary of `{name:operator}` pairs

`Init Named Parameters` -> clears the named_parameters dictionary of `{name:parameter}` pairs

The component's parameters are sparse. The two most important are `Purge`, as mentioned, and `Init Named Operators`, which will simply clear the entire dictionary of `{name:operator}` pairs.

All names are also added to a drop-down menu called in the `Operator` parameter. The `Path` parameter will reflect the full path to your selected operator. This is one easy way to get the path to your named operator, if so desired.

Note, however, that NAPs stores the actual operator object, so anything you can do with the `op()` call, you should be able to do with the `OPS` call, including retrieving the full path.
