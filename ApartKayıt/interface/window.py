from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QToolButton, QComboBox, QListWidget, QPushButton, QWidget
from PyQt5.QtWidgets import QGroupBox

from modules import reservation


class Pencere(QWidget):

    def __init__(self):
        super().__init__()

        self.setupUi()
        self.apart()

    def setupUi(self):
        self.setWindowTitle("ApartKayıt")
        self.resize(800, 600)
        v_box = QVBoxLayout()
        h_box_ust = QHBoxLayout()
        h_box_alt = QHBoxLayout()

        self.comboBox_2 = QComboBox()
        self.comboBox_2.addItem("Bugün")
        self.comboBox_2.addItem("Geçmiş")
        self.comboBox_2.addItem("Tümü")
        h_box_ust.addWidget(self.comboBox_2)

        self.toolButton = QToolButton()
        h_box_ust.addWidget(self.toolButton)

        v_box.addLayout(h_box_ust)

        self.listWidget = QListWidget()
        v_box.addWidget(self.listWidget)

        self.pushButton = QPushButton()
        h_box_alt.addWidget(self.pushButton)
        self.pushButton.setText("Sil")

        self.pushButton_2 = QPushButton()
        h_box_alt.addWidget(self.pushButton_2)
        self.pushButton_2.setText("Yenile")

        # Rezervasyon Kayıt
        self.groupBox = QGroupBox()

        v_box.addLayout(h_box_alt)

        self.setLayout(v_box)

    def apart(self):

        apartList = reservation.Reservation().printed()
        self.listWidget.addItems(apartList)

