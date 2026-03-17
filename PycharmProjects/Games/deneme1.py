import pygame
import random

# --- BAŞLATMA ---
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Python Platformer - Menü Sistemi")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
font_buyuk = pygame.font.SysFont("Arial", 72, bold=True)

# --- RENKLER ---
RENK_ARKA_PLAN = (30, 30, 35)
RENK_OYUNCU = (0, 255, 128)
RENK_PLATFORM = (100, 100, 110)
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 50, 50)


# --- OYUNU SIFIRLAMA FONKSİYONU ---
def oyunu_sifirla():
    global oyuncu_rect, hiz_y, ziplama_hakki, can, puan, oyun_bitti, hasar_suresi
    oyuncu_rect = pygame.Rect(100, 450, 40, 40)
    hiz_y = 0
    ziplama_hakki = 2
    can = 3
    puan = 0
    hasar_suresi = 0
    oyun_bitti = False
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

oyunu_sifirla()  # İlk kez başlatırken sıfırla

# --- ANA DÖNGÜ ---
calisiyor = True
tus_basili = False

while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    if not oyun_bitti:
        # --- OYUN MANTIĞI ---
        tuslar = pygame.key.get_pressed()
        eski_x = oyuncu_rect.x

        if tuslar[pygame.K_LEFT]: oyuncu_rect.x -= 6
        if tuslar[pygame.K_RIGHT]: oyuncu_rect.x += 6

        for p in platformlar:
            if oyuncu_rect.colliderect(p): oyuncu_rect.x = eski_x

        if tuslar[pygame.K_SPACE]:
            if not tus_basili and ziplama_hakki > 0:
                hiz_y = -15
                ziplama_hakki -= 1
                tus_basili = True
        else:
            tus_basili = False

        hiz_y += 0.8
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
        # --- MENÜ MANTIĞI (GAME OVER EKRANI) ---
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_r]:
            oyunu_sifirla()
        if tuslar[pygame.K_q]:
            calisiyor = False

    # --- ÇİZİM ---
    ekran.fill(RENK_ARKA_PLAN)

    if not oyun_bitti:
        for p in platformlar:
            pygame.draw.rect(ekran, RENK_PLATFORM, p, border_radius=5)

        if hasar_suresi % 10 < 5:
            pygame.draw.rect(ekran, RENK_OYUNCU, oyuncu_rect, border_radius=8)

        pygame.draw.ellipse(ekran, RENK_ALTIN, altin_rect)
        pygame.draw.rect(ekran, RENK_DUSMAN, dusman_rect, border_radius=15)

        ekran.blit(font.render(f"Puan: {puan}", True, (255, 255, 255)), (20, 20))
        ekran.blit(font.render(f"Can: {'❤' * can}", True, (255, 50, 50)), (20, 50))
    else:
        # MENÜ EKRANI TASARIMI
        pygame.draw.rect(ekran, (20, 20, 25), (150, 150, 500, 300), border_radius=20)

        msg = font_buyuk.render("OYUN BİTTİ", True, (255, 50, 50))
        puan_msg = font.render(f"Toplam Puan: {puan}", True, (255, 255, 255))
        tekrar_msg = font.render("Yeniden Başlamak için 'R'", True, (0, 255, 128))
        cikis_msg = font.render("Çıkış yapmak için 'Q'", True, (200, 200, 200))

        ekran.blit(msg, (GENISLIK // 2 - 180, 200))
        ekran.blit(puan_msg, (GENISLIK // 2 - 80, 300))
        ekran.blit(tekrar_msg, (GENISLIK // 2 - 140, 360))
        ekran.blit(cikis_msg, (GENISLIK // 2 - 110, 400))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()