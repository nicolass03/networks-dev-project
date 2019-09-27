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
        self.horizontal_motion = ""
        self.vertical_motion = ""

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
        if self.x+self.radius > 670:
            colliding.append("right")
        if self.y + self.radius > 490:
            colliding.append("down")
        if self.y < 0:
            colliding.append("up")

        return colliding

    def rebound(self):
        if self.x + self.radius >= self.display_width:
            self.horizontal_motion = "left"
        if self.x <= 0:
            self.horizontal_motion = "right"
        if self.y + self.radius >= self.display_height:
            self.vertical_motion = "up"
        if self.y <= 0:
            self.vertical_motion = "down"

    def validate_goal(self):
        goal = ""
        if self.x > self.display_width - 10 and self.y > ((self.display_height / 2) - 50) and self.y < ((self.display_height / 2) + 50):
            goal = "home"
        if self.x <= 0 + 5 and self.y > ((self.display_height / 2) - 50) and self.y < ((self.display_height / 2) + 50):
            goal = "away"
        return goal

    def quit_motions(self):
        self.horizontal_motion = ""
        self.vertical_motion = ""
        self.speed = 0