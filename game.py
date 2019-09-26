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
            if self.p2.hasTheBall():
                self.quit_ball(self.p2)
                self.give_ball(self.p1)

    def shoot(self):
        keys = pygame.key.get_pressed()
        self.ball.collided_left = False
        self.ball.collided_right = False
        self.ball.collided_down = False
        self.ball.collided_up = False

        if keys[pygame.K_z] and self.ball.speed == 0:
            self.ball.collided_left = False
            self.ball.collided_right = False
            self.ball.collided_down = False
            self.ball.collided_up = False
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
            if keys[pygame.K_DOWN] :
                self.ball.aim.append("down")
                self.ball.y += 50

        elif not self.p1.hasTheBall() and not self.p2.hasTheBall() and self.ball.speed > 0:

            for x in range(len(self.ball.aim)):
                if self.ball.aim[x] == "left":
                    if self.ball.collided_left:
                        print("////////////////////////// collided left ///////////////////////")
                        self.ball.x += self.ball.speed / len(self.ball.aim)
                    else:
                        self.ball.x -= self.ball.speed / len(self.ball.aim)
                    if not self.ball.collided_left:
                        self.ball.collided_left_border()

                if self.ball.aim[x] == "right":
                    if self.ball.collided_right:
                        print(" /////////////////////// collided right  /////////////////////////")
                        self.ball.x -= self.ball.speed / len(self.ball.aim)
                    else:
                        self.ball.x += self.ball.speed / len(self.ball.aim)
                    if not self.ball.collided_right:
                        self.ball.collided_right_border()

                if self.ball.aim[x] == "up":
                    if self.ball.collided_up:
                        print("//////////////////////////// collided up ////////////////////////////")
                        self.ball.y += self.ball.speed / len(self.ball.aim)
                    else:
                        self.ball.y -= self.ball.speed / len(self.ball.aim)
                    if not self.ball.collided_up:
                        self.ball.collided_up_border()

                if self.ball.aim[x] == "down":
                    if self.ball.collided_down:
                        print("/////////////////////////////// collided down //////////////////////////")
                        self.ball.y -= self.ball.speed / len(self.ball.aim)
                    else:
                        self.ball.y += self.ball.speed / len(self.ball.aim)
                    if not self.ball.collided_down:
                        self.ball.collided_down_border()

                self.ball.speed *= .60
                self.ball.update()
            #self.ball.update()

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

    def reset_positions(self):
        self.ball.x = 250
        self.ball.y = 250
        self.p1.x = 40
        self.p1.y = 255
        self.p2.x = 640
        self.p2.y = 255
        self.ball.update()

    def reset(self):
        self.score = [0, 0]
        self.reset_positions()

