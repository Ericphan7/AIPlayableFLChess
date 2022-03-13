import copy
import random

from ChessGame import Game

game = Game()

class AIFunctions:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.board = game.get__board()
        self.total_success_moves = 0
        self.total_moves_attempted = 0

    def updateBoard(self, board):
        self.board = game.get__board()

    # weights attack areas based on friendly piece power
    def attackRef(self, x, y, piece):
        a = 0
        b = 0
        defpiece = None
        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if a == x and b == y:
                        defpiece = item2.piece
                a = a + 1
            b = b + 1
            a = 0

        # TODO: case needs to be handled where defpiece isn't assigned or determine why it isn't
        if defpiece:
            type = defpiece.get_type()
        else:
            return 0

        if piece.get_type() == 'Pawn':
            if type == 'Pawn':
                return 3
            elif type == 'Bishop':
                return 2
            else:
                return 1
        elif piece.get_type() == 'Rook':
            if type == 'Pawn' or type == 'Bishop' or type == 'Rook':
                return 2
            else:
                return 3
        elif piece.get_type() == 'Bishop':
            if type == 'Pawn':
                return 4
            elif type == 'Bishop':
                return 3
            else:
                return 2
        elif piece.get_type() == 'Knight':
            if type == 'Pawn':
                return 5
            else:
                return 2
        elif piece.get_type() == 'Queen':
            if type == 'Rook':
                return 2
            elif type == 'Pawn':
                return 5
            else:
                return 3
        else:
            if type == 'Rook':
                return 2
            elif type == 'Pawn':
                return 6
            else:
                return 3

    # returns piece object and its potential movement areas
    def moveMap(self):
        self.updateBoard(self.board)
        moveData = []
        heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

        x = 0
        y = 0

        player = "white" if game.tracker.get_current_player() else "black"

        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if self.color == item2.piece.is_white():
                        moveList = game.get_possible_moves_for_piece_at(x=y, y=x)

                        if (item2.piece.get_type() == 'Pawn'):
                            spotVal = 2
                        elif (item2.piece.get_type() == 'Bishop' or item2.piece.get_type() == 'King'):
                            # originally 2, changed to 1 as weights for movement effect choices
                            spotVal = 1
                        else:
                            spotVal = 4
                        for l, m, p in moveList:
                            if (p):
                                heatmap[m][l] += self.attackRef(x, y, item2.piece)

                            #weighting longer moves higher
                            if (m - x == 2 or x - m == 2 or y - l == 2 or l - y == 2):
                                heatmap[m][l] += 1
                                if player == "white":
                                    if (m - x == 2 or x - m == 2 or y - l == 2):
                                        heatmap[m][l] += 2
                                if player == "black":
                                    if (m - x == 2 or x - m == 2 or l - y == 2):
                                        heatmap[m][l] += 2
                            elif (m - x == 3 or x - m == 3 or y - l == 3 or l - y == 3):
                                heatmap[m][l] += 2
                                if player == "white":
                                    if (m - x == 3 or x - m == 3 or y - l == 3):
                                        heatmap[m][l] += 2
                                if player == "black":
                                    if (m - x == 3 or x - m == 3 or l - y == 3):
                                        heatmap[m][l] += 2
                            elif (m - x == 4 or x - m == 4 or y - l == 4 or l - y == 4):
                                heatmap[m][l] += 2
                                if player == "white":
                                    if (m - x == 4 or x - m == 4 or y - l == 4):
                                        heatmap[m][l] += 2
                                if player == "black":
                                    if (m - x == 2 or x - m == 2 or l - y == 2):
                                        heatmap[m][l] += 2
                            elif (m - x == 5 or x - m == 5 or y - l == 5 or l - y == 5):
                                heatmap[m][l] += 3
                                if player == "white":
                                    if (m - x == 5 or x - m == 5 or y - l == 5):
                                        heatmap[m][l] += 2
                                if player == "black":
                                    if (m - x == 5 or x - m == 5 or l - y == 5):
                                        heatmap[m][l] += 2
                            heatmap[m][l] += spotVal
                        dataChunk = [item2.piece, heatmap]

                        #
                        heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]]

                        moveData.append(dataChunk)
                y = y + 1
            x = x + 1
            y = 0
            print('\n')

        # self.displayMoveData(moveData)

        return moveData

    def displayMoveData(self, moveData):

        for element, array in moveData:
            print(element.get_name())
            for row in array:
                print(row)

    def best_move(self, moveData):
        max_weight = None
        BestSameScore = []
        # print('start check')
        for element, array in moveData:
            SameScore = []
            max_weight_piece = None

            for y, row in enumerate(array):
                if max(row)>0:
                    for x, weight in enumerate(row):
                        if weight != 0:
                            if not max_weight_piece:
                                # sets up a max weight if there is not one already set
                                max_weight_piece = (x, y, weight, element.get_name() + element.corp.get_name(), element.x_loc, element.y_loc)
                                SameScore = [max_weight_piece]
                            else:
                                if weight > max_weight_piece[2]:
                                    max_weight_piece = (x, y, weight, element.get_name() + element.corp.get_name(), element.x_loc, element.y_loc)
                                    SameScore = [max_weight_piece]

                                elif weight == max_weight_piece[2]:
                                    SameScore.append((x, y, weight, element.get_name() + element.corp.get_name(), element.x_loc, element.y_loc))

            # # to check max weight piece after every from piece is checked
            # if max_weight_piece:
            #     print('max pc', max_weight_piece)

            if len(SameScore)>0:
                # Shuffles the SameScore Array twice to pull a random move
                random.shuffle(SameScore)
                max_weight_piece = SameScore[0]

                if not max_weight:
                    max_weight = max_weight_piece[2]
                elif max_weight < max_weight_piece[2]:
                    BestSameScore = []
                    max_weight = max_weight_piece[2]

                if max_weight==max_weight_piece[2]:
                    BestSameScore.append(max_weight_piece)

        random.shuffle(BestSameScore)
        if len(BestSameScore)==0:
            game.tracker.end_turn()
            BestMove = self.best_move(self.moveMap())
        else:
            BestMove = BestSameScore[0]

        # print('end check, result', BestMove)

        print("Best Move after everything: ", BestMove, "\n\n")


        return BestMove

    def AI_move(self, BestMove):

        #self.displayMoveData(moveData)
        #self.best_move(moveData)
        print(BestMove)
        print("Moving ", BestMove[3], " from x: ", BestMove[4], " y: ", BestMove[5], "Moving to x: ", BestMove[0], " y: ", BestMove[1])

        if game.move_piece(from_x=BestMove[4], from_y=BestMove[5], to_x=BestMove[0], to_y=BestMove[1]):
            self.total_success_moves+=1
        self.total_moves_attempted += 1
        #self.displayMoveData(moveData)

    def make_move(self):
        print("starting new move:")
        player = "white" if game.tracker.get_current_player() else "black"
        print('current player:', player)
        x = self.moveMap()
        y = self.best_move(x)
        self.AI_move(y)
        colour = "white" if self.color else "black"
        print(colour, "team had", self.total_success_moves, 'successful moves out of', self.total_moves_attempted)



aiAssistWhite = AIFunctions(game, True)
aiAssistBlack = AIFunctions(game, False)


for num in range (44):
    if not game.game_status():
        if game.tracker.get_current_player():
            aiAssistWhite.make_move()
        else:
            aiAssistBlack.make_move()
    else:
        print("Game Over!")
        break


