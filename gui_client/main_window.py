from multiprocessing.util import debug

from PyQt5 import QtCore, QtGui, QtWidgets
import json
from client.client import Client
from ip_window import IPDialog
from client_window import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionAdd_IP.triggered.connect(self.show_ip_dialog)
        self.pushButton.clicked.connect(self.handle_search)
        self.lineEdit.setInputMask("000.000.000-00;_")
        self.client = Client('localhost', 9000)
        self.client.response_received.connect(self.update_table)
        self.client.connect()
        self.client.start_receiving()

        self.current_index = 0
        self.previousButton.clicked.connect(self.previous_id)
        self.nextButton.clicked.connect(self.next_id)

    def show_ip_dialog(self):
        dialog = IPDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                self.client = Client(dialog.lineEdit.text(), int(dialog.lineEdit_2.text()))
                self.client.response_received.connect(self.update_table)
                self.client.connect()
                self.client.start_receiving()
            except ConnectionError as e:
                self.show_error_message(str(e))

    def show_error_message(self, message):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Connection Error")
        msg_box.setText("An error occurred while connecting:")
        msg_box.setInformativeText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    def handle_search(self):
        cpf = self.lineEdit.text()
        name = self.lineEdit_2.text()
        date = self.dateEdit.date()

        if date > QtCore.QDate(2024, 1, 1):
            date_string = ""
        else:
            date_string = date.toString("yyyy-MM-dd")

        if self.client:
            self.client.send_user(name, cpf, "", date_string)
        else:
            print("No connection on the server")

    def closeEvent(self, event):
        if self.client:
            self.client.close()
        event.accept()

    def update_table(self):
        if not self.client.lista_id:
            print("No IDs received yet.")
            return

        target_id = self.client.lista_id[self.current_index]

        try:
            with open("responses.json", "r", encoding="utf-8") as file:
                responses = json.load(file)

            target_response = None
            for response in responses["responses"]:
                if response["request_id"] == target_id:
                    target_response = response
                    print(target_response)
                    break

            if not target_response:
                print(f"No response found with ID {target_id}")
                return

            data_list = target_response["user_data"]
            print(data_list)
            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(["Name", "CPF", "Gender", "Birth Date"])

            if isinstance(data_list, list):
                for user in data_list:
                    name_item = QtGui.QStandardItem(str(user.get("name", "")))
                    cpf_item = QtGui.QStandardItem(str(user.get("cpf", "")))
                    gender_item = QtGui.QStandardItem(str(user.get("gender", "")))
                    date_item = QtGui.QStandardItem(str(user.get("date", "")))
                    model.appendRow([name_item, cpf_item, gender_item, date_item])
            else:
                name_item = QtGui.QStandardItem(str(data_list.get("name", "")))
                cpf_item = QtGui.QStandardItem(str(data_list.get("cpf", "")))
                gender_item = QtGui.QStandardItem(str(data_list.get("gender", "")))
                date_item = QtGui.QStandardItem(str(data_list.get("date", "")))
                model.appendRow([name_item, cpf_item, gender_item, date_item])

            self.tableView.setModel(model)
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.update_navigation_buttons()

        except Exception as e:
            print(f"Error updating table: {e}")

    def update_navigation_buttons(self):
        if not self.client.lista_id:
            self.previousButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            return

        if self.current_index <= 0:
            self.previousButton.setEnabled(False)
        else:
            self.previousButton.setEnabled(True)

        if self.current_index >= len(self.client.lista_id) - 1:
            self.nextButton.setEnabled(False)
        else:
            self.nextButton.setEnabled(True)

    def previous_id(self):
        if self.client.lista_id:
            if self.current_index > 0:
                self.current_index -= 1
                self.update_table()
            else:
                print("Already at the first ID.")
        self.update_navigation_buttons()

    def next_id(self):
        if self.client.lista_id:
            if self.current_index < len(self.client.lista_id) - 1:
                self.current_index += 1
                self.update_table()
            else:
                print("Already at the last ID.")
        self.update_navigation_buttons()