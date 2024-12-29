import pygame
import os  
import time
from bird import Bird
from pipe import Pipe
from base import Base

class Game:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("EZGİ SANA AŞIGIM BİR TANEM <3")
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
        
        # Arka plan resmi
        bg_image_path = 'flappy-bird-game/src/assets/images/çimen.jpg'
        try:
            self.background = pygame.image.load(bg_image_path)
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            print(f"Error: Background image '{bg_image_path}' could not be loaded.")
            self.background = None

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
            self.screen.fill((0, 0, 0))
            if self.background:
                self.screen.blit(self.background, (0, 0))
            
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
                        self.running = False
                        return "exit"
            
            self.clock.tick(30)

    def _show_settings(self):
        back_image = pygame.image.load("flappy-bird-game/src/assets/images/back.jpeg")
        self.in_settings = True
        while self.in_settings and self.running:
            self.screen.fill((0, 0, 0))
            if self.background:
                self.screen.blit(self.background, (0, 0))
            
            # Geri dön oku (sol üst köşe)
            back_arrow = self._create_small_button("←", 20, 20, (34, 139, 34))
            
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
                    if back_arrow.collidepoint(mouse_pos):
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
            # Arkaplanı karart
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
        # Skor metnini oluştur
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        # Metni ekranın üst ortasına yerleştir
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 50))
        # Skoru çiz
        self.screen.blit(score_text, score_rect)

    def _draw(self):
        # Arka plan resmini çiz
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((135, 206, 235))  # Açık mavi arka plan (resim yüklenemezse)
        
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.base.draw(self.screen)