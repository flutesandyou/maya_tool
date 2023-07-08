import sys
import imp
from Qt.QtWidgets import QApplication, QMainWindow
import main_window_ui
from CodeEditor import *
from fileTreeView import *

imp.reload(main_window_ui)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        # Create an instance of the UI class
        #self.ui = main_window_ui.Ui_MainWindow()
        #self.ui.setupUi(self)
      
        self.file_tree_view = FileTreeView()
        
        # Create an instance of the custom CodeEditor
        self.code_editor = CodeEditor()

        self.splitter = QtWidgets.QSplitter()
        self.splitter.addWidget(self.file_tree_view)
        self.splitter.addWidget(self.code_editor)
        self.setCentralWidget(self.splitter)

        self.file_tree_view.clicked.connect(self.file_tree_item_clicked)


    # Slot function to handle toolButton click
    def toolButtonClicked(self):
        print("toolButton clicked!")

    def file_tree_item_clicked(self, index):
        selected_file = self.file_tree_view.get_selected_file()
        if selected_file:
            self.code_editor.load_file(selected_file)

# Create a QApplication instance
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

# Create an instance of the main window
window = MyMainWindow()
window.show()

sys.exit(app.exec_())