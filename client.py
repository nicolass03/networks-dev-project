import pygame
import globals
from network import Network, GameData
from player import Player
from ball import Ball

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
        text = font.render("Waiting for Player...", 1, (0, 0, 0), True)
        window.blit(text, (globals.window_width / 2 - text.get_width() / 2, globals.window_height / 2 - text.get_height() / 2))


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
    update_ball = None

    n = Network()
    start_info = n.getStartInfo()
    player = Player(start_info.player_pos1[0], start_info.player_pos1[1], 50, 50, (0, 0, 255), start_info.number, globals.window_height, globals.window_width)
    opponent = Player(start_info.player_pos2[0], start_info.player_pos2[1], 50, 50, (0, 255, 0), 0, globals.window_height, globals.window_width)
    ball = Ball(250, 250, 20, (0, 0, 255), globals.window_height, globals.window_width)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        game = None
        try:
            game = n.send(GameData((player.x, player.y), player.number, (ball.x, ball.y), update_ball))
        except:
            break
        update_ball = False
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

            if game.update_ball:
                ball.setOwner(False)

        if pygame.sprite.collide_mask(player, ball) and pygame.key.get_pressed()[pygame.K_SPACE]:
            ball.setOwner(True)
            update_ball = True
            game.ball_owner = ball.owner

        if pygame.sprite.collide_mask(player, ball) and ball.owner:
            ball.move()

        redrawWindow(win, game, player, opponent, ball)


main()
