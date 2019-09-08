import pygame
from network import Network
from player import Player
pygame.font.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Soccer game")

def redrawWindow(win, game, p1, p2):

    win.fill((255,255,255))
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        p1.draw(win)
        p2.draw(win)
    pygame.display.update()

def main():

    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        game = None
        try:
            game = n.send("g")
            p2 = None
            if p.number == 1:
                p2 = game.getPlayer2()
            else:
                p2 = game.getPlayer1()
        except:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if(game.connected()):
            p.move()
        redrawWindow(win, game, p, p2)



main()
