class Player(object):
    def __init__(self, movex, movey, sizex, sizey, id):
        self.movex = movex
        self.movey = movey
        self.sizex = sizex
        self.sizey = sizey
        self.id = id
        self.jumpSpeed = 0

    def jump(self):
        self.movey = -15
        self.jumpSpeed = 25

    def move(self, board):
        board.move(self.id, self.movex, self.movey)
        if self.jumpSpeed > 0:
            self.movey += 1
            self.jumpSpeed -= 1

        if self.movey < 0:
            board.score -= self.movey
            board.itemconfigure(board.find_withtag("score"), text=board.score)

        if self.movex > 0:
            self.movex -= 1
        elif self.movex < 0:
            self.movex += 1

    def moveLeft(self, board):
        if self.movex > -20:
            self.movex -= 5

    def moveRight(self, board):
        if self.movex < 20:
            self.movex += 5
