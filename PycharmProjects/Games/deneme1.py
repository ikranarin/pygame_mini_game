import pygame

pygame.init()
ekran = pygame.display.set_mode((800, 600))
saat = pygame.time.Clock()

# Karakter ve Fizik Değişkenleri
x, y = 400, 500  # Başlangıç konumu (Yerde)
hiz_x = 5
hiz_y = 0  # Dikey hız (başlangıçta 0)
yercekimi = 0.8  # Her karede bizi aşağı çeken kuvvet
ziplama_gucu = -16  # Yukarı doğru verilen ilk itme (Y ekseni yukarı (-) yönlüdür)
yerde_mi = True

calisiyor = True
while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    # Girdi Kontrolü
    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_LEFT]: x -= hiz_x
    if tuslar[pygame.K_RIGHT]: x += hiz_x

    # Zıplama Tuşu (Sadece yerdeyken zıplayabilir)
    if tuslar[pygame.K_SPACE] and yerde_mi:
        hiz_y = ziplama_gucu
        yerde_mi = False

    # --- FİZİK HESAPLAMALARI ---
    hiz_y += yercekimi  # Yerçekimi hızı her an artırır (aşağı çeker)
    y += hiz_y  # Karakterin konumu hıza göre değişir

    # Yer Kontrolü (Ekranın altına çarpma)
    if y >= 500:
        y = 500
        hiz_y = 0
        yerde_mi = True

    # Çizim
    ekran.fill((30, 30, 30))
    pygame.draw.rect(ekran, (0, 255, 128), (x, y, 50, 50))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()