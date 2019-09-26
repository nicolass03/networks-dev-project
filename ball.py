import pygame

POWER = 20

class Ball:
    def __init__(self, x, y, radius, color, display_height, display_width):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.center = (self.x, self.y)
        self.color = color
        self.online = False
        self.display_height = display_height
        self.display_width = display_width
        self.speed = 0
        self.aim = []
        self.collided_up = False
        self.collided_down = False
        self.collided_left = False
        self.collided_right = False

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.center, self.radius)

    def getStatus(self):
        return self.online

    #def move(self):
        #power = 3
        #acceleration = power
        #keys = pygame.key.get_pressed()
        #for acceleration in reversed(range(power)):
        #if keys[pygame.K_LEFT]:
          #self.x -= acceleration
        #elif keys[pygame.K_RIGHT]:
          #self.x += acceleration
        #elif keys[pygame.K_UP]:
          #self.y -= acceleration
       # elif keys[pygame.K_DOWN]:
          #self.y += acceleration
        #else:
          #return
        #self.update()

    def update(self):
        self.center = (self.x, self.y)
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def border_collide(self):
        colliding = []
        if self.x < 0:
            colliding.append("left")
        if self.x > 690:
            colliding.append("right")
        if self.y > 500:
            colliding.append("down")
        if self.y < 0:
            colliding.append("up")

        return colliding

    def collided_left_border(self):
        self.collided_left = (True, False)[self.x <= 0]

    def collided_up_border(self):
        self.collided_up = (True, False)[self.y <= 0]

    def collided_right_border(self):
        self.collided_right = (True, False)[self.x >= 690]

    def collided_down_border(self):
        self.collided_down = (True, False)[self.y >= 500]
