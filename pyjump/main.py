from Tkinter import Canvas, Frame, Tk
from PIL import ImageTk
from random import randint
import tkFont
import os
import player
import platform


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
        self.highestPlat = ""
        self.initObj()
        self.after(DELAY, self.onTimer)
        self.bind_all("<a>", self.playerMoveLeft)
        self.bind_all("<d>", self.playerMoveRight)

    def initObj(self):
        bg_img = ImageTk.PhotoImage(file=ROOT_DIR + "/pyjump/gfx/bg.png")
        self.bg_img = bg_img
        self.bglist = []
        self.bglist.append(self.create_image(0, -50, image=self.bg_img, tag="bg1", anchor="nw"))
        self.bglist.append(self.create_image(0, -850, image=self.bg_img, tag="bg2", anchor="nw"))
        self.spawnPlatform()
        self.player = player.Player(0, 5, 50, 50, self.create_rectangle(50, HEIGHT - 200, 100, HEIGHT - 150, tag="player", fill="green"))

    def checkCollision(self):
        if int(self.gety(self.player.id)) >= HEIGHT - self.player.sizey:
            self.player.jump()

    def doMove(self):
        self.player.move(self)

        if self.player.movey < 0:
            for bg in self.bglist:
                self.move(bg, 0, -self.player.movey)

                if self.gety(bg) >= HEIGHT:
                    self.move(bg, 0, -1550)

        for plat in self.find_withtag("platform"):
            if self.player.movey < 0:
                platMovey = self.player.movey
            else:
                platMovey = 0
            self.move(plat, 0, -platMovey)

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
        self.spawn()

    def spawn(self):
        if self.gety(self.highestPlat) > 50:
            self.spawnPlatform()

    def spawnPlatform(self):
        randx = randint(10, WIDTH - 50)
        self.highestPlat = self.create_rectangle(randx, -10, randx + 50, 0, fill="blue", width=0, tag="platform")


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
