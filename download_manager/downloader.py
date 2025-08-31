import requests
import threading
import os
from PyQt6.QtCore import QObject, pyqtSignal

class Downloader(QObject):
    # Signals to communicate with the GUI
    progress = pyqtSignal(int)  # Percentage
    finished = pyqtSignal(bool) # Success or failure
    status_changed = pyqtSignal(str)

    def __init__(self, url, save_path, parent=None):
        super().__init__(parent)
        self.url = url
        self.save_path = save_path
        self.paused = False
        self.cancelled = False
        self.thread = None
        self.total_size = 0
        self.downloaded_size = 0

    def start(self):
        self.thread = threading.Thread(target=self._download)
        self.thread.start()

    def pause(self):
        self.paused = True
        self.status_changed.emit("Paused")

    def resume(self):
        self.paused = False
        self.status_changed.emit("Downloading")
        self.start()

    def cancel(self):
        self.cancelled = True
        self.status_changed.emit("Cancelled")

    def _download(self):
        try:
            headers = {}
            if os.path.exists(self.save_path):
                self.downloaded_size = os.path.getsize(self.save_path)
                headers['Range'] = f'bytes={self.downloaded_size}-'
            else:
                self.downloaded_size = 0

            response = requests.get(self.url, headers=headers, stream=True, timeout=10)

            if response.status_code == 206: # Partial content
                pass # Resuming download
            elif response.status_code == 200: # Full content
                self.downloaded_size = 0
            else:
                self.status_changed.emit(f"Error: {response.status_code}")
                self.finished.emit(False)
                return

            self.total_size = int(response.headers.get('content-length', 0)) + self.downloaded_size

            with open(self.save_path, 'ab' if self.downloaded_size > 0 else 'wb') as f:
                self.status_changed.emit("Downloading")
                for chunk in response.iter_content(chunk_size=1024):
                    if self.cancelled:
                        self.finished.emit(False)
                        return

                    while self.paused:
                        if self.cancelled:
                            self.finished.emit(False)
                            return
                        threading.sleep(0.1)

                    if chunk:
                        f.write(chunk)
                        self.downloaded_size += len(chunk)
                        if self.total_size > 0:
                            progress_percentage = int((self.downloaded_size / self.total_size) * 100)
                            self.progress.emit(progress_percentage)

            if not self.cancelled:
                self.status_changed.emit("Completed")
                self.finished.emit(True)

        except requests.RequestException as e:
            self.status_changed.emit(f"Error: {e}")
            self.finished.emit(False)
