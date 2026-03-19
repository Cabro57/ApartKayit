# ApartKayıt

Modern ve şık bir arayüze sahip apart rezervasyon ve müşteri takip uygulaması.

## 🚀 Özellikler
- **Apart Yönetimi**: Apart ekleme, kaldırma ve listeleme.
- **Rezervasyon Takibi**: Müşteri giriş-çıkış tarihleri, ücret ve kişi sayısı kaydı.
- **Filtreleme**: Bugünün, geçmişin veya tüm rezervasyonların görüntülenmesi.
- **Modern Arayüz**: `qt-material` ile desteklenen mavi/beyaz tema.
- **Veritabanı**: SQLite3 tabanlı yerel veri depolama.

## 🛠️ Kurulum

Projeyi çalıştırmak için öncelikle bir sanal ortam oluşturun ve gerekli paketleri yükleyin:

1. **Sanal Ortam Oluşturma (Opsiyonel):**
   ```bash
   python -m venv .venv
   ```

2. **Bağımlılıkları Yükleme:**
   ```bash
   .\.venv\Scripts\pip install -r requirements.txt
   ```

## 🎮 Çalıştırma

Uygulamayı başlatmak için ana dizinde şu komutu çalıştırın:
```bash
.\.venv\Scripts\python main.py
```

## 📦 Gereksinimler
- Python 3.8+
- PyQt5
- qt-material==2.14
