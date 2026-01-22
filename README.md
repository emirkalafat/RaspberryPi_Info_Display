# Raspberry Pi OLED Info Display

Bu proje, bir Raspberry Pi'ye bağlı 128x64 OLED ekran üzerinde sistem istatistiklerini (CPU, RAM, Sıcaklık) ve Crafty Controller (Minecraft Sunucu Yönetimi) verilerini görüntüleyen şık bir Python uygulamasıdır.

## 🌟 Özellikler

*   **Sistem Takibi:**
    *   IP Adresi
    *   CPU Kullanımı (%)
    *   RAM Kullanımı (%)
    *   CPU Sıcaklığı
*   **Crafty Controller Entegrasyonu:**
    *   Aktif sunucuları otomatik algılama
    *   Çevrimiçi oyuncu sayısı ve listesi
    *   Sunucu durumu (Açık/Kapalı)
    *   **2FA Limiti:** 2FA etkin hesaplarda otomatik olarak "Public Mode"a geçerek çalışır (Oyuncu isimleri görüntülenmez).
*   **Bilgi Ekranları (Yeni):**
    *   **Tarih & Saat:** Dijital saat, takvim ve gün.
    *   **Hava Durumu:** Anlık sıcaklık, durum (Açık, Yağmurlu vb.) - *Open-Meteo kullanır, API Key gerektirmez.*
    *   **Finans:** Güncel Dolar, Euro ve Altın (Gram) fiyatları.
*   **Akıllı Arayüz:**
    *   Sayfalar arası otomatik geçiş (Carousel)
    *   İsteğe bağlı buton ile manuel geçiş
    *   Crafty API'ye erişilemezse otomatik olarak sadece sistem moduna geçer
    *   Sadece sistem istatistiklerini gösterme modu (`--stats-only` veya konfigürasyon ile)
*   **Yüksek Performans:**
    *   Tüm veri çekme işlemleri (Hava durumu, Borsa, Crafty) arkaplanda (threading) yapılır.
    *   Arayüz ve animasyonlar asla donmaz.

## 📂 Proje Yapısı

*   `run.sh`: Uygulamayı başlatmak için kullanılan ana script.
*   `src/`: Kaynak kodlar.
    *   `app.py`: Ana uygulama.
    *   `ui.py`: Ekran yönetimi.
    *   `services/`: Arkaplan servisleri.
    *   `pages/`: Ekran tasarımları.
*   `config.json`: Kullanıcı ayarları.

## 🛠 Donanım Gereksinimleri

*   Raspberry Pi (Zero, 3, 4, 5 modelleri desteklenir)
*   0.96" I2C OLED Ekran (SSD1306 Sürücülü)
*   4 adet Jumper Kablo (Dişi-Dişi veya Erkek-Dişi)
*   (İsteğe Bağlı) 1 adet Buton (Manuel geçiş için)

### Bağlantı Şeması (I2C)

| OLED Pin | Raspberry Pi GPIO Pin |
|----------|-----------------------|
| VCC      | 3.3V (Pin 1)          |
| GND      | GND (Pin 6)           |
| SCL      | SCL (GPIO 3 / Pin 5)  |
| SDA      | SDA (GPIO 2 / Pin 3)  |

**(İsteğe Bağlı) Buton:** Bir bacağı GPIO 4 (Pin 7), diğer bacağı GND.

## 🚀 Kurulum

### 1. Raspberry Pi I2C Aktivasyonu

Terminali açın ve şu komutu çalıştırın:
```bash
sudo raspi-config
```
`Interface Options` -> `I2C` -> `Yes` seçerek aktifleştirin ve cihazı yeniden başlatın.

### 2. Projeyi İndirme

```bash
cd ~
git clone https://github.com/emirkalafat/RaspberryPi_Info_Display.git
cd RaspberryPi_Info_Display
```

### 3. Sanal Ortam (Önerilen)

Sistem kütüphanelerini karıştırmamak için sanal ortam oluşturun:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Kütüphanelerin Yüklenmesi

```bash
pip install -r requirements.txt
```

## ⚙️ Yapılandırma

Crafty Controller bilgilerinizi girmek için `.env` dosyasını oluşturun:

```bash
nano .env
```

İçeriğini aşağıdaki gibi düzenleyin:

```ini
CRAFTY_URL="https://192.168.1.100:8443"
CRAFTY_USERNAME="admin"
CRAFTY_PASSWORD="sifreniz"
```
*Not: URL'in `https://` ile başladığından emin olun.*

Detaylı yapılandırma seçenekleri (Hava durumu konumu, gösterilecek sayfalar vb.) için [CONFIG.md](CONFIG.md) dosyasına göz atın. `config.json` üzerinden hangi sayfaların gösterileceğini (`enabled_pages`) ayarlayabilirsiniz.

## ▶️ Çalıştırma

### Kolay Başlatma (Önerilen)

`run.sh` scripti, sanal ortamı otomatik kontrol eder ve uygulumayı başlatır.

```bash
chmod +x run.sh
./run.sh
```

### Manuel Parametreler

`run.sh` üzerinden de parametre gönderebilirsiniz:

Eğer buton pini farklıysa:
```bash
./run.sh --button-pin 4
```

Sadece sistem istatistiklerini görmek isterseniz:
```bash
./run.sh --stats-only
```

## 🤖 Otomatik Başlatma (Systemd Servisi)

Raspberry Pi açıldığında programın otomatik çalışması için:

1. Servis dosyasını oluşturun:
```bash
sudo nano /etc/systemd/system/oled-display.service
```

2. Aşağıdaki içeriği yapıştırın (Dosya yollarını kendi kullanıcı adınıza göre düzenleyin, genelde `pi` veya `<kullanıcı_adınız>`):

```ini
[Unit]
Description=OLED Info Display Service
After=network.target

[Service]
Type=simple
User=<kullanıcı_adınız>
WorkingDirectory=/home/<kullanıcı_adınız>/RaspberryPi_Info_Display
ExecStart=/home/<kullanıcı_adınız>/RaspberryPi_Info_Display/run.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Servisi başlatın:
```bash
sudo systemctl daemon-reload
sudo systemctl enable oled-display.service
sudo systemctl start oled-display.service
```

## 🤝 Katkıda Bulunma
Herhangi bir hata bulursanız veya özellik eklemek isterseniz, lütfen bir "Issue" açın veya "Pull Request" gönderin.

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.  
Bu, projeyi dilediğiniz gibi kullanabileceğiniz, değiştirebileceğiniz ve dağıtabileceğiniz anlamına gelir; tek şart, orijinal geliştiriciye atıfta bulunmanızdır.
