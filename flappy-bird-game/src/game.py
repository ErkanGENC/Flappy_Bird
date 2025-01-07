import pygame
import os  
import time
import json
from bird import Bird
from pipe import Pipe
from base import Base
from PIL import Image, ImageSequence  # PIL kütüphanesini ekleyin

class Game:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        
        # Font ayarları
        pygame.font.init()
        self.font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 48)
        
        # Oyun ayarları
        self.bird_speed = 10  # Kuş hızı
        self.game_speed = 30  # Oyun FPS
        
        # Can sistemi
        self.max_lives = 3
        self.lives = self.max_lives
        
        # Kalp resmi
        try:
            heart_image = pygame.image.load("flappy-bird-game/src/assets/images/heart.png")
            self.heart_image = pygame.transform.scale(heart_image, (30, 30))
        except:
            self.heart_image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.polygon(self.heart_image, (255, 0, 0), [
                (15, 5), (20, 0), (25, 5), (30, 10), (15, 25), (0, 10), (5, 5), (10, 0)
            ])
        
        # Animasyonlu arka plan için değişkenler
        self.bg_frames = []
        self.current_frame = 0
        self.frame_delay = 100  # milisaniye cinsinden frame değişim süresi
        self.last_frame_time = time.time() * 1000  # milisaniye cinsinden şimdiki zaman
        
        # Animasyonlu arka planı yükle
        self._load_animated_background()

        self.running = True
        self.in_menu = True
        self.in_settings = False

    def _create_button(self, text, y_position, color=(34, 139, 34)):
        button_width = 200
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_rect = pygame.Rect(button_x, y_position, button_width, button_height)
        
        pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
        button_text = self.menu_font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        
        return button_rect

    def _create_small_button(self, text, x, y, color=(34, 139, 34)):
        button_width = 40
        button_height = 40
        button_rect = pygame.Rect(x, y, button_width, button_height)
        
        pygame.draw.rect(self.screen, color, button_rect, border_radius=5)
        button_text = self.menu_font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        
        return button_rect

    def _show_menu(self):
        while self.in_menu and self.running:
            # Menüde düz siyah arka plan kullan
            self.screen.fill((0, 0, 0))
            
            # Menü başlığı
            title = self.game_over_font.render("Flappy Bird", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.screen_width // 2, 200))
            self.screen.blit(title, title_rect)
            
            # Butonları oluştur
            start_button = self._create_button("Oyuna Başla", 300)
            settings_button = self._create_button("Ayarlar", 400)
            exit_button = self._create_button("Çıkış", 500, color=(139, 0, 0))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self._show_exit_confirmation():  # Çıkış onayı iste
                        self.running = False
                        return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_button.collidepoint(mouse_pos):
                        self.in_menu = False
                        return "start"
                    elif settings_button.collidepoint(mouse_pos):
                        if self._show_settings() == "exit":
                            return "exit"
                    elif exit_button.collidepoint(mouse_pos):
                        if self._show_exit_confirmation():  # Çıkış onayı iste
                            self.running = False
                            return "exit"
            
            self.clock.tick(30)

    def _show_settings(self):
        # Geri dön ikonunu yükle ve boyutlandır
        try:
            back_image = pygame.image.load("flappy-bird-game/src/assets/images/back.jpeg")
            back_image = pygame.transform.scale(back_image, (40, 40))  # Buton boyutuna uygun olarak ölçekle
        except:
            print("Error loading back icon")
            back_image = None
        
        self.in_settings = True
        while self.in_settings and self.running:
            # Ayarlarda düz siyah arka plan kullan
            self.screen.fill((0, 0, 0))
            
            # Geri dön butonu (sol üst köşe)
            back_rect = pygame.Rect(20, 20, 40, 40)
            if back_image:
                self.screen.blit(back_image, back_rect)
            else:
                # Eğer ikon yüklenemezse ok işareti göster
                self._create_small_button("←", 20, 20, (34, 139, 34))
            
            # Ayarlar başlığı
            title = self.game_over_font.render("Ayarlar", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.screen_width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Kuş hızı ayarları
            bird_speed_text = self.menu_font.render(f"Kuş Hızı: {self.bird_speed}", True, (255, 255, 255))
            bird_text_rect = bird_speed_text.get_rect(center=(self.screen_width // 2, 250))
            self.screen.blit(bird_speed_text, bird_text_rect)
            
            # Kuş hızı butonları
            bird_minus = self._create_small_button("-", 100, 235, (139, 0, 0))
            bird_plus = self._create_small_button("+", self.screen_width - 135, 235, (0, 139, 0))
            
            # Oyun hızı ayarları
            game_speed_text = self.menu_font.render(f"Oyun Hızı: {self.game_speed}", True, (255, 255, 255))
            game_text_rect = game_speed_text.get_rect(center=(self.screen_width // 2, 350))
            self.screen.blit(game_speed_text, game_text_rect)
            
            # Oyun hızı butonları
            game_minus = self._create_small_button("-", 100, 335, (139, 0, 0))
            game_plus = self._create_small_button("+", self.screen_width - 135, 335, (0, 139, 0))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if back_rect.collidepoint(mouse_pos):  # back_rect'i kullan
                        self.in_settings = False
                        return "menu"
                    elif bird_minus.collidepoint(mouse_pos) and self.bird_speed > 5:
                        self.bird_speed -= 1
                    elif bird_plus.collidepoint(mouse_pos) and self.bird_speed < 15:
                        self.bird_speed += 1
                    elif game_minus.collidepoint(mouse_pos) and self.game_speed > 20:
                        self.game_speed -= 5
                    elif game_plus.collidepoint(mouse_pos) and self.game_speed < 60:
                        self.game_speed += 5
            
            self.clock.tick(30)

    def _init_game(self):
        self.bird = Bird(230, 350)
        self.base = Base(730)
        self.pipes = [Pipe(600)]
        self.run_game = True
        self.score = 0
        self.game_over = False

    def _show_game_over(self):
        waiting_for_restart = True
        
        while waiting_for_restart:
            # Game over ekranında düz siyah arka plan kullan
            self.screen.fill((0, 0, 0))
            s = pygame.Surface((self.screen_width, self.screen_height))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))
            
            # "Puan Durumunuz" yazısı
            game_over_text = self.game_over_font.render("Puan Durumunuz", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
            self.screen.blit(game_over_text, text_rect)
            
            # Final skoru
            score_text = self.game_over_font.render(str(self.score), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
            self.screen.blit(score_text, score_rect)
            
            # Tekrar oyna butonu
            button_color = (34, 139, 34)  # Koyu yeşil
            button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
            
            # Buton yazısı
            button_text = pygame.font.Font(None, 36).render("Tekrar Oyna", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)
            
            pygame.display.update()
            
            # Olay kontrolü
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_rect.collidepoint(mouse_pos):
                        self._init_game()  # Oyunu sıfırla
                        return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._init_game()  # Space tuşu ile de yeniden başlat
                        return True
            
            self.clock.tick(30)

    def _draw_lives(self):
        # Canları sol üst köşeye çiz
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (10 + i * 35, 10))

    def _handle_death(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            return True
        else:
            # Oyunu resetle ama canları koruyarak
            self.bird = Bird(230, 350)
            self.pipes = [Pipe(600)]
            return False

    def run(self):
        while self.running:
            if self.in_menu:
                result = self._show_menu()
                if result == "exit":
                    break
                elif result == "start":
                    self._init_game()
            
            self.clock.tick(self.game_speed)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.bird.flap()
                    elif event.key == pygame.K_ESCAPE:  # ESC tuşu ile menüye dön
                        self.in_menu = True
                        continue

            if not self.game_over:
                self.bird.move()
                self.base.move()
                self._handle_pipes()
                
                if self.bird.y >= self.screen_height - 100:
                    if self._handle_death():
                        self._draw()
                        if self._show_game_over():
                            self.lives = self.max_lives
                            continue
                        else:
                            self.running = False
                            break
                    continue
            
            if self.game_over:
                self._draw()
                if self._show_game_over():
                    self.lives = self.max_lives
                    continue
                else:
                    self.running = False
                    break
            
            self._draw()
            self._draw_score()
            self._draw_lives()
            pygame.display.update()

    def _handle_pipes(self):
        for pipe in self.pipes:
            pipe.move()
            if self.bird.x > pipe.x + pipe.width and not hasattr(pipe, 'scored'):
                self.score += 1
                pipe.scored = True
                
            if pipe.collide(self.bird):
                if self._handle_death():  # Canlar bittiyse
                    self.game_over = True
                return

            if pipe.off_screen():
                self.pipes.remove(pipe)
                self.pipes.append(Pipe(self.screen_width))

    def _draw_score(self):
        # Skor metnini "Skor: X" formatında oluştur
        score_text = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        # Metni ekranın sağ üst köşesine yerleştir (10 piksel boşluk bırakarak)
        score_rect = score_text.get_rect()
        score_rect.topright = (self.screen_width - 10, 10)
        # Skoru çiz
        self.screen.blit(score_text, score_rect)

    def _load_animated_background(self):
        """Animasyonlu arka planı yükler ve frame'lere ayırır"""
        try:
            # GIF dosyasının yolunu belirtin
            gif_path = 'flappy-bird-game/src/assets/images/background.gif'
            gif = Image.open(gif_path)
            
            for frame in ImageSequence.Iterator(gif):
                # Her frame'i pygame surface'e çevir
                frame = frame.convert('RGB')  # RGBA yerine RGB kullan
                frame = frame.resize((self.screen_width, self.screen_height))
                frame_str = frame.tobytes()
                pygame_frame = pygame.image.fromstring(
                    frame_str, frame.size, 'RGB'  # RGBA yerine RGB modu kullan
                )
                self.bg_frames.append(pygame_frame)
            
            if not self.bg_frames:  # Eğer frame yüklenemezse
                raise Exception("No frames loaded from GIF")
                
        except Exception as e:
            print(f"Error loading animated background: {e}")
            self.bg_frames = []
            # Yedek olarak düz renk kullan
            backup_surface = pygame.Surface((self.screen_width, self.screen_height))
            backup_surface.fill((135, 206, 235))  # Açık mavi
            self.bg_frames.append(backup_surface)

    def _update_background(self):
        """Arka plan animasyonunu günceller"""
        current_time = time.time() * 1000
        if current_time - self.last_frame_time > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.last_frame_time = current_time

    def _draw(self):
        # Sadece oyun oynanırken animasyonlu arka planı göster
        if not self.game_over and not self.in_menu and not self.in_settings:
            self._update_background()
            self.screen.blit(self.bg_frames[self.current_frame], (0, 0))
        else:
            self.screen.fill((0, 0, 0))  # Diğer durumlarda siyah arka plan
        
        # Diğer öğeleri çiz
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.base.draw(self.screen)

    def _show_scoreboard(self):
        """Skor tablosunu göster."""
        scores = self._load_scores()
        self.screen.fill((0, 0, 0))
        # Animasyonlu arka planı skor tablosunda da kullan
        self._update_background()
        self.screen.blit(self.bg_frames[self.current_frame], (0, 0))
        
        # ... geri kalan kod aynı ...

    def _show_exit_confirmation(self):
        """Çıkış onay ekranını gösterir"""
        # Yarı saydam siyah overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Daha küçük font boyutu kullan
        confirmation_font = pygame.font.Font(None, 36)  # Font boyutunu 48'den 36'ya düşür
        
        # Onay mesajı
        message = confirmation_font.render("Çıkmak istediğinizden emin misiniz?", True, (255, 255, 255))
        message_rect = message.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(message, message_rect)
        
        # Butonları oluştur
        button_width = 100
        button_height = 40
        spacing = 20  # Butonlar arası boşluk
        
        # Evet butonu (kırmızı)
        yes_rect = pygame.Rect(
            self.screen_width // 2 - button_width - spacing // 2,
            self.screen_height // 2 + 20,
            button_width,
            button_height
        )
        pygame.draw.rect(self.screen, (139, 0, 0), yes_rect, border_radius=5)
        yes_text = confirmation_font.render("Evet", True, (255, 255, 255))
        yes_text_rect = yes_text.get_rect(center=yes_rect.center)
        self.screen.blit(yes_text, yes_text_rect)
        
        # Hayır butonu (yeşil)
        no_rect = pygame.Rect(
            self.screen_width // 2 + spacing // 2,
            self.screen_height // 2 + 20,
            button_width,
            button_height
        )
        pygame.draw.rect(self.screen, (34, 139, 34), no_rect, border_radius=5)
        no_text = confirmation_font.render("Hayır", True, (255, 255, 255))
        no_text_rect = no_text.get_rect(center=no_rect.center)
        self.screen.blit(no_text, no_text_rect)
        
        pygame.display.update()
        
        # Kullanıcı cevabını bekle
        waiting_for_answer = True
        while waiting_for_answer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if yes_rect.collidepoint(mouse_pos):
                        return True
                    elif no_rect.collidepoint(mouse_pos):
                        return False
            self.clock.tick(30)

    def _load_scores(self):
        """Skorları yükle"""
        try:
            with open("flappy-bird-game/src/scores.json", "r") as f:
                return json.load(f)
        except:
            return []