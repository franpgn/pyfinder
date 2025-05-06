from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QIcon("../repository/resources/Icon.png"))
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        /* Campos de texto */
        QLineEdit, QDateEdit {
            background-color: #2c2c2c;
            color: #ffffff;
            border: 1px solid #444444;
            border-radius: 6px;
            padding: 6px;
        }

        /* Labels */
        QLabel {
            color: #bbbbbb;
        }

        /* Tabela */
        QTableView {
            background-color: #252525;
            alternate-background-color: #2d2d2d;
            color: #ffffff;
            gridline-color: #444444;
            selection-background-color: #444444;
            selection-color: #ffffff;
            border: none;
        }

        /* Cabeçalho da tabela */
        QHeaderView::section {
            background-color: #333333;
            color: #ffffff;
            padding: 6px;
            border: none;
            font-weight: bold;
        }

        /* Botões */
        QPushButton {
            background-color: #3d7eff;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }

        QPushButton:hover {
            background-color: #629aff;
        }

        QPushButton:pressed {
            background-color: #2c5eff;
        }

        /* Scroll */
        QScrollBar:vertical, QScrollBar:horizontal {
            background: #2c2c2c;
            border: none;
            width: 8px;
            height: 8px;
        }

        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #555555;
            border-radius: 4px;
        }

        /* Menu Bar */
        QMenuBar {
            background-color: #1e1e1e;
        }

        QMenuBar::item {
            background-color: transparent;
            color: #ffffff;
            padding: 4px 10px;
        }

        QMenuBar::item:selected {
            background-color: #333333;
            color: #ffffff;
        }

        /* Menu Dropdown */
        QMenu {
            background-color: #2c2c2c;
            color: #ffffff;
            border: 1px solid #444444;
        }

        QMenu::item:selected {
            background-color: #3d7eff;
            color: #ffffff;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(276, 268))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(16777210, 25))
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.dateEdit = QtWidgets.QDateEdit(self.frame)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate(2025, 1, 1))
        self.verticalLayout_2.addWidget(self.dateEdit)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 267))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 760, 245))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tableView = QtWidgets.QTableView(self.scrollAreaWidgetContents)
        # Criar um layout horizontal para os botões
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.previousButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.previousButton.setText("Previous")
        self.previousButton.setObjectName("previousButton")
        self.buttonLayout.addWidget(self.previousButton)

        # ── NEW: Add label to display current request ID ──
        self.idLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.idLabel.setObjectName("idLabel")
        self.idLabel.setText("")  # start empty
        self.idLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLayout.addWidget(self.idLabel)
        # ─────────────────────────────────────────────────

        self.nextButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.nextButton.setText("Next")
        self.nextButton.setObjectName("nextButton")
        self.buttonLayout.addWidget(self.nextButton)

        # Adicionar o layout de botões no verticalLayout_4 (embaixo da tabela)
        self.verticalLayout_4.addLayout(self.buttonLayout)

        self.tableView.setObjectName("tableView")
        self.tableView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addWidget(self.tableView)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.actionAdd_IP = QtWidgets.QAction(MainWindow)
        self.actionAdd_IP.setMenuRole(QtWidgets.QAction.NoRole)
        self.actionAdd_IP.setObjectName("actionAdd_IP")
        self.menufile.addAction(self.actionAdd_IP)
        self.menubar.addAction(self.menufile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client"))
        self.label.setText(_translate("MainWindow", "CPF"))
        self.label_2.setText(_translate("MainWindow", "Name"))
        self.label_3.setText(_translate("MainWindow", "Birth Date"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.actionAdd_IP.setText(_translate("MainWindow", "Add IP"))