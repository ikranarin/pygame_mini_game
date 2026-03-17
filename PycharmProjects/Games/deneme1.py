import pygame
import random

pygame.init()
ekran = pygame.display.set_mode((800, 600))
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# --- DEĞİŞKENLER ---
x, y = 100, 500
hiz_x, hiz_y = 6, 0
yercekimi = 0.8
ziplama_gucu = -14

# ÇİFT ZIPLAMA İÇİN
ziplama_hakki = 2
tus_basili = False  # Sürekli zıplamayı önlemek için

# PLATFORMLAR (Liste olarak tutuyoruz)
# [x, y, genislik, yukseklik]
platformlar = [
    pygame.Rect(0, 550, 800, 50),  # Yer
    pygame.Rect(200, 400, 200, 20),  # Havada 1
    pygame.Rect(450, 250, 200, 20),  # Havada 2
    pygame.Rect(100, 150, 150, 20)  # Havada 3
]

# ALTIN
altin_rect = pygame.Rect(random.randint(100, 700), random.randint(100, 400), 25, 25)
puan = 0

calisiyor = True
while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT: calisiyor = False

    # --- KONTROLLER ---
    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_LEFT]: x -= hiz_x
    if tuslar[pygame.K_RIGHT]: x += hiz_x

    # Çift Zıplama Mantığı
    if tuslar[pygame.K_SPACE]:
        if not tus_basili and ziplama_hakki > 0:
            hiz_y = ziplama_gucu
            ziplama_hakki -= 1
            tus_basili = True
    else:
        tus_basili = False

    # --- FİZİK ---
    hiz_y += yercekimi
    y += hiz_y

    karakter_rect = pygame.Rect(x, y, 40, 40)

    # Platform Çarpışması
    yerde_mi = False
    for p in platformlar:
        if karakter_rect.colliderect(p):
            # Sadece yukarıdan düşerken platformun üstünde durmalı
            if hiz_y > 0:
                y = p.top - 40
                hiz_y = 0
                ziplama_hakki = 2  # Platforma değince zıplama hakkı yenilenir
                yerde_mi = True

    # Altın Toplama
    if karakter_rect.colliderect(altin_rect):
        puan += 1
        altin_rect.x = random.randint(100, 700)
        altin_rect.y = random.randint(100, 400)

    # --- ÇİZİM ---
    ekran.fill((40, 44, 52))  # Modern koyu tema

    for p in platformlar:
        pygame.draw.rect(ekran, (100, 100, 100), p)  # Platformlar gri

    pygame.draw.rect(ekran, (0, 255, 128), karakter_rect)  # Karakter yeşil
    pygame.draw.ellipse(ekran, (255, 215, 0), altin_rect)  # Altın sarı

    puan_yazisi = font.render(f"Puan: {puan} | Ziplama: {ziplama_hakki}", True, (255, 255, 255))
    ekran.blit(puan_yazisi, (20, 20))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()