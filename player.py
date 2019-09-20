import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, number, display_height, display_width):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = width / 2
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 3
        self.online = False
        self.number = number
        self.display_height = display_height
        self.display_width = display_width

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def getStatus(self):
        return self.online

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]\
                and self.x - self.vel >= 0:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]\
                and self.x + self.vel <= self.display_height - self.height:
            self.x += self.vel

        if keys[pygame.K_UP]\
                and self.y - self.vel >= 0:
            self.y -= self.vel

        if keys[pygame.K_DOWN]\
                and self.y + self.vel <= self.display_height - self.height:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
