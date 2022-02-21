from typing import Tuple
from xmlrpc.client import Boolean
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton 
from PyQt5.QtGui import QPixmap, QMouseEvent, QFont
import matplotlib.pyplot as plt
import tkinter
from PIL import Image, ImageTk
import random

from ChessGame import game as chess_game

def board_to_screen(x, y, size):
    new_x = x * size
    new_y = y * size
    return (new_x, new_y)

def screen_to_board(x, y, size):
    b_x = int(x / size)
    b_y = int(y / size)
    return (b_x, b_y)

def dice_roller():
    root = Tkinter.Tk()
    root.geometry("400x400")
    root.title("Roll the Dice")
    root.configure(bg="#B9C6C9")
    root.mainloop()


class PieceVis(QLabel):
    def __init__(self, visual, visual_h, parent=None):
        super(PieceVis, self).__init__(parent)

        # Set up some properties
        self.labelPos = QPoint()

        self.onBoarder = False
        self.moves = []                    # is only accurate between picking up and placing a piece
        self.startingPosition = [0, 0]     # and boardvis will no longer be in charge of whether a piece can move. 
        self.endingPosition = [0, 0]       # pieces will ask chessgame if they can move
        self.default_vis = QPixmap('./picture/' + visual)
        self.active_vis = QPixmap('./picture/' + visual_h)
        self.is_active = False
        self.set_img()

    def get_active(self):
        return self.is_active

    def set_active(self, val):
        self.is_active = val
        self.set_img()

    def set_img(self):
        if self.is_active:
            self.setPixmap(self.active_vis)
        else:
            self.setPixmap(self.default_vis)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        #If user clicks on a piece, it will be moved to the starting position
        self.startingPosition =  screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
        print("starting pos: ", self.startingPosition)
        self.parent().remove_all_h()
        self.moves = self.parent().controller.get_possible_moves_for_piece_at(x=self.startingPosition[0] -1, y=self.startingPosition[1] -1)
        self.parent().add_group_h(self.moves)
        self.raise_()
    # Set the region limits of the board that the piece can move to
    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)) \
                and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < \
                (0 + (self.parent().tileSize / 2)):
            self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                    0 + (self.parent().tileSize / 2))
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < (0 + (self.parent().tileSize / 2)) \
                and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
            self.labelPos = QPoint(self.parent().tileSize * 9.25 - (self.parent().tileSize / 2),
                                    0 + (self.parent().tileSize / 2))
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)) and \
                ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
            self.labelPos = QPoint(self.parent().tileSize * 9.25 - (self.parent().tileSize / 2),
                                    self.parent().tileSize * 9.25 - (self.parent().tileSize / 2))
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)) \
                and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
            self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                    self.parent().tileSize * 9.25 - (self.parent().tileSize / 2))
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)):
            self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                    (ev.globalPos().y() - self.parent().pos().y()) - 30)
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < (0 + (self.parent().tileSize / 2)):
            self.labelPos = QPoint((ev.globalPos().x() - self.parent().pos().x()) - 0,
                                    0 + (self.parent().tileSize / 2))
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
            self.labelPos = QPoint(self.parent().tileSize * 9.25 - (self.parent().tileSize / 2),
                                    (ev.globalPos().y() - self.parent().pos().y()) - 30)
            self.onBoarder = True
        elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
            self.labelPos = QPoint((ev.globalPos().x() - self.parent().pos().x()) - 0,
                                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)))
            self.onBoarder = True

        if not self.onBoarder:
            self.lablePos = ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30))
        self.move(self.lablePos - QPoint(self.parent().tileSize / 2, (self.parent().tileSize / 2)))
        self.onBoarder = False


    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        # Make sure it is the right turn for the piece and that the commander has command points.
            self.onBoarder = False
            self.endingPosition = screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
            ending_adjust = (self.endingPosition[0] - 1, self.endingPosition[1] - 1)
            print("ending pos: ", self.endingPosition)
            if ending_adjust in self.moves:
                new_spot = board_to_screen(self.endingPosition[0], self.endingPosition[1], self.parent().tileSize)
                self.parent().controller.move_piece(from_x=self.startingPosition[0] -1, from_y=self.startingPosition[1] -1, to_x=ending_adjust[0], to_y=ending_adjust[1])
            else:
                new_spot = board_to_screen(self.startingPosition[0], self.startingPosition[1], self.parent().tileSize)
            self.move(new_spot[0], new_spot[1])
            #self.parent().movePieceRelease(self.startingPosition, self.endingPosition)


class TileVis(QLabel):
    def __init__(self, visual, parent=None):
        super(TileVis, self).__init__(parent)
        # Set up some properties
        self.is_active = False
        self.active_vis = QPixmap('./picture/yt')
        self.default_vis = QPixmap('./picture/' + visual)
        self.set_img()

    def set_active(self, val):
        self.is_active = val
        self.set_img()

    def set_img(self):
        if self.is_active:
            self.setPixmap(self.active_vis)
        else:
            self.setPixmap(self.default_vis)

    def get_active(self):
        return self.is_active

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if self.is_active:
            self.parent().list_remove(self)
        else:
            self.parent().add_to_h(self)


class BoardVis(QMainWindow):
    def __init__(self):
        super(BoardVis,self).__init__()
        self.controller = chess_game
        self.h_mode = False
        #This block sets up the window properties
        self.setGeometry(500, 200, 300, 300)
        self.setWindowTitle("Chess Board")
        self.highlighted = []
        # This button allow you can stop your turn
        self.stopButton = QPushButton("End Turn", self)

        # This button allow you can reset the game when you want to start new game
        self.newGameButton = QPushButton("Restart", self)
        

        self.tableOption = QLabel(self)
        
        #Show remaining moves
        self.moveIndicator = QLabel(self)


        self.tileSetup = [["yt", "A", "B", "C", "D", "E", "F", "G", "H"],
                          ["1", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["2", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                          ["3", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["4", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                          ["5", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["6", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                          ["7", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["8", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"]]
        # Holds labels for the tiles on the board.
        self.tilePos = [[" ", "A", "B", "C", "D", "E", "F", "G", "H"],
                        ["1","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["2","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["3","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["4","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["5","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["6","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["7","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["8","0", "0", "0", "0", "0", "0", "0", "0"]]

        # Holds labels for the pieces on the board.
        self.piecePos = [[" ", "A", "B", "C", "D", "E", "F", "G", "H"],
                        ["1", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["2", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["3", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["4", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["5", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["6", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["7", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["8", "0", "0", "0", "0", "0", "0", "0", "0"]]

        self.chooseSideText = QLabel(self)
        self.startScreen = QLabel(self)

        # Choose side button on start screen
        self.whiteButton = QPushButton("White side", self)
        self.blackButton = QPushButton("Black side", self)

        self.showBoard()
        self.showSideChoice()

    def set_h_mode(self, val: Boolean):
        self.h_mode = val

    def add_to_h(self, tile: TileVis):
        if not self.h_mode:
            return
        if tile not in self.highlighted:
            tile.set_active(True)
            self.highlighted.append(tile)

    def add_group_h(self, squares: Tuple):
        if not self.h_mode:
            return
        for pos in squares:
            tile = self.tilePos[pos[1] + 1][pos[0] + 1]
            tile.set_active(True)
            self.highlighted.append(tile)

    def remove_all_h(self):
        if not self.highlighted:
            #print("highlighted empty")
            return
        for row in self.tilePos:
            for tile in row:
                if type(tile) is TileVis:
                    tile.set_active(False)
        for tile in self.highlighted:
            self.list_remove(tile)

    def list_remove(self, tile:TileVis):
        tile.set_active(False)
        self.highlighted.remove(tile)

    def showBoard(self):
        # Initialize the board.
        self.setBoard()
        self.resize(self.boardSize + self.tableOption.width(), self.boardSize )


    def setBoard(self):
        self.tileSize = 75
        self.boardSize = self.tileSize * 9.5
        #add the tile images
        self.addBoardComponents(self.tileSetup, self.tilePos)

        #get data from controller and display it
        board = self.controller.get_board()
        self._update_pieces(board)
    
    #Create table option properties
        self.tableOption.setText("First Turn: White")
        self.tableOption.setAlignment(Qt.AlignCenter)
        self.tableOption.resize(200, 25)
        font = QFont()
        font.setFamily("Impact")
        font.setPixelSize(self.tableOption.height() * 0.8)
        self.tableOption.setFont(font)
        self.tableOption.move(int(self.boardSize), int(self.boardSize /2 -75)
                              - (self.tableOption.height()) * 0.5)

    #Create show information of move indicator
        self.moveIndicator.setText("Remaining Move:"
                                   "\nLeft Side  :  "+
                                   "\nRight Side: "+
                                   "\n Center     : ")
        self.moveIndicator.setAlignment(Qt.AlignCenter)
        self.moveIndicator.resize(200, 100)
        font = QFont()
        font.setFamily("impact")
        font.setPixelSize(self.moveIndicator.height() * 0.2)
        self.moveIndicator.setFont(font)
        self.moveIndicator.move(int(self.boardSize), int(self.boardSize /2)
                                - (self.moveIndicator.height()) * 0.5)


    #Create stop button properties
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(self.stopButton.height() * 0.7)
        self.stopButton.setFont(font)
        self.stopButton.move(int(self.boardSize - ((self.stopButton.width() - self.tableOption.width()) / 2)),
                              int(self.boardSize / 2 + 250) - (self.stopButton.height() * 0.5))

    #Create restart button properties
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(self.newGameButton.height() * 0.8)
        self.newGameButton.setFont(font)
        self.newGameButton.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)),
                             int(self.boardSize / 2 + 300) - (self.newGameButton.height() * 0.5))
        # Create StartScreen properties
        self.startScreen.setAlignment(Qt.AlignCenter)
        self.startScreen.resize(self.boardSize, self.boardSize)
        self.startScreen.setStyleSheet("background-image: url(./picture/startscreen.jpg);"
                                       "background-repeat: no-repeat;"
                                       "background-position: center;")
        self.startScreen.move(0, 0)
        self.startScreen.hide()

        # Set up choose side text properties
        self.chooseSideText.setAlignment(Qt.AlignCenter)
        self.chooseSideText.setText("Welcome to the chess game!"
                                    "\nPlease Choose Your Side")
        self.chooseSideText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseSideText.height() * 0.4)
        self.chooseSideText.setFont(font)
        self.chooseSideText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.chooseSideText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)),
                                 int((self.boardSize / 2) - 300))
        self.chooseSideText.hide()

        # Set up for white button properties
        self.whiteButton.clicked.connect(self.whiteButtonClicked)
        self.whiteButton.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.whiteButton.height() * 0.4)
        self.whiteButton.setFont(font)
        self.whiteButton.move(int((self.boardSize / 2) - (self.whiteButton.width() / 2))
                              , int((self.boardSize / 2) - 150))

        # Set up for black button properties
        self.blackButton.clicked.connect(self.blackButtonClicked)
        self.blackButton.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.blackButton.height() * 0.4)
        self.blackButton.setFont(font)
        self.blackButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2))
                              , int((self.boardSize / 2) - 50))

    def stopButtonClicked(self):
        self.switchTurn()


    def swictchTurn(self):
        if self.turn == "white":
            self.turn = "black"
            self.tableOption.setText("Turn: black")
            self.moveIndicator.setText("Remaining Move:"
                                       "\nLeft Side  :  " +
                                       "\nRight Side: " +
                                       "\n Center     : ")
        else:
            self.turn = "white"
            self.tableOption.setText("Turn: White")
            self.moveIndicator.setText("Remaining Move:"
                                       "\nLeft Side  :  " +
                                       "\nRight Side: " +
                                       "\n Center     : ")


    def showSideChoice(self):
        self.startScreen.show()
        self.startScreen.raise_()
        self.chooseSideText.show()
        self.chooseSideText.raise_()
        self.whiteButton.show()
        self.whiteButton.raise_()
        self.blackButton.show()
        self.blackButton.raise_()

    def hideStartScreen(self):
        self.startScreen.hide()
        self.chooseSideText.hide()
        self.whiteButton.hide()
        self.blackButton.hide()

    def whiteButtonClicked(self):
        self.player = 0
        self.hideStartScreen()


    def blackButtonClicked(self):
        self.player = 1
        #the AI runsnings
        self.hideStartScreen()

    #def update_pieces(self, ):
    def _update_pieces(self, pieces_array):
        k_pieces = {
            "wKt": "wk",
            "bKt": "bk",
            "wKg": "wki",
            "bKg": "bki"
        }

        for y in range(8):
            for x in range(8):
                piece = pieces_array[y][x]
                if piece == "___":
                    continue
                if piece[:3] in k_pieces.keys():
                     piece = k_pieces[piece[:3]]
                else:
                    piece = piece[:2]
                label = PieceVis(piece, piece + 'bl', parent=self)
                    # Set the image based on the array element.
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int((x+1) * self.tileSize), int((y+1) * self.tileSize))
                label.show()
                self.piecePos[y+1][x+1] = label

    def addBoardComponents(self, sender, destination):
        # These are used as iterators to move through the arrays.
        x_iter = 0
        y_iter = 0
        
        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in sender:
            x_iter = 0
            for tile in row:
                if tile == "0":
                    continue
                if len(tile) == 1:
                    #these are the board letters and number 
                     label = QLabel(parent=self)            
                     label.setPixmap(QPixmap('./picture/' + tile))                   
                elif tile[1] == 't':
                    label =TileVis(tile, parent=self)

                else:
                    label = PieceVis(tile, tile + 'bl', parent=self)
                    # Set the image based on the array element.
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int(x_iter * self.tileSize), int(y_iter * self.tileSize))
                label.show()

                # Move the new label to the label array.
                destination[y_iter][x_iter] = label

                x_iter += 1
            y_iter += 1

    #This function is snap the piece back to it place when the person releases wrong place
    def movePieceRelease(self, fromPos, toPos):
        return

    #def screen_to_board(self, screen_val):
    #    return round( (screen_val - 37.5) / 75 )
    #def pixel_to_coordinates(self, pixel_val):
        
