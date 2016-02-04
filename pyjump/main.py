from Tkinter import Canvas, Frame, Tk
import tkFont
import os


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

    def initObj(self):
        self.create_rectangle(50, 50, 100, 100, tag="square", fill="green")

    def checkCollision(self):
        pass

    def doMove(self):
        self.move(self.find_withtag("square"), 1, 1)

    def checkHealth(self):
        if self.gameOver > 0:
            self.create_text(WIDTH / 2, HEIGHT / 2 - 100, text="Game Over", font=tkFont.Font(size="70"), tag="GameOver")
        else:
            self.timer = self.after(DELAY, self.onTimer)

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
