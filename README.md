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
*   **Akıllı Arayüz:**
    *   Sayfalar arası otomatik geçiş (Carousel)
    *   İsteğe bağlı buton ile manuel geçiş
    *   Crafty API'ye erişilemezse otomatik olarak sadece sistem moduna geçer
    *   Sadece sistem istatistiklerini gösterme modu (`--stats-only` veya konfigürasyon ile)

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

## ▶️ Çalıştırma

```bash
python3 app.py
```

Eğer buton kullanıyorsanız ve pini değiştirdiyseniz:
```bash
python3 app.py --button-pin 4
```

Sadece sistem istatistiklerini görmek isterseniz (Crafty sunucularını gizle):
```bash
python3 app.py --stats-only
```

## 🤖 Otomatik Başlatma (Systemd Servisi)

Raspberry Pi açıldığında programın otomatik çalışması için:

1. Servis dosyasını oluşturun:
```bash
sudo nano /etc/systemd/system/oled-display.service
```

2. Aşağıdaki içeriği yapıştırın (Dosya yollarını kendi kullanıcı adınıza göre düzenleyin, genelde `pi` veya `emirk`):

```ini
[Unit]
Description=OLED Info Display Service
After=network.target

[Service]
Type=simple
User=emirk
WorkingDirectory=/home/emirk/RaspberryPi_Info_Display
ExecStart=/home/emirk/RaspberryPi_Info_Display/.venv/bin/python3 app.py
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
