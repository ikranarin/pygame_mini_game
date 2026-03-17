import pygame
import random
import time

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Python Platformer - Yakışıklı Karakter")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
font_buyuk = pygame.font.SysFont("Arial", 72, bold=True)

# --- RENKLER ---
RENK_ARKA_PLAN = (30, 30, 35)
RENK_PLATFORM = (100, 100, 110)
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 50, 50)

# YAKIŞIKLI KARAKTER RENKLERİ
RENK_VUCUT = (50, 150, 255)  # Canlı Mavi
RENK_GÖZ = (255, 255, 255)  # Beyaz


# --- OYUNU SIFIRLAMA FONKSİYONU ---
def oyunu_sifirla():
    global oyuncu_rect, hiz_y, ziplama_hakki, can, puan, oyun_bitti, hasar_suresi, anim_sayaci, bakis_yonu
    oyuncu_rect = pygame.Rect(100, 450, 40, 50)  # Biraz daha uzun bir karakter
    hiz_y = 0
    ziplama_hakki = 2
    can = 3
    puan = 0
    hasar_suresi = 0
    oyun_bitti = False
    anim_sayaci = 0  # Animasyon için kare sayacı
    bakis_yonu = 1  # 1: Sağ, -1: Sol
    yeni_konum(altin_rect)
    yeni_konum(dusman_rect)


def yeni_konum(rect):
    rect.x = random.randint(50, 750)
    rect.y = random.randint(50, 400)


# --- NESNE TANIMLAMALARI ---
altin_rect = pygame.Rect(0, 0, 25, 25)
dusman_rect = pygame.Rect(0, 0, 30, 30)
platformlar = [
    pygame.Rect(0, 560, 800, 40),
    pygame.Rect(200, 420, 200, 25),
    pygame.Rect(450, 300, 200, 25),
    pygame.Rect(150, 180, 180, 25),
]

oyunu_sifirla()

# --- ANA DÖNGÜ ---
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

        # Hareket ve Yön Kontrolü
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

        # Zıplama
        if tuslar[pygame.K_SPACE]:
            if not tus_basili and ziplama_hakki > 0:
                hiz_y = -16
                ziplama_hakki -= 1
                tus_basili = True
        else:
            tus_basili = False

        # Fizik
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

        # Animasyon Sayacı Güncelleme
        if kosuyor_mu and yerde_mi:
            anim_sayaci += 1
        elif not yerde_mi:
            anim_sayaci = 0  # Havadayken sabit dur
        else:
            anim_sayaci = 0  # Dururken sabit dur

        # Çarpışmalar
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

    # --- ÇIZIM VE KARAKTER TASARIMI ---
    ekran.fill(RENK_ARKA_PLAN)

    if not oyun_bitti:
        for p in platformlar:
            pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=5)

        # --- YAKIŞIKLI KARAKTER ÇİZİMİ ---
        if hasar_suresi % 10 < 5:
            # Koşma animasyonu efekti (Vücudun y ekseninde hafifçe oynaması)
            anim_offset = 0
            if anim_sayaci % 20 < 10: anim_offset = 2

            # Vücut (Mavi Dikdörtgen)
            vucut_rect = pygame.Rect(oyuncu_rect.x, oyuncu_rect.y + anim_offset, 40, 50 - anim_offset)
            pygame.draw.rect(ekran, RENK_VUCUT, vucut_rect, border_radius=10)

            # Göz (Baktığı yöne göre konumu değişir)
            goz_x = oyuncu_rect.x + 25 if bakis_yonu == 1 else oyuncu_rect.x + 5
            goz_y = oyuncu_rect.y + 15 + anim_offset
            pygame.draw.circle(ekran, RENK_GÖZ, (goz_x, goz_y), 5)
            # Göz bebeği
            pygame.draw.circle(ekran, (0, 0, 0), (goz_x + (bakis_yonu * 2), goz_y), 2)

            # Ayaklar (Küçük animasyonlu çizgiler)
            ayak_y = oyuncu_rect.bottom
            ayak_sol_x = oyuncu_rect.x + 10
            ayak_sag_x = oyuncu_rect.x + 30

            if anim_sayaci % 20 < 10:
                pygame.draw.line(ekran, (200, 200, 200), (ayak_sol_x, ayak_y), (ayak_sol_x, ayak_y + 8), 4)
                pygame.draw.line(ekran, (200, 200, 200), (ayak_sag_x, ayak_y - 3), (ayak_sag_x, ayak_y + 5), 4)
            else:
                pygame.draw.line(ekran, (200, 200, 200), (ayak_sol_x, ayak_y - 3), (ayak_sol_x, ayak_y + 5), 4)
                pygame.draw.line(ekran, (200, 200, 200), (ayak_sag_x, ayak_y), (ayak_sag_x, ayak_y + 8), 4)

        # Diğer Nesneler ve Yazılar
        pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)
        pygame.draw.rect(ekran, RENK_DUSMAN, dusman_rect, border_radius=15)
        ekran.blit(font.render(f"Puan: {puan}", True, (255, 255, 255)), (20, 20))
        ekran.blit(font.render(f"Can: {'❤' * can}", True, (255, 50, 50)), (20, 50))
    else:
        # Menü Ekranı (Eski kodla aynı)
        pygame.draw.rect(ekran, (20, 20, 25), (150, 150, 500, 300), border_radius=20)
        msg = font_buyuk.render("OYUN BİTTİ", True, (255, 50, 50))
        puan_msg = font.render(f"Toplam Puan: {puan}", True, (255, 255, 255))
        tekrar_msg = font.render("Yeniden Başlamak için 'R'", True, (0, 255, 128))
        ekran.blit(msg, (GENISLIK // 2 - 180, 200))
        ekran.blit(puan_msg, (GENISLIK // 2 - 80, 300))
        ekran.blit(tekrar_msg, (GENISLIK // 2 - 140, 360))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()