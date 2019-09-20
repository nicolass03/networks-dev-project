import pygame
from network import Network, GameData
from player import Player


pygame.font.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Soccer game")


def redrawWindow(window,game,  p1, p2, ball):
    window.fill((255, 255, 255))
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, (0, 0, 0), True)
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        p1.draw(window)
        p2.update()
        p2.draw(window)
        ball.draw(window)

    pygame.display.update()


def main():
    run = True
    n = Network()
    start_info = n.getStartInfo()
    p1 = Player(start_info.player_pos1[0], start_info.player_pos1[1], 50, 50, (0, 0, 255), start_info.number, 500, 500)
    p2 = Player(start_info.player_pos2[0], start_info.player_pos2[1], 50, 50, (0, 255, 0), 0, 500, 500)
    b = n.getB()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        game = None
        try:
            game = n.send(GameData((p1.x, p1.y), p1.number, b))
        except:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if game.connected():
            if p1.number == 1:
                p2.setPos(game.getPos2())
            else:
                p2.setPos(game.getPos1())
            b = game.ball
            p1.move()
        if pygame.sprite.collide_rect(p1, b):
            b.move()

        redrawWindow(win, game, p1, p2, b)


main()
