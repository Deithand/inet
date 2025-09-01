# Python Download Manager

This project is a simple Internet Download Manager built with Python and PyQt6. It includes a browser extension for Chrome/Firefox to intercept downloads and send them to the desktop application.

## Features

- **Intercept downloads:** Catches download links from your browser.
- **Download Queue:** Manages multiple downloads in a list.
- **Pause/Resume:** Supports pausing and resuming downloads (server-dependent).
- **Progress Display:** Shows the progress of each download.
- **Simple UI:** A clean and simple user interface built with PyQt6.

## How to Use

### 1. Prerequisites

- Python 3.6+
- A modern web browser (Google Chrome, Mozilla Firefox, etc.)

### 2. Setup the Desktop Application

1.  **Clone or download this repository.**
2.  **Install dependencies:**
    Open a terminal or command prompt and navigate to the project's root directory. Then run:
    ```bash
    pip install PyQt6 requests
    ```
3.  **Run the application:**
    From the same directory, run the following command:
    ```bash
    python -m download_manager.main
    ```
    The application window should now be open. Keep it running to receive downloads from your browser.

### 3. Install the Browser Extension

These instructions are for Google Chrome, but the process is very similar for other Chromium-based browsers and Firefox.

1.  **Open your browser** and navigate to the extensions page (e.g., `chrome://extensions` for Chrome).
2.  **Enable Developer Mode.** There is usually a toggle switch in the top-right corner of the page.
3.  **Load the extension:**
    - Click the **"Load unpacked"** button.
    - In the file selection dialog, navigate to and select the `browser_extension` folder from this project.
4.  The "Download Manager Assistant" extension is now installed and active.

### 4. How it Works

1.  With the Python application running, simply click any download link in your browser.
2.  The browser extension will intercept the download and send it to the desktop application.
3.  The new download will appear in the application's list and start downloading automatically.

## Project Structure

- `download_manager/`: Contains the source code for the PyQt6 desktop application.
  - `main.py`: The main entry point of the application.
  - `gui.py`: Defines the main window and UI components.
  - `downloader.py`: Handles the logic for downloading files.
  - `server.py`: Runs a local server to listen for requests from the browser extension.
  - `settings.py`: Manages user settings.
- `browser_extension/`: Contains the files for the browser extension.
  - `manifest.json`: The manifest file for the extension.
  - `background.js`: The script that intercepts downloads.
