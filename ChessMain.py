"""
xử lý thông tin đầu vào của người dùng và hiển thị thông tin trạng thái trò chơi hiện tại
"""

import pygame as p
from Chess import ChessEngine

p.init()
WIDTH = HEIGHT = 512  # chieu rong va chieu cao cua quan co
DIMENSION = 8  # kich thuoc ban co vua se la 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

light_color = (240, 240, 240)  # Màu sáng
dark_color = (100, 100, 100)  # Màu tối
highlight_color = (255, 255, 100)

'''
Khởi tạo một dictionary hoặc hình ảnh. Sẽ gọi chính xác một lần trong phần main
'''


def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bN", "bB", "bQ", "bK", "bR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # truy cập hình ảnh bằng cách sử dụng folder IMAGES


'trình điều khiển chính nó sẽ xử lý thông tin đầu vào người dùng và cập nhật đồ họa'


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.Game_state()
    validMoves = gs.getValidMoves()  # lấy tất cả các nước đi hợp lệ trong bàn cờ vua
    moveMade = False  # biến này để xác định xem người dùng đã thực hiện nước đi chưa
    loadImages()
    running = True
    sqSelected = ()  # theo doi lan click chuot cuoi cung
    playerClicks = []  # theo doi so lan click chuot cua nguoi choi (vi du [2,4] => [4,6])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) vị trí của con mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # người dùng click cùng một vị trí
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # thêm vào  lần click chuột t1 và t2
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:  # nếu nước đi nằm trong nước các nước đi hợp lệ thì có thể di chuyển
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # hoàn tác lại khi tôi nhấn z
                    gs.undoMove()
                    moveMade = True
        if moveMade:  # sau khi nước đi được thực hiện thì sẽ cập nhật lại danh sách các nước đi hợp lệ
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)  # vẽ những ô vuông trên bảng
    drawPieces(screen, gs.board)  # vẽ các quân cờ lên trên các hình vuông đó


def drawBoard(screen):
    colorother = [p.Color("light gray"), p.Color("dark green")]
    colors = [p.Color(light_color), p.Color(dark_color)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colorother[((row + col) % 2)]  # light_color if (row + col) % 2 ==0 else dark_color
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
