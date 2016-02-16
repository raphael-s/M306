from Tkinter import Canvas, Frame, Tk
import tkFont
import os
import player


WIDTH = 500
HEIGHT = 750
DELAY = 50
ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))


class Board(Canvas):
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="white", highlightthickness=0)
        self.initGame()
        self.pack()

    def initGame(self):
        self.gameOver = False
        self.initObj()
        self.after(DELAY, self.onTimer)
        self.bind_all("<a>", self.playerMoveLeft)
        self.bind_all("<d>", self.playerMoveRight)

    def initObj(self):
        self.player = player.Player(0, 5, 50, 50, self.create_rectangle(50, HEIGHT - 200, 100, HEIGHT - 150, tag="player", fill="green"))

    def checkCollision(self):
        if int(self.gety(self.player.id)) >= HEIGHT - self.player.sizey:
            self.player.jump()

    def doMove(self):
        self.player.move(self)

    def checkHealth(self):
        if self.gameOver > 0:
            self.create_text(WIDTH / 2, HEIGHT / 2 - 100, text="Game Over", font=tkFont.Font(size="70"), tag="GameOver")
        else:
            self.timer = self.after(DELAY, self.onTimer)

    def getx(self, id):
        return self.coords(id)[0]

    def gety(self, id):
        return self.coords(id)[1]

    def playerMoveRight(self, e):
        self.player.moveRight(self)

    def playerMoveLeft(self, e):
        self.player.moveLeft(self)

    def onTimer(self):
        self.checkHealth()
        self.checkCollision()
        self.doMove()


class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.board = Board()
        self.pack()


def main():
    root = Tk()
    root.title("PyJump")
    Game()
    root.mainloop()


if __name__ == '__main__':
    main()
