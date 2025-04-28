from PyQt5 import QtCore, QtGui, QtWidgets

from client.client import Client
from ip_window import Ui_Dialog, IPDialog
from client_window import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionAdd_IP.triggered.connect(self.show_ip_dialog)
        self.pushButton.clicked.connect(self.handle_search)
        self.lineEdit.setInputMask("000.000.000-00;_")
        self.client = Client("localhost", 8080)
        self.client.connect()

    def show_ip_dialog(self):
        dialog = IPDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.client.close()
            self.client.set_server_ip(dialog.lineEdit.text())
            self.client.set_server_ip(dialog.lineEdit_2.text())
            self.client.connect()

    def handle_search(self):
        cpf = self.lineEdit.text()
        name = self.lineEdit_2.text()
        date = self.dateEdit.date()
        self.client.add_requisition()
        self.client.send_user(cpf, name, date)
