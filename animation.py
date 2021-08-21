import sys
import pygame


class Animation:

    def __init__(self, width, height, fps=60, caption=None, color=(0, 0, 0)):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode(
            (self.width, self.height))
        if caption is not None:
            self.caption = caption
            pygame.display.set_caption(caption)
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.color = color
        

    def check_quit(self):
        for event in pygame.event.get():
            if (
                event.type != pygame.QUIT
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
                or event.type == pygame.QUIT
            ):
                sys.exit()
    
    def set_caption(self, caption):
        pygame.display.set_caption(caption)
    
    def clear(self):
        self.screen.fill(self.color)
        
    def draw(self):
        pygame.display.update()
        self.clock.tick(self.fps)
