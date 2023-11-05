import os
from CodeEditor import CodeEditor
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QInputDialog, QFileDialog
from PySide2.QtCore import Signal, Qt

class FileTreeView(QtWidgets.QTreeView):
    # Define the signal here
    file_content_loaded = Signal(str)

    def __init__(self, parent=None):
        super(FileTreeView, self).__init__(parent)

        
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setHeaderHidden(True)

        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.root_item = self.model.invisibleRootItem()

        self.setup_context_menu()

        # Create the CodeEditor instance
        self.code_editor = CodeEditor()

    def setup_context_menu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.context_menu = QtWidgets.QMenu(self)
        self.new_file_action = QtWidgets.QAction("New File", self)
        self.load_file_action = QtWidgets.QAction("Load File", self)
        self.delete_item_action = QtWidgets.QAction("Delete Item", self)
        self.save_file_action = QtWidgets.QAction("Save File", self)

        self.context_menu.addAction(self.new_file_action)
        self.context_menu.addAction(self.load_file_action)
        self.context_menu.addAction(self.delete_item_action)
        self.context_menu.addAction(self.save_file_action)

        self.new_file_action.triggered.connect(self.new_file)
        self.load_file_action.triggered.connect(self.load_file)
        self.delete_item_action.triggered.connect(self.delete_item)
        self.save_file_action.triggered.connect(self.save_file)

    def save_file(self):
        selected_item = self.get_selected_item()
        if selected_item:
            file_path = selected_item.data(QtCore.Qt.UserRole)
            if file_path:
                # Get the code from the CodeEditor
                code = self.code_editor.get_plain_text()

                # Update the cached content
                self.cached_files_content[file_path] = code

                # Save the code to the file
                with open(file_path, 'w') as file:
                    file.write(code)

    def file_tree_item_selected(self, selected, deselected):
        if selected.indexes():
            selected_item = self.model.itemFromIndex(selected.indexes()[0])
            file_path = selected_item.data(QtCore.Qt.UserRole)

            # Save any changes from the previous file
            previous_item = self.get_selected_item()
            if previous_item:
                previous_file_path = previous_item.data(QtCore.Qt.UserRole)
                previous_code = self.code_editor.get_plain_text()
                self.cached_files_content[previous_file_path] = previous_code

            # Load and display the selected file content
            if file_path in self.cached_files_content:
                self.code_editor.set_plain_text(self.cached_files_content[file_path])
            else:
                self.code_editor.load_file(file_path)

    def get_selected_file(self):
        selected_index = self.currentIndex()
        selected_item = self.model.itemFromIndex(selected_index)
        if selected_item:
            # Assuming you set the file path as the item's data
            file_path = selected_item.data(QtCore.Qt.UserRole)
            return file_path

    def show_context_menu(self, position):
        global_position = self.viewport().mapToGlobal(position)
        self.context_menu.exec_(global_position)

    def new_file(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setWindowTitle("New File")
        dialog.setLabelText(QFileDialog.Accept, "Save")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setDefaultSuffix("py")
        dialog.setFileMode(QFileDialog.AnyFile)

        if dialog.exec_() == QFileDialog.Accepted:
            file_paths = dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]

                # Create the file
                with open(file_path, 'w') as file:
                    file.write("")

                # Add the file to the FileTreeView
                self.add_file(file_path)
                # Load the file in the CodeEditor
                self.code_editor.load_file(file_path)
        
    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Python File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                file_content = file.read()
                self.file_content_loaded.emit(file_content)

            # Add the filename to the FileTreeView
            file_item = QStandardItem(file_path.split("/")[-1])  # Get only the filename without path
            file_item.setData(file_path, Qt.UserRole)  # Set the file path as item data
            self.root_item.appendRow(file_item)
            
    def delete_item(self):
        selected_item = self.get_selected_item()
        if selected_item:
            self.model.removeRow(selected_item.row())

    def save_file(self):
        selected_item = self.get_selected_item()
        if selected_item:
            file_path = selected_item.data(QtCore.Qt.UserRole)
            if file_path:
                # Get the code from the CodeEditor
                code = self.code_editor.toPlainText()

                # Save the code to the file
                with open(file_path, 'w') as file:
                    file.write(code)

    def add_file(self, file_path):
        file_name = QtCore.QFileInfo(file_path).fileName()
        file_item = QStandardItem(file_name)
        file_item.setData(file_path, QtCore.Qt.UserRole)
        self.root_item.appendRow(file_item)

    def add_folder(self, folder_path):
        folder_name = QtCore.QDir(folder_path).dirName()
        folder_item = QStandardItem(folder_name)
        folder_item.setData(folder_path, QtCore.Qt.UserRole)
        self.root_item.appendRow(folder_item)

    def get_selected_file(self):
        selected_indexes = self.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            if selected_index.isValid():
                item = self.model.itemFromIndex(selected_index)
                if item.data(QtCore.Qt.UserRole):
                    return item.data(QtCore.Qt.UserRole)
        return None

    def get_selected_item(self):
        selected_indexes = self.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            if selected_index.isValid():
                return self.model.itemFromIndex(selected_index)
        return None

    def get_full_path(self, item):
        path = []
        while item is not None:
            path.insert(0, item.data(QtCore.Qt.UserRole))
            item = item.parent()
        return "/".join(path)
