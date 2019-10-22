import pygame
from ball import POWER
class Game:

    def __init__(self, id):
        self.ready = False
        self.id = id
        self.score = (0, 0)
        self.p1 = None
        self.p2 = None
        self.ball = None
        self.score_record = set()
        self.ended = False
        self.ball_owner = 0

    def connected(self):
        return self.ready

    def getPlayer1(self):
        """ Returns the games p1 member
            Returns:
                p1(Player):Player 1 of the game
        """
        return self.p1

    def getPlayer2(self):
        """ Returns the games p2 member
            Returns:
                p1(Player):Player 1 of the game
        """
        return self.p2

    def getPlayer(self, number):
        """ Returns the games player with the corresponding number
            Parameters:
                number (int):The number of the player need

            Returns:
                p1 or p2 (Player):Player 1 or 2 of the game
        """
        if number == 1:
            return self.p1
        elif number == 2:
            return self.p2
        else:
            raise ValueError("No Player matches the specified arg")

    def ballIsRolling(self):
        """ Returns true if the ball is rolling and false otherwise
            Returns:
                Bool: True/False
        """
        return (False, True)[self.ball.speed > 0]

    def bothOnline(self):
        return self.p1 and self.p2

    def move(self, win):
        self.p1.draw(win)
        self.p2.draw(win)
        self.ball.draw(win)

    def give_ball(self, player):
        self.ball.speed = 0
        player.setBall(True)
        self.ball_owner = player.number

    def give_ball_nr(self, number):
        if self.p1.number == number:
            self.p1.setBall(True)
            self.p2.setBall(False)
            #self.ball.speed = 0
        elif self.p2.number == number:
            self.p2.setBall(True)
            self.p1.setBall(False)
            #self.ball.speed = 0

    def quit_ball(self, player):
        self.ball.speed = 0
        player.setBall(False)

    def ballValidation(self):
        if self.ball_owner == 1 and self.ball.speed == 0:
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

        elif self.ball_owner == 2 and self.ball.speed == 0:
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
            if self.ball_owner == 1:
                self.quit_ball(self.p1)
                self.give_ball(self.p2)
                self.ball_owner = self.p2.number
                return True
            elif self.ball_owner == 2:
                self.quit_ball(self.p2)
                self.give_ball(self.p1)
                self.ball_owner = self.p1.number
                return True
        return False

    def shoot(self):
        """  Determines whether the player wants to shoot the ball.
        Once the ball is shot the speed is decreased down to 0.
        Possible rebounds are handled
        """

        keys = pygame.key.get_pressed()
        goal = ""
        if keys[pygame.K_z] and self.ball.speed == 0:
            self.ball.horizontal_motion = ""
            self.ball.vertical_motion = ""
            self.ball.speed = 15
            if keys[pygame.K_LEFT]:
                self.ball.horizontal_motion = "left"
                self.ball.x -= 100
            elif keys[pygame.K_RIGHT]:
                self.ball.horizontal_motion = "right"
                self.ball.x += 100
            if keys[pygame.K_UP]:
                self.ball.vertical_motion = "up"
                self.ball.y -= 100
            elif keys[pygame.K_DOWN]:
                self.ball.vertical_motion = "down"
                self.ball.y += 100
            #self.ball_owner = 0

        elif self.ball.speed > 0:
            self.ball.rebound()
            if self.ball.horizontal_motion == "left":
                self.ball.x -= self.ball.speed
            elif self.ball.horizontal_motion == "right":
                self.ball.x += self.ball.speed
            if self.ball.vertical_motion == "up":
                self.ball.y -= self.ball.speed
            elif self.ball.vertical_motion == "down":
                self.ball.y += self.ball.speed
            if self.ball.speed < 1.0:
                self.ball.speed = 0
            else:
                self.ball.speed *= .95

            goal = self.ball.validate_goal()
            if goal != "":
                self.ball.quit_motions()
                if goal == "home":
                    self.add_goal(self.p1, "")
                elif goal == "away":
                    self.add_goal(self.p2, "")

        self.ball.update()

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
        self.p1.x = 40
        self.p1.y = 255
        self.p2.x = 640
        self.p2.y = 255
        self.ball.x = 330
        self.ball.y = 220
        self.ball.update()

    def reset(self):
        self.score = (0, 0)
        self.reset_positions()

    def add_goal(self, player, time):
        #if player.number == 1:
            #self.score[0] += 1
        #else:
            #self.score[1] += 1
        player.goals+=1
        self.reset_positions()
        #self.score_record.add((player, time))

