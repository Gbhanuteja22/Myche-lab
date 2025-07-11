# ui.py
import pygame
import sys

# Set screen size
WIDTH, HEIGHT = 1200, 700
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLUE = (100, 180, 255)
BLACK = (0, 0, 0)

# Lab items info
lab_items = [
    {"name": "Beaker", "rect": pygame.Rect(50, 100, 100, 100)},
    {"name": "Test Tube", "rect": pygame.Rect(50, 250, 100, 100)},
    {"name": "Burner", "rect": pygame.Rect(50, 400, 100, 100)},
    {"name": "Cooler", "rect": pygame.Rect(50, 550, 100, 100)},
]

class VirtualLabApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Virtual Chemistry Lab")
        self.clock = pygame.time.Clock()
        self.dragging = None
        self.offset_x = 0
        self.offset_y = 0

    def draw_lab(self):
        self.screen.fill(WHITE)
        font = pygame.font.SysFont(None, 24)

        for item in lab_items:
            pygame.draw.rect(self.screen, BLUE, item["rect"])
            label = font.render(item["name"], True, BLACK)
            label_rect = label.get_rect(center=item["rect"].center)
            self.screen.blit(label, label_rect)

    def run(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for item in lab_items:
                        if item["rect"].collidepoint(event.pos):
                            self.dragging = item
                            mouse_x, mouse_y = event.pos
