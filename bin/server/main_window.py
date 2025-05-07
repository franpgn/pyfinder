# main_window.py
from __future__ import annotations

import logging
import threading
import time

from pathlib import Path
from typing import Optional

from PyQt5 import QtCore, QtWidgets

from server import ServerRequestHandler, Server
from ui_main_window import Ui_MainWindow


class DummyServer(threading.Thread):
    def __init__(self, ip: str, port: int, workers: int, parent: "MainWindow"):
        super().__init__(daemon=True)
        self._alive = threading.Event()
        self._alive.set()
        self.ip = ip
        self.port = port
        self.workers = workers
        self.parent = parent
        self.server = None

    def run(self) -> None:
        self.server = Server((self.ip, self.port), ServerRequestHandler, workers=self.workers, db_path=self.parent.db_path)
        logger = logging.getLogger('Server')
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.start()

        logger.info('Server running on %s:%s', self.ip, self.port)

        try:
            while self._alive.is_set():
                time.sleep(0.5)
        finally:
            logger.info('Server shutting down...')
            self.server.shutdown()
            self.server.server_close()
            logger.info('Server closed.')

    def stop(self) -> None:
        self._alive.clear()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # internal state
        self._db_path: Optional[Path] = None
        self._server: Optional[DummyServer] = None

        self.pushButton.clicked.connect(self._choose_db)
        self.pushButton_2.clicked.connect(self._toggle_server)

        self.lineEdit_port.setPlaceholderText("9000")
        self.lineEdit_ip.setPlaceholderText("0.0.0.0")
        self.spinBox.setRange(1, 64)
        self.spinBox.setValue(4)

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
            self._server.stop()
            self._server = None
            self.pushButton_2.setText("Start Server")
            QtWidgets.QMessageBox.information(self, "Server stopped",
                                              "Server thread stopped.")
            return

        try:
            ip = self.lineEdit_ip.text() or self.lineEdit_ip.placeholderText()
            port = int(self.lineEdit_port.text() or self.lineEdit_port.placeholderText())

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

        self._server = DummyServer(ip, port, workers, self)
        self._server.start()
        self.pushButton_2.setText("Stop Server")
        QtWidgets.QMessageBox.information(
            self, "Server started",
            f"Listening on {ip}:{port} with {workers} workers.\n"
            f"DB: {self._db_path}"
        )

    def closeEvent(self, event: QtCore.QCloseEvent) -> None:
        if self._server and self._server.is_alive():
            self._server.stop()
            self._server.join()
        super().closeEvent(event)

    @property
    def db_path(self):
        return self._db_path
