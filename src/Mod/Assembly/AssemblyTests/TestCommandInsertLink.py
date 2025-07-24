# SPDX-License-Identifier: LGPL-2.1-or-later
# /****************************************************************************
#                                                                           *
#    Copyright (c) 2023 Ondsel <development@ondsel.com>                     *
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

import FreeCAD as App
import FreeCADGui as Gui
import Part
import unittest
from PySide import QtCore, QtGui


# Create mock Qt classes
class MockQIcon:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def fromTheme(theme_name, fallback=None):
        return MockQIcon()


class MockQTreeWidgetItem:
    def __init__(self, *args, **kwargs):
        self.text_values = {}
        self.data_values = {}
        self._children = []

    def setText(self, column, text):
        self.text_values[column] = text

    def text(self, column):
        return self.text_values.get(column, "")

    def setData(self, column, role, data):
        self.data_values[(column, role)] = data

    def data(self, column, role):
        return self.data_values.get((column, role))

    def setIcon(self, column, icon):
        pass

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


# Patch QtGui with our mock classes
QtGui.QIcon = MockQIcon
QtGui.QTreeWidgetItem = MockQTreeWidgetItem


# Create mock GUI components for testing
class MockCheckBox:
    def __init__(self):
        self.checked = False
        self.stateChanged = MockSignal()

    def setChecked(self, checked):
        self.checked = checked

    def isChecked(self):
        return self.checked


class MockButton:
    def __init__(self):
        pass

    @property
    def clicked(self):
        return MockSignal()


class MockLineEdit:
    def __init__(self):
        self.textChanged = MockSignal()

    def text(self):
        return ""

    def setText(self, text):
        pass


class MockForm:
    def __init__(self):
        self.partList = MockPartList()
        self.CheckBox_ShowOnlyParts = MockCheckBox()
        self.CheckBox_RigidSubAsm = MockCheckBox()
        self.openFileButton = MockButton()
        self.filterPartList = MockLineEdit()

    def installEventFilter(self, filter_obj):
        """Mock method for Qt widget event filter installation."""
        pass

    def setWindowTitle(self, title):
        """Mock method for setting window title."""
        pass

    def show(self):
        """Mock method for showing the widget."""
        pass

    def hide(self):
        """Mock method for hiding the widget."""
        pass


class MockPartList:
    def __init__(self):
        self.itemClicked = MockSignal()
        self.itemDoubleClicked = MockSignal()
        self._items = []

    def header(self):
        return MockHeader()

    def clear(self):
        self._items = []

    def addTopLevelItem(self, item):
        self._items.append(item)

    def installEventFilter(self, filter_obj):
        """Mock method for Qt widget event filter installation."""
        pass

    def expandAll(self):
        """Mock method for expanding all tree items."""
        pass

    def topLevelItemCount(self):
        """Mock method for getting top level item count."""
        return len(self._items)

    def topLevelItem(self, index):
        """Mock method for getting top level item by index."""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def sizeHintForRow(self, row):
        """Mock method for getting size hint for a row."""
        return 20  # Return a reasonable default height

    def setMinimumHeight(self, height):
        """Mock method for setting minimum height."""
        pass


class MockHeader:
    def hide(self):
        pass


class MockSignal:
    def connect(self, slot):
        """Mock method for connecting signals to slots."""
        pass


class MockPySideUic:
    @staticmethod
    def loadUi(ui_file):
        return MockForm()


# Mock the PySideUic if it doesn't exist
if not hasattr(Gui, "PySideUic"):
    Gui.PySideUic = MockPySideUic

# Mock additional Gui methods that might be missing
if not hasattr(Gui, "getDocument"):

    def mock_getDocument(doc_name):
        """Mock method for getting GUI document."""
        return type(
            "MockGuiDocument",
            (),
            {
                "Name": doc_name,
                "getObject": lambda obj_name: None,
                "TreeRootObjects": [],  # Empty list of tree root objects
            },
        )()

    Gui.getDocument = mock_getDocument

# Mock Selection module
if not hasattr(Gui, "Selection"):
    Gui.Selection = type(
        "MockSelection",
        (),
        {
            "clearSelection": lambda *args: None,
            "addSelection": lambda *args: None,
            "getSelection": lambda *args: [],
        },
    )()

# Mock addModule method
if not hasattr(Gui, "addModule"):

    def mock_addModule(module_name):
        """Mock method for adding a module."""
        pass

    Gui.addModule = mock_addModule

# Mock doCommandSkip method
if not hasattr(Gui, "doCommandSkip"):

    def mock_doCommandSkip(commands):
        """Mock method for executing commands."""
        pass

    Gui.doCommandSkip = mock_doCommandSkip

# Make QtCore, QtGui and Gui available in the global namespace for CommandInsertLink import
import sys
import builtins

builtins.QtCore = QtCore
builtins.QtGui = QtGui
builtins.Gui = Gui
builtins.QIcon = MockQIcon

# Now we can import CommandInsertLink
import CommandInsertLink


def _msg(text, end="\n"):
    """Write messages to the console including the line ending."""
    App.Console.PrintMessage(text + end)


class TestCommandInsertLink(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """setUpClass()...
        This method is called upon instantiation of this test class.  Add code and objects here
        that are needed for the duration of the test() methods in this class.  In other words,
        set up the 'global' test environment here; use the `setUp()` method to set up a 'local'
        test environment.
        This method does not have access to the class `self` reference, but it
        is able to call static methods within this same class.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """tearDownClass()...
        This method is called prior to destruction of this test class.  Add code and objects here
        that cleanup the test environment after the test() methods in this class have been executed.
        This method does not have access to the class `self` reference.  This method
        is able to call static methods within this same class.
        """
        pass

    def setUp(self):
        """setUp()...
        This method is called prior to each `test()` method.  Add code and objects here
        that are needed for multiple `test()` methods.
        """
        doc_name = self.__class__.__name__
        if App.ActiveDocument:
            if App.ActiveDocument.Name != doc_name:
                App.newDocument(doc_name)
        else:
            App.newDocument(doc_name)
        App.setActiveDocument(doc_name)
        self.doc = App.ActiveDocument

        self.assembly = App.ActiveDocument.addObject("Assembly::AssemblyObject", "Assembly")

        _msg("  Temporary document '{}'".format(self.doc.Name))

    def tearDown(self):
        """tearDown()...
        This method is called after each test() method. Add cleanup instructions here.
        Such cleanup instructions will likely undo those in the setUp() method.
        """
        App.closeDocument(self.doc.Name)

    def test_mixed_valid_and_invalid_objects(self):
        """Test that accept() handles a mix of valid and invalid objects correctly."""
        operation = "Handle mixed valid/invalid objects"
        _msg("  Test '{}'".format(operation))

        mock_view = type("MockView", (), {"getSize": lambda: (800, 600)})()
        task = CommandInsertLink.TaskAssemblyInsertLink(self.assembly, mock_view)

        # Create a mix of valid and invalid objects
        test_objects = [
            # Valid object (would work in real scenario)
            {
                "addedObject": type(
                    "ValidObject",
                    (),
                    {
                        "Name": "ValidObject",
                        "Label": "Valid Object",
                        "LinkedObject": type(
                            "ValidLinkedObject", (), {"Name": "ValidLinkedObjectName"}
                        )(),
                    },
                )(),
                "translation": App.Vector(1, 1, 1),
            },
            # Invalid: LinkedObject is None
            {
                "addedObject": type(
                    "InvalidObject1",
                    (),
                    {"Name": "InvalidObject1", "Label": "Invalid Object 1", "LinkedObject": None},
                )(),
                "translation": App.Vector(2, 2, 2),
            },
            # Invalid: No LinkedObject attribute
            {
                "addedObject": type(
                    "InvalidObject2", (), {"Name": "InvalidObject2", "Label": "Invalid Object 2"}
                )(),
                "translation": App.Vector(3, 3, 3),
            },
            # Invalid: LinkedObject.Name is None
            {
                "addedObject": type(
                    "InvalidObject3",
                    (),
                    {
                        "Name": "InvalidObject3",
                        "Label": "Invalid Object 3",
                        "LinkedObject": type("LinkedObjectWithNoneName", (), {"Name": None})(),
                    },
                )(),
                "translation": App.Vector(4, 4, 4),
            },
            # Invalid: No Name attribute
            {
                "addedObject": type(
                    "InvalidObject4",
                    (),
                    {
                        "Label": "Invalid Object 4",
                        "LinkedObject": type("LinkedObject", (), {"Name": "Something"})(),
                    },
                )(),
                "translation": App.Vector(5, 5, 5),
            },
        ]

        # Add all objects to insertion stack
        for obj_data in test_objects:
            task.insertionStack.append(obj_data)

        # Should handle the mix gracefully - invalid objects skipped, valid ones processed
        try:
            result = task.accept()
            self.assertTrue(
                result, "accept() should return True even with mixed valid/invalid objects"
            )
            _msg("  Successfully handled mixed valid/invalid objects")
        except Exception as e:
            self.fail("Failed to handle mixed objects: {}".format(e))

    def test_empty_insertion_stack(self):
        """Test that accept() handles empty insertion stack correctly."""
        operation = "Handle empty insertion stack"
        _msg("  Test '{}'".format(operation))

        mock_view = type("MockView", (), {"getSize": lambda: (800, 600)})()
        task = CommandInsertLink.TaskAssemblyInsertLink(self.assembly, mock_view)

        # Don't add anything to insertion stack - it should remain empty
        self.assertEqual(len(task.insertionStack), 0, "Insertion stack should be empty")

        try:
            result = task.accept()
            self.assertTrue(result, "accept() should return True even with empty insertion stack")
            _msg("  Successfully handled empty insertion stack")
        except Exception as e:
            self.fail("Failed to handle empty insertion stack: {}".format(e))
