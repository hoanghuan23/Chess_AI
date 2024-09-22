import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)] # trả về một nước đi ngẫu nhiên trong các nước đi hợp lệ

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppoentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxscore = STALEMATE
        elif gs.checkMate:
            opponentMaxscore = -CHECKMATE
        else:
            opponentMaxscore = -CHECKMATE
            for opponentMove in oppoentsMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxscore:
                    opponentMaxscore = score
                gs.undoMove()
        if opponentMaxscore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxscore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

# def findBestMoveMinMax(gs, validMoves, depth):
#     global nextMove
#     findMoveMinMax(gs, validMoves, depth, gs.whiteToMove)
#     return nextMove
#
# def findMoveMinMax(gs, validMoves, depth, whiteToMove):
#     global nextMove
#     if depth == 0:
#         return scoreMaterial(gs.board)
#
#     if whiteToMove:
#         maxScore = -CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = findMoveMinMax(gs, nextMoves, depth - 1, False)
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return maxScore
#     else:
#         minScore = CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = findMoveMinMax(gs, nextMoves, depth - 1, True)
#             if score < minScore:
#                 minScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return minScore
#
# def scoreBoard(gs):
#     if gs.checkMate:
#         if gs.whiteToMove:
#             return -CHECKMATE
#         else:
#             return CHECKMATE
#     elif gs.staleMate:
#         return STALEMATE
#     score = scoreMaterial(gs.board)
#     return score


def scoreMaterial(board): # đánh giá điểm số của bàn cờ hiện tại dựa trên giá trị của các quân cờ
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

