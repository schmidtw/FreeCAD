# SPDX-License-Identifier: LGPL-2.1-or-later
# /**************************************************************************
#                                                                           *
#    Copyright (c) 2025 Weston Schmidt <weston_schmidt@alumni.purdue.edu>   *
#                                                                           *
#    This file is part of FreeCAD.                                          *
#                                                                           *
#    FreeCAD is free software: you can redistribute it and/or modify it     *
#    under the terms of the GNU Lesser General Public License as            *
#    published by the Free Software Foundation, either version 2.1 of the   *
#    License, or (at your option) any later version.                        *
#                                                                           *
#    FreeCAD is distributed in the hope that it will be useful, but         *
#    WITHOUT ANY WARRANTY; without even the implied warranty of             *
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
#    Lesser General Public License for more details.                        *
#                                                                           *
#    You should have received a copy of the GNU Lesser General Public       *
#    License along with FreeCAD. If not, see                                *
#    <https://www.gnu.org/licenses/>.                                       *
#                                                                           *
# ***************************************************************************/

"""
Mock classes for FreeCAD GUI testing.

This module provides mock implementations of FreeCAD and Qt classes
to enable unit testing without requiring the full FreeCAD environment.
"""

import builtins
from unittest.mock import MagicMock, patch


class MockQIcon:
    """Mock QIcon class using MagicMock with spec."""
    
    def __init__(self, *args, **kwargs):
        self._mock = MagicMock()
        # Store the original arguments for potential use
        self._args = args
        self._kwargs = kwargs
    
    @staticmethod
    def fromTheme(theme_name, fallback=None):
        """Mock fromTheme method."""
        return MockQIcon()
    
    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockQTreeWidgetItem:
    """Mock QTreeWidgetItem class using MagicMock with spec."""

    def __init__(self, *args, **kwargs):
        self._mock = MagicMock()
        self.text_values = {}
        self.data_values = {}
        self._children = []

    def setText(self, column, text):
        """Mock setText method."""
        self.text_values[column] = text
        return self._mock.setText(column, text)

    def text(self, column):
        """Mock text method."""
        return self.text_values.get(column, "")

    def setData(self, column, role, data):
        """Mock setData method."""
        self.data_values[(column, role)] = data
        return self._mock.setData(column, role, data)

    def data(self, column, role):
        """Mock data method."""
        return self.data_values.get((column, role))

    def childCount(self):
        """Mock method for getting child count."""
        return len(self._children)

    def child(self, index):
        """Mock method for getting child by index."""
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def addChild(self, child):
        """Mock method for adding a child item."""
        self._children.append(child)
    
    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockSignal:
    """Mock Signal class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()



    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockCheckBox:
    """Mock CheckBox class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()
        self.checked = False
        self.stateChanged = MockSignal()

    def setChecked(self, checked):
        """Mock setChecked method."""
        self.checked = checked

    def isChecked(self):
        """Mock isChecked method."""
        return self.checked

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)

class MockButton:
    """Mock Button class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()
        self._clicked_signal = MockSignal()

    @property
    def clicked(self):
        """Mock clicked signal."""
        return self._clicked_signal

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockLineEdit:
    """Mock LineEdit class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()
        self.textChanged = MockSignal()
        self._text = ""

    def text(self):
        """Mock text method."""
        return self._text

    def setText(self, text):
        """Mock setText method."""
        self._text = text

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockHeader:
    """Mock Header class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()

    def hide(self):
        """Mock hide method."""
        pass

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockPartList:
    """Mock PartList class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()
        self.itemClicked = MockSignal()
        self.itemDoubleClicked = MockSignal()
        self._items = []

    def header(self):
        """Mock header method."""
        return MockHeader()

    def clear(self):
        """Mock clear method."""
        self._items = []

    def addTopLevelItem(self, item):
        """Mock addTopLevelItem method."""
        self._items.append(item)

    def expandAll(self):
        """Mock expandAll method."""
        pass

    def topLevelItemCount(self):
        """Mock topLevelItemCount method."""
        return len(self._items)

    def topLevelItem(self, index):
        """Mock topLevelItem method."""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def sizeHintForRow(self, row):
        """Mock sizeHintForRow method."""
        return 20

    def setMinimumHeight(self, height):
        """Mock setMinimumHeight method."""
        pass

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockForm:
    """Mock Form class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()
        self.partList = MockPartList()
        self.CheckBox_ShowOnlyParts = MockCheckBox()
        self.CheckBox_RigidSubAsm = MockCheckBox()
        self.openFileButton = MockButton()
        self.filterPartList = MockLineEdit()

    def installEventFilter(self, filter_obj):
        """Mock installEventFilter method."""
        pass

    def setWindowTitle(self, title):
        """Mock setWindowTitle method."""
        pass

    def show(self):
        """Mock show method."""
        pass

    def hide(self):
        """Mock hide method."""
        pass

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)


class MockPySideUic:
    """Mock PySideUic class using MagicMock."""

    def __init__(self):
        self._mock = MagicMock()

    @staticmethod
    def loadUi(ui_file):
        """Mock loadUi method."""
        return MockForm()

    def __getattr__(self, name):
        """Delegate all other attributes to the MagicMock."""
        return getattr(self._mock, name)

def MockGetDocument(doc_name):
    """Mock getDocument function using MagicMock."""
    mock_doc = MagicMock()
    mock_doc.Name = doc_name
    mock_doc.getObject = MagicMock(return_value=None)
    mock_doc.TreeRootObjects = []
    return mock_doc


def MockAddModule(module_name):
    """Mock addModule function using MagicMock."""
    pass


def MockDoCommandSkip(commands):
    """Mock doCommandSkip function using MagicMock."""
    pass


def SetupGuiMocks():
    """Set up all FreeCAD GUI mocks for testing using unittest.mock."""
    import sys
    from types import ModuleType
    import FreeCAD as App  # pylint: disable=import-error,import-outside-toplevel

    # Force GuiUp to be True so GUI-dependent code gets loaded
    App.GuiUp = True

    # Try to import FreeCADGui, create mock if it doesn't exist (CLI mode)
    try:
        import FreeCADGui as Gui  # pylint: disable=import-error,import-outside-toplevel
    except ImportError:
        # FreeCADGui doesn't exist (CLI mode), create a mock module
        Gui = ModuleType('FreeCADGui')
        sys.modules['FreeCADGui'] = Gui

    # Try to import PySide modules, create mocks if they don't exist
    try:
        from PySide import QtCore, QtGui, QtWidgets  # pylint: disable=import-error,import-outside-toplevel
    except ImportError:
        # PySide doesn't exist, create mock modules
        QtCore = ModuleType('PySide.QtCore')
        QtGui = ModuleType('PySide.QtGui')
        QtWidgets = ModuleType('PySide.QtWidgets')
        # Create PySide parent module if needed
        if 'PySide' not in sys.modules:
            PySide = ModuleType('PySide')
            PySide.QtCore = QtCore
            PySide.QtGui = QtGui
            PySide.QtWidgets = QtWidgets
            sys.modules['PySide'] = PySide
        sys.modules['PySide.QtCore'] = QtCore
        sys.modules['PySide.QtGui'] = QtGui
        sys.modules['PySide.QtWidgets'] = QtWidgets

    # Add QObject to QtCore for TaskAssemblyInsertLink inheritance
    if not hasattr(QtCore, 'QObject'):
        QtCore.QObject = type('QObject', (), {})

    # Replace QtGui classes directly (permanent replacement)
    QtGui.QIcon = MockQIcon
    QtGui.QTreeWidgetItem = MockQTreeWidgetItem

    # Mock the PySideUic if it doesn't exist
    if not hasattr(Gui, "PySideUic"):
        Gui.PySideUic = MockPySideUic()

    # Mock additional Gui methods that might be missing
    if not hasattr(Gui, "getDocument"):
        Gui.getDocument = MockGetDocument

    # Mock Selection module using MagicMock
    if not hasattr(Gui, "Selection"):
        mock_selection = MagicMock()
        mock_selection.clearSelection = MagicMock()
        mock_selection.addSelection = MagicMock()
        mock_selection.getSelection = MagicMock(return_value=[])
        Gui.Selection = mock_selection

    # Mock addModule method
    if not hasattr(Gui, "addModule"):
        Gui.addModule = MockAddModule

    # Mock doCommandSkip method
    if not hasattr(Gui, "doCommandSkip"):
        Gui.doCommandSkip = MockDoCommandSkip

    # Mock addCommand method (used to register FreeCAD commands)
    if not hasattr(Gui, "addCommand"):
        Gui.addCommand = MagicMock()

    # Mock Control.showDialog
    if not hasattr(Gui, "Control"):
        mock_control = MagicMock()
        mock_control.showDialog = MagicMock()
        Gui.Control = mock_control

    # Mock activeDocument
    if not hasattr(Gui, "activeDocument"):
        Gui.activeDocument = MagicMock()

    # Make QtCore, QtGui, QtWidgets and Gui available in the global namespace
    builtins.QtCore = QtCore
    builtins.QtGui = QtGui
    builtins.QtWidgets = QtWidgets
    builtins.Gui = Gui
    builtins.QIcon = MockQIcon

    return True
