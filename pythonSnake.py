#!/home/smender/anaconda3/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import numpy as np
import pandas as pd
from PyQt4 import QtGui, QtCore
    
class pythonSnake(QtGui.QMainWindow):
    """
    Main class with Snake game.
    """
    
    def __init__(self):
        """
        Class constructor.
        """
        
        super(pythonSnake, self).__init__()
        self.initUI()
    
    size = 300
    winSize = int((size ** 2) / 100)
    speed = 150
    checkedSize = -2
    checkedSpeed = -3
    lastCheckedSize = -2
    lastCheckedSpeed = -3
    highscore = 0
    played = False
    paused = True
    over = False
    timer = QtCore.QBasicTimer()

    def initUI(self):
        """
        Method which initiates GUI.
        """
        
        self.resize(540, 580)
        self.center()
        self.setWindowTitle("pythonSnake")
        self.setWindowIcon(QtGui.QIcon("pythonSnake.png"))    
        
        menubar = self.menuBar()
        
        newGameAction = QtGui.QAction("&New Game        N", self)
        newGameAction.triggered.connect(self.newGameEvent)
        optionsAction = QtGui.QAction("&Options             O", self)
        optionsAction.triggered.connect(self.optionsEvent)
        exitAction = QtGui.QAction("&Quit                    Q", self)
        exitAction.triggered.connect(self.close)
  
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(newGameAction)
        fileMenu.addAction(optionsAction)
        fileMenu.addAction(exitAction)
        
        aboutAction = QtGui.QAction("&About        A", self)
        aboutAction.triggered.connect(self.aboutEvent)
        
        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(aboutAction)
        
        self.statusBar()
        
        if self.played:        
            self.newGame()
        
        self.show()
    
    def center(self):
        """
        Method which puts game's window in the center of desktop.
        """
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def newGameEvent(self):
        """
        Method which initiates game when "New Game" or "N" is pressed.
        """
        
        self.played = True
        self.newGame()
    
    def optionsEvent(self):
        """
        Method which initiates game's options when "Options" or "O" is pressed.
        """
        
        if self.played:
            self.pauseEnd()
        self.lastCheckedSize == self.lastCheckedSize
        self.lastCheckedSpeed == self.lastCheckedSpeed
        self.optionsWin = optionsWindow(self)
    
    def closeEvent(self, event):
        """
        Method which closes game when "Quit" or "Q" is pressed.
        """
        
        if self.played:
            self.pauseEnd()
        reply = QtGui.QMessageBox.question(self, "Goodbye?",
            "Are you tired with this WILD game?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  
            
    def aboutEvent(self):
        """
        Method which initiates information about game when "About" or "A" is pressed.
        """
        
        if self.played:
            self.pauseEnd()
        QtGui.QMessageBox.about(self, "About", """pythonSnake game\n\n
        How to play:
        Use arrow keys to move. To make snake
        go faster, press longer one of arrow
        keys. To start game after pause, press
        one of arrow keys or P key.\n
        Keyboad shortcuts:
        - N - start new game,
        - P - pause/unpause game,
        - O - game's options,
        - Q - quit game,
        - A - information about game.\n
        Piotr Smuda
        29.12.2015""")

    def paintEvent(self, event):
        """
        Main method connected with paint events which draws game.
        """
        
        board = QtGui.QPainter()
        board.begin(self)
        board.setPen(QtGui.QPen(QtGui.QColor(215, 215, 215, 255)))
        board.setBrush(QtGui.QColor(235, 235, 235, 255))
        board.drawRect(20, 40, self.size, self.size)
        if self.lastCheckedSize != self.checkedSize:
            self.lastCheckedSize = self.checkedSize
            self.over = False
            self.food = False
            self.snakeHeadX = int((self.size / 2) + 10);
            self.snakeHeadY = int((self.size / 2) + 30);
            self.lastPressed = "NOT PRESSED"
            self.snake = pd.Series([
            [self.snakeHeadX, self.snakeHeadY],
            [self.snakeHeadX + 10, self.snakeHeadY],
            [self.snakeHeadX + 20, self.snakeHeadY]
        ])
        if self.played:    
            self.drawFood(board)    
            self.drawSnake(board)
        board.end()
        
    def timerEvent(self, event):
        """
        Main method connected with timer events which initiates movement of snake.
        """
        
        if event.timerId() == self.timer.timerId():
            self.tryMove(self.lastPressed)
            self.repaint()
        else:
            QtGui.QFrame.timerEvent(self, event)
        
    def drawSnake(self, board):
        """
        Method which draws snake.
        """
        
        board.setPen(QtGui.QColor(235, 235, 235, 255))
        board.setBrush(QtGui.QColor(0, 0, 0, 255))
        for elem in self.snake:
            board.drawRect(elem[0], elem[1], 10, 10)    
            
    def drawFood(self, board):
        """
        Method which draws food.
        """
        
        if self.food == False:
            while self.food == False:
                self.foodX = 20 + np.round(random.randint(0, self.size - 10), -1)
                self.foodY = 40 + np.round(random.randint(0, self.size - 10), -1)
                if not np.any(self.snake.apply(lambda elem: elem == [self.foodX, self.foodY])):
                    self.food = True
        board.setPen(QtGui.QColor(0, 0, 0, 255))
        board.setBrush(QtGui.QColor(255, 0, 0, 255))
        board.drawRect(self.foodX + 1, self.foodY + 1, 6, 6)
        
    def newGame(self):
        """
        Main method which initiates game with it's initial settings.
        """
        
        self.played = True
        self.paused = True
        self.over = False
        self.food = False
        self.snakeHeadX = int((self.size / 2) + 10);
        self.snakeHeadY = int((self.size / 2) + 30);
        self.lastPressed = "NOT PRESSED"
        self.snake = pd.Series([
            [self.snakeHeadX, self.snakeHeadY],
            [self.snakeHeadX + 10, self.snakeHeadY],
            [self.snakeHeadX + 20, self.snakeHeadY]
        ])
        self.start()

    def start(self):
        """
        Method which starts/unpauses game.
        """
        
        self.paused = False
        self.statusBar().showMessage("")
        self.timer.start(self.speed, self)
        self.update()
        
    def pauseEnd(self):
        """
        Method which pauses/ends game.
        """
        
        self.paused = True
        if self.played and self.over:
            score = len(self.snake) - 3
            if score > self.highscore:
                self.highscore = score
            self.statusBar().showMessage("Game Over. Highscore: " + str(self.highscore)
                                         + ". Your score: " + str(score) + ".")
        else:         
            self.statusBar().showMessage("Game Paused.")
        self.timer.stop()
        self.update()
        
    def win(self):
        """
        Method which ends game if it is finished.
        """
        
        self.paused = True
        self.highscore = len(self.snake) - 3
        self.statusBar().showMessage("Game finished. You Win! Highscore: " 
                                     + str(self.highscore) + ".")
        self.timer.stop()
        self.update()    
        
    def keyPressEvent(self, event):
        """
        Method connected with key press events.
        """
        
        key = event.key()
        if key == QtCore.Qt.Key_N:
            self.newGame()
        elif key == QtCore.Qt.Key_O:
            self.optionsEvent()
        elif key == QtCore.Qt.Key_Q:
            self.close()
        elif key == QtCore.Qt.Key_A:
            self.aboutEvent()
        elif self.played and not self.over:
            if key == QtCore.Qt.Key_Up and self.lastPressed != "DOWN":
                self.lastPressed = "UP"
                self.tryMove("UP")
                self.start()
            elif key == QtCore.Qt.Key_Down and self.lastPressed != "UP":
                self.lastPressed = "DOWN"
                self.tryMove("DOWN")
                self.start()
            elif key == QtCore.Qt.Key_Left and self.lastPressed != "RIGHT":
                self.lastPressed = "LEFT"
                self.tryMove("LEFT")
                self.start()
            elif key == QtCore.Qt.Key_Right and self.lastPressed == "NOT PRESSED":
                self.snake[0], self.snake[2] = self.snake[2], self.snake[0]
                self.snakeHeadX = self.snake[0][0]
                self.snakeHeadY = self.snake[0][1]
                self.lastPressed = "RIGHT"
                self.tryMove("RIGHT")
                self.start() 
            elif key == QtCore.Qt.Key_Right and self.lastPressed != "LEFT":
                self.lastPressed = "RIGHT"
                self.tryMove("RIGHT")
                self.start()
            elif key == QtCore.Qt.Key_P and self.paused == False:
                self.pauseEnd()
            elif key == QtCore.Qt.Key_P:
                self.start()

    def tryMove(self, direction):
        """
        Method which moves snake.
        """
        
        tempGameStatus = self.gameStatus()
        if self.lastPressed != "NOT PRESSED" and tempGameStatus[0]:
            if tempGameStatus[1] == 2:
                self.snake = self.snake[:-1]
            if direction == "UP":
                self.snakeHeadY -= 10
            elif direction == "DOWN":
                self.snakeHeadY += 10
            elif direction == "LEFT":
                self.snakeHeadX -= 10
            elif direction == "RIGHT":
                self.snakeHeadX += 10
            temp = pd.Series([[self.snakeHeadX, self.snakeHeadY]])
            temp = temp.append(self.snake)
            temp.index = np.arange(len(temp))
            self.snake = temp

    def gameStatus(self):
        """
        Method which checks game's status:
        - snake ate food,
        - game over (snake bit itself or snake is out of bound),
        - game is finished,
        - everything is ok.
        """
        
        temp = self.snake[1:]
        if self.snakeHeadX == self.foodX and self.snakeHeadY == self.foodY:
            self.food = False
            return True, 1
        elif self.snakeHeadX < 20 or self.snakeHeadY < 40 or self.snakeHeadX > self.size + 10 or self.snakeHeadY > self.size + 30:
            self.over = True
            self.pauseEnd()
            return False, 1
        elif np.any(temp.apply(lambda elem: elem == self.snake[0])):
            self.over = True
            self.pauseEnd()
            return False, 1
        elif len(self.snake) == self.winSize:
            self.over = True
            self.win()
            return False, 1
        return True, 2

class optionsWindow(QtGui.QDialog):
    """
    Class with options' window.
    """
    
    def __init__(self, parent = None):
        """
        Class constructor.
        """
        
        super(optionsWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        """
        Method which initiates GUI.
        """
        
        mainLayout = QtGui.QVBoxLayout() 
        
        buttonSize = QtGui.QPushButton("Change map size")
        buttonSize.setAutoDefault(False)
        buttonSize.clicked.connect(self.sizeEvent)
        self.radioButtonSize1 = QtGui.QRadioButton("300 x 300")
        self.radioButtonSize2 = QtGui.QRadioButton("400 x 400")
        self.radioButtonSize3 = QtGui.QRadioButton("500 x 500")
        layoutSize = QtGui.QVBoxLayout()
        layoutSize.addWidget(self.radioButtonSize1)
        layoutSize.addWidget(self.radioButtonSize2)
        layoutSize.addWidget(self.radioButtonSize3)
        layoutSize.addWidget(buttonSize)
        
        buttonSpeed = QtGui.QPushButton("Change snake's speed")
        buttonSpeed.setAutoDefault(False)
        buttonSpeed.clicked.connect(self.speedEvent)
        self.radioButtonSpeed1 = QtGui.QRadioButton("Slow")
        self.radioButtonSpeed2 = QtGui.QRadioButton("Medium")
        self.radioButtonSpeed3 = QtGui.QRadioButton("Fast")
        layoutSpeed = QtGui.QVBoxLayout()
        layoutSpeed.addWidget(self.radioButtonSpeed1)
        layoutSpeed.addWidget(self.radioButtonSpeed2)
        layoutSpeed.addWidget(self.radioButtonSpeed3)
        layoutSpeed.addWidget(buttonSpeed)

        self.groupSize = QtGui.QButtonGroup()
        self.groupSize.addButton(self.radioButtonSize1)
        self.groupSize.addButton(self.radioButtonSize2)
        self.groupSize.addButton(self.radioButtonSize3)

        self.groupSpeed = QtGui.QButtonGroup()
        self.groupSpeed.addButton(self.radioButtonSpeed1)
        self.groupSpeed.addButton(self.radioButtonSpeed2)
        self.groupSpeed.addButton(self.radioButtonSpeed3)
        
        buttonClose = QtGui.QPushButton("Close options")
        buttonClose.setAutoDefault(False)
        buttonClose.clicked.connect(self.close)
        
        mainLayout.addLayout(layoutSize)
        mainLayout.addLayout(layoutSpeed)
        mainLayout.addWidget(buttonClose)
        self.setLayout(mainLayout)
        
        self.makeChecked()
        
        self.show()
        
    def makeChecked(self):
        """
        Method which checks proper radiobuttons.
        """
        
        if pythonSnake.checkedSize == -2:
            self.radioButtonSize1.setChecked(True)
        elif pythonSnake.checkedSize == -3:
            self.radioButtonSize2.setChecked(True)
        elif pythonSnake.checkedSize == -4:
            self.radioButtonSize3.setChecked(True)
        if pythonSnake.checkedSpeed == -2:
            self.radioButtonSpeed1.setChecked(True)
        elif pythonSnake.checkedSpeed == -3:
            self.radioButtonSpeed2.setChecked(True)
        elif pythonSnake.checkedSpeed == -4:
            self.radioButtonSpeed3.setChecked(True)
        
    def sizeEvent(self):
        """
        Method connected with changing size in options events which changes map's size.
        """
        
        checked = self.groupSize.checkedId()
        if checked == -2:
            pythonSnake.checkedSize = -2
            pythonSnake.size = 300
        elif checked == -3:
            pythonSnake.checkedSize = -3
            pythonSnake.size = 400
        elif checked == -4:
            pythonSnake.checkedSize = -4
            pythonSnake.size = 500
        pythonSnake.winSize = int((pythonSnake.size ** 2) / 100)
        
    def speedEvent(self):
        """
        Method connected with changing speed in options events which changes snake's speed.
        """
        
        checked = self.groupSpeed.checkedId()
        if checked == -2:
            pythonSnake.checkedSpeed = -2
            pythonSnake.speed = 300
        elif checked == -3:
            pythonSnake.checkedSpeed = -3
            pythonSnake.speed = 150
        elif checked == -4:
            pythonSnake.checkedSpeed = -4
            pythonSnake.speed = 50
    
def main():
    app = QtGui.QApplication(sys.argv)
    pythonSnakeGame = pythonSnake()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
