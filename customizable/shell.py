from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, QApplication, QSplitter, QLabel
)
from PyQt5.QtGui import QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt
import subprocess
import os
import sys


class ModernShell(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integrated Shell")
        # self.setGeometry(100, 100, 800, 400)

        # Set main background color
        self.setStyleSheet("background-color: #1e1e1e;")  # Dark modern look

        # Layout
        layout = QVBoxLayout(self)

        # Initialize the current working directory
        self.current_directory = os.getcwd()

        # Current working directory label
        self.cwd_label = QLabel(self)
        self.cwd_label.setFont(QFont("Courier New", 11))
        self.cwd_label.setStyleSheet(
            """
            background-color: #2e2e2e;
            color: #ffffff;
            padding: 8px;
            border-radius: 5px;
            font-weight: bold;
            """
        )
        self.update_cwd_label()

        # Terminal output area
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Courier New", 11))
        self.output_area.setStyleSheet(
            """
            background-color: #282828;
            color: #dcdcdc;
            border: 1px solid #444444;
            border-radius: 5px;
            padding: 10px;
            """
        )
        self.output_area.append(
            f"<span style='color: green;'>Welcome to the Shell! Type commands below.</span>"
        )

        # Command input area
        self.input_area = QLineEdit(self)
        self.input_area.setFont(QFont("Courier New", 11))
        self.input_area.setStyleSheet(
            """
            background-color: #3e3e3e;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 8px;
            """
        )
        self.input_area.returnPressed.connect(self.execute_command)

        # History and command handling
        self.command_history = []
        self.current_history_index = -1

        # Layout adjustments
        layout.addWidget(self.cwd_label)
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)
        self.setLayout(layout)

    def update_cwd_label(self):
        """Update the current working directory label."""
        self.cwd_label.setText(f"Current Directory: {self.current_directory}")

    def execute_command(self):
        command = self.input_area.text().strip()

        if command:
            self.command_history.append(command)
            self.current_history_index = len(self.command_history)
            self.output_area.append(
                f"<span style='color: cyan;'>{self.current_directory}> {command}</span>"
            )

            if command.startswith("cd"):
                # Change directory
                try:
                    path = command.split(" ", 1)[1]
                    os.chdir(path)
                    self.current_directory = os.getcwd()
                    self.update_cwd_label()
                    self.output_area.append(
                        f"<span style='color: green;'>Changed directory to {self.current_directory}</span>"
                    )
                except (IndexError, FileNotFoundError):
                    self.output_area.append("<span style='color: red;'>Invalid directory.</span>")
            else:
                # Execute the command
                try:
                    result = subprocess.run(
                        command, shell=True, text=True, capture_output=True, cwd=self.current_directory
                    )
                    if result.stdout:
                        self.output_area.append(result.stdout.strip())
                    if result.stderr:
                        self.output_area.append(f"<span style='color: red;'>{result.stderr.strip()}</span>")
                except Exception as e:
                    self.output_area.append(f"<span style='color: red;'>Error: {e}</span>")

        self.input_area.clear()
        self.output_area.moveCursor(QTextCursor.End)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            # Navigate command history (backward)
            if self.current_history_index > 0:
                self.current_history_index -= 1
                self.input_area.setText(self.command_history[self.current_history_index])
        elif event.key() == Qt.Key_Down:
            # Navigate command history (forward)
            if self.current_history_index < len(self.command_history) - 1:
                self.current_history_index += 1
                self.input_area.setText(self.command_history[self.current_history_index])
            else:
                self.input_area.clear()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shell = ModernShell()
    shell.show()
    sys.exit(app.exec_())
