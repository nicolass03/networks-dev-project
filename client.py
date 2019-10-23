import pygame
from client_handler import ClientHandler
from player import Player
import time

class GrahicsPlayer(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.x = player.x
        self.y = player.y
        self.width = player.width
        self.height = player.height
        self.radius = int(self.width / 2)
        self.color = player.color
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.vel = 3
        self.online = False
        self.display_height = player.display_height
        self.display_width = player.display_width
        self.image = pygame.image.load("sprites/player" + str(player.number) + ".png")
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        #pygame.draw.rect(win, self.color, self.rect)
        win.blit(self.image, self.rect)


class GraphicBall(pygame.sprite.Sprite):
    def __init__(self, ball):
        super().__init__()
        self.x = ball.x
        self.y = ball.y
        self.radius = ball.radius
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.center = (self.x, self.y)
        self.color = ball.color
        self.online = False
        self.display_height = ball.display_height
        self.display_width = ball.display_width
        self.image = pygame.image.load("sprites/ball2.png")

    def draw(self, win):
        win.blit(self.image, self.rect)
        #pygame.draw.circle(win, self.color, self.center, self.radius)


pygame.font.init()
pygame.mixer.init()

width = 670
height = 490
ground = pygame.image.load("Images/ground.jpg")
waitScreen = pygame.image.load("Images/waitScreen.jpg")
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Soccer game")
pygame.mixer.music.load('Music/gameMusic.mp3')
period = "1st Half"

def redrawWindow(window, game, grPl1, grPl2, grBa,time, p):
    new_owner = False
    window.fill((255, 255, 255))
    if not (game.connected()):

        window.blit(waitScreen, (-40, 10))

        font = pygame.font.SysFont("comicsans", 60)

        font1 = pygame.font.SysFont("comicsans", 40)

        text = font.render("Waiting for other player...", 1, (255, 255, 255), True)

        text1 = font1.render("Press SPACE to claim the ball", 1, (255, 255, 255), True)

        text2 = font1.render("Press UP/DOWN/LEFT/RIGHT to move", 1, (255, 255, 255), True)

        text3 =  font1.render("Press Z to shoot the ball", 1, (255, 255, 255), True)



        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 60))

        window.blit(text1, (width / 2 - text1.get_width() / 2, (height / 2 - text.get_height() / 2) + 115))

        window.blit(text2, (width / 2 - text2.get_width() / 2, (height / 2 - text.get_height() / 2) + 150))

        window.blit(text3, ((width / 2 - text2.get_width() / 2) + 80, (height / 2 - text.get_height() / 2) + 190))



    else:

        font = pygame.font.SysFont("comicsans", 40)
        txtHome = font.render("Home: ", 1, (0, 0, 0), True)
        txtAway = font.render("Away: ", 1, (0, 0, 0), True)
        txtHalf = font.render(period, 1, (0, 0, 0), True)
        txtTimer = font.render((str(time[0]) + ":" + ('%02d' % time[1])), 1, (0, 0, 0), True)
        textScore1 = font.render(str(game.getPlayer1().getGoals()), 1, (0, 0, 0), True)
        textScore2 = font.render(str(game.getPlayer2().getGoals()), 1, (0, 0, 0), True)

        window.blit(ground, (2, 50))
        window.blit(txtHome, (120, 10))
        window.blit(txtAway, (450, 10))
        window.blit(txtTimer, (width / 2 - txtTimer.get_width() / 2, 0))
        window.blit(txtHalf, (width / 2 - txtHalf.get_width() / 2, 25))
        window.blit(textScore1, (130 + txtHome.get_width(), 10))
        window.blit(textScore2, (460 + txtAway.get_width(), 10))

        grPl1.draw(win)
        grPl2.draw(win)
        grBa.draw(win)

        #game.give_ball_nr(game.ball_owner)

        if pygame.sprite.collide_mask(grPl1, grPl2) and (
                game.ball_owner > 0):
            new_owner = game.steal_ball()
        elif pygame.sprite.collide_mask(grPl1, grBa) and (game.ball_owner == 0 or game.ball.speed > 0):
            game.give_ball(game.getPlayer1())
            new_owner = True
        elif pygame.sprite.collide_mask(grPl2, grBa) and (game.ball_owner == 0 or game.ball.speed > 0):
            game.give_ball(game.getPlayer2())
            new_owner = True

        game.ballValidation()
        if game.shoot():
            new_owner = True
        #game.move(window)
    pygame.display.update()
    return new_owner

def show_summary(g):
    win.fill((255,255,255))
    font = pygame.font.SysFont("comicsans", 60)

    txtSummary = font.render("SUMMARY ", 1, (0, 0, 0), True)
    txtHome = font.render("Home: ", 1, (0, 0, 0), True)
    txtAway = font.render("Away: ", 1, (0, 0, 0), True)
    txtPointHome = font.render(str(g.getPlayer1().getGoals()), 1, (0, 0, 0), True)
    txtPointAway = font.render(str(g.getPlayer2().getGoals()), 1, (0, 0, 0), True)

    win.blit(txtSummary, (width / 2 - txtSummary.get_width() / 2, 100))
    win.blit(txtHome, ((width / 2 - txtHome.get_width() / 2)/2, 160))
    win.blit(txtAway, (width / 2 - txtHome.get_width() / 2+(width / 2 - txtAway.get_width() / 2)/2, 160))
    win.blit(txtPointHome, ((width / 2 - txtHome.get_width() / 2) / 2 +30, 280))
    win.blit(txtPointAway, (width / 2 - txtHome.get_width() / 2 + (width / 2 - txtAway.get_width() / 2) / 2 +30, 280))


    pygame.display.update()


global ended

def main():
    run = True
    n = ClientHandler()
    p = n.getP()
    minutes = 0
    seconds = 60
    dt = 0
    start_timer = False
    ended = False
    clock = pygame.time.Clock()
    game = None

    new_owner = False

    while not ended:
        clock.tick(60)
        gp1 = None
        gp2 = None
        gb = None
        try:
            if game:
                if game.ball_owner == p.number or game.ballIsRolling():
                    p.goals = game.getPlayer(p.number).getGoals()
                    game = n.send((p, game.ball, game.ball_owner, new_owner))
                else:
                    if p.goals != game.getPlayer(p.number).getGoals():
                        p.goals = game.getPlayer(p.number).getGoals()
                        game = n.send((p, game.ball, game.ball_owner, True))
                    else:
                        p.goals = game.getPlayer(p.number).getGoals()
                        game = n.send(p)
            else:
                game = n.send(p)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    n.send("disconnect")
                    pygame.quit()

            if game.connected():
                if p.number == 1:
                    gp1 = GrahicsPlayer(p)
                    gp2 = GrahicsPlayer(game.getPlayer2())
                else:
                    gp2 = GrahicsPlayer(p)
                    gp1 = GrahicsPlayer(game.getPlayer1())

                seconds -= dt
                if seconds <= 0:
                    if minutes <= 0 and seconds <= 0:
                        ended = True
                        break
                    else:
                        seconds = 60
                        minutes -= 0
                        period = "2nd Half"
                        game.reset_positions()

                gb = GraphicBall(game.getBall())
                p.move()
            new_owner = False
            new_owner = redrawWindow(win, game, gp1, gp2, gb, (minutes, seconds), p)
            dt = clock.tick(60) / 1000

        except Exception as e:
            print(e)
            break

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        show_summary(game)

pygame.mixer.music.play()
main()

