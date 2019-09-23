import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, display_height, display_width):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.center = (self.x, self.y)
        self.color = color
        self.online = False
        self.display_height = display_height
        self.display_width = display_width
        self.owner = None

        self.image = pygame.image.load("sprites/ball.png")
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, self.rect)

    def getStatus(self):
        return self.online

    def move(self):
        power = 3
        acceleration = power
        keys = pygame.key.get_pressed()
        #for acceleration in reversed(range(power)):
        if keys[pygame.K_LEFT]:
          self.x -= acceleration
        elif keys[pygame.K_RIGHT]:
          self.x += acceleration
        elif keys[pygame.K_UP]:
          self.y -= acceleration
        elif keys[pygame.K_DOWN]:
          self.y += acceleration
        else:
          return
        self.update()

    def update(self):
        self.center = (self.x, self.y)
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.update()

    def setOwner(self, bool):
        self.owner = bool


