# me - this DAT
# 
# comp - the List Component that holds this panel
# row - the row number of the cell being updated
# col - the column number of the cell being updated
#
# attribs contains the following members:
#
# text                 str            cell contents
# help                 str            help text
#
# textColor            r g b a        font color
# textOffsetX          n              horizontal text offset
# textOffsetY          n              vertical text offset
# textJustify          m              m is one of:  JustifyType.TOPLEFT, JustifyType.TOPCENTER,
#                                                   JustifyType.TOPRIGHT, JustifyType.CENTERLEFT,
#                                                   JustifyType.CENTER, JustifyType.CENTERRIGHT,
#                                                   JustifyType.BOTTOMLEFT, JustifyType.BOTTOMCENTER,
#                                                   JustifyType.BOTTOMRIGHT
#
# bgColor              r g b a        background color
#
# leftBorderInColor    r g b a         inside left border color
# rightBorderInColor   r g b a         inside right border color
# bottomBorderInColor  r g b a         inside bottom border color
# topBorderInColor     r g b a         inside top border color
#
# leftBorderOutColor   r g b a         outside left border color
# rightBorderOutColor  r g b a         outside right border color
# bottomBorderOutColor r g b a         outside bottom border color
# topBorderOutColor    r g b a         outside top border color
#
# colWidth             w              sets column width
# colStetch            True/False     sets column stretchiness (width is min width)
# rowHeight            h              sets row height
# rowStetch            True/False     sets row stretchiness (height is min height)
# rowIndent            w              offsets entire row by this amount
#
# editable             int            number of clicks to activate editing the cell.
# draggable            True/False     allows cell to be drag/dropped elsewhere
# fontBold             True/False     render font bolded
# fontItalic           True/False     render font italicized
# fontSizeX            float          font X size in pixels
# fontSizeY            float          font Y size in pixels, if not specified, uses X size
# sizeInPoints         True/False     If true specify font size in points, rather than pixels.
# wordWrap             True/False     word wrap
# top                  TOP            background TOP operator
#
# fontFace             str            font face, example 'Verdana'
# fontFile             str            font file, when specified on disk or embedded in VFS.
#                                     When fontFace and fontFile are both defined in the same attrib,
#                                     fontFile takes precedence
#
# select   true when the cell/row/col is currently being selected by the mouse
# rollover true when the mouse is currently over the cell/row/col
# radio    true when the cell/row/col was last selected
# focus    true when the cell/row/col is being edited
#
#

# called when Reset parameter is pulsed, or on load
turqBlue = [0, 0.92578, 0.92578, 1]
hotPink = [0.90234, 0.08203, 0.90234, 1]
coal = [0.11718, 0.11718, 0.11718, 1]
lightCoal = [0.15625, 0.17578, 0.17578, 1]
lightCoalRollover = [0.25625, 0.27578, 0.27578, 1]
darkCoal = [0.07812, 0.09765, 0.09765, 1]
dullWhite = [0.95703, 0.95703, 0.95703, 1]

rw_color = darkCoal
ro_color = [0.8, 0.2, 0.8, 1]

named_parameters = op("named_parameters_out")
named_ops_dict = op.NAPs.storage["named_parameters"]

columnHeaders = ["NAME", "OWNER", "RO","DELETE"]
columnWidths = [200, 270, 30, 100]

def onInitCell(comp, row, col, attribs):

	if row > 0:
		attribs.text = named_parameters[row, col]
		if col == 2:
			par_name = named_parameters[row, 0].val
			ro_state = op.NAPs.Pars(par_name).ro_ANY

			if ro_state == True:
				attribs.bgColor = ro_color
			else:
				attribs.bgColor = rw_color
		if col == 3:
			attribs.text = "delete"
	elif row == 0:
		attribs.text = columnHeaders[col]
		# sizing

	attribs.colWidth = columnWidths[col]
	# attribs.colStretch = True
		# text styling
	attribs.textColor = dullWhite
	# attribs.textOffsetX = 5
		# styling

	attribs.leftBorderOutColor = lightCoal
	attribs.rightBorderOutColor = darkCoal
	attribs.bottomBorderOutColor = lightCoal
	attribs.topBorderOutColor = darkCoal

	attribs.leftBorderInColor = darkCoal
	attribs.rightBorderInColor = lightCoal
	attribs.bottomBorderInColor = darkCoal
	attribs.topBorderInColor = lightCoal

	if row > 0 and col == 0:
		attribs.editable = 2

def onInitRow(comp, row, attribs):
	if row == 0:
		attribs.bgColor = lightCoal
	else:
		attribs.bgColor = darkCoal

			
def onInitCol(comp, col, attribs):
	stretch = [1, 1, 1]
def onInitTable(comp, attribs):
	return

# called during specific events
#
# coords - a named tuple containing the following members:
#   x
#   y
#   u
#   v

def onRollover(comp, row, col, coords, prevRow, prevCol, prevCoords):
	pass
	# if row != prevRow and row > 0:
	# 	rowAttribs = comp.rowAttribs[row]
	# 	comp.rowAttribs[row].bgColor = lightCoalRollover

	# if row != prevRow and prevRow > 0:
	# 	if row:
	# 		try:
	# 			comp.rowAttribs[prevRow].bgColor = darkCoal
	# 		except AttributeError:
	# 			print("python's being dumb")

def onSelect(comp, startRow, startCol, startCoords, endRow, endCol, endCoords, start, end):
	# if startCol == endCol:
	# 	if startCol == 2:
	# prevColor = eval(comp.cellAttribs[startRow, startCol].bgColor)
	# print(prevColor)
	btn_delete = False
	btn_ro = False
	if start:
		if startRow == endRow and startCol == endCol:
			par_name = named_parameters[startRow, 0].val
			if startCol == 3:
				btn_delete = True
				# prevColor = comp.cellAttribs[startRow, startCol].bgColor
				comp.cellAttribs[startRow, startCol].bgColor = [0.8, 0.2, 0.2, 1]
				# par_name = named_parameters[startRow, 0].val
				op.NAPs.DeleteNamedParameter(par_name)
			
			if startCol == 2:
				btn_ro = True
				# rw_color = darkCoal
				# ro_color = [0.8, 0.2, 0.8, 1]

				ro_state = op.NAPs.Pars(par_name).ro_ANY
				# print(ro_state)
				if ro_state == True:
					op.NAPs.Pars(par_name).ro_ANY = False
					comp.cellAttribs[startRow, startCol].bgColor = rw_color
				elif ro_state == False:
					op.NAPs.Pars(par_name).ro_ANY = True
					comp.cellAttribs[startRow, startCol].bgColor = ro_color

	
	if end:
		if btn_ro:
			return
		elif btn_delete:
			try:
				comp.cellAttribs[startRow, startCol].bgColor = darkCoal
			except AttributeError:
				pass

def onRadio(comp, row, col, prevRow, prevCol):
	return

def onFocus(comp, row, col, prevRow, prevCol):
	return

def onEdit(comp, row, col, val):
	
	current_name = named_parameters[row, col].val
	op.NAPs.RenameParameter(current_name, val)
