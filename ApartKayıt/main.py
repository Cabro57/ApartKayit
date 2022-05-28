import sys, time

from PyQt5.QtCore import Qt
from PySide2 import QtUiTools
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QMessageBox, QDialog, QStatusBar
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QLabel, QLineEdit, QMenu, QFrame, QDateEdit, QSpinBox
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QToolButton, QComboBox, QListWidget, QPushButton, QAction
from PyQt5 import QtGui, QtCore

from qt_material import apply_stylesheet, QtStyleTools

from modules import room  # Oda oluşturma modülü
from modules import customer  # Müşteri kaydetme modülü
from modules import reservation  # Rezervasyon kaydetme modülü
from modules import date  # tarih döndürme modülü

from interface.apart import DialogAdd, DialogRemove, DialogList  # Apart Ekle - Kaldır - Listele

ress = reservation.Reservation()
oda = room.Room()

panel_aktif = "<html><head/><body><h1 align=\"center\"><span style=\" color: #27AE60; font-size: 24px; font-weight: bold;\"> {} </span></h1>" \
              "<p><br/></p>" \
              "<p align=\"center\"><span style=\" font-size:12pt; color:#000000; font-weight: bold; color: #27AE60;\">Giriş: </span><span style=\" font-size:12pt; font-weight:400; color:#000000;\"> {}</span></p>" \
              "<p align=\"center\"><span style=\" font-size:12pt; color:#000000; font-weight: bold; color: #E74C3C;\">Çıkış: </span><span style=\" font-size:12pt; font-weight:400; color:#000000;\"> {}</span></p>" \
              "<p align=\"center\"><span style=\" font-size:12pt; color:#000000; font-weight: bold; color: #3498DB;\">Yer:</span><span style=\" font-size:12pt; font-weight:400; color:#000000;\"> {} ({} kişi)</span></p>" \
              "<p align=\"center\"><span style=\" font-size:16pt; font-weight:bold; color:#0E6251;\"> {} TL</span></p></body></html>"

panel_deaktif = "<html><head/><body><h1 align=\"center\"><span style=\" color: #E74C3C; font-size: 24px; font-weight: bold;\">{}</span></h1>" \
                "<p><br/></p>" \
                "<p align=\"center\"><span style=\" font-size:12pt; color:#000000; font-weight: bold; color: #27AE60;\">Giriş: </span><span style=\" font-size:12pt; font-weight:400; color:#000000;\"> {}</span></p>" \
                "<p align=\"center\"><span style=\" font-size:12pt; color:#000000; font-weight: bold; color: #E74C3C;\">Çıkış: </span><span style=\" font-size:12pt; font-weight:400; color:#000000;\"> {}</span></p>" \
                "<p align=\"center\"><span style=\" font-size:12pt; color:#000000; font-weight: bold; color: #3498DB;\">Yer:</span><span style=\" font-size:12pt; font-weight:400; color:#000000;\"> {} ({} kişi)</span></p>" \
                "<p align=\"center\"><span style=\" font-size:16pt; font-weight:bold; color:#0E6251;\"> {} TL</span></p></body></html>"


class Pencere(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setupUI()
        self.cMenu()

    def setupUI(self):
        # Ust Ayarlar
        self.title()
        self.arayuz()

        apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)

        self.show()

    def title(self):
        self.setWindowTitle("ApartKayıt")
        self.setMinimumSize(810, 610)
        self.setMaximumSize(810, 610)
        self.setWindowIcon(QIcon("icon/logo.ico"))

    def arayuz(self):
        widget = QWidget()

        ana_box = QHBoxLayout()
        v_box = QVBoxLayout()
        h_box_ust = QHBoxLayout()
        h_box_alt = QHBoxLayout()

        self.filtre = QComboBox()
        self.filtre.addItem("Tümü")
        self.filtre.addItem("Bugün")
        self.filtre.addItem("Geçmiş")
        self.filtre.currentIndexChanged.connect(self.yenile_button)
        h_box_ust.addWidget(self.filtre)

        self.filter_spacer = QSpacerItem(30, 20, QSizePolicy.Expanding)
        h_box_ust.addItem(self.filter_spacer)

        self.toolButton = QToolButton()
        self.toolButton.setIcon(QtGui.QIcon("icon/enter.ico"))
        self.toolButton.setIconSize(QtCore.QSize(16, 16))
        self.toolButton.clicked.connect(self.ress_prnd)
        self.toolButton.clicked.connect(self.ress_goster)
        self.toolButton.setToolTip("Ekrana yazdır")
        h_box_ust.addWidget(self.toolButton)

        v_box.addLayout(h_box_ust)

        self.listWidget = QListWidget()
        self.yenile_button()
        #self.itemWidget.setCursor(Qt.PointingHandCursor)
        self.listWidget.setStyleSheet("QListWidget {color: yellow;}"
                                      #"QListWidget {background-image: url(icon/listbackround.jpg); show-decoration-selected: 1;}"
                                      #"QListWidget:item:selected {color: white}"
                                      #"QListWidget:item:selected:hover {color: white;}"
                                      "QListWidget:item:hover {color: #2979ff;}"
                                      "QListWidget:item {font-weight: bold;}")
        self.listWidget.currentItemChanged.connect(self.ress_goster)
        v_box.addWidget(self.listWidget)

        self.yenile = QPushButton()
        h_box_alt.addWidget(self.yenile)
        self.yenile.setText("Yenile")
        self.yenile.setCursor(Qt.PointingHandCursor)
        self.yenile.setStyleSheet("QPushButton::hover {background-color : #2979ff; color: white;}")
        self.yenile.clicked.connect(self.yenile_button)

        self.sil = QPushButton()
        h_box_alt.addWidget(self.sil)
        self.sil.clicked.connect(self.sil_button)
        self.sil.setCursor(Qt.PointingHandCursor)
        self.sil.setStyleSheet("QPushButton::hover {background-color : #2979ff; color: white;}"
                               "QPushButton:pressed {top: 2px;;}")
        self.sil.setText("Sil")

        # Rezervasyon Kayıt
        rezer_box = QVBoxLayout()

        self.gosterge = QLabel()
        self.gosterge.setText(
            "<html><head/><body><p align=\"center\"><span style=\" color: #2979ff; font-size: 24px; font-weight: bold;  font-family: \"Brush Script MT\";\">HOŞGELDİN</span></p></body></html>")
        self.gosterge.setMinimumSize(500, 200)
        self.gosterge.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.gosterge.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # -İsim-
        isim_box = QHBoxLayout()
        self.isim_label = QLabel("İsim:")
        isim_box.addWidget(self.isim_label)
        self.isim_line = QLineEdit()
        self.isim_line.setPlaceholderText("Örn: Metehan Özdoğru / Polisci")
        isim_box.addWidget(self.isim_line)

        # -Giriş Tarihi-
        giris_box = QHBoxLayout()
        self.giris_label = QLabel("Giriş Tarihi:")
        giris_box.addWidget(self.giris_label)
        self.giris_date = QDateEdit()
        self.giris_date.setDate(date.today())
        giris_box.addWidget(self.giris_date)

        # -Çıkış Tarihi-
        cikis_box = QHBoxLayout()
        self.cikis_label = QLabel("Çıkış Tarihi:")
        cikis_box.addWidget(self.cikis_label)
        self.cikis_date = QDateEdit()
        self.cikis_date.setDate(date.today())
        cikis_box.addWidget(self.cikis_date)

        # -Ücret-
        ucret_box = QHBoxLayout()
        self.ucret_label = QLabel("Ücret:")
        ucret_box.addWidget(self.ucret_label)
        self.ucret_spin = QSpinBox()
        self.ucret_spin.setMaximum(999999999)
        self.ucret_spin.setSuffix(" TL")
        ucret_box.addWidget(self.ucret_spin)

        # -Kişi Sayısı-
        kisisayi_box = QHBoxLayout()
        self.kisisayi_label = QLabel("Kişi Sayısı:")
        kisisayi_box.addWidget(self.kisisayi_label)
        self.kisisayi_combo = QComboBox()
        amount = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        self.kisisayi_combo.addItems(amount)
        kisisayi_box.addWidget(self.kisisayi_combo)

        # -Durum-
        durum_box = QHBoxLayout()
        self.durum_label = QLabel("Durum:")
        durum_box.addWidget(self.durum_label)
        self.durum_combo = QComboBox()
        self.durum_combo.addItems(["Aktif", "DeAktif"])
        durum_box.addWidget(self.durum_combo)

        # -Apart-
        apart_box = QHBoxLayout()
        self.apart_label = QLabel("Apart:")
        apart_box.addWidget(self.apart_label)
        self.apart_combo = QComboBox()
        apart = oda.printed()
        apart2 = []
        for i in apart:
            i = i.split(" ")
            apart2.append(i[0])
        self.apart_combo.addItems(apart2)
        apart_box.addWidget(self.apart_combo)

        # -Kayıt Butonu-
        kayit_box = QHBoxLayout()
        self.kayit_spacer = QSpacerItem(260, 20, QSizePolicy.Ignored)
        kayit_box.addItem(self.kayit_spacer)
        self.kayit_buton = QPushButton("Kayıt")
        self.kayit_buton.clicked.connect(self.reservation_save)
        self.kayit_buton.setCursor(Qt.PointingHandCursor)
        self.kayit_buton.setStyleSheet("QPushButton::hover {background-color : #2979ff; color: white;}")
        kayit_box.addWidget(self.kayit_buton)

        # -Yatay Çizgi-
        h_line = QFrame()
        h_line.setSizeIncrement(550, 20)
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)

        # -Dikey Çizgi-
        v_line = QFrame()
        v_line.setSizeIncrement(550, 20)
        v_line.setFrameShape(QFrame.VLine)
        v_line.setFrameShadow(QFrame.Sunken)

        rezer_box.addWidget(self.gosterge)
        rezer_box.addWidget(h_line)
        rezer_box.addLayout(isim_box)
        rezer_box.addLayout(giris_box)
        rezer_box.addLayout(cikis_box)
        rezer_box.addLayout(ucret_box)
        rezer_box.addLayout(kisisayi_box)
        rezer_box.addLayout(durum_box)
        rezer_box.addLayout(apart_box)
        rezer_box.addLayout(kayit_box)

        v_box.addLayout(h_box_alt)

        ana_box.addLayout(v_box)
        ana_box.addWidget(v_line)
        ana_box.addLayout(rezer_box)

        widget.setLayout(ana_box)

        self.setCentralWidget(widget)
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)


    def ress_goster(self):
        sel_item = self.listWidget.currentRow()
        if sel_item != -1:
            sel_item = self.listWidget.currentItem().text()
            if sel_item != "Rezervasyon Ekle +":
                bok = sel_item.replace(")", "")
                bok = bok.split("(")
                bok = ress.info("string", bok[1])
                if bok[4] == "Aktif":
                    self.gosterge.setText(panel_aktif.format(bok[0], bok[1], bok[2], bok[3], bok[5], bok[6]))

                elif bok[4] == "DeAktif":
                    self.gosterge.setText(panel_deaktif.format(bok[0], bok[1], bok[2], bok[3], bok[5], bok[6]))
            else:
                self.gosterge.setText(
                    "<html><head/><body><p align=\"center\"><span style=\" color:#2979ff; font-size: 24px; font-weight: bold;  font-family: \"Brush Script MT\";\">Yeni Kayıt</span></p></body></html>")

    def ress_prnd(self):
        sel_item = self.listWidget.currentRow()
        if sel_item != -1:
            sel_item = self.listWidget.currentItem().text()
            if sel_item != "Rezervasyon Ekle +":
                sel_item = sel_item.replace(")", "")
                sel_item = sel_item.split("(")
                sel_item = ress.info("date", sel_item[1])
                self.isim_line.setText(sel_item[0])
                self.giris_date.setDate(sel_item[1])
                self.cikis_date.setDate(sel_item[2])
                self.apart_combo.setCurrentText(sel_item[3])
                self.durum_combo.setCurrentText(sel_item[4])
                self.kisisayi_combo.setCurrentText(str(sel_item[5]))
                self.ucret_spin.setValue(sel_item[6])
                self.kayit_buton.setText("Güncelle")
            else:
                self.isim_line.clear()
                self.giris_date.setDate(date.today())
                self.cikis_date.setDate(date.today())
                self.apart_combo.setCurrentText("Kat-1")
                self.durum_combo.setCurrentText("Aktif")
                self.kisisayi_combo.setCurrentText("1")
                self.ucret_spin.setValue(0)
                self.kayit_buton.setText("Kayıt")

    def reservation_save(self):
        global _id
        if self.kayit_buton.text() == "Kayıt":
            kisi = self.isim_line.text()
            giris = self.giris_date.text()
            day, month, year = giris.split(".")
            giris = date.takeDate(int(day), int(month), int(year))
            cikis = self.cikis_date.text()
            day, month, year = cikis.split(".")
            cikis = date.takeDate(int(day), int(month), int(year))
            ucret = self.ucret_spin.text()
            ucret = ucret.replace(" TL", "")
            kisi_sayi = self.kisisayi_combo.currentText()
            durum = self.durum_combo.currentText()
            apart = self.apart_combo.currentText()

            if date.calculate(giris, cikis) == False:
                self.sorunKutusuGoster("calculate")
            elif kisi == "" or apart == "":
                self.sorunKutusuGoster("isim-apart")
            else:
                # ress.create(kisi, int(giris), int(cikis), apart, durum, int(kisi_sayi), int(ucret))
                self.statusbar.showMessage(
                    ress.create(kisi, int(giris), int(cikis), apart, durum, int(kisi_sayi), int(ucret)), 3000)

        elif self.kayit_buton.text() == "Güncelle":
            sel_item = self.listWidget.currentRow()
            if sel_item != -1:
                sel_item = self.listWidget.currentItem().text()

                if sel_item != "Rezervasyon Ekle +":
                    self.listWidget.takeItem(self.listWidget.currentRow())
                    sel_item = sel_item.replace(")", "")
                    sel_item = sel_item.split("(")
                    _id = sel_item[1]
            kisi = self.isim_line.text()
            giris = self.giris_date.text()
            day, month, year = giris.split(".")
            giris = date.takeDate(int(day), int(month), int(year))
            cikis = self.cikis_date.text()
            day, month, year = cikis.split(".")
            cikis = date.takeDate(int(day), int(month), int(year))
            ucret = self.ucret_spin.text()
            ucret = ucret.replace(" TL", "")
            kisi_sayi = self.kisisayi_combo.currentText()
            durum = self.durum_combo.currentText()
            apart = self.apart_combo.currentText()
            if kisi == "" or apart == "":
                self.sorunKutusuGoster("isim-apart")
            else:
                self.statusbar.showMessage(
                    ress.update(_id, kisi, int(giris), int(cikis), apart, durum, int(kisi_sayi), int(ucret)), 3000)
                self.ress_goster()
        self.yenile_button()

    def yenile_button(self):
        if self.filtre.currentText() == "Bugün":
            if len(ress.today()) == 0:
                self.listWidget.clear()
                self.listWidget.addItem("Rezervasyon Ekle +")
            else:
                self.listWidget.clear()
                self.listWidget.addItems(ress.today())
                self.listWidget.addItem("Rezervasyon Ekle +")
        elif self.filtre.currentText() == "Geçmiş":
            if len(ress.past()) == 0:
                self.listWidget.clear()
                self.listWidget.addItem("Rezervasyon Ekle +")
            else:
                self.listWidget.clear()
                self.listWidget.addItems(ress.past())
                self.listWidget.addItem("Rezervasyon Ekle +")
        elif self.filtre.currentText() == "Tümü":
            if len(ress.printed()) == 0:
                self.listWidget.clear()
                self.listWidget.addItem("Rezervasyon Ekle +")
            else:
                self.listWidget.clear()
                self.listWidget.addItems(ress.printed())
                self.listWidget.addItem("Rezervasyon Ekle +")

    def sil_button(self):
        sel_item = self.listWidget.currentRow()
        if sel_item != -1:
            sel_item = self.listWidget.currentItem().text()

            if sel_item != "Rezervasyon Ekle +":
                self.listWidget.takeItem(self.listWidget.currentRow())
                sel_item = sel_item.replace(")", "")
                sel_item = sel_item.split("(")
                self.statusbar.showMessage(ress.remove(sel_item[1], sel_item[0]), 3000)
                self.yenile_button()
                self.listWidget.setCurrentRow(0)

    def sorunKutusuGoster(self, param):
        if param == "calculate":
            QMessageBox.warning(self, "Hata!", "Giriş tarihi, çıkış tarihinden büyük olamaz.", QMessageBox.Ok)
        if param == "isim-apart":
            QMessageBox.warning(self, "Uyarı!", "İsim veya apart paramatresi girlmemiş.", QMessageBox.Ok)

    def cMenu(self):
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        # Menu: Dosya
        self.dosya = QMenu(self.menuBar)
        self.dosya.setTitle("Dosya")
        self.menuBar.addMenu(self.dosya)
        # Action: Aç
        self.ac = QAction(self.dosya)
        self.ac.setText("Aç")
        self.dosya.addAction(self.ac)
        # Action: Kaydet
        self.kaydet = QAction(self.dosya)
        self.kaydet.setText("Kaydet")
        self.dosya.addAction(self.kaydet)
        # Action: Çıkış
        self.cikis = QAction(self.dosya)
        self.cikis.setText("Çıkış")
        self.dosya.addAction(self.cikis)

        # Menu: Apart
        self.apart = QMenu(self.menuBar)
        self.apart.setTitle("Apart")
        self.menuBar.addMenu(self.apart)
        # Action: Ekle
        self.ekle = QAction(self.apart)
        self.ekle.setText("Ekle")
        self.apart.addAction(self.ekle)
        # Action: Kaldır
        self.kaldir = QAction(self.apart)
        self.kaldir.setText("Kaldır")
        self.apart.addAction(self.kaldir)
        # Action: Listele
        self.listele = QAction(self.apart)
        self.listele.setText("Listele")
        self.apart.addAction(self.listele)

        self.ekle.triggered.connect(self.apart1)
        self.kaldir.triggered.connect(self.apart2)
        self.listele.triggered.connect(self.apart3)

        # Menu: Müşteri
        self.musteri = QMenu(self.menuBar)
        self.musteri.setTitle("Müşteri")
        self.menuBar.addMenu(self.musteri)
        # Action: Ekle
        self.ekle_2 = QAction(self.musteri)
        self.ekle_2.setText("Ekle")
        self.musteri.addAction(self.ekle_2)
        # Action: Kaldır
        self.kaldir_2 = QAction(self.musteri)
        self.kaldir_2.setText("Kaldır")
        self.musteri.addAction(self.kaldir_2)
        # Action: Sorgula
        self.sorgula = QAction(self.musteri)
        self.sorgula.setText("Sorgula")
        self.musteri.addAction(self.sorgula)
        # Action: Listele
        self.listele_2 = QAction(self.musteri)
        self.listele_2.setText("Listele")
        self.musteri.addAction(self.listele_2)

        # Menu: Tema
        self.tema = QMenu(self.menuBar)
        self.tema.setTitle("Tema")
        self.menuBar.addMenu(self.tema)

        # Menu: Yardım
        self.help = QMenu(self.menuBar)
        self.help.setTitle("Yardım")
        self.menuBar.addMenu(self.help)

    def apart1(self):
        dlg = EkleDlg(self)
        dlg.exec()

    def apart2(self):
        dlg = CikarDlg(self)
        dlg.exec()

    def apart3(self):
        dlg = ListeDlg(self)
        dlg.exec()


basarili = "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#00d000;\">Başarılı</span></p></body></html>"
basarisiz = "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#fe4d3d;\">Başarısız</span></p></body></html>"


class EkleDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = DialogAdd()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.ekle_calistir)

    def ekle_calistir(self):
        isim = self.ui.lineEdit.text()
        if isim != "":
            if oda.query(isim) == False:
                oda.create(isim)
                self.ui.label.setText(basarili)
            else:
                self.ui.label.setText(basarisiz)
        else:
            self.ui.label.setText(basarisiz)


class CikarDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = DialogRemove()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.cikar_calistir)

    def cikar_calistir(self):
        isim = self.ui.lineEdit.text()
        if oda.query(isim) == True:
            oda.remove(isim)
            self.ui.label.setText(basarili)
        else:
            self.ui.label.setText(basarisiz)


class ListeDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = DialogList()
        self.ui.setupUi(self)

        self.listele_calistir()
        self.ui.pushButton.clicked.connect(self.earn_reset)

    def listele_calistir(self):
        if len(oda.printed()) == 0:
            self.ui.listWidget.addItem("Sonuç Yok")
        else:
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(oda.printed())
            self.ui.total.setText("Toplam: {}TL".format(oda.calculate()))

    def earn_reset(self):
        sel_item = self.ui.listWidget.currentRow()
        if sel_item == -1:
            self.ui.label.setText(basarisiz)
        else:
            sel_item = self.ui.listWidget.currentItem().text()
            # sel_item = sel_item.split(" ")
            if sel_item == "Sonuç Yok":
                self.ui.label.setText(basarisiz)
            else:
                sel_item = self.ui.listWidget.currentRow()
                oda.reset(sel_item + 1)
                # oda.reset(sel_item[0])
                self.ui.label.setText(basarili)
                self.listele_calistir()


stylesheet = """
            Pencere {
                background-color: #AED6F1 ;
                background-repeat: no-repeat;
                background-position: center;
                }
            """

# Pencere açılış kodu
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(stylesheet)
    pencere = Pencere()
    sys.exit(app.exec_())
