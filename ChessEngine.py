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


class Move():
    def __init__(self, startSq, endSq, board):
        self.startSq = startSq[0]
        self.startSq = startSq[1]
        self.endSq = endSq[0]
        self.endSq = endSq[1]
