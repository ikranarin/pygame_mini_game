import pygame

# 1. Başlatma
pygame.init()
ekran = pygame.display.set_mode((800, 600))
saat = pygame.time.Clock()

# Karakter özellikleri
x, y = 400, 300
hiz = 5

calisiyor = True
while calisiyor:
    # 2. Olay Kontrolü (Girdi)
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    # Tuş kontrolleri
    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_LEFT]: x -= hiz
    if tuslar[pygame.K_RIGHT]: x += hiz
    if tuslar[pygame.K_UP]: y -= hiz
    if tuslar[pygame.K_DOWN]: y += hiz

    # 3. Güncelleme ve Çizim
    ekran.fill((30, 30, 30))  # Arka planı koyu gri yap
    pygame.draw.rect(ekran, (0, 255, 128), (x, y, 50, 50))  # Yeşil kare

    pygame.display.flip()
    saat.tick(60)  # Saniyede 60 kare (FPS)

pygame.quit()