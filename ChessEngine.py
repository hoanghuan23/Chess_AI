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
        self.moveFunctions = {'P': self.getPawnMove, 'N': self.getKnightMoves, 'R': self.getRookMove,
                              'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}  # các hàm di chuyển của các quân cờ
        # xác định xem lượt của ai đi trắng rồi tới đen
        self.whiteToMove = True
        # danh sách nhật ký nước đi
        self.moveLog = []

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        self.pins = []
        self.checks = []

    # quân cờ sau khi di chuyển thì vị trí bắt đầu sẽ được làm trống và vị trí kết thúc sẽ được cập nhập hình ảnh
    def makeMove(self, move):
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
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    # '''các nước đi cần xem xét kểm tra'''
    def getValidMoves(self):  # loại bỏ các nước đi không hợp lệ làm cho vua bị chiếu
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  # quân cờ đang chiếu
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i,
                                       kingCol + check[3] * i)  # xác định các ô nằm giữa quân vua và quân đang chiếu
                        validSquares.append(validSquare)
                        if validSquares[0] == checkRow and validSquares[
                            1] == checkCol:  # vòng lặp dừng lại khi gặp quân cờ đang chiếu
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        return moves

    def inCheck(self):  # kiểm tra xem vua của người chơi hiện tại đang bị chiếu ko
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

    def checkForPinsAndChecks(self):  # kiểm tra quân vua có bị chiếu không và các quân bị ghim
        pins = []  # danh sách các quân cờ bị ghim
        checks = []  # danh sách các quân đang chiếu vua
        inCheck = False

        if self.whiteToMove:  # nếu trắng di chuyển
            enemyColor = 'b'  # quân địch
            allyColor = 'w'  # quân đồng minh
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # vị trí quân cờ đồng minh có thể bị ghim
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if (0 <= j <= 3 and pieceType == 'R') or (4 <= j <= 7 and pieceType == 'B') or (
                                i == 1 and pieceType == 'P' and (
                                (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (
                                pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                            # (quân xe là vị trí 0,1,2,3) hoặc (quân tượng là vị trí 4,5,6,7) hoặc (quân tốt đen tấn công vị trí 6, 7 - quân tốt trắng tấn công vị trí 4,5 ) hoặc (quân hậu là all vị trí và quân vua cũng all vị trí)
                            # i là thể hiện đi một bước
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def getPawnMove(self, row, col, moves):  # xác định nước đi của quân tốt
        piecePinned = False  # quân tốt mặc định không bị ghim
        pinDirection = ()  # hướng bị ghim
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])  # xác định hướng bị ghim [2] lên xuống, [3] trái phải
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if self.board[row - 1][col] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col), (row - 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    if not piecePinned or pinDirection == (
                    -1, -1):  # nếu quân tố không bị ghim và hướng bị ghim trùng với hướng di chuyển của quân tốt
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            if self.board[row + 1][col] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def getKnightMoves(self, row, col, moves): # quân mã di chuyển
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]  # di chuyển cho quân mã từ trái vòng xuống dưới sang phải
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--" or endPiece[0] != allyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))

    def getRookMove(self, row, col, moves):  # quân xe di chuyển
        piecePinned = False
        pinDirection = ()  # hướng bị ghim
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # phải, trái, lên, xuống
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            i = 1
            while True:
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
                else:
                    break
                i = i + 1

    def getBishopMoves(self, row, col, moves): # quân tịnh di chuyển
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # (trái dưới - phải dưới, trái trên - phải trên)
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            i = 1
            while True:
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
                else:
                    break
                i = i + 1

    def getQueenMoves(self, row, col, moves):  # di chuyển quân hậu 22
        self.getRookMove(row, col, moves) # hàm hậu thì bao gồm hàm xe và tịnh
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves): # hàm di chuyển quân vua
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1),(-1, 0)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins , checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)

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
