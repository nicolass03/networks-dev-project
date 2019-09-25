import pygame
from ball import POWER
class Game:

    def __init__(self, id):
        self.ready = False
        self.id = id
        self.score = [0, 0]
        self.p1 = None
        self.p2 = None
        self.ball = None

    def connected(self):
        return self.ready

    def getPlayer1(self):
        return self.p1

    def getPlayer2(self):
        return self.p2

    def getPlayer(self, number):
        if number == 1:
            return self.p1
        elif number == 2:
            return self.p2
        else:
            raise ValueError("No Player matches the specified arg")

    def ballIsRolling(self):
        return (False, True)[self.ball.speed > 0]

    def bothOnline(self):
        return self.p1Online and self.p2Online

    def move(self, win):
        self.p1.draw(win)
        self.p2.draw(win)
        self.ball.draw(win)

    def give_ball(self, player):
        self.ball.speed = 0
        player.setBall(True)

    def quit_ball(self, player):
        self.ball.speed = 0
        player.setBall(False)

    def ballValidation(self):
        if self.p1.hasTheBall():
            if self.p1.is_moving_down():
                self.ball.y = self.p1.y #+ self.p1.height
                self.ball.x = self.p1.x# + int(self.p1.width/2)
            if self.p1.is_moving_up():
                self.ball.y = self.p1.y
                self.ball.x = self.p1.x #+ int(self.p1.width / 2)
            if self.p1.is_moving_left():
                self.ball.y = self.p1.y #+ int(self.p1.height/2)
                self.ball.x = self.p1.x
            if self.p1.is_moving_right():
                self.ball.y = self.p1.y #+ int(self.p1.height/2)
                self.ball.x = self.p1.x #+ self.p1.width

        elif self.p2.hasTheBall():
            if self.p2.is_moving_down():
                self.ball.y = self.p2.y #+ self.p2.height
                self.ball.x = self.p2.x #+ int(self.p2.width / 2)
            if self.p2.is_moving_up():
                self.ball.y = self.p2.y
                self.ball.x = self.p2.x #+ int(self.p2.width / 2)
            if self.p2.is_moving_left():
                self.ball.y = self.p2.y #+ int(self.p2.height / 2)
                self.ball.x = self.p2.x
            if self.p2.is_moving_right():
                self.ball.y = self.p2.y #+ int(self.p2.height / 2)
                self.ball.x = self.p2.x #+ self.p2.width

        self.ball.update()

    def steal_ball(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            print("space pressed")
            if self.p1.hasTheBall():
                self.quit_ball(self.p1)
                self.give_ball(self.p2)
            elif self.p2.hasTheBall():
                self.quit_ball(self.p2)
                self.give_ball(self.p1)

    def shoot(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z] and self.ball.speed == 0:
            self.ball.aim = []
            self.ball.speed = 15
            if keys[pygame.K_LEFT]:
                self.ball.aim.append("left")
                self.ball.x -= 70
            if keys[pygame.K_RIGHT]:
                self.ball.aim.append("right")
                self.ball.x += 50
            if keys[pygame.K_UP]:
                self.ball.aim.append("up")
                self.ball.y -= 70
            if keys[pygame.K_DOWN]:
                self.ball.aim.append("down")
                self.ball.y += 50

        elif not self.p1.hasTheBall() and not self.p2.hasTheBall() and self.ball.speed > 0:
            for x in range(len(self.ball.aim)):
                if self.ball.aim[x] == "left":
                    self.ball.x -= self.ball.speed / len(self.ball.aim)
                if self.ball.aim[x] == "right":
                    self.ball.x += self.ball.speed / len(self.ball.aim)
                if self.ball.aim[x] == "up":
                    self.ball.y -= self.ball.speed / len(self.ball.aim)
                if self.ball.aim[x] == "down":
                    self.ball.y += self.ball.speed / len(self.ball.aim)
                self.ball.speed *= .90

        self.ball.update()

    def out(self,msg):
        print(msg)

    def getPlayer1(self):
        return self.p1

    def getPlayer2(self):
        return self.p2

    def getBall(self):
        return self.ball

    def setPlayer1(self, p):
        self.p1 = p

    def setPlayer2(self, p):
        self.p2 = p

    def setBall(self,b):
        self.ball = b