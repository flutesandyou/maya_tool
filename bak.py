from Qt.QtWidgets import *
from Qt.QtCore import *
#from PyQt5.Qsci import *
from Qt.QtGui import *

import sys
from pathlib import Path

class AnotherWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # add before init
        self.side_bar_clr = "#282c34"
        #self.init.ui()

        self.current_file = None
    def init_ui(self):

        self.setWindowTitle("PyQt Code Editor")
        self.resize(1300,900)

        self.setStyleSheet(open("./src/css/style.qss", "r").read())
        
        # alternative Consolas font
        self.window_font = QFont("Fire Code")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()

        

        self.show()


    def set_up_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        new_file = file_menu.AddAction("New File")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+Shift+K")
        open_folder.triggered.connect(self.open_folder)

        # Edit_menu

        edit_menu = menu_bar.addMenu("Edit")
        copy_action = file_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        #add more

    def new_file(self):
        ...
    def open_file(self):
        ...
    def open_folder(self):
        ...
    def copy(self):
        ...

    def set_up_body(self):

        # Body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0,0,0,0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0,0,0,0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        # side_bar
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StylePanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet('''
            background-color: {self.side_bar_clr};
            '''
        )
        side_bar_layout = QHBoxLayout()
        side_bar_layout.setContentMargins(5,10,5,0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.side_bar.setLayout(side_bar_layout)
        body.addWidget(self.side_bar)

        # split view
        self.hsplit = QSplitter(Qt.Horizontal)

        # frame and layout to hold tree view (file manager)
        self.tree_frame = QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100, 0)
        self.tree_frame.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0,0,0,0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;       
            }
            QFrame:hover {
                color: white;                   
            }      
        ''')

        # Create File system mode to show in tree view
        self.model = QFileSystemMode()
        self.model.setRootPath(os.getcwd())
        # File system filters
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        # Tree View
        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("FiraCode", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.NoEditTriggers)
        #add custom context menu
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        # handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def tree_view_context_menu(self, pos):
        ...

    def tree_view_clicked(self):
        ...
