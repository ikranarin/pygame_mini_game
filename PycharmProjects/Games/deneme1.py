import pygame
import random
import math
import time
import os

# --- AYARLAR ---
GENISLIK, YUKSEKLIK = 800, 600
FPS = 60
SKOR_DOSYASI = "high_score.txt"

# --- RENKLER ---
RENK_GOKYUZU = (10, 10, 30)
RENK_VUCUT = (60, 160, 255)
RENK_ALTIN = (255, 215, 0)
RENK_ALTIN_PARLAK = (255, 255, 150)
RENK_DUSMAN = (255, 60, 60)
RENK_YILDIZ = (255, 255, 210)
RENK_BULUT = (100, 110, 140, 80)

KONFETI_RENKLERI = [(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50), (255, 50, 255), (50, 255, 255),
                    (255, 255, 255)]


# --- PARÇACIK SINIFI ---
class Particle:
    def __init__(self, x, y, renk):
        self.x, self.y = x, y
        self.renk = renk
        aci = random.uniform(0, math.pi * 2)
        hiz = random.uniform(2, 6)
        self.vel_x = math.cos(aci) * hiz
        self.vel_y = math.sin(aci) * hiz
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.size = random.randint(3, 6)
        self.gravity = 0.1

    def update(self):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, ekran):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.renk, alpha), (self.size, self.size), self.size)
            ekran.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class Player:
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        self.rect = pygame.Rect(100, 450, 40, 50)
        self.vel_y = 0
        self.speed = 7
        self.gravity = 0.85
        self.jump_power = -17
        self.jump_count = 2
        self.can = 3
        self.max_can = 3
        self.puan = 0
        self.hasar_suresi = 0
        self.bakis_yonu = 1
        self.anim_sayaci = 0
        self.yerde_mi = False
        self.kosuyor_mu = False

    def handle_input(self):
        tuslar = pygame.key.get_pressed()
        self.kosuyor_mu = False
        if tuslar[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.bakis_yonu = -1
            self.kosuyor_mu = True
        if tuslar[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.bakis_yonu = 1
            self.kosuyor_mu = True

    def jump(self):
        if self.jump_count > 0:
            self.vel_y = self.jump_power
            self.jump_count -= 1

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def draw(self, ekran):
        if self.hasar_suresi % 10 < 5:
            g, yk = 40, 50
            x_c, y_c = self.rect.x, self.rect.y
            if not self.yerde_mi:
                g -= 8;
                yk += 12;
                x_c += 4
            elif self.kosuyor_mu and self.anim_sayaci % 20 < 10:
                yk -= 4;
                y_c += 4

            pygame.draw.rect(ekran, RENK_VUCUT, (x_c, y_c, g, yk), border_radius=12)
            gx = x_c + (g * 0.7 if self.bakis_yonu == 1 else g * 0.1)
            pygame.draw.circle(ekran, (255, 255, 255), (int(gx), int(y_c + yk * 0.3)), 5)
            pygame.draw.circle(ekran, (0, 0, 0), (int(gx + self.bakis_yonu * 2), int(y_c + yk * 0.3)), 2)

            ay_y = y_c + yk
            if self.yerde_mi:
                s_off = (6 if self.anim_sayaci % 20 < 10 else 0) if self.kosuyor_mu else 4
                sa_off = (0 if self.anim_sayaci % 20 < 10 else 6) if self.kosuyor_mu else 4
                pygame.draw.line(ekran, (200, 200, 200), (x_c + 12, ay_y), (x_c + 12, ay_y + s_off), 4)
                pygame.draw.line(ekran, (200, 200, 200), (x_c + g - 12, ay_y), (x_c + g - 12, ay_y + sa_off), 4)
            else:
                pygame.draw.line(ekran, (200, 200, 200), (x_c + 10, ay_y - 5), (x_c + 15, ay_y), 4)
                pygame.draw.line(ekran, (200, 200, 200), (x_c + g - 10, ay_y - 5), (x_c + g - 15, ay_y), 4)


class Game:
    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
        pygame.display.set_caption("Mavi Jöle - Dönen Altınlar")
        self.saat = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.player = Player()
        self.particles = []
        self.yuksek_skor = self.yuksek_skor_yukle()

        self.yildizlar = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK), random.random()] for _ in
                          range(60)]
        self.bulutlar = [[random.randint(0, GENISLIK), random.randint(40, 200), random.randint(120, 220),
                          random.random() * 0.4 + 0.1] for _ in range(6)]

        self.platforms = [pygame.Rect(0, 560, 800, 40), pygame.Rect(150, 430, 200, 25), pygame.Rect(450, 320, 220, 25),
                          pygame.Rect(100, 200, 180, 25)]

        self.altin_rect = pygame.Rect(0, 0, 30, 30)
        self.dusman_rect = pygame.Rect(0, 0, 35, 35)
        self.yeni_konum(self.altin_rect)
        self.yeni_konum(self.dusman_rect)

        self.running = True
        self.game_over = False

    def yuksek_skor_yukle(self):
        if os.path.exists(SKOR_DOSYASI):
            try:
                with open(SKOR_DOSYASI, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def yuksek_skor_kaydet(self):
        with open(SKOR_DOSYASI, "w") as f: f.write(str(self.yuksek_skor))

    def yeni_konum(self, rect):
        gecerli = False
        while not gecerli:
            rect.x, rect.y = random.randint(50, 750), random.randint(100, 450)
            cakisma = any(rect.inflate(40, 40).colliderect(p) for p in self.platforms)
            diger = self.dusman_rect if rect == self.altin_rect else self.altin_rect
            if rect.inflate(100, 100).colliderect(diger): cakisma = True
            if not cakisma: gecerli = True

    def reset(self):
        self.player.reset_stats()
        self.yeni_konum(self.altin_rect)
        self.yeni_konum(self.dusman_rect)
        self.particles = []
        self.game_over = False

    def run(self):
        while self.running:
            t = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_q:
                            self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()

            if not self.game_over:
                self.player.handle_input()
                self.player.apply_gravity()
                self.player.yerde_mi = False
                for p in self.platforms:
                    if self.player.rect.colliderect(p):
                        if self.player.vel_y > 0:
                            self.player.rect.bottom = p.top; self.player.vel_y = 0; self.player.jump_count = 2; self.player.yerde_mi = True
                        elif self.player.vel_y < 0:
                            self.player.rect.top = p.bottom; self.player.vel_y = 0

                if self.player.rect.colliderect(self.altin_rect):
                    self.player.puan += 1
                    for _ in range(20): self.particles.append(
                        Particle(self.altin_rect.centerx, self.altin_rect.centery, random.choice(KONFETI_RENKLERI)))
                    self.yeni_konum(self.altin_rect)

                if self.player.hasar_suresi > 0: self.player.hasar_suresi -= 1
                if self.player.rect.colliderect(self.dusman_rect) and self.player.hasar_suresi == 0:
                    self.player.can -= 1;
                    self.player.hasar_suresi = 60;
                    self.yeni_konum(self.dusman_rect)
                    if self.player.can <= 0:
                        self.game_over = True
                        if self.player.puan > self.yuksek_skor: self.yuksek_skor = self.player.puan; self.yuksek_skor_kaydet()

                if self.player.kosuyor_mu and self.player.yerde_mi: self.player.anim_sayaci += 1
                for p in self.particles[:]:
                    p.update()
                    if p.life <= 0: self.particles.remove(p)

            # --- ÇİZİM ---
            self.ekran.fill(RENK_GOKYUZU)
            # Yıldızlar ve Bulutlar
            for y in self.yildizlar:
                p = math.sin(t * 2 + y[0]) * 0.5 + 0.5
                pygame.draw.circle(self.ekran, RENK_YILDIZ, (y[0], y[1]), int(y[2] * 2 * p + 1))
            for b in self.bulutlar:
                b[0] += b[3]
                if b[0] > GENISLIK + b[2]: b[0] = -b[2]
                pygame.draw.ellipse(self.ekran, RENK_BULUT, (b[0], b[1], b[2], b[2] // 2))

            for p in self.platforms: pygame.draw.rect(self.ekran, (70, 75, 90), p, border_radius=6)

            # --- DÖNEN ALTIN ÇİZİMİ ---
            donme_hizi = t * 5
            genislik_carpan = math.sin(donme_hizi)  # -1 ile 1 arası
            hover_offset = math.sin(t * 3) * 5  # Hafif süzülme

            altin_w = abs(int(self.altin_rect.width * genislik_carpan))
            if altin_w < 2: altin_w = 2  # Görünmez olmasın

            altin_x = self.altin_rect.centerx - altin_w // 2
            altin_y = self.altin_rect.y + hover_offset

            # Altın gövdesi ve parlaması
            pygame.draw.ellipse(self.ekran, RENK_ALTIN, (altin_x, altin_y, altin_w, self.altin_rect.height))
            if altin_w > 10:  # Yeterince genişse iç parlamayı çiz
                pygame.draw.ellipse(self.ekran, RENK_ALTIN_PARLAK,
                                    (altin_x + altin_w // 4, altin_y + 5, altin_w // 2, self.altin_rect.height - 10))

            pygame.draw.rect(self.ekran, RENK_DUSMAN, self.dusman_rect, border_radius=12)
            for p in self.particles: p.draw(self.ekran)
            self.player.draw(self.ekran)

            # UI
            self.ekran.blit(
                self.font.render(f"Puan: {self.player.puan}  |  Rekor: {self.yuksek_skor}", True, (255, 255, 255)),
                (20, 15))
            pygame.draw.rect(self.ekran, (50, 50, 50), (20, 55, 150, 12), border_radius=4)
            pygame.draw.rect(self.ekran, (50, 255, 50) if self.player.can > 1 else (255, 50, 50),
                             (20, 55, (self.player.can / self.player.max_can) * 150, 12), border_radius=4)

            if self.game_over:
                overlay = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA);
                overlay.fill((0, 0, 0, 180));
                self.ekran.blit(overlay, (0, 0))
                text = self.font.render("OYUN BİTTİ - 'R' Restart | 'Q' Quit", True, (255, 255, 255))
                self.ekran.blit(text, text.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2)))

            pygame.display.flip()
            self.saat.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()