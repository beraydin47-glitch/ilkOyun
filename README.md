# ilkOyun — Yılan

pygame ile yazılmış, dokunmatik ekran ve klavye destekli yılan oyunu.

## Kontroller
- **Dokunmatik:** parmağını kaydırarak yön ver, ekrana dokunarak başlat / duraklat / yeniden başlat
- **Klavye:** yön tuşları veya WASD, `Enter`/`Boşluk`/`P` = başlat/duraklat, `ESC` = çıkış

Her 4 yemde yılan hızlanır. En yüksek puan `rekor.txt` dosyasına kaydedilir.

## Android'de çalıştırma

### Kolay yol: Pydroid 3
`main.py` dosyasını Pydroid 3'te aç ve ▶ düğmesine bas. pygame uygulamayla birlikte geliyor.

### Termux
```bash
pkg update && pkg upgrade -y
pkg install x11-repo -y
pkg install python python-numpy python-pygame termux-x11-nightly git -y
git clone https://github.com/beraydin47-glitch/ilkOyun.git
cd ilkOyun
```
Termux:X11 uygulamasını da kur (F-Droid / GitHub). Sonra:
```bash
termux-x11 :0 &
DISPLAY=:0 python main.py
```
ve Termux:X11 uygulamasını aç.

## Bilgisayarda
```bash
pip install pygame numpy
python main.py
```
numpy isteğe bağlıdır; yalnızca ses efektleri için kullanılır.
