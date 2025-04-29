# main_window.py
from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Optional

from PyQt5 import QtCore, QtWidgets
from ui_main_window import Ui_MainWindow


class DummyServer(threading.Thread):
    """
    Very small background thread that just prints a heartbeat every
    two seconds – replace with your real server implementation.
    """
    def __init__(self, port: int, workers: int, parent: "MainWindow"):
        super().__init__(daemon=True)
        self._alive = threading.Event()
        self._alive.set()
        self.port = port
        self.workers = workers
        self.parent = parent

    def run(self) -> None:
        while self._alive.is_set():
            print(f"[DummyServer] running on port {self.port} "
                  f"with {self.workers} workers…")
            time.sleep(2)

    def stop(self) -> None:
        self._alive.clear()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # internal state
        self._db_path: Optional[Path] = None
        self._server: Optional[DummyServer] = None

        # wire-up signals
        self.pushButton.clicked.connect(self._choose_db)       # Open DB
        self.pushButton_2.clicked.connect(self._toggle_server) # Start / Stop

        # sensible defaults
        self.lineEdit.setPlaceholderText("9000")  # default port
        self.spinBox.setRange(1, 64)
        self.spinBox.setValue(4)

    # ---------- UI slots -------------------------------------------------

    def _choose_db(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            caption="Select database file",
            filter="SQLite (*.db *.sqlite);;All files (*)"
        )
        if path:
            self._db_path = Path(path)
            QtWidgets.QMessageBox.information(
                self, "DB selected", f"Using database:\n{self._db_path}"
            )

    def _toggle_server(self) -> None:
        if self._server and self._server.is_alive():
            # --- stop the running server ---------------------------------
            self._server.stop()
            self._server = None
            self.pushButton_2.setText("Start")
            QtWidgets.QMessageBox.information(self, "Server stopped",
                                              "Server thread stopped.")
            return

        # --- start a new server ------------------------------------------
        try:
            port = int(self.lineEdit.text() or self.lineEdit.placeholderText())
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Invalid port",
                                           "Port must be an integer.")
            return

        workers = self.spinBox.value()
        if self._db_path is None:
            QtWidgets.QMessageBox.warning(
                self, "No DB selected", "Please select a database first."
            )
            return

        self._server = DummyServer(port, workers, self)
        self._server.start()
        self.pushButton_2.setText("Stop")
        QtWidgets.QMessageBox.information(
            self, "Server started",
            f"Listening on port {port} with {workers} workers.\n"
            f"DB: {self._db_path}"
        )

    # ---------- clean shutdown -------------------------------------------

    def closeEvent(self, event: QtCore.QCloseEvent) -> None:
        if self._server and self._server.is_alive():
            self._server.stop()
            self._server.join()
        super().closeEvent(event)
