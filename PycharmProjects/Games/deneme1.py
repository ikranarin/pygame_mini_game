import pygame
import random
import math
import time

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mavi Jöle: Simetrik Bacaklar Edition")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)
font_buyuk = pygame.font.SysFont("Arial", 72, bold=True)

# --- RENKLER ---
RENK_GOKYUZU = (15, 15, 35)
RENK_PLATFORM = (70, 75, 90)
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 60, 60)
RENK_VUCUT = (60, 160, 255)
RENK_GOZ = (255, 255, 255)
RENK_BACAK = (200, 200, 200)
RENK_YILDIZ = (255, 255, 210)
RENK_BULUT = (120, 130, 160, 100)

# --- ARKA PLAN SİSTEMİ ---
yildizlar = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK), random.random()] for _ in range(60)]
bulutlar = [
    [random.randint(0, GENISLIK), random.randint(40, 200), random.randint(120, 220), random.random() * 0.4 + 0.1] for _
    in range(6)]


def oyunu_sifirla():
    global oyuncu_rect, hiz_y, ziplama_hakki, can, puan, oyun_bitti, hasar_suresi, anim_sayaci, bakis_yonu, max_can
    oyuncu_rect = pygame.Rect(100, 450, 40, 50)
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
    rect.y = random.randint(100, 450)


altin_rect = pygame.Rect(0, 0, 25, 25)
dusman_rect = pygame.Rect(0, 0, 35, 35)
platformlar = [
    pygame.Rect(0, 560, 800, 40),
    pygame.Rect(150, 430, 200, 25),
    pygame.Rect(450, 320, 220, 25),
    pygame.Rect(100, 200, 180, 25),
]

oyunu_sifirla()
tus_basili = False
calisiyor = True

while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT: calisiyor = False

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
                hiz_y = -17
                ziplama_hakki -= 1
                tus_basili = True
        else:
            tus_basili = False

        hiz_y += 0.85
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
    ekran.fill(RENK_GOKYUZU)

    # Arka Plan
    for yildiz in yildizlar:
        p = math.sin(time.time() * 2 + yildiz[0]) * 0.5 + 0.5
        pygame.draw.circle(ekran, RENK_YILDIZ, (yildiz[0], yildiz[1]), int(yildiz[2] * 2 * p + 1))
    for b in bulutlar:
        b[0] += b[3]
        if b[0] > GENISLIK + b[2]: b[0] = -b[2]
        pygame.draw.ellipse(ekran, RENK_BULUT, (b[0], b[1], b[2], b[2] // 2))

    if not oyun_bitti:
        for p in platformlar:
            pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=6)

        # Karakter Çizimi
        if hasar_suresi % 10 < 5:
            g, yk = 40, 50
            x_c, y_c = oyuncu_rect.x, oyuncu_rect.y

            # Squash & Stretch
            if not yerde_mi:
                g -= 8;
                yk += 12;
                x_c += 4
            elif kosuyor_mu and anim_sayaci % 20 < 10:
                yk -= 4;
                y_c += 4

            # Vücut ve Göz
            pygame.draw.rect(ekran, RENK_VUCUT, (x_c, y_c, g, yk), border_radius=12)
            gx = x_c + (g * 0.7 if bakis_yonu == 1 else g * 0.1)
            pygame.draw.circle(ekran, RENK_GOZ, (int(gx), int(y_c + yk * 0.3)), 5)
            pygame.draw.circle(ekran, (0, 0, 0), (int(gx + bakis_yonu * 2), int(y_c + yk * 0.3)), 2)

            # --- BACAKLAR (DURURKEN TAM EŞİT, KOŞARKEN SİMETRİK) ---
            ayak_y_temel = y_c + yk
            ayak_sol_x = x_c + 12
            ayak_sag_x = x_c + g - 12

            if yerde_mi:
                if kosuyor_mu:
                    # KOŞARKEN: Sarkaç gibi biri inerken diğeri çıksın
                    sol_offset = 6 if anim_sayaci % 20 < 10 else 0
                    sag_offset = 0 if anim_sayaci % 20 < 10 else 6
                else:
                    # DURURKEN: Her iki bacak da tam eşit ve sabit (4 piksel uzunlukta)
                    sol_offset = 4
                    sag_offset = 4

                # Bacak Çizimleri
                pygame.draw.line(ekran, RENK_BACAK, (ayak_sol_x, ayak_y_temel), (ayak_sol_x, ayak_y_temel + sol_offset),
                                 4)
                pygame.draw.line(ekran, RENK_BACAK, (ayak_sag_x, ayak_y_temel), (ayak_sag_x, ayak_y_temel + sag_offset),
                                 4)
            else:
                # HAVADAYKEN: Bacaklar simetrik katlanır
                pygame.draw.line(ekran, RENK_BACAK, (x_c + 10, ayak_y_temel - 5), (x_c + 15, ayak_y_temel), 4)
                pygame.draw.line(ekran, RENK_BACAK, (x_c + g - 10, ayak_y_temel - 5), (x_c + g - 15, ayak_y_temel), 4)

        # Altın, Düşman ve Can Barı
        pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)
        pygame.draw.rect(ekran, RENK_DUSMAN, dusman_rect, border_radius=12)
        pygame.draw.rect(ekran, (50, 50, 50), (20, 50, 150, 18), border_radius=5)
        bar_w = (can / max_can) * 150
        pygame.draw.rect(ekran, (50, 255, 50) if can > 1 else (255, 50, 50), (20, 50, bar_w, 18), border_radius=5)
        pygame.draw.rect(ekran, (200, 200, 200), (20, 50, 150, 18), 2, border_radius=5)
        ekran.blit(font.render(f"Puan: {puan}", True, (255, 255, 255)), (20, 15))

    else:
        # Menü
        pygame.draw.rect(ekran, (25, 25, 40), (150, 150, 500, 300), border_radius=20)
        ekran.blit(font_buyuk.render("OYUN BİTTİ", True, (255, 60, 60)), (210, 200))
        ekran.blit(font.render(f"Puanın: {puan} | Restart için 'R' | Çıkış için 'Q'", True, (255, 255, 255)),
                   (215, 340))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
