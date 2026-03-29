import pygame
import random
import math
import time
import os

# --- AYARLAR ---
GENISLIK, YUKSEKLIK = 800, 600
FPS = 60
SKOR_DOSYASI = "high_score.txt"
PARA_DOSYASI = "total_gold.txt"
RENK_KAYIT_DOSYASI = "saved_color.txt"

# --- RENKLER ---
RENK_GOKYUZU = (10, 10, 30)
RENK_GOKYUZU_L2 = (30, 10, 50)
RENK_GOKYUZU_L3 = (10, 40, 40)
RENK_GOKYUZU_L4 = (50, 10, 10)
RENK_VUCUT_VARSAYILAN = (60, 160, 255)
RENK_DUSMAN_VUCUT = (255, 50, 50)
RENK_ALTIN = (255, 215, 0)
RENK_YILDIZ = (255, 255, 210)
RENK_BULUT = (100, 110, 140, 80)
RENK_MERMI = (255, 0, 0)

MARKET_URUNLERI = {
    "1": {"isim": "Yeşil", "renk": (50, 255, 50), "fiyat": 20},
    "2": {"isim": "Mor", "renk": (200, 50, 255), "fiyat": 50},
    "3": {"isim": "Turuncu", "renk": (255, 150, 50), "fiyat": 100}
}


class Bullet:
    def __init__(self, x, y, hedef_x, hedef_y):
        self.rect = pygame.Rect(x, y, 10, 10)
        aci = math.atan2(hedef_y - y, hedef_x - x)
        hiz = 5
        self.dx = math.cos(aci) * hiz
        self.dy = math.sin(aci) * hiz

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, ekran):
        pygame.draw.circle(ekran, RENK_MERMI, self.rect.center, 5)
        pygame.draw.circle(ekran, (255, 255, 255), self.rect.center, 2)


class Particle:
    def __init__(self, x, y, renk):
        self.x, self.y = x, y
        self.renk = renk
        aci = random.uniform(0, math.pi * 2)
        hiz = random.uniform(2, 6)
        self.vel_x, self.vel_y = math.cos(aci) * hiz, math.sin(aci) * hiz
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.size = random.randint(3, 6)

    def update(self):
        self.vel_y += 0.1
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, ekran):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.renk, alpha), (int(self.size), int(self.size)), int(self.size))
            ekran.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class Player:
    def __init__(self):
        self.total_gold = self.dosya_oku(PARA_DOSYASI)
        saved_rgb = self.renk_oku()
        self.current_color = saved_rgb if saved_rgb else RENK_VUCUT_VARSAYILAN
        self.reset_stats()

    def dosya_oku(self, dosya):
        if os.path.exists(dosya):
            with open(dosya, "r") as f:
                try:
                    return int(f.read())
                except:
                    return 0
        return 0

    def renk_oku(self):
        if os.path.exists(RENK_KAYIT_DOSYASI):
            with open(RENK_KAYIT_DOSYASI, "r") as f:
                try:
                    return tuple(map(int, f.read().split(',')))
                except:
                    return None
        return None

    def renk_kaydet(self, rgb):
        with open(RENK_KAYIT_DOSYASI, "w") as f:
            f.write(f"{rgb[0]},{rgb[1]},{rgb[2]}")

    def reset_stats(self):
        self.rect = pygame.Rect(100, 450, 40, 50)
        self.vel_y = 0
        self.speed, self.gravity, self.jump_power = 7, 0.85, -17
        self.jump_count, self.can, self.puan, self.level = 2, 3, 0, 1
        self.hasar_suresi, self.bakis_yonu, self.anim_sayaci = 0, 1, 0
        self.yerde_mi, self.kosuyor_mu = False, False

    def handle_input(self):
        tuslar = pygame.key.get_pressed()
        self.kosuyor_mu = False
        if tuslar[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.bakis_yonu, self.kosuyor_mu = -1, True
        if tuslar[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.bakis_yonu, self.kosuyor_mu = 1, True
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > GENISLIK: self.rect.right = GENISLIK

    def jump(self):
        if self.jump_count > 0:
            self.vel_y = self.jump_power
            self.jump_count -= 1

    def draw(self, ekran):
        if self.hasar_suresi % 10 < 5:
            g, yk = 40, 50
            x_c, y_c = self.rect.x, self.rect.y
            if not self.yerde_mi:
                g -= 8; yk += 12; x_c += 4
            elif self.kosuyor_mu and self.anim_sayaci % 20 < 10:
                yk -= 4; y_c += 4
            pygame.draw.rect(ekran, self.current_color, (x_c, y_c, g, yk), border_radius=12)
            gx = x_c + (g * 0.7 if self.bakis_yonu == 1 else g * 0.1)
            pygame.draw.circle(ekran, (255, 255, 255), (int(gx), int(y_c + yk * 0.3)), 5)
            pygame.draw.circle(ekran, (0, 0, 0), (int(gx + self.bakis_yonu * 2), int(y_c + yk * 0.3)), 2)
            ay_y = y_c + yk
            if self.yerde_mi:
                off1 = (6 if self.anim_sayaci % 20 < 10 else 0) if self.kosuyor_mu else 4
                off2 = (0 if self.anim_sayaci % 20 < 10 else 6) if self.kosuyor_mu else 4
                pygame.draw.line(ekran, (200, 200, 200), (x_c + 12, ay_y), (x_c + 12, ay_y + off1), 4)
                pygame.draw.line(ekran, (200, 200, 200), (x_c + g - 12, ay_y), (x_c + g - 12, ay_y + off2), 4)


class Game:
    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
        pygame.display.set_caption("Mavi Jöle Serüveni")
        self.saat = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.player = Player()
        self.particles, self.bullets, self.state = [], [], "MENU"
        self.yildizlar = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK), random.random()] for _ in
                          range(60)]
        self.bulutlar = [[random.randint(0, GENISLIK), random.randint(40, 200), random.randint(120, 220),
                          random.random() * 0.3 + 0.1] for _ in range(5)]
        self.platforms = []
        self.yeni_level_platformlari()
        self.altin_rect = pygame.Rect(0, 0, 30, 30)
        self.dusman_rect = pygame.Rect(0, 0, 40, 50)
        self.ates_sayaci = 0
        self.dusman_reset()
        self.yeni_konum(self.altin_rect)

    def yeni_level_platformlari(self):
        self.platforms = [pygame.Rect(0, 560, 800, 40)]
        for i in range(4):
            w = random.randint(160, 240)
            self.platforms.append(pygame.Rect(random.randint(50, GENISLIK - w - 50), 150 + (i * 100), w, 25))

    def yeni_konum(self, rect):
        gecerli = False
        while not gecerli:
            rect.x, rect.y = random.randint(50, 750), random.randint(100, 450)
            if not any(rect.inflate(30, 30).colliderect(p) for p in self.platforms): gecerli = True

    def dusman_reset(self):
        l = self.player.level
        self.dx, self.dy = (3, 0) if l == 1 else (6, 0) if l == 2 else (4, 3) if l == 3 else (6, 5)
        self.dyon_x, self.dyon_y = 1, 1
        self.dusman_rect.topleft = (50, 200)
        self.bullets = []

    def draw_bg(self):
        t = time.time()
        c = {1: RENK_GOKYUZU, 2: RENK_GOKYUZU_L2, 3: RENK_GOKYUZU_L3}.get(self.player.level, RENK_GOKYUZU_L4)
        self.ekran.fill(c)
        for s in self.yildizlar:
            p = math.sin(t * 2 + s[0]) * 0.5 + 0.5
            pygame.draw.circle(self.ekran, RENK_YILDIZ, (s[0], s[1]), int(s[2] * 2 * p + 1))
        for b in self.bulutlar:
            b[0] += b[3]
            if b[0] > 800: b[0] = -200
            pygame.draw.ellipse(self.ekran, RENK_BULUT, (b[0], b[1], b[2], b[2] // 2))

    def run(self):
        while True:
            t = time.time()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); return
                if ev.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if ev.key == pygame.K_RETURN: self.state = "PLAYING"
                        if ev.key == pygame.K_m: self.state = "SHOP"
                        if ev.key == pygame.K_q: pygame.quit(); return
                    elif self.state == "SHOP":
                        if ev.key == pygame.K_ESCAPE: self.state = "MENU"
                        for k, v in MARKET_URUNLERI.items():
                            if ev.key == getattr(pygame, f"K_{k}"):
                                if self.player.total_gold >= v["fiyat"]:
                                    self.player.total_gold -= v["fiyat"]
                                    self.player.current_color = v["renk"]
                                    with open(PARA_DOSYASI, "w") as f: f.write(str(self.player.total_gold))
                                    self.player.renk_kaydet(v["renk"])
                    elif self.state == "PLAYING" and ev.key == pygame.K_SPACE:
                        self.player.jump()
                    elif self.state == "GAMEOVER":
                        if ev.key == pygame.K_r: self.player.reset_stats(); self.dusman_reset(); self.state = "PLAYING"
                        if ev.key == pygame.K_q: pygame.quit(); return

            if self.state == "MENU":
                self.draw_bg()
                title = self.big_font.render("JÖLE SERÜVENİ", True, self.player.current_color)
                self.ekran.blit(title, title.get_rect(center=(400, 150)))
                fy = math.sin(t * 3) * 15
                pygame.draw.rect(self.ekran, self.player.current_color, (250, 250 + fy, 80, 100), border_radius=12)
                pygame.draw.rect(self.ekran, RENK_DUSMAN_VUCUT, (470, 250 - fy, 80, 100), border_radius=12)
                st = self.font.render("[ENTER] BAŞLA | [M] MARKET | [Q] ÇIKIŞ", True, (255, 255, 255))
                self.ekran.blit(st, st.get_rect(center=(400, 480)))
                self.ekran.blit(self.font.render(f"Altın: {self.player.total_gold}", True, RENK_ALTIN), (360, 420))

            elif self.state == "SHOP":
                self.ekran.fill((20, 20, 40))
                self.ekran.blit(self.big_font.render("MARKET", True, RENK_ALTIN), (280, 50))
                for i, (k, v) in enumerate(MARKET_URUNLERI.items()):
                    txt = self.font.render(f"{k}. {v['isim']}: {v['fiyat']} Altın", True, v["renk"])
                    self.ekran.blit(txt, (300, 200 + i * 50))
                self.ekran.blit(self.font.render(f"Bakiyen: {self.player.total_gold}", True, (255, 255, 255)),
                                (320, 450))
                self.ekran.blit(self.font.render("[ESC] GERİ", True, (150, 150, 150)), (330, 520))

            elif self.state == "PLAYING":
                self.player.handle_input()
                self.player.vel_y += self.player.gravity
                self.player.rect.y += self.player.vel_y
                self.player.yerde_mi = False
                for p in self.platforms:
                    if self.player.rect.colliderect(p):
                        if self.player.vel_y > 0:
                            self.player.rect.bottom = p.top; self.player.vel_y = 0; self.player.jump_count = 2; self.player.yerde_mi = True
                        elif self.player.vel_y < 0:
                            self.player.rect.top = p.bottom; self.player.vel_y = 0

                if self.player.rect.colliderect(self.altin_rect):
                    self.player.puan += 1;
                    self.player.total_gold += 1
                    with open(PARA_DOSYASI, "w") as f:
                        f.write(str(self.player.total_gold))
                    for _ in range(15): self.particles.append(
                        Particle(self.altin_rect.centerx, self.altin_rect.centery, RENK_ALTIN))
                    self.yeni_konum(self.altin_rect)
                    if self.player.puan % 10 == 0: self.player.level += 1; self.yeni_level_platformlari(); self.dusman_reset()

                # Düşman Hareketi
                self.dusman_rect.x += self.dx * self.dyon_x
                if self.player.level >= 3: self.dusman_rect.y += self.dy * self.dyon_y
                if self.dusman_rect.right > 800 or self.dusman_rect.left < 0: self.dyon_x *= -1
                if self.player.level >= 3 and (
                        self.dusman_rect.bottom > 600 or self.dusman_rect.top < 0): self.dyon_y *= -1
                for p in self.platforms:
                    if self.dusman_rect.colliderect(p):
                        self.dyon_x *= -1;
                        self.dusman_rect.x += self.dyon_x * 10
                        if self.player.level >= 3: self.dyon_y = random.choice([1, -1])

                # Seviye 6+ Ateş Etme
                if self.player.level >= 6:
                    self.ates_sayaci += 1
                    if self.ates_sayaci >= 90:
                        self.bullets.append(
                            Bullet(self.dusman_rect.centerx, self.dusman_rect.centery, self.player.rect.centerx,
                                   self.player.rect.centery))
                        self.ates_sayaci = 0

                # Mermi Kontrolü & HASAR MANTIĞI
                for b in self.bullets[:]:
                    b.update()
                    if b.rect.colliderect(self.player.rect) and self.player.hasar_suresi == 0:
                        self.player.can -= 1;
                        self.player.hasar_suresi = 60
                        self.bullets.remove(b)
                        if self.player.can <= 0: self.state = "GAMEOVER"  # ÖLÜM KONTROLÜ EKLENDİ
                    elif not self.ekran.get_rect().colliderect(b.rect) or any(
                            b.rect.colliderect(p) for p in self.platforms):
                        try:
                            self.bullets.remove(b)
                        except:
                            pass

                # Canavar Çarpışma Hasarı
                if self.player.rect.colliderect(self.dusman_rect) and self.player.hasar_suresi == 0:
                    self.player.can -= 1;
                    self.player.hasar_suresi = 60
                    if self.player.can <= 0: self.state = "GAMEOVER"

                if self.player.hasar_suresi > 0: self.player.hasar_suresi -= 1
                self.draw_bg()
                for p in self.platforms: pygame.draw.rect(self.ekran, (70, 75, 90), p, border_radius=6)

                # Dönen Altın
                gw = abs(int(15 * math.sin(t * 5)))
                pygame.draw.ellipse(self.ekran, RENK_ALTIN,
                                    (self.altin_rect.centerx - gw, self.altin_rect.y + math.sin(t * 3) * 5, gw * 2, 30))

                # Düşman Gözleri
                xd, yd = self.dusman_rect.x, self.dusman_rect.y + (math.sin(t * 4) * 3 if self.player.level < 3 else 0)
                pygame.draw.rect(self.ekran, RENK_DUSMAN_VUCUT, (xd, yd, 40, 50), border_radius=12)
                pygame.draw.circle(self.ekran, (255, 255, 255), (int(xd + 12), int(yd + 15)), 6)
                pygame.draw.circle(self.ekran, (255, 255, 255), (int(xd + 28), int(yd + 15)), 6)
                pygame.draw.circle(self.ekran, (0, 0, 0), (int(xd + 12 + self.dyon_x * 2), int(yd + 15)), 3)
                pygame.draw.circle(self.ekran, (0, 0, 0), (int(xd + 28 + self.dyon_x * 2), int(yd + 15)), 3)

                for b in self.bullets: b.draw(self.ekran)
                for part in self.particles[:]:
                    part.update();
                    part.draw(self.ekran)
                    if part.life <= 0: self.particles.remove(part)

                self.player.draw(self.ekran)
                ui_txt = f"Puan: {self.player.puan} | Level: {self.player.level} | Altın: {self.player.total_gold}"
                self.ekran.blit(self.font.render(ui_txt, True, (255, 255, 255)), (20, 20))
                pygame.draw.rect(self.ekran, (50, 250, 50), (20, 55, (self.player.can / 3) * 150, 12), border_radius=4)

                if self.player.hasar_suresi > 0:
                    s = pygame.Surface((800, 600), pygame.SRCALPHA);
                    s.fill((255, 0, 0, self.player.hasar_suresi * 2));
                    self.ekran.blit(s, (0, 0))

            elif self.state == "GAMEOVER":
                self.ekran.fill((30, 0, 0))
                self.ekran.blit(self.big_font.render("OYUN BİTTİ", True, (255, 50, 50)), (240, 200))
                self.ekran.blit(
                    self.font.render(f"Puan: {self.player.puan} | [R] Restart | [Q] Quit", True, (255, 255, 255)),
                    (220, 350))

            pygame.display.flip()
            self.saat.tick(FPS)


if __name__ == "__main__":
    Game().run()