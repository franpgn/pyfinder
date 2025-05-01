from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QIcon("../repository/resources/Icon.png"))
        MainWindow.resize(500, 300)

        MainWindow.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        QLineEdit, QSpinBox {
            background-color: #2c2c2c;
            color: #ffffff;
            border: 1px solid #444444;
            border-radius: 6px;
            padding: 6px;
            selection-background-color: #555555;
            selection-color: white;
        }

        QLabel {
            color: #bbbbbb;
            font-weight: normal;
        }

        QPushButton {
            background-color: #3d7eff;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #629aff;
        }

        QPushButton:pressed {
            background-color: #2c5eff;
        }

        QPushButton:focus {
            outline: none;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Frame para Open DB + IP + Port
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMinimumHeight(30)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.lineEdit_ip = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_ip.setMinimumHeight(30)
        self.lineEdit_ip.setPlaceholderText("IP Address")
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.horizontalLayout.addWidget(self.lineEdit_ip)

        self.lineEdit_port = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_port.setMinimumHeight(30)
        self.lineEdit_port.setPlaceholderText("Port")
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout.addWidget(self.lineEdit_port)

        self.verticalLayout.addWidget(self.frame)

        # Frame para Threads e Start
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)

        self.spinBox = QtWidgets.QSpinBox(self.frame_2)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setMinimumHeight(30)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_2.addWidget(self.spinBox)

        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setMinimumHeight(40)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.verticalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Server"))
        self.pushButton.setText(_translate("MainWindow", "Open DB"))
        self.label.setText(_translate("MainWindow", "Threads"))
        self.pushButton_2.setText(_translate("MainWindow", "Start Server"))
