from ui_main import IDE
import sys
from PyQt5.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    
    # Apply the global style to the application
    app.setStyleSheet("""
        QWidget {
            background-color: #282c34;
        }
    """)
    
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
