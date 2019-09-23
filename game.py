class Game:
    p1 = None
    p2 = None
    ball = None
    ball_owner = None

    def __init__(self, id):
        self.ready = False
        self.id = id
        self.score = [0, 0]

    def connected(self):
        return self.ready

    def getPos1(self):
        return self.p1

    def getPos2(self):
        return self.p2

    def getBall(self):
        return self.ball

    def bothOnline(self):
        return self.p1Online and self.p2Online

    def move(self, win):
        self.p1.draw(win)
        self.p2.draw(win)
        self.ball.draw(win)
