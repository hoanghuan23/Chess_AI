"""
xử lý thông tin đầu vào của người dùng và hiển thị thông tin trạng thái trò chơi hiện tại
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512  # chieu rong va chieu cao cua quan co
DIMENSION = 8  # kich thuoc ban co vua se la 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Khởi tạo một dictionary hoặc hình ảnh. Sẽ gọi chính xác một lần trong phần main
'''

def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bN", "bB", "bQ", "bK", "bR"]
    IMAGES[pieces] = p.image,