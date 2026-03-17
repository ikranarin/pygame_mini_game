import pygame
import random

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Python Platformer - Can Barı Sistemi")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
font_buyuk = pygame.font.SysFont("Arial", 72, bold=True)

# --- RENKLER ---
RENK_ARKA_PLAN = (30, 30, 35)
RENK_PLATFORM = (100, 100, 110)
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 50, 50)
RENK_VUCUT = (50, 150, 255)
RENK_GOZ = (255, 255, 255)
RENK_CAN_BARI = (50, 255, 50)  # Başlangıçta yeşil


def oyunu_sifirla():
    global oyuncu_rect, hiz_y, ziplama_hakki, can, puan, oyun_bitti, hasar_suresi, anim_sayaci, bakis_yonu, max_can
    oyuncu_rect = pygame.Rect(100, 450, 40, 50)
    hiz_y = 0
    ziplama_hakki = 2
    max_can = 3  # Toplam can kapasitesi
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

        if kosuyor_mu and yerde_mi:
            anim_sayaci += 1
        else:
            anim_sayaci = 0

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
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_r]: oyunu_sifirla()
        if tuslar[pygame.K_q]: calisiyor = False

    # --- ÇİZİM ---
    ekran.fill(RENK_ARKA_PLAN)

    if not oyun_bitti:
        for p in platformlar:
            pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=5)

        # Karakter Çizimi
        if hasar_suresi % 10 < 5:
            anim_offset = 2 if anim_sayaci % 20 < 10 else 0
            vucut = pygame.Rect(oyuncu_rect.x, oyuncu_rect.y + anim_offset, 40, 50 - anim_offset)
            pygame.draw.rect(ekran, RENK_VUCUT, vucut, border_radius=10)
            goz_x = oyuncu_rect.x + 25 if bakis_yonu == 1 else oyuncu_rect.x + 5
            pygame.draw.circle(ekran, RENK_GOZ, (goz_x, oyuncu_rect.y + 15 + anim_offset), 5)

        # --- CAN BARI ÇİZİMİ ---
        bar_genislik = 150
        bar_yukseklik = 20
        x_konum, y_konum = 20, 50

        # 1. Barın Arka Planı (Koyu Gri)
        pygame.draw.rect(ekran, (60, 60, 60), (x_konum, y_konum, bar_genislik, bar_yukseklik), border_radius=5)

        # 2. Can Miktarına Göre Dolgu (Kırmızıdan Yeşile)
        guncel_genislik = (can / max_can) * bar_genislik
        bar_rengi = (255, 50, 50) if can == 1 else (50, 255, 50)
        pygame.draw.rect(ekran, bar_rengi, (x_konum, y_konum, guncel_genislik, bar_yukseklik), border_radius=5)

        # 3. Barın Çerçevesi (Beyaz)
        pygame.draw.rect(ekran, (200, 200, 200), (x_konum, y_konum, bar_genislik, bar_yukseklik), 2, border_radius=5)

        # Yazılar
        ekran.blit(font.render(f"Puan: {puan}", True, (255, 255, 255)), (20, 15))

        pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)
        pygame.draw.rect(ekran, RENK_DUSMAN, dusman_rect, border_radius=15)
    else:
        # Menü Ekranı
        pygame.draw.rect(ekran, (20, 20, 25), (150, 150, 500, 300), border_radius=20)
        ekran.blit(font_buyuk.render("OYUN BİTTİ", True, (255, 50, 50)), (210, 200))
        ekran.blit(font.render(f"Toplam Puan: {puan}", True, (255, 255, 255)), (320, 300))
        ekran.blit(font.render("Yeniden Başlamak için 'R' | Çıkış için 'Q'", True, (0, 255, 128)), (220, 360))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()