"""
lưu dữ tất cả thông tin về trạng thái hiện tại của trò chơi, giữ nhật ký các nước đi để có thể hoàn lại
"""


class Game_state():
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
        # xác định xem lượt của ai đi trắng rồi tới đen
        self.whiteToMove = True
        # danh sách nhật ký nước đi
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove


class Move():
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

    def getChessNotation(self):  # chuyển đổi 2 vị trí là vị trí trước khi và sau khi di chuyển
        return "di chuyen " + self.getRankFile(self.startRow, self.startCol) + " sang " + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):  # chuyển đổi một cặp hàng thành ký hiệu cờ vua (ví dụ như 6,4 thành e,2)
        return self.colsToFiles[col] + self.rowsToRanks[row]


