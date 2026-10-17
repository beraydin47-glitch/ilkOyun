"""Yılan oyunu - pygame ile, dokunmatik ekran ve klavye destekli.

Kontroller:
  - Dokunmatik: ekranda parmağını kaydır (yukarı/aşağı/sola/sağa)
  - Klavye: yön tuşları veya WASD, P = duraklat, ESC = çıkış
  - Başlamak / yeniden başlamak için ekrana dokun veya Enter'a bas
"""

import os
import random
import sys

import pygame

# --- Ayarlar ---
SUTUN = 20                # yatayda kaç kare olacak
BASLANGIC_HIZ = 7         # saniyedeki adım sayısı
MAKS_HIZ = 20
KAYDIRMA_ESIK = 30        # piksel; bundan kısa hareket "dokunma" sayılır
REKOR_DOSYASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rekor.txt")

ARKAPLAN = (18, 18, 24)
IZGARA = (28, 28, 36)
YILAN_BAS = (120, 220, 90)
YILAN_GOVDE = (70, 170, 60)
YEM = (230, 70, 70)
YAZI = (235, 235, 235)
SOLUK = (150, 150, 160)

YUKARI, ASAGI, SOL, SAG = (0, -1), (0, 1), (-1, 0), (1, 0)


def android_mi():
    return "ANDROID_ARGUMENT" in os.environ or "ANDROID_ROOT" in os.environ


def rekor_oku():
    try:
        with open(REKOR_DOSYASI) as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        return 0


def rekor_yaz(deger):
    try:
        with open(REKOR_DOSYASI, "w") as f:
            f.write(str(deger))
    except OSError:
        pass


def ses_yap(frekans, sure_ms):
    """numpy varsa kısa bir bip sesi üretir, yoksa None döner."""
    try:
        import numpy as np

        oran, _, kanal = pygame.mixer.get_init()
        t = np.linspace(0, sure_ms / 1000, int(oran * sure_ms / 1000), False)
        dalga = np.sin(2 * np.pi * frekans * t) * np.linspace(1, 0, t.size)
        veri = (dalga * 12000).astype(np.int16)
        if kanal == 2:
            veri = np.column_stack((veri, veri))
        return pygame.sndarray.make_sound(veri)
    except Exception:
        return None


class Oyun:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass

        if android_mi():
            self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.ekran = pygame.display.set_mode((480, 800))
        pygame.display.set_caption("Yılan")

        g, y = self.ekran.get_size()
        self.kare = g // SUTUN
        self.ust_bosluk = max(60, y // 12)
        self.satir = (y - self.ust_bosluk) // self.kare
        self.ox = (g - SUTUN * self.kare) // 2
        self.oy = self.ust_bosluk

        self.font = pygame.font.Font(None, max(32, self.kare * 2))
        self.kucuk_font = pygame.font.Font(None, max(24, int(self.kare * 1.3)))
        self.saat = pygame.time.Clock()

        self.yeme_sesi = ses_yap(880, 80) if pygame.mixer.get_init() else None
        self.olme_sesi = ses_yap(160, 400) if pygame.mixer.get_init() else None

        self.rekor = rekor_oku()
        self.durum = "baslangic"  # baslangic, oyun, duraklat, bitti
        self.sifirla()

    def sifirla(self):
        ortax, ortay = SUTUN // 2, self.satir // 2
        self.yilan = [(ortax, ortay), (ortax - 1, ortay), (ortax - 2, ortay)]
        self.yon = SAG
        self.yon_kuyrugu = []
        self.puan = 0
        self.hiz = BASLANGIC_HIZ
        self.yem_koy()

    def yem_koy(self):
        bos = [(x, y) for x in range(SUTUN) for y in range(self.satir)
               if (x, y) not in self.yilan]
        self.yem = random.choice(bos) if bos else None

    def yon_ver(self, yeni):
        # Aynı adımda birden fazla dönüşü kaybetmemek için kuyrukta tut
        son = self.yon_kuyrugu[-1] if self.yon_kuyrugu else self.yon
        if yeni != son and (yeni[0] + son[0], yeni[1] + son[1]) != (0, 0):
            if len(self.yon_kuyrugu) < 3:
                self.yon_kuyrugu.append(yeni)

    def dokunma(self):
        if self.durum in ("baslangic", "bitti"):
            self.sifirla()
            self.durum = "oyun"
        elif self.durum == "oyun":
            self.durum = "duraklat"
        elif self.durum == "duraklat":
            self.durum = "oyun"

    def olaylar(self):
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                return False
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    return False
                tuslar = {
                    pygame.K_UP: YUKARI, pygame.K_w: YUKARI,
                    pygame.K_DOWN: ASAGI, pygame.K_s: ASAGI,
                    pygame.K_LEFT: SOL, pygame.K_a: SOL,
                    pygame.K_RIGHT: SAG, pygame.K_d: SAG,
                }
                if olay.key in tuslar and self.durum == "oyun":
                    self.yon_ver(tuslar[olay.key])
                elif olay.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_p):
                    self.dokunma()
            elif olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
                self.basla_pos = olay.pos
            elif olay.type == pygame.MOUSEBUTTONUP and olay.button == 1:
                if getattr(self, "basla_pos", None) is None:
                    continue
                dx = olay.pos[0] - self.basla_pos[0]
                dy = olay.pos[1] - self.basla_pos[1]
                self.basla_pos = None
                if max(abs(dx), abs(dy)) < KAYDIRMA_ESIK:
                    self.dokunma()
                elif self.durum == "oyun":
                    if abs(dx) > abs(dy):
                        self.yon_ver(SAG if dx > 0 else SOL)
                    else:
                        self.yon_ver(ASAGI if dy > 0 else YUKARI)
        return True

    def guncelle(self):
        if self.yon_kuyrugu:
            self.yon = self.yon_kuyrugu.pop(0)
        bx, by = self.yilan[0]
        bas = (bx + self.yon[0], by + self.yon[1])

        carpti = not (0 <= bas[0] < SUTUN and 0 <= bas[1] < self.satir)
        # Kuyruğun son karesi bu adımda boşalacağı için sayılmaz
        if bas in self.yilan[:-1]:
            carpti = True
        if carpti:
            self.durum = "bitti"
            if self.olme_sesi:
                self.olme_sesi.play()
            if self.puan > self.rekor:
                self.rekor = self.puan
                rekor_yaz(self.rekor)
            return

        self.yilan.insert(0, bas)
        if bas == self.yem:
            self.puan += 1
            self.hiz = min(MAKS_HIZ, BASLANGIC_HIZ + self.puan // 4)
            if self.yeme_sesi:
                self.yeme_sesi.play()
            self.yem_koy()
            if self.yem is None:  # tüm alan doldu
                self.durum = "bitti"
        else:
            self.yilan.pop()

    def kare_ciz(self, x, y, renk, bosluk=1):
        r = pygame.Rect(self.ox + x * self.kare + bosluk, self.oy + y * self.kare + bosluk,
                        self.kare - 2 * bosluk, self.kare - 2 * bosluk)
        pygame.draw.rect(self.ekran, renk, r, border_radius=self.kare // 4)

    def yazi(self, metin, font, renk, merkez):
        yuzey = font.render(metin, True, renk)
        self.ekran.blit(yuzey, yuzey.get_rect(center=merkez))

    def ciz(self):
        self.ekran.fill(ARKAPLAN)
        alan = pygame.Rect(self.ox, self.oy, SUTUN * self.kare, self.satir * self.kare)
        pygame.draw.rect(self.ekran, IZGARA, alan)

        g = self.ekran.get_width()
        self.yazi(f"Puan: {self.puan}", self.kucuk_font, YAZI, (g // 4, self.ust_bosluk // 2))
        self.yazi(f"Rekor: {self.rekor}", self.kucuk_font, SOLUK, (3 * g // 4, self.ust_bosluk // 2))

        if self.yem:
            self.kare_ciz(*self.yem, YEM, bosluk=2)
        for i, (x, y) in enumerate(self.yilan):
            self.kare_ciz(x, y, YILAN_BAS if i == 0 else YILAN_GOVDE)

        merkez = alan.center
        if self.durum == "baslangic":
            self.yazi("YILAN", self.font, YAZI, (merkez[0], merkez[1] - self.kare * 3))
            self.yazi("Başlamak için dokun", self.kucuk_font, SOLUK, merkez)
            self.yazi("Yön için parmağını kaydır", self.kucuk_font, SOLUK,
                      (merkez[0], merkez[1] + self.kare * 2))
        elif self.durum == "duraklat":
            self.yazi("DURAKLATILDI", self.font, YAZI, merkez)
        elif self.durum == "bitti":
            self.yazi("OYUN BİTTİ", self.font, YEM, (merkez[0], merkez[1] - self.kare * 2))
            self.yazi(f"Puan: {self.puan}", self.kucuk_font, YAZI, merkez)
            self.yazi("Tekrar için dokun", self.kucuk_font, SOLUK,
                      (merkez[0], merkez[1] + self.kare * 2))

        pygame.display.flip()

    def calistir(self):
        birikim = 0.0
        while self.olaylar():
            dt = self.saat.tick(60) / 1000
            if self.durum == "oyun":
                birikim += dt
                adim = 1 / self.hiz
                while birikim >= adim and self.durum == "oyun":
                    birikim -= adim
                    self.guncelle()
            else:
                birikim = 0.0
            self.ciz()
        pygame.quit()


if __name__ == "__main__":
    Oyun().calistir()
    sys.exit()
