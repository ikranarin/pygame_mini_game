import pygame
import random
import math
import time

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Python Platformer - Gelişmiş Görseller")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
font_buyuk = pygame.font.SysFont("Arial", 72, bold=True)

# --- RENKLER ---
RENK_GOKYUZU = (10, 10, 30)  # Koyu Gece Mavisi
RENK_PLATFORM = (60, 60, 70)  # Koyu Gri
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 50, 50)
RENK_VUCUT = (50, 150, 255)  # Canlı Mavi
RENK_GOZ = (255, 255, 255)
RENK_BACAK = (200, 200, 200)  # Açık Gri/Beyazımsı bacaklar
RENK_YILDIZ = (255, 255, 200)  # Hafif Sarımsı Beyaz
RENK_BULUT = (100, 100, 120, 150)  # Şeffaf Gri-Mavi

# --- ARKA PLAN NESNELERİ ---
yildizlar = []
for _ in range(50):
    yildizlar.append([random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK), random.random() + 0.5])

bulutlar = []
for _ in range(5):
    bulutlar.append(
        [random.randint(0, GENISLIK), random.randint(50, 250), random.randint(100, 200), random.random() * 0.5 + 0.1])


def oyunu_sifirla():
    global oyuncu_rect, hiz_y, ziplama_hakki, can, puan, oyun_bitti, hasar_suresi, anim_sayaci, bakis_yonu, max_can
    oyuncu_rect = pygame.Rect(100, 450, 40, 50)  # Karakter boyutu
    hiz_y = 0
    ziplama_hakki = 2
    max_can = 3
    can = 3
    puan = 0
    hasar_suresi = 0
    oyun_bitti = False
    anim_sayaci = 0
    bakis_yonu = 1
    yeni_konum(altin_rect)
    yeni_konum(dusman_rect)


def yeni_konum(rect):
    rect.x = random.randint(50, 750)
    rect.y = random.randint(50, 400)


altin_rect = pygame.Rect(0, 0, 25, 25)
dusman_rect = pygame.Rect(0, 0, 30, 30)
platformlar = [
    pygame.Rect(0, 560, 800, 40),
    pygame.Rect(200, 420, 200, 25),
    pygame.Rect(450, 300, 200, 25),
    pygame.Rect(150, 180, 180, 25),
]

oyunu_sifirla()

calisiyor = True
tus_basili = False

while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    if not oyun_bitti:
        tuslar = pygame.key.get_pressed()
        eski_x = oyuncu_rect.x
        kosuyor_mu = False

        if tuslar[pygame.K_LEFT]:
            oyuncu_rect.x -= 7
            bakis_yonu = -1
            kosuyor_mu = True
        if tuslar[pygame.K_RIGHT]:
            oyuncu_rect.x += 7
            bakis_yonu = 1
            kosuyor_mu = True

        for p in platformlar:
            if oyuncu_rect.colliderect(p): oyuncu_rect.x = eski_x

        if tuslar[pygame.K_SPACE]:
            if not tus_basili and ziplama_hakki > 0:
                hiz_y = -16
                ziplama_hakki -= 1
                tus_basili = True
        else:
            tus_basili = False

        hiz_y += 0.8
        oyuncu_rect.y += hiz_y

        yerde_mi = False
        for p in platformlar:
            if oyuncu_rect.colliderect(p):
                if hiz_y > 0:
                    oyuncu_rect.bottom = p.top
                    hiz_y = 0
                    ziplama_hakki = 2
                    yerde_mi = True
                elif hiz_y < 0:
                    oyuncu_rect.top = p.bottom
                    hiz_y = 0

        # Animasyon Sayacı Güncelleme (Koşma ve Yerde Olma Kontrolü)
        if kosuyor_mu and yerde_mi:
            anim_sayaci += 1
        elif not yerde_mi:
            anim_sayaci = 0  # Havadayken sabit dur (veya zıplama pozu)
        else:
            anim_sayaci = 0  # Dururken sabit dur

        if oyuncu_rect.colliderect(altin_rect):
            puan += 1
            yeni_konum(altin_rect)

        if hasar_suresi > 0: hasar_suresi -= 1

        if oyuncu_rect.colliderect(dusman_rect) and hasar_suresi == 0:
            can -= 1
            hasar_suresi = 60
            yeni_konum(dusman_rect)
            if can <= 0: oyun_bitti = True

    else:
        # Menü Mantığı
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_r]: oyunu_sifirla()
        if tuslar[pygame.K_q]: calisiyor = False

    # --- ÇİZİM VE GÖRSEL EFEKTLER ---
    ekran.fill(RENK_GOKYUZU)  # Koyu Gökyüzü

    # 1. Arka Plan Nesnelerini Çiz (Dinamik)
    # Yıldızlar (Yavaş Parıltı)
    for yildiz in yildizlar:
        parilti = math.sin(time.time() * 2 + yildiz[0]) * 0.5 + 0.5  # Basit parıltı efekti
        boyut = int(yildiz[2] * parilti + 1)
        pygame.draw.circle(ekran, RENK_YILDIZ, (yildiz[0], yildiz[1]), boyut)

    # Bulutlar (Yavaş Hareket)
    for bulut in bulutlar:
        bulut[0] += bulut[3]  # Hareket
        if bulut[0] > GENISLIK + bulut[2]: bulut[0] = -bulut[2]  # Ekranda sonsuz döngü

        # Basit elips bulut
        pygame.draw.ellipse(ekran, RENK_BULUT, (bulut[0], bulut[1], bulut[2], bulut[2] // 2))

    if not oyun_bitti:
        # Platformlar
        for p in platformlar:
            pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=5)

        # --- KARAKTER ÇİZİMİ (BACAKLI) ---
        if hasar_suresi % 10 < 5:
            # Koşma animasyonu efekti (Vücudun y ekseninde hafifçe oynaması)
            anim_offset = 0
            if anim_sayaci % 20 < 10: anim_offset = 2

            # Vücut (Mavi Dikdörtgen)
            vucut_rect = pygame.Rect(oyuncu_rect.x, oyuncu_rect.y + anim_offset, 40, 50 - anim_offset)
            pygame.draw.rect(ekran, RENK_VUCUT, vucut_rect, border_radius=10)

            # Göz
            goz_x = oyuncu_rect.x + 25 if bakis_yonu == 1 else oyuncu_rect.x + 5
            goz_y = oyuncu_rect.y + 15 + anim_offset
            pygame.draw.circle(ekran, RENK_GOZ, (goz_x, goz_y), 5)
            pygame.draw.circle(ekran, (0, 0, 0), (goz_x + (bakis_yonu * 2), goz_y), 2)  # Göz bebeği

            # --- BACAKLAR (HAREKETLİ) ---
            ayak_y = oyuncu_rect.bottom
            ayak_sol_x = oyuncu_rect.x + 10
            ayak_sag_x = oyuncu_rect.x + 30

            # Basit koşma animasyonu (Bacakların aşağı-yukarı oynaması)
            if anim_sayaci % 20 < 10:
                # Sol bacak aşağıda, sağ bacak yukarıda
                pygame.draw.line(ekran, RENK_BACAK, (ayak_sol_x, ayak_y), (ayak_sol_x, ayak_y + 8), 4)
                pygame.draw.line(ekran, RENK_BACAK, (ayak_sag_x, ayak_y - 3), (ayak_sag_x, ayak_y + 5), 4)
            else:
                # Sol bacak yukarıda, sağ bacak aşağıda
                pygame.draw.line(ekran, RENK_BACAK, (ayak_sol_x, ayak_y - 3), (ayak_sol_x, ayak_y + 5), 4)
                pygame.draw.line(ekran, RENK_BACAK, (ayak_sag_x, ayak_y), (ayak_sag_x, ayak_y + 8), 4)

        # Diğer Nesneler ve Can Barı
        pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)
        pygame.draw.rect(ekran, RENK_DUSMAN, dusman_rect, border_radius=15)

        # Can Barı
        bar_genislik, bar_yukseklik = 150, 20
        x_konum, y_konum = 20, 50
        pygame.draw.rect(ekran, (60, 60, 60), (x_konum, y_konum, bar_genislik, bar_yukseklik), border_radius=5)
        guncel_genislik = (can / max_can) * bar_genislik
        bar_rengi = (255, 50, 50) if can == 1 else (50, 255, 50)
        pygame.draw.rect(ekran, bar_rengi, (x_konum, y_konum, guncel_genislik, bar_yukseklik), border_radius=5)
        pygame.draw.rect(ekran, (200, 200, 200), (x_konum, y_konum, bar_genislik, bar_yukseklik), 2, border_radius=5)

        ekran.blit(font.render(f"Puan: {puan}", True, (255, 255, 255)), (20, 15))

    else:
        # Menü Ekranı (Eski kodla aynı, sadece arka plan farklı)
        pygame.draw.rect(ekran, (20, 20, 25), (150, 150, 500, 300), border_radius=20)
        ekran.blit(font_buyuk.render("OYUN BİTTİ", True, (255, 50, 50)), (210, 200))
        ekran.blit(font.render(f"Toplam Puan: {puan}", True, (255, 255, 255)), (320, 300))
        ekran.blit(font.render("Yeniden Başlamak için 'R' | Çıkış için 'Q'", True, (0, 255, 128)), (220, 360))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()