import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QProgressBar, QFileDialog, QLineEdit, QMessageBox)
from PyQt6.QtCore import QUrl
from .downloader import Downloader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Manager")
        self.setGeometry(100, 100, 800, 400)

        self.downloads = []
        self.download_dir = os.path.expanduser("~") # Default to home directory

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter download URL here")
        self.layout.addWidget(self.url_input)

        # Add download button
        self.add_button = QPushButton("Add Download")
        self.add_button.clicked.connect(self.add_download_manually)
        self.layout.addWidget(self.add_button)

        # Downloads table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["File Name", "Size", "Progress", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        # Settings button could be added here later

    def add_download_manually(self):
        url = self.url_input.text().strip()
        if url:
            self.add_download(url)
            self.url_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a URL.")

    def add_download(self, url):
        file_name = os.path.basename(QUrl(url).path())
        save_path = os.path.join(self.download_dir, file_name)

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(file_name))
        self.table.setItem(row_position, 1, QTableWidgetItem("0 MB")) # Size

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        self.table.setCellWidget(row_position, 2, progress_bar)

        self.table.setItem(row_position, 3, QTableWidgetItem("Pending"))

        downloader = Downloader(url, save_path)
        downloader.progress.connect(lambda p: self.update_progress(row_position, p))
        downloader.finished.connect(lambda s: self.download_finished(row_position, s))
        downloader.status_changed.connect(lambda s: self.update_status(row_position, s))

        self.downloads.append({"downloader": downloader, "row": row_position})
        downloader.start()

    def update_progress(self, row, percentage):
        progress_bar = self.table.cellWidget(row, 2)
        if progress_bar:
            progress_bar.setValue(percentage)

    def update_status(self, row, status):
        self.table.setItem(row, 3, QTableWidgetItem(status))

    def download_finished(self, row, success):
        status = "Completed" if success else "Failed"
        self.table.setItem(row, 3, QTableWidgetItem(status))
        # here you could add logic to re-enable buttons etc.

    def closeEvent(self, event):
        # Cancel all running downloads before closing
        for download in self.downloads:
            download['downloader'].cancel()
        event.accept()
