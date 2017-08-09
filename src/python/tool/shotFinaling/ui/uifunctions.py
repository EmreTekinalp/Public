from PySide import QtGui


class UIFunctions():
    """Class for getting information out of the ui, that Qt doesn't provide out
    of the box.
    """
    def __init__(self):
        pass

    def get_row_column(self, widget):
        """Returns the row and column of the given widget."""
        return_row = None
        return_column = None
        table = self.get_object_table(widget)
        rows = table.rowCount()
        columns = table.columnCount()
        for row in range(rows):
            for column in range(columns):
                cellwidget = table.cellWidget(row, column)
                if cellwidget is widget:
                    return_row = row
                    return_column = column
                    break
                elif type(cellwidget) == QtGui.QWidget:
                    for i in range(cellwidget.layout().count()):
                        innerwidget = cellwidget.layout().itemAt(i).widget()
                        if widget is innerwidget:
                            return_row = row
                            return_column = column
                            break
                    # end for i in range(cellwidget.layout().count())
                else:
                    if widget is table.cellWidget(row, column):
                        return_row = row
                        return_column = column
                        break
            # end for column in range(columns)
        # end for row in range(rows)
        return return_row, return_column
    # end def get_row_column()

    def get_object_table(self, widget):
        """Returns the object table, the given widget resides in."""
        found = False
        while not found:
            widget = widget.parent()
            if type(widget) == QtGui.QTableWidget:
                found = True
        return widget
    # end def get_object_table()

    def get_object_tab(self, widget):
        """Returns the tab, the given widget resides in."""
        tab = widget
        found = False
        while not found:
            tab = tab.parent()
            if type(tab) == QtGui.QTabWidget:
                found = True
        tab_label = tab.tabText(tab.currentIndex())
        return (tab, tab_label)
    # end def get_object_tab()

    def get_character_tab(self, widget):
        """Retrieves the character tab, the given widget resides in."""
        obj_tab = self.get_object_tab(widget)[0]
        tab = obj_tab.parent().parent()
        tab_label = tab.tabText(tab.currentIndex())
        return (tab, tab_label)
    # end def get_character_tab()
# end class UIFunctions()
