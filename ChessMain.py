"""
xử lý thông tin đầu vào của người dùng và hiển thị thông tin trạng thái trò chơi hiện tại
"""

import pygame as p
from Chess import ChessEngine, ChessAI

p.init()
WIDTH = HEIGHT = 512  # chieu rong va chieu cao cua quan co
DIMENSION = 8  # kich thuoc ban co vua se la 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

light_color = (240, 240, 240)  # Màu sáng
dark_color = (100, 100, 100)  # Màu tối
highlight_color = (255, 255, 100)
colors = [p.Color(light_color), p.Color(dark_color)]

# Load sound
move_sound = p.mixer.Sound("song/dichuyen.mp3")
check_sound = p.mixer.Sound("song/chieu.mp3")
nhapthanh_sound = p.mixer.Sound("song/nhapthanh.mp3")
anquan_sound = p.mixer.Sound("song/anquan.mp3")

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
    p.mixer.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.Game_state()
    validMoves = gs.getValidMoves()  # lấy tất cả các nước đi hợp lệ trong bàn cờ vua
    moveMade = False  # biến này để xác định xem người dùng đã thực hiện nước đi chưa
    animate = False # biến này để xác định xem nước đi đã được thực hiện chưa
    loadImages()
    running = True
    sqSelected = ()  # theo doi lan click chuot cuoi cung
    playerClicks = []  # theo doi so lan click chuot cua nguoi choi (vi du [2,4] => [4,6])
    gameOver = False
    playerOne = True  # nếu người chơi quân trắng thì True, nếu máy chơi thì False
    playerTwo = False # tương tự nhưng màu đen
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:  # kiểm tra xem nước đi có hợp lệ không
                                gs.makeMove(validMoves[i])
                                play_sound(validMoves[i], gs)
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # hoàn tác lại khi tôi nhấn z
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: # reset lại bàn cờ khi tôi nhấn r
                    gs = ChessEngine.Game_state()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        # AI tìm kieem
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            play_sound(AIMove, gs)
            moveMade = True
            animate = True

        if moveMade:  # sau khi nước đi được thực hiện thì sẽ cập nhật lại danh sách các nước đi hợp lệ
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

# hiển thị các ô vuông mà người dùng có thể di chuyển và ô vuông đang được chọn
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"):  # kiểm tra xem người chơi có chọn quân cờ của mình không
            # vẽ ô vuông đã chọn
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # đặt độ mờ của ô vuông
            s.fill(p.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # vẽ các nước đi hợp lệ
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    dot_x = (move.endCol * SQ_SIZE) + SQ_SIZE // 2
                    dot_y = (move.endRow * SQ_SIZE) + SQ_SIZE // 2
                    p.draw.circle(screen, p.Color("Black"), (dot_x, dot_y), 10)


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # vẽ những ô vuông trên bảng
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # vẽ các quân cờ lên trên các hình vuông đó


def drawBoard(screen):
    global colors
    colorother = [p.Color("light gray"), p.Color("dark green")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colorother[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def play_sound(move, gs):
    if move.isCastleMove:
        nhapthanh_sound.play()
    elif move.isEnpassantMove or move.pieceCaptured != "--":
        anquan_sound.play()
    else:
        move_sound.play()

    # if gs.inCheck:
    #     check_sound.play()

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# vẽ nước đi đã di chuyển
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 6  # di chuyển mỗi ô vuông trong 10 khung hình
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # xóa quân cờ đã di chuyển từ vị trí cũ
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # vẽ quân cờ đã di chuyển
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                     HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
if __name__ == "__main__":
    main()
