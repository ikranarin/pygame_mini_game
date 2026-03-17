import pygame
import random

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Python Platform Oyunu - Can Sistemi")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
font_buyuk = pygame.font.SysFont("Arial", 64)

# --- RENKLER ---
RENK_ARKA_PLAN = (30, 30, 35)
RENK_OYUNCU = (0, 255, 128)
RENK_PLATFORM = (100, 100, 110)
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 50, 50)  # Kırmızı can kaybettiren nesne

# --- OYUNCU AYARLARI ---
oyuncu_rect = pygame.Rect(100, 450, 40, 40)
hiz_x, hiz_y = 6, 0
yercekimi, ziplama_gucu = 0.8, -15
ziplama_hakki = 2
tus_basili = False

# CAN SİSTEMİ
can = 3
hasar_suresi = 0  # Karakter hasar alınca kısa süreliğine dokunulmaz olur
oyun_bitti = False

# --- PLATFORMLAR ---
platformlar = [
    pygame.Rect(0, 560, 800, 40),
    pygame.Rect(200, 420, 200, 25),
    pygame.Rect(450, 300, 200, 25),
    pygame.Rect(150, 180, 180, 25),
]

# --- NESNELER ---
altin_rect = pygame.Rect(random.randint(100, 700), 100, 25, 25)
dusman_rect = pygame.Rect(random.randint(100, 700), 100, 30, 30)
puan = 0


def yeni_konum(rect):
    rect.x = random.randint(50, 750)
    rect.y = random.randint(50, 400)


# --- ANA OYUN DÖNGÜSÜ ---
calisiyor = True
while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    if not oyun_bitti:
        # 2. Girdiler ve Hareket
        tuslar = pygame.key.get_pressed()
        eski_x = oyuncu_rect.x

        if tuslar[pygame.K_LEFT]: oyuncu_rect.x -= hiz_x
        if tuslar[pygame.K_RIGHT]: oyuncu_rect.x += hiz_x

        for p in platformlar:
            if oyuncu_rect.colliderect(p):
                oyuncu_rect.x = eski_x

        if tuslar[pygame.K_SPACE]:
            if not tus_basili and ziplama_hakki > 0:
                hiz_y = ziplama_gucu
                ziplama_hakki -= 1
                tus_basili = True
        else:
            tus_basili = False

        # 3. Fizik
        hiz_y += yercekimi
        oyuncu_rect.y += hiz_y

        for p in platformlar:
            if oyuncu_rect.colliderect(p):
                if hiz_y > 0:
                    oyuncu_rect.bottom = p.top
                    hiz_y = 0
                    ziplama_hakki = 2
                elif hiz_y < 0:
                    oyuncu_rect.top = p.bottom
                    hiz_y = 0

        # Altın Toplama
        if oyuncu_rect.colliderect(altin_rect):
            puan += 1
            yeni_konum(altin_rect)

        # --- DÜŞMAN ÇARPIŞMASI ---
        if hasar_suresi > 0:
            hasar_suresi -= 1  # Dokunulmazlık süresini azalt

        if oyuncu_rect.colliderect(dusman_rect) and hasar_suresi == 0:
            can -= 1
            hasar_suresi = 60  # Yaklaşık 1 saniye dokunulmazlık
            yeni_konum(dusman_rect)
            if can <= 0:
                oyun_bitti = True

    # 4. Çizim İşlemleri
    ekran.fill(RENK_ARKA_PLAN)

    for p in platformlar:
        pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=5)

    # Karakter hasar aldığında yanıp sönsün
    if hasar_suresi % 10 < 5:
        pygame.draw.rect(ekran, RENK_OYUNCU, oyuncu_rect, border_radius=8)

    pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)
    pygame.draw.rect(ekran, RENK_DUSMAN, dusman_rect, border_radius=15)  # Kırmızı Düşman

    # Bilgi Yazıları
    puan_metni = font.render(f"Puan: {puan}", True, (255, 255, 255))
    can_metni = font.render(f"Can: {'❤️' * can}", True, (255, 50, 50))
    ekran.blit(puan_metni, (20, 20))
    ekran.blit(can_metni, (20, 50))

    if oyun_bitti:
        son_metin = font_buyuk.render("OYUN BİTTİ", True, (255, 0, 0))
        ekran.blit(son_metin, (GENISLIK // 2 - 150, YUKSEKLIK // 2 - 50))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()