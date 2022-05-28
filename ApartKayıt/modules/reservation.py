import sqlite3
import random
from modules import date


class Reservation():

    def __init__(self):
        self.baglanti_olustur()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("storage/apartkayıt.db")
        self.cursor = self.baglanti.cursor()
        sorgu = "Create Table if not exists rezervasyon (_id INT, kisi TEXT, giris INT, cikis INT, apart TEXT, " \
                "durum Text, kisi_sayisi INT, ucret INT) "
        self.cursor.execute(sorgu)
        self.baglanti.commit()

    def baglanti_kes(self):
        self.baglanti.close()

    # _id'yi farklı bir _id ile çakıştırmadan oluşturur.
    def _id(self):
        self.cursor.execute("Select * From rezervasyon")
        reser = self.cursor.fetchall()
        if len(reser) == 0:
            _id = random.randint(1000, 9999)
            return _id
        else:
            while True:
                _id = random.randint(1000, 9999)
                self.cursor.execute("Select * From rezervasyon where _id= ?", (_id,))
                reser = self.cursor.fetchall()
                if len(reser) == 0:
                    return _id
                else:
                    pass

    # Girilen değerleri tabloya ekler
    def create(self, kisi, giris, cikis, apart, durum, kisi_sayisi, ucret):
        _id = Reservation()._id()
        self.cursor.execute("Insert into rezervasyon Values(?,?,?,?,?,?,?,?)",
                            (_id, kisi, giris, cikis, apart, durum, kisi_sayisi, ucret))
        self.baglanti.commit()
        return "{} adlı kişinin rezervasyon kaydı yapıldı.".format(kisi)

    def update(self, _id, kisi, giris, cikis, apart, durum, kisi_sayisi, ucret):
        ress_update = "Update rezervasyon set kisi=?, giris=?, cikis=?,apart=?, durum=?, kisi_sayisi=?, ucret=? where _id=?"
        self.cursor.execute(ress_update, (kisi, giris, cikis, apart, durum, kisi_sayisi, ucret, _id))
        self.baglanti.commit()
        return "{} adlı kişinin rezervasyonu güncellendi.".format(kisi)


    # Girilen değerin karşılık geldiği listeyi siler
    def remove(self, param,arg):
        self.cursor.execute("Delete From rezervasyon where _id = ?", (param,))
        self.baglanti.commit()
        param = arg
        return "{} adlı kişinin rezervasyonu kaldırıldı.".format(param)


    # Tablodan silmez fakat işleme sokmaz
    def cancel(self, param):
        pass


    # Tüm tabloyu yazdırır
    def printed(self):
        self.cursor.execute("Select * From rezervasyon")
        rezerv = self.cursor.fetchall()
        if len(rezerv) == 0:
            return []
        else:
            alist = []
            for i in rezerv:
                ret = "{}({})".format(i[1], i[0])
                alist.append(ret)
            return alist


    # Girilen değere karşılık rezervasyon olup olmadığını döndürür
    def query(self, param):
        param = param.lower().capitalize()
        self.cursor.execute("Select * From rezervasyon where kisi= ?", (param,))
        resers = self.cursor.fetchall()
        if len(resers) == 0:
            return "Böyle bir oda bulunmuyor"

        else:
            return "{} - {}TL".format(resers[0][0], resers[0][1])


    # Bugün'e karşılık gelenleri yazdırır
    def today(self):
        self.cursor.execute("Select * From rezervasyon")
        resers = self.cursor.fetchall()
        todays = []
        for i in resers:
            if date.giveDate(i[2],"bool") == True:
                ret = "{}({})".format(i[1], i[0])
                todays.append(ret)
        return todays


    def past(self):
        self.cursor.execute("Select * From rezervasyon")
        resers = self.cursor.fetchall()
        pasts = []
        for i in resers:
            if date.giveDate(i[2],"bool") == False:
                ret = "{}({})".format(i[1], i[0])
                pasts.append(ret)
        return pasts


    # Girilen değer hakkında bilgi verir
    def info(self, arg, param):
        self.cursor.execute("Select * From rezervasyon where _id= ?", (param,))
        info = self.cursor.fetchone()
        if arg == "string":
            return [info[1], date.giveDate(info[2],"string"), date.giveDate(info[3],"string"), info[4], info[5], info[6], info[7], info[0]]
        elif arg == "date":
            return [info[1], date.giveDate(info[2],"date"), date.giveDate(info[3],"date"), info[4], info[5], info[6], info[7], info[0]]