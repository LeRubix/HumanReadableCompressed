# Made by Rubix (@LeRubix on GitHub) 26/08/2024

import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox,
                             QLabel, QHBoxLayout)
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt
import subprocess

# Import the compress_file and decompress_file functions from hrc.py and hrdc.py
from hrc import compress_file
from hrdc import decompress_file


class HRCApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Human Readable Compressed')
        self.setGeometry(300, 300, 400, 200)
        
        # Set the window icon
        self.setWindowIcon(QIcon('icons/hrc.ico'))

        layout = QVBoxLayout()

        # Add a centered title
        title_label = QLabel('Human Readable Compressed (.hrc) GUI', self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        compress_btn = QPushButton('Choose a file to compress (.json/.jsonl/.yaml/.yml)', self)
        compress_btn.clicked.connect(self.compress_file)
        layout.addWidget(compress_btn)

        decompress_btn = QPushButton('Choose a file to decompress (.hrc)', self)
        decompress_btn.clicked.connect(self.decompress_file)
        layout.addWidget(decompress_btn)

        self.comparison_label = QLabel('', self)
        self.comparison_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.comparison_label)

        self.open_location_btn = QPushButton('Open file location', self)
        self.open_location_btn.clicked.connect(self.open_file_location)
        self.open_location_btn.setVisible(False)
        layout.addWidget(self.open_location_btn)

        self.setLayout(layout)

    def compress_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file to compress",
            "",
            "Supported Files (*.json *.jsonl *.yaml *.yml);;All Files (*)"
        )
        if file_path:
            try:
                original_size = os.path.getsize(file_path)
                compressed_file_path = compress_file(file_path)
                
                if compressed_file_path is None:
                    # Assume compression was successful but the function doesn't return the path
                    compressed_file_path = file_path + '.hrc'
                
                if not os.path.exists(compressed_file_path):
                    raise FileNotFoundError(f"Compressed file not found: {compressed_file_path}")
                
                compressed_size = os.path.getsize(compressed_file_path)
                
                size_diff = original_size - compressed_size
                percentage = (size_diff / original_size) * 100

                comparison_text = f"Original: {original_size:,} bytes<br>"
                comparison_text += f"Compressed: {compressed_size:,} bytes<br>"
                comparison_text += f"<font color='green'>Difference: {size_diff:,} bytes ({percentage:.2f}% smaller)</font>"

                self.comparison_label.setText(comparison_text)
                self.comparison_label.setTextFormat(Qt.TextFormat.RichText)
                
                self.open_location_btn.setVisible(True)
                self.last_compressed_file = compressed_file_path

                QMessageBox.information(self, "Success", "File compressed successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
                self.comparison_label.setText("")
                self.open_location_btn.setVisible(False)

    def decompress_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to decompress", "", "Compressed Files (*.hrc)")
        if file_path:
            try:
                decompress_file(file_path)
                QMessageBox.information(self, "Success", "File decompressed successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def open_file_location(self):
        if hasattr(self, 'last_compressed_file'):
            file_path = os.path.abspath(self.last_compressed_file)
            if sys.platform == 'win32':
                os.startfile(os.path.dirname(file_path))
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', os.path.dirname(file_path)])
            else:
                subprocess.Popen(['xdg-open', os.path.dirname(file_path)])

def set_dark_theme(app):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_dark_theme(app)
    ex = HRCApp()
    ex.show()
    sys.exit(app.exec())