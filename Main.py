import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel,
    QTextEdit, QMessageBox, QGroupBox, QMenuBar
)
from PySide6.QtGui import QAction  # Correct import for QAction
from PySide6.QtCore import QThread, Signal

class ConversionThread(QThread):
    output_received = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        try:
            # Simplified ffmpeg command
            command = [
                "ffmpeg",
                "-i", self.input_file,
                self.output_file
            ]
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            # Capture real-time output
            while True:
                output = process.stderr.readline()
                if output:
                    self.output_received.emit(output.strip())
                if process.poll() is not None:
                    break

            # Check for successful completion
            if process.returncode == 0:
                self.finished.emit(True, "Conversion successful!")
            else:
                self.finished.emit(False, "Conversion failed. Check the logs for details.")
        except Exception as e:
            self.finished.emit(False, f"Error occurred: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MKV to MOV Converter")
        self.setGeometry(300, 300, 700, 500)

        # Add Menu Bar
        self.create_menu_bar()

        # Section: File Selection
        self.file_group = QGroupBox("Step 1: Select Your MKV File")
        self.file_label = QLabel("Choose an MKV file to convert:")
        self.file_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.file_button = QPushButton("Select MKV File")
        self.file_button.clicked.connect(self.select_file)

        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        self.file_group.setLayout(file_layout)

        # Section: Generate MOV
        self.convert_group = QGroupBox("Step 2: Generate MOV File")
        self.convert_label = QLabel("Click 'Generate MOV' to choose where to save the output file.")
        self.convert_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.convert_button = QPushButton("Generate MOV")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.start_conversion)

        convert_layout = QVBoxLayout()
        convert_layout.addWidget(self.convert_label)
        convert_layout.addWidget(self.convert_button)
        self.convert_group.setLayout(convert_layout)

        # Section: Output Logs
        self.output_group = QGroupBox("Step 3: Monitor Conversion Progress")
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("font-family: Consolas, monospace; font-size: 12px; color: green;")

        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output_text)
        self.output_group.setLayout(output_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_group)
        main_layout.addWidget(self.convert_group)
        main_layout.addWidget(self.output_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # State
        self.input_file = None
        self.output_file = None
        self.thread = None
        self.is_dark_theme = False

    def create_menu_bar(self):
        """Create a standard menu bar with theme toggle."""
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")

        # File menu options
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu options
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        # Theme toggle
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        menu_bar.addAction(theme_action)

        self.setMenuBar(menu_bar)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.is_dark_theme:
            self.setStyleSheet("")
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #2E3440; color: #D8DEE9; }
                QLabel, QGroupBox { color: #D8DEE9; }
                QPushButton { background-color: #4C566A; color: #D8DEE9; border: none; padding: 5px; }
                QPushButton:hover { background-color: #5E81AC; }
                QTextEdit { background-color: #3B4252; color: green; border: 1px solid #D8DEE9; }
            """)
        self.is_dark_theme = not self.is_dark_theme

    def show_about_dialog(self):
        """Display an About dialog."""
        QMessageBox.information(self, "About", "MKV to MOV Converter\nVersion 1.0\nPowered by FFmpeg and PySide6")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MKV File", "", "MKV Files (*.mkv)")
        if file_path:
            self.input_file = file_path
            self.file_label.setText(f"Selected File: {file_path}")
            self.convert_button.setEnabled(True)

    def start_conversion(self):
        if not self.input_file:
            QMessageBox.warning(self, "Warning", "Please select an MKV file first.")
            return

        # Prompt user for output file location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save MOV File As", "", "MOV Files (*.mov)")
        if not file_path:
            QMessageBox.warning(self, "Warning", "No save location selected.")
            return

        if not file_path.lower().endswith(".mov"):
            file_path += ".mov"
        self.output_file = file_path

        self.file_label.setText("Converting... Please wait.")
        self.output_text.clear()
        self.convert_button.setEnabled(False)

        # Start conversion thread
        self.thread = ConversionThread(self.input_file, self.output_file)
        self.thread.output_received.connect(self.update_output)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()

    def update_output(self, text):
        self.output_text.append(text)
        self.output_text.verticalScrollBar().setValue(self.output_text.verticalScrollBar().maximum())

    def conversion_finished(self, success, message):
        self.convert_button.setEnabled(True)
        if success:
            QMessageBox.information(self, "Success", message)
            self.file_label.setText("Conversion Complete!")
        else:
            QMessageBox.critical(self, "Error", message)
            self.file_label.setText("Conversion Failed.")


if __name__ == "__main__":
    # Set QT platform for Wayland issues
    os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
