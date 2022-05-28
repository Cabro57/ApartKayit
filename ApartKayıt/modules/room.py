import sqlite3


class Room():
    def __init__(self):
        self.baglanti_olustur()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("storage/apartkayıt.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("Create Table if not exists odalar (isim TEXT, kazanç INT)")
        self.baglanti.commit()

    def baglanti_kes(self):
        self.baglanti.close()

    # Girilen değer isminde oda oluşturur
    def create(self, room):
        self.cursor.execute("Insert into odalar Values(?,?)", (room, 0))
        self.baglanti.commit()

    # Girilen değeri varsa siler
    def remove(self, room):
        #listr = room.split(" ")
        #self.cursor.execute("Delete From odalar where rowid = ?", (listr[0],))
        self.cursor.execute("Delete From odalar where rowid = ?", (room,))
        self.baglanti.commit()

    # Tüm odaları döndürür (Tüm değerleriyle beraber)
    def printed(self):
        self.cursor.execute("Select * From odalar")
        odalar = self.cursor.fetchall()
        if len(odalar) == 0:
            return []
        else:
            alist = []
            for i in odalar:
                alist.append("{} - {}TL".format(i[0],i[1]))
            return alist

    # Kullanım dışı
    def earn_prnd(self):
        self.cursor.execute("Select * From odalar")
        odalar = self.cursor.fetchall()
        if len(odalar) == 0:
            return []
        else:
            alist = []
            for i in odalar:
                d = "{}TL".format(i[1])
                alist.append(d)
            return alist


    # Girilen değere karşılık oda olup olmadığını döndürür
    def query(self, room):
        room = room.lower().capitalize()
        self.cursor.execute("Select * From odalar where isim= ?", (room,))
        odalar = self.cursor.fetchall()
        if len(odalar) == 0:
            return False

        else:
            return True

    # Tüm odaların toplam kazancını döndürür
    def calculate(self):
        total = 0
        self.cursor.execute("Select * From odalar")
        odalar = self.cursor.fetchall()
        if len(odalar) == 0:
            return "Kayıtlı oda bulunmuyor"
        else:
            for earn in odalar:
                total +=earn[1]
                #print("{} - {}TL".format(earn[0],earn[1]))
            return total

    # Tüm odaların veya bir odanın kazançlarını sıfırlar
    def reset(self, param):
        if param == "All" or param == "tüm" or param == "hepsi":
            self.cursor.execute("Update odalar set kazanç= ?", (0,))
            self.baglanti.commit()
        else:
            self.cursor.execute("Update odalar set kazanç= ? where rowid= ?", (0, param))
            self.baglanti.commit()
