İSG MEGA AKADEMİ - APK'ye Hazır Kivy Projesi

Dosyalar:
- main.py: Uygulama kodu
- data.json: Konular, kartlar ve test soruları
- buildozer.spec: APK derleme ayarları

Pydroid3'te test:
1) main.py ve data.json aynı klasörde olsun.
2) Pydroid3 içinde Kivy kurulu olsun.
3) main.py dosyasını çalıştır.

APK derleme:
Linux veya Windows WSL Ubuntu içinde proje klasöründe:
1) sudo apt update
2) sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
3) pip install --user buildozer cython
4) buildozer android debug

APK çıktı dosyası genelde bin/ klasöründe oluşur.
