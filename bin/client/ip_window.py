from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(134, 147)
        Dialog.setStyleSheet("QDialog {\n"
                             "    background-color: black;\n"
                             "    color: white;\n"
                             "    font-family: Arial;\n"
                             "    font-size: 14px;\n"
                             "    border: 1px solid #444;\n"
                             "}\n"
                             "\n"
                             "/* Campos de texto (IP e Porta) */\n"
                             "QLineEdit {\n"
                             "    background-color: #222;\n"
                             "    color: white;\n"
                             "    border: 1px solid #555;\n"
                             "    border-radius: 4px;\n"
                             "    padding: 4px;\n"
                             "}\n"
                             "\n"
                             "/* Label de texto */\n"
                             "QLabel {\n"
                             "    color: white;\n"
                             "}\n"
                             "\n"
                             "/* Botões (OK, Cancel) */\n"
                             "QPushButton {\n"
                             "    background-color: #333;\n"
                             "    color: white;\n"
                             "    border: 1px solid #666;\n"
                             "    border-radius: 4px;\n"
                             "    padding: 6px 12px;\n"
                             "}\n"
                             "\n"
                             "QPushButton:hover {\n"
                             "    background-color: #444;\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {\n"
                             "    background-color: #222;\n"
                             "}\n"
                             "")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "IP"))
        self.label_2.setText(_translate("Dialog", "Port"))


class IPDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
