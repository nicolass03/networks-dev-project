import pygame
from client_handler import ClientHandler
from player import Player

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

width = 690
height = 500
ground = pygame.image.load("Images/ground.jpg")
waitScreen = pygame.image.load("Images/waitScreen.jpg")
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Soccer game")
pygame.mixer.music.load('Music/gameMusic.mp3')

def redrawWindow(window, game, grPl1, grPl2, grBa):
    window.fill((255, 255, 255))
    if not (game.connected()):

        window.blit(waitScreen, (-40,20))

        font = pygame.font.SysFont("comicsans", 60)

        font1 = pygame.font.SysFont("comicsans", 40)

        text = font.render("Waiting for Player...", 1, (255, 255, 255), True)

        text1 = font1.render("Press Q to claim the ball", 1, (255, 255, 255), True)

        text2 = font1.render("Press Space and UP/DOWN/LEFT/RIGHT", 1, (255, 255, 255), True)

        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 60))

        window.blit(text1, (width / 2 - text1.get_width() / 2, (height / 2 - text.get_height() / 2) + 115))

        window.blit(text2, (width / 2 - text2.get_width() / 2, (height / 2 - text.get_height() / 2) + 150))
    else:


        font = pygame.font.SysFont("comicsans", 40)

        txtHome = font.render("Home: ", 1, (0, 0, 0), True)
        txtAway = font.render("Away: ", 1, (0, 0, 0), True)

        window.blit(ground, (15, 50))
        window.blit(txtHome, (120,10))
        window.blit(txtAway, (450,10))


        grPl1.draw(win)
        grPl2.draw(win)
        grBa.draw(win)

        if pygame.sprite.collide_mask(grPl1, grBa):
            game.give_ball(game.getPlayer1())
        elif pygame.sprite.collide_mask(grPl2, grBa):
            game.give_ball(game.getPlayer2())
        if pygame.sprite.collide_mask(grPl1, grPl2) and (
                game.getPlayer1().hasTheBall() or game.getPlayer2().hasTheBall()):
            game.out("colliding /////////////////////////////////////////////////////")
            game.steal_ball()

        game.ballValidation()
        game.shoot()
        #game.move(window)
    pygame.display.update()

def main():
    run = True
    n = ClientHandler()
    p = n.getP()

    clock = pygame.time.Clock()
    game = None

    power = 0
    while run:
        clock.tick(60)
        gp1 = None
        gp2 = None
        gb = None
        try:
            if game:
                if game.getPlayer(p.number).hasTheBall() or game.ballIsRolling():
                    game = n.send((p, game.ball))
                else:
                    game = n.send(p)
            else:
                game = n.send(p)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            if game.connected():

                if p.number == 1:
                    gp1 = GrahicsPlayer(p)
                    gp2 = GrahicsPlayer(game.getPlayer2())
                else:
                    gp2 = GrahicsPlayer(p)
                    gp1 = GrahicsPlayer(game.getPlayer1())



                gb = GraphicBall(game.getBall())
                p.move()
            redrawWindow(win, game, gp1, gp2, gb)

        except Exception as e:
            print(e)
            break

pygame.mixer.music.play()
main()

