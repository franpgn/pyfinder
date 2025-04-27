from PyQt5 import QtWidgets
from ip_window import IPDialog
from client_window import Ui_MainWindow
from repository.user import User

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionAdd_IP.triggered.connect(self.show_ip_dialog)
        self.pushButton.clicked.connect(self.handle_search)
        self.lineEdit.setInputMask("000.000.000-00;_")

    def show_ip_dialog(self):
        dialog = IPDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ip = dialog.lineEdit.text()
            port = dialog.lineEdit_2.text()

    def handle_search(self):
        cpf = self.lineEdit.text()
        name = self.lineEdit_2.text()
        date = self.dateEdit.date()
        user = User(name, cpf, date)
        user.export_user()
