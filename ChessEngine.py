"""
lưu dữ tất cả thông tin về trạng thái hiện tại của trò chơi, giữ nhật ký các nước đi để có thể hoàn lại
"""


class Game_state:
    def __init__(self):
        # bàn cờ có 8*8 = 64 ô cờ, những ô có hai ký tự là ô trống
        # b đại diện cho màu đen , sau đó là tên quân cờ
        # w đại diện cho màu trắng, sau đó là tên quân cờ.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'P': self.getPawnMove, 'N': self.getKnightMoves, 'R': self.getRookMove, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves} # các hàm di chuyển của các quân cờ
        # xác định xem lượt của ai đi trắng rồi tới đen
        self.whiteToMove = True
        # danh sách nhật ký nước đi
        self.moveLog = []

        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.pins = []
        self.checks = []

    # quân cờ sau khi di chuyển thì vị trí bắt đầu sẽ được làm trống và vị trí kết thúc sẽ được cập nhập hình ảnh
    def makeMove(self, move):
        print(f"Di chuyển: {move.pieceMoved} từ ({move.startRow}, {move.startCol}) đến ({move.endRow}, {move.endCol})")
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    # hoàn tác nước cờ cuối cùng (hàm pieceMoved để xác định đó là quân cờ nào (vua, hậu, mã, xe...))
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # hoàn tác lại vị trí của quân vua nếu ta hoàn tác lại nước đi
            if move.pieceMoved =='wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)


    # '''các nước đi cần xem xét kểm tra'''
    def getValidMoves(self): # loại bỏ các nước đi không hợp lệ làm cho vua bị chiếu
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            if len(moves) == 0:
                if self.inCheck():
                    self.checkMate = True
                    print("Checkmate")
                else:
                    self.staleMate = True
                    print("Stalemate")
        return moves


    def inCheck(self): # kiểm tra xem vua của người chơi hiện tại đang bị chiếu ko
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, row, col):  # kiểm tra xe một ô có đang bị tấn công ko
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False

    '''các nước đi không cần xem xét kiểm tra'''
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # xác định màu quân cờ
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]  # xác định loại quân cờ
                    self.moveFunctions[piece](row, col, moves)
        return moves



    def getPawnMove(self, row, col, moves):  # xác định nước đi của quân tốt
        if self.whiteToMove:  # quân tốt trắng di chuyển
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:  # bắt quân cờ bên trái (bắt quân đen)
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:  # bắt quân cờ bên phải (bắt quân đen)
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:  # quân tốt đen di chuyển
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
    #
    def getKnightMoves(self, row, col, moves):
        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]  #  di chuyển cho quân mã từ trái vòng xuống dưới sang phải
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            i = 1
            while True:
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                i = i + 1

    def getRookMove(self, row, col, moves): # quân xe
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # phải, trái, lên, xuống
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            i = 1
            while True:
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0]  == enemycolor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                i = i + 1

    def getBishopMoves(self, row, col, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # (trái dưới - phải dưới, trái trên - phải trên)
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            i = 1
            while True:
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                i = i + 1

    def getQueenMoves(self, row, col, moves):  # di chuyển quân hậu 22
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1,1), (0, 1), (-1, 1), (-1, 0)]
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            i = 1
            while True:
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                i = i + 1

    def getKingMoves(self, row, col, moves):
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]   # di chuyển cho quân vua từ trái vòng xuống dưới sang phải
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((row, col), (endRow, endCol), self.board))
                elif endPiece[0] == enemycolor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

class Move:
    # gán biến cho các hàng của bàn cờ
    ranksTorows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksTorows.items()}
    # gán biến cho các cột của bàn cờ
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # quân cờ được di chuyển
        self.pieceCaptured = board[self.endRow][self.endCol]  # quân cờ bị bắt (nếu có)
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''overriding the equals method'''
    def __eq__(self, other):  # xác định xem hai nước đi có giống nhau không
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):  # chuyển đổi 2 vị trí là vị trí trước khi và sau khi di chuyển
        return ("di chuyen " + self.getRankFile(self.startRow, self.startCol) + " sang "
                + self.getRankFile(self.endRow, self.endCol))

    def getRankFile(self, row, col):  # chuyển đổi một cặp hàng thành ký hiệu cờ vua (ví dụ như 6,4 thành e,2)
        return self.colsToFiles[col] + self.rowsToRanks[row]
