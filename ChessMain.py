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
    # print(gs.board)
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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
            color = colorother[((row + col) % 2)]                # light_color if (row + col) % 2 ==0 else dark_color
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blits()


if __name__ == "__main__":
    main()