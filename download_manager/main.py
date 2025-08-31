import sys
from PyQt6.QtWidgets import QApplication
from .gui import MainWindow
from .server import ServerThread, UrlReceiver
from .settings import Settings

def main():
    app = QApplication(sys.argv)

    # Load settings
    settings = Settings()
    download_dir = settings.get("download_directory")

    # Create main window
    main_window = MainWindow()
    main_window.download_dir = download_dir

    # Set up the server to listen for downloads from the browser extension
    url_receiver = UrlReceiver()
    url_receiver.new_url.connect(main_window.add_download)

    server_thread = ServerThread(url_receiver)
    server_thread.daemon = True # Allows main thread to exit even if this thread is running
    server_thread.start()

    # Make sure server is stopped when app closes
    app.aboutToQuit.connect(server_thread.stop)

    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
