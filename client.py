import pygame
import globals
from network import Network, GameData
from player import Player
from ball import Ball
import time

pygame.font.init()
pygame.mixer.init()
globals.init()

ground = pygame.image.load("Images/ground.jpg")
scoreboard = pygame.image.load("Images/scoreBoard.jpg")

win = pygame.display.set_mode((globals.window_width, globals.window_height))
pygame.display.set_caption("Soccer game")


def redrawWindow(window,game,  player, opponent, ball):

    window.fill((255, 255, 255))
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        font1 = pygame.font.SysFont("comicsans", 40)

        text = font.render("Waiting for Player...", 1, (0, 0, 0), True)
        text1 = font1.render("Press Q to claim the ball", 1, (0, 0, 0), True)
        text2 = font1.render("Press Space and UP/DOWN/LEFT/RIGHT", 1, (0, 0, 0), True)

        window.blit(text,  (globals.window_width / 2 - text.get_width() / 2, globals.window_height / 2 - text.get_height() / 2))
        window.blit(text1, (globals.window_width / 2 - text1.get_width() / 2, (globals.window_height / 2 - text.get_height() / 2) + 100))
        window.blit(text2, (globals.window_width / 2 - text2.get_width() / 2, (globals.window_height / 2 - text.get_height() / 2) + 150))



    else:
        window.blit(ground,(15,50))
        window.blit(scoreboard, (300,0))
        player.draw(window)
        opponent.update()
        opponent.draw(window)
        ball.draw(window)

    pygame.display.update()


def main():
    run = True
    ball_owner = 0
    new_owner = False
    power = 0
    direction = ""

    n = Network()
    start_info = n.getStartInfo()
    player = Player(start_info.player_pos1[0], start_info.player_pos1[1], 50, 50, (0, 0, 255), start_info.number, globals.window_height, globals.window_width)
    opponent = Player(start_info.player_pos2[0], start_info.player_pos2[1], 50, 50, (0, 255, 0), 0, globals.window_height, globals.window_width)
    ball = Ball(250, 250, 20, (0, 0, 255), globals.window_height, globals.window_width)
    clock = pygame.time.Clock()

    while run:
        time.clock()
        clock.tick(60)
        game = None
        try:
            game = n.send(GameData((player.x, player.y), player.number, (ball.x, ball.y), ball_owner, new_owner))
        except:
            break
        new_owner = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if game.connected():
            if player.number == 1:
                opponent.setPos(game.getPos2())
            else:
                opponent.setPos(game.getPos1())
            ball.setPos(game.ball)
            player.move()

            #if game.ball_owner is True:
            #ball.setOwner(False)

        if player.number != game.ball_owner:
            ball.owner = False

        if power > 0:
            ball.shoot(power, direction)

        if pygame.sprite.collide_mask(player, ball) and pygame.key.get_pressed()[pygame.K_q]:
            power = 0
            ball.setOwner(True)
            new_owner = True
            ball_owner = player.number
            game.ball_owner = ball.owner

        elif pygame.sprite.collide_mask(player, ball) and pygame.key.get_pressed()[pygame.K_SPACE]:
            aim = ball.aim()
            if aim:
                ball.setOwner(True)
                new_owner = True
                ball_owner = player.number
                game.ball_owner = ball.owner
                power = 20
                direction = aim

        if pygame.sprite.collide_mask(player, ball) and ball.owner is True:
            ball.move()

        redrawWindow(win, game, player, opponent, ball)
        power *= .90

main()
