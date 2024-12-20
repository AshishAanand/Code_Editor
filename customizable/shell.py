from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, QApplication, QSplitter, QLabel, QPushButton, QComboBox
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

        # Clear button
        self.clear_button = QPushButton("Clear Shell", self)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6347;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        self.clear_button.clicked.connect(self.clear_output)
        layout.addWidget(self.clear_button)


        self.filter_box = QComboBox(self)
        self.filter_box.addItems(["All", "Errors", "Warnings"])
        self.filter_box.setStyleSheet("""
            QComboBox {
                background-color: #3e3e3e;
                color: white;
                padding: 5px;
                border: 1px solid #555555;
                border-radius: 5px;
            }
        """)
        self.filter_box.currentTextChanged.connect(self.apply_filter)
        layout.addWidget(self.filter_box)


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
                    if result.returncode == 0:
                        self.output_area.append(f"<span style='color: lightgreen;'>[Success]</span>")
                    else:
                        self.output_area.append(f"<span style='color: red;'>[Failed]</span>")

                    if result.stdout:
                        self.output_area.append(f"<span style='color: lightgreen;'>{result.stdout.strip()}</span>")
                    if result.stderr:
                        if "warning" in result.stderr.lower():
                            self.output_area.append(f"<span style='color: yellow;'>{result.stderr.strip()}</span>")
                        else:
                            self.output_area.append(f"<span style='color: red;'>{result.stderr.strip()}</span>")
                except Exception as e:
                    self.output_area.append(f"<span style='color: red;'>Error: {e}</span>")

        self.input_area.clear()
        self.output_area.moveCursor(QTextCursor.End)

    def apply_filter(self, filter_type):
        """Filter the output based on the selected type."""
        lines = self.output_area.toPlainText().split("\n")
        self.output_area.clear()
        for line in lines:
            if filter_type == "All":
                self.output_area.append(line)
            elif filter_type == "Errors" and "color: red" in line:
                self.output_area.append(line)
            elif filter_type == "Warnings" and "color: yellow" in line:
                self.output_area.append(line)


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
    
    def clear_output(self):
        """Clear the output area."""
        self.output_area.clear()

    def run_code(self, file_path, code):
        self.language = self.detect_language(file_path)
        if self.language == "Unknown":
            self.output_area.append("<span style='color: orange;'>Unsupported language</span>")
        try:
            if self.language == "Python":
                # result = subprocess.run(["python", file_path], check=True, capture_output=True, text=True)
                # def run_python_code(code):
                    # Save the user code to a temporary file
                    with open("temp_code.py", "w") as file:
                        file.write(code)

                    # Run the Python file and capture output
                    try:
                        result = subprocess.run(
                            ["python", "temp_code.py"],
                            text=True,
                            capture_output=True,
                            check=True
                        )
                        print("Output:\n", result.stdout)
                    except subprocess.CalledProcessError as e:
                        print("Error:\n", e.stderr)

                # # Example usage
                # user_code = """
                # print("Hello, World!")
                # for i in range(5):
                #     print("Line", i)
                # """
                # run_python_code(user_code)
            elif self.language == "C++":
                output_file = "a.out"
                subprocess.run(["g++", file_path, "-o", output_file], check=True)
                result = subprocess.run([f"./{output_file}"], check=True, capture_output=True, text=True)
            elif self.language == "Java":
                subprocess.run(["javac", file_path], check=True)
                class_name = os.path.splitext(os.path.basename(file_path))[0]
                result = subprocess.run(["java", class_name], check=True, capture_output=True, text=True)
            elif self.language == "JavaScript":
                result = subprocess.run(["node", file_path], check=True, capture_output=True, text=True)
            else:
                self.output_area.append("<span style='color: orange;'>Unsupported language</span>")
                return

            self.output_area.append(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            self.output_area.append(f"<span style='color: red;'>Execution Error: {e}</span>")

    
    def detect_language(self, file_path):
        self.language_map = {
            ".py": "Python",
            ".cpp": "C++",
            ".c": "C",
            ".java": "Java",
            ".js": "JavaScript",
            ".html": "HTML",
            ".css": "CSS",
        }
        _, self.extension = os.path.splitext(file_path)
        return self.language_map.get(self.extension, "Unknown")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shell = ModernShell()
    shell.show()
    sys.exit(app.exec_())
