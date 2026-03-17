import pygame
import random

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Python Platform Oyunu")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- RENKLER ---
RENK_ARKA_PLAN = (30, 30, 35)
RENK_OYUNCU = (0, 255, 128)
RENK_PLATFORM = (100, 100, 110)
RENK_ALTIN = (255, 215, 0)

# --- OYUNCU AYARLARI ---
oyuncu_rect = pygame.Rect(100, 450, 40, 40)
hiz_x = 6
hiz_y = 0
yercekimi = 0.8
ziplama_gucu = -15
ziplama_hakki = 2
tus_basili = False

# --- PLATFORMLAR ---
# [x, y, genislik, yukseklik]
platformlar = [
    pygame.Rect(0, 560, 800, 40),  # Yer
    pygame.Rect(200, 420, 200, 25),  # Alt platform
    pygame.Rect(450, 300, 200, 25),  # Orta platform
    pygame.Rect(150, 180, 180, 25),  # Üst platform
]

# --- NESNELER ---
altin_rect = pygame.Rect(random.randint(100, 700), 100, 25, 25)
puan = 0


def yeni_altin_konumu():
    altin_rect.x = random.randint(50, 750)
    altin_rect.y = random.randint(50, 400)


# --- ANA OYUN DÖNGÜSÜ ---
calisiyor = True
while calisiyor:
    # 1. Olay Kontrolü
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    # 2. Girdiler ve Yatay Hareket
    tuslar = pygame.key.get_pressed()
    eski_x = oyuncu_rect.x  # Çarpışma öncesi x konumu

    if tuslar[pygame.K_LEFT]:
        oyuncu_rect.x -= hiz_x
    if tuslar[pygame.K_RIGHT]:
        oyuncu_rect.x += hiz_x

    # YATAY ÇARPIŞMA KONTROLÜ (Platformun yanından geçememe)
    for p in platformlar:
        if oyuncu_rect.colliderect(p):
            if tuslar[pygame.K_LEFT] or tuslar[pygame.K_RIGHT]:
                oyuncu_rect.x = eski_x  # Yan tarafa çarptıysa geri it

    # Zıplama Kontrolü
    if tuslar[pygame.K_SPACE]:
        if not tus_basili and ziplama_hakki > 0:
            hiz_y = ziplama_gucu
            ziplama_hakki -= 1
            tus_basili = True
    else:
        tus_basili = False

    # 3. Fizik ve Dikey Hareket
    hiz_y += yercekimi
    oyuncu_rect.y += hiz_y

    # DİKEY ÇARPIŞMA KONTROLÜ (Yer ve Kafa çarpması)
    for p in platformlar:
        if oyuncu_rect.colliderect(p):
            if hiz_y > 0:  # Düşerken (Ayağı bastı)
                oyuncu_rect.bottom = p.top
                hiz_y = 0
                ziplama_hakki = 2
            elif hiz_y < 0:  # Çıkarken (Kafasını vurdu)
                oyuncu_rect.top = p.bottom
                hiz_y = 0

    # Altın Toplama
    if oyuncu_rect.colliderect(altin_rect):
        puan += 1
        yeni_altin_konumu()

    # 4. Çizim İşlemleri
    ekran.fill(RENK_ARKA_PLAN)

    for p in platformlar:
        pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=5)

    pygame.draw.rect(ekran, RENK_OYUNCU, oyuncu_rect, border_radius=8)
    pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)

    # Bilgi Yazıları
    puan_metni = font.render(f"Puan: {puan}", True, (255, 255, 255))
    ziplama_metni = font.render(f"Zıplama Hakkı: {ziplama_hakki}", True, (200, 200, 200))
    ekran.blit(puan_metni, (20, 20))
    ekran.blit(ziplama_metni, (20, 50))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()