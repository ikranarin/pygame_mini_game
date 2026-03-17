import pygame
import random
import math
import time

# --- AYARLAR ---
GENISLIK, YUKSEKLIK = 800, 600
FPS = 60

# --- RENKLER ---
RENK_GOKYUZU = (15, 15, 35)
RENK_VUCUT = (60, 160, 255)
RENK_ALTIN = (255, 215, 0)
RENK_DUSMAN = (255, 60, 60)
RENK_YILDIZ = (255, 255, 210)
RENK_BULUT = (120, 130, 160, 100)


class Player:
    def __init__(self):
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

            # Squash & Stretch
            if not self.yerde_mi:
                g -= 8;
                yk += 12;
                x_c += 4
            elif self.kosuyor_mu and self.anim_sayaci % 20 < 10:
                yk -= 4;
                y_c += 4

            # Vücut
            pygame.draw.rect(ekran, RENK_VUCUT, (x_c, y_c, g, yk), border_radius=12)
            # Göz
            gx = x_c + (g * 0.7 if self.bakis_yonu == 1 else g * 0.1)
            pygame.draw.circle(ekran, (255, 255, 255), (int(gx), int(y_c + yk * 0.3)), 5)
            pygame.draw.circle(ekran, (0, 0, 0), (int(gx + self.bakis_yonu * 2), int(y_c + yk * 0.3)), 2)

            # Bacaklar (Simetrik Düzeltme Dahil)
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
        pygame.display.set_caption("OOP Platformer - Gelişmiş Görseller")
        self.saat = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.player = Player()

        # Arka Plan Elemanları
        self.yildizlar = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK), random.random()] for _ in
                          range(60)]
        self.bulutlar = [[random.randint(0, GENISLIK), random.randint(40, 200), random.randint(120, 220),
                          random.random() * 0.4 + 0.1] for _ in range(6)]

        self.platforms = [
            pygame.Rect(0, 560, 800, 40),
            pygame.Rect(150, 430, 200, 25),
            pygame.Rect(450, 320, 220, 25),
            pygame.Rect(100, 200, 180, 25)
        ]
        self.altin = pygame.Rect(400, 200, 25, 25)
        self.dusman = pygame.Rect(200, 100, 35, 35)
        self.running = True
        self.game_over = False

    def reset(self):
        self.player = Player()
        self.game_over = False

    def draw_background(self):
        self.ekran.fill(RENK_GOKYUZU)
        # Yıldızlar
        for yildiz in self.yildizlar:
            p = math.sin(time.time() * 2 + yildiz[0]) * 0.5 + 0.5
            pygame.draw.circle(self.ekran, RENK_YILDIZ, (yildiz[0], yildiz[1]), int(yildiz[2] * 2 * p + 1))
        # Bulutlar
        for b in self.bulutlar:
            b[0] += b[3]
            if b[0] > GENISLIK + b[2]: b[0] = -b[2]
            pygame.draw.ellipse(self.ekran, RENK_BULUT, (b[0], b[1], b[2], b[2] // 2))

    def check_collisions(self):
        self.player.yerde_mi = False
        for p in self.platforms:
            if self.player.rect.colliderect(p):
                if self.player.vel_y > 0:
                    self.player.rect.bottom = p.top
                    self.player.vel_y = 0
                    self.player.jump_count = 2
                    self.player.yerde_mi = True
                elif self.player.vel_y < 0:
                    self.player.rect.top = p.bottom
                    self.player.vel_y = 0

        if self.player.rect.colliderect(self.altin):
            self.player.puan += 1
            self.altin.x = random.randint(50, 750)
            self.altin.y = random.randint(100, 450)

        if self.player.hasar_suresi > 0: self.player.hasar_suresi -= 1
        if self.player.rect.colliderect(self.dusman) and self.player.hasar_suresi == 0:
            self.player.can -= 1
            self.player.hasar_suresi = 60
            self.dusman.x = random.randint(50, 750)
            if self.player.can <= 0: self.game_over = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.player.jump()
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()

            if not self.game_over:
                self.player.handle_input()
                self.player.apply_gravity()
                self.check_collisions()
                if self.player.kosuyor_mu and self.player.yerde_mi:
                    self.player.anim_sayaci += 1

            self.draw_background()
            for p in self.platforms: pygame.draw.rect(self.ekran, (70, 75, 90), p, border_radius=6)
            pygame.draw.ellipse(self.ekran, RENK_ALTIN, self.altin)
            pygame.draw.rect(self.ekran, RENK_DUSMAN, self.dusman, border_radius=12)
            self.player.draw(self.ekran)

            # Can Barı ve UI
            pygame.draw.rect(self.ekran, (50, 50, 50), (20, 50, 150, 18), border_radius=5)
            bw = (self.player.can / self.player.max_can) * 150
            pygame.draw.rect(self.ekran, (50, 255, 50) if self.player.can > 1 else (255, 50, 50), (20, 50, bw, 18),
                             border_radius=5)
            self.ekran.blit(self.font.render(f"Puan: {self.player.puan}", True, (255, 255, 255)), (20, 15))

            if self.game_over:
                overlay = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.ekran.blit(overlay, (0, 0))
                self.ekran.blit(self.font.render("GAME OVER - 'R' to Restart", True, (255, 255, 255)), (280, 280))

            pygame.display.flip()
            self.saat.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()