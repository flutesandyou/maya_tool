import sys
import importlib
from Qt.QtWidgets import QApplication, QMainWindow
from Qt.QtGui import QPalette, QColor
import main_window_ui
from CodeEditor import *
from fileTreeView import *

importlib.reload(main_window_ui)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.initUI()
        # Create an instance of the UI class
        #self.ui = main_window_ui.Ui_MainWindow()
        #self.ui.setupUi(self)s
        self.file_tree_view = FileTreeView()
        self.file_tree_view.clicked.connect(self.file_tree_item_clicked)

        # Create an instance of the custom CodeEditor
        self.code_editor = CodeEditor()
        
        self.splitter = QtWidgets.QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.file_tree_view)
        self.splitter.addWidget(self.code_editor)
        self.setCentralWidget(self.splitter)

    def initUI(self):
        self.setWindowTitle('My shitty Tool')
        
        # Get screen resolution
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()

        # Set the window size relative to screen resolution
        window_width = int(screen_rect.width() * 0.5)  # 70% of screen width
        window_height = int(screen_rect.height() * 0.7)  # 70% of screen height
        self.setGeometry(screen_rect.left(), screen_rect.top(), window_width, window_height)



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

    set_dark_palette(app)
# Create an instance of the main window
window = MyMainWindow()

window.show()
sys.exit(app.exec_())