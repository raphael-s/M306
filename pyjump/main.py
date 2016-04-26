from PIL import ImageTk
from random import randint
from Tkinter import Canvas
from Tkinter import Frame
from Tkinter import Tk
import os
import platform
import player
import tkFont


WIDTH = 500
HEIGHT = 750
DELAY = 50
ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))


class Board(Canvas):
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="white", highlightthickness=0)
        self.initInfoScreen()
        self.pack()

    def initInfoScreen(self):
        self.infoList = []
        self.titleFont = tkFont.Font(size="60")
        self.listHeaderFont = tkFont.Font(size="25")
        self.listSmallHeaderFont = tkFont.Font(size="21")
        self.listFont = tkFont.Font(size="18")
        self.startGameFont = tkFont.Font(size="30")
        self.infoList.append(self.create_rectangle(0, 0, WIDTH, HEIGHT, width=0, fill="grey", tag="infoBg"))
        self.infoList.append(self.create_text(WIDTH / 2, 50, text="PyJump", font=self.titleFont))
        self.infoList.append(self.create_text(120, 150, text="Controls:", font=self.listHeaderFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 200, text="- <a> to move left", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 230, text="- <d> to move right", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 260, text="- <space> to shoot", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(130, 290, text="- <p> to pause", font=self.listFont, anchor="nw"))
        self.infoList.append(self.create_text(WIDTH / 2, 700, text="Press <space> to start the game", font=self.startGameFont))
        self.bind_all("<space>", self.startGame)

    def startGame(self, arg1):
        self.unbind_all("<space>")
        self.delete("all")
        self.initGame()

    def initGame(self):
        self.gameOver = False
        self.gamePaused = False
        self.score = 0
        self.highestPlat = ""
        self.initObj()
        self.after(DELAY, self.onTimer)
        self.bind_all("<a>", self.playerMoveLeft)
        self.bind_all("<d>", self.playerMoveRight)
        self.bind_all("<p>", self.togglePause)

    def initObj(self):
        bg_img = ImageTk.PhotoImage(file=ROOT_DIR + "/pyjump/gfx/bg.png")
        self.bg_img = bg_img
        self.bglist = []
        self.bglist.append(self.create_image(0, -50, image=self.bg_img, tag="bg1", anchor="nw"))
        self.bglist.append(self.create_image(0, -850, image=self.bg_img, tag="bg2", anchor="nw"))
        self.spawnPlatform()
        self.create_rectangle(0, 0, WIDTH, 30, tag="topBar", fill="grey")
        self.topBarFont = tkFont.Font(size="20")
        self.create_text(WIDTH / 2, 15, text="PyJump", font=self.topBarFont, tag="topBar")
        self.create_text(WIDTH - 100, 15, text="Score:", font=self.topBarFont, tag="topBar")
        self.create_text(WIDTH -50, 15, text=self.score, font=self.topBarFont, tag="score")
        self.player = player.Player(0, 5, 50, 50, self.create_rectangle(50, HEIGHT - 200, 100, HEIGHT - 150, tag="player", fill="green"))

    def checkCollision(self):
        if int(self.gety(self.player.id)) >= HEIGHT - self.player.sizey:
            self.player.jump()

        if self.getx(self.player.id) >= WIDTH:
            self.move(self.player.id, -WIDTH -self.player.sizex, 0)

        if self.getx(self.player.id) <= -self.player.sizex:
            self.move(self.player.id, WIDTH + self.player.sizex, 0)

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
            self.gameoverfont = tkFont.Font(size="70")
            self.gameoversmallfont = tkFont.Font(size="40")
            self.restartfont = tkFont.Font(size="35")
            self.create_rectangle(50, HEIGHT / 2 - (50 * 3), WIDTH - 50, HEIGHT / 2 + (50 * 2), fill="white", tag="gameOverBg", width=0)
            self.create_text(WIDTH / 2, HEIGHT / 2 - (50 * 2), text="Game Over", font=self.gameoverfont, tag="gameOverText")
            self.create_text(WIDTH / 2, HEIGHT / 2, text="Score: " + str(self.score), font=self.gameoversmallfont, tag="finalScore")
            self.create_rectangle(50, HEIGHT - (50 * 2), WIDTH - 50, HEIGHT - 50, fill="white", tag="startNewGame", width=0)
            self.create_text(WIDTH / 2, HEIGHT - 75, text="Press <space> to restart", font=self.restartfont, tag="restartGameText")
            self.unbind_all("<a>")
            self.unbind_all("<d>")
            self.unbind_all("<space>")
            self.unbind_all("<p>")
            self.bind_all("<space>", self.startGame)
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
        if not self.gamePaused:
            self.checkHealth()
            self.checkCollision()
            self.doMove()
            self.spawn()

    def togglePause(self, e):
        if self.gamePaused:
            self.gamePaused = False
            for item in self.find_withtag("pauseMenu"):
                self.delete(item)
            self.checkHealth()
        else:
            self.gamePaused = True
            self.pauseFont = tkFont.Font(size="90")
            self.create_rectangle(WIDTH / 2 - 150, 300, WIDTH / 2 + 150, 400, fill="white", width=0, tag="pauseMenu")
            self.create_text(WIDTH / 2 - 120, 300, text="Pause", font=self.pauseFont, tag="pauseMenu", anchor="nw")

    def spawn(self):
        if self.gety(self.highestPlat) > 120:
            self.spawnPlatform()

    def spawnPlatform(self):
        randx = randint(10, WIDTH - 50)
        self.highestPlat = self.create_rectangle(randx, 30, randx + 50, 40, fill="blue", width=0, tag="platform")


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
