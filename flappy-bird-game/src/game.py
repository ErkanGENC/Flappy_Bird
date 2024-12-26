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
        pygame.display.set_caption("Console")  # Pencere başlığını ayarla
        self.clock = pygame.time.Clock()
        self._init_game()  # Oyun değişkenlerini başlatma fonksiyonu
        
        # Font ayarları
        pygame.font.init()
        self.font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 64)  # Game over yazısı için daha büyük font
        
        # Arka plan resmini yükle
        bg_image_path = 'flappy-bird-game/src/assets/images/çimen.jpg'
        try:
            self.background = pygame.image.load(bg_image_path)
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            print(f"Error: Background image '{bg_image_path}' could not be loaded.")
            self.background = None

        # Kuş resmi
        image_path = 'assets/images/erkan.jpg'
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
        else:
            print(f"Error: No file '{image_path}' found.")
            self.image = None

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

    def run(self):
        while self.run_game:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.bird.flap()

            if not self.game_over:
                self.bird.move()
                self.base.move()
                self._handle_pipes()
                
                # Yere çarpma kontrolü
                if self.bird.y >= self.screen_height - 100:  # Base yüksekliğini hesaba katarak
                    self.game_over = True
            
            # Oyun bitti mi kontrol et
            if self.game_over:
                self._draw()  # Son kareyi çiz
                if self._show_game_over():  # Skor ekranını göster ve yeniden başlatma kontrolü
                    continue  # Oyun yeniden başlatıldı
                else:
                    self.run_game = False  # Oyundan çık
                    break
            
            self._draw()
            self._draw_score()
            pygame.display.update()

    def _handle_pipes(self):
        for pipe in self.pipes:
            pipe.move()
            if self.bird.x > pipe.x + pipe.width and not hasattr(pipe, 'scored'):
                self.score += 1
                pipe.scored = True
                
            if pipe.collide(self.bird):
                self.game_over = True
                return  # Çarpışma olduğunda hemen dön

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