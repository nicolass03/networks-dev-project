import pygame


class Player:
    def __init__(self, x, y, width, height, color, number, display_height, display_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.online = False
        self.number = number
        self.display_height = display_height
        self.display_width = display_width
        self.imageURL = "sprites/" + ("opponent", "player")[number > 0] + ".png"
        self.ball = False
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    # draw(self, win):
        #img = pygame.image.load(self.imageURL)
        #mask = pygame.mask.from_surface(img)
        #win.blit(img, self.rect)

    def hasTheBall(self):
        return self.ball

    def getStatus(self):
        return self.online

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x - self.vel >= 50:
            self.x -= self.vel
            self.moving_left = True
            print("left")
        elif not keys[pygame.K_LEFT]:
            self.moving_left = False
            print("not left")

        if keys[pygame.K_RIGHT] \
                and (self.x + self.vel) <= (self.display_width - self.height):
            self.x += self.vel
            self.moving_right = True
            print("right")
        elif not keys[pygame.K_RIGHT]:
            self.moving_right = False
            print("not right")

        if keys[pygame.K_UP] \
                and self.y - self.vel >= 60:
            self.y -= self.vel
            self.moving_up = True
            print("up")

        elif not keys[pygame.K_UP]:
            self.moving_up = False
            print("no up")

        if keys[pygame.K_DOWN] \
                and self.y + self.vel <= self.display_height - self.height:
            self.y += self.vel
            self.moving_down = True
            print("down")

        elif not keys[pygame.K_DOWN]:
            self.moving_down = False
            print("no down")

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def is_moving_up(self):
        return self.moving_up

    def is_moving_down(self):
        return self.moving_down

    def is_moving_left(self):
        return self.moving_left

    def is_moving_right(self):
        return self.moving_right

    def setBall(self, value):
        self.ball = value