import sys
import importlib
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QColor
import MainWindow_ui
from CodeEditor import *
from FileTreeView import *
from ExecutionWidget import *

# importlib.reload(main_window_ui)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.initUI()
        # Create an instance of the UI class
        #self.ui = main_window_ui.Ui_MainWindow()
        #self.ui.setupUi(self)s
        self.file_tree_view = FileTreeView()
        self.code_editor = CodeEditor()
        self.execution_widget = ExecutionWidget(self.file_tree_view)

        self.file_tree_view.clicked.connect(self.file_tree_item_clicked)

        self.file_tree_view.file_content_loaded.connect(self.load_file_into_editor)  # Connect to the correct signal

        # Create an instance of the custom CodeEditor

        top_splitter = QtWidgets.QSplitter(Qt.Horizontal)
        top_splitter.addWidget(self.file_tree_view)
        top_splitter.addWidget(self.execution_widget)

        main_splitter = QtWidgets.QSplitter(Qt.Vertical)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.code_editor)

        self.setCentralWidget(main_splitter)
        
        
    def initUI(self):
        self.setWindowTitle('My shitty Tool')
        
        # Get screen resolution
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()

        # Set the window size relative to screen resolution
        window_width = int(screen_rect.width() * 0.5)  # 70% of screen width
        window_height = int(screen_rect.height() * 0.7)  # 70% of screen height
        self.setGeometry(screen_rect.left(), screen_rect.top(), window_width, window_height)

        # Calculate the center position for the window
        screen_rect = QApplication.desktop().screenGeometry()
        window_rect = self.frameGeometry()
        center_position = screen_rect.center() - window_rect.center()
        # Set window to center
        self.move(center_position)

    def load_file_into_editor(self, file_content):
        self.code_editor.setPlainText(file_content)

    # Slot function to handle toolButton click
    def toolButtonClicked(self):
        print("toolButton clicked!")

    def file_tree_item_clicked(self, index):
        selected_file = self.file_tree_view.get_selected_file()
        if selected_file:
            self.code_editor.load_file(selected_file)

# Step 2: Customize the dark palette to set the colors for various widgets
def set_dark_palette(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(51, 51, 51))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(80, 80, 80))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 122, 204))
    palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

# Create a QApplication instance
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')


    qss_path = os.path.join(os.path.dirname(__file__), 'qss/style.qss')
    stylesheet = open(qss_path).read()
    app.setStyleSheet(stylesheet)

    # set_dark_palette(app)
# Create an instance of the main window
window = MyMainWindow()

window.show()
sys.exit(app.exec_())