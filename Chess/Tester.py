from Player import Player
from Board import Board
from enum import Enum, auto
from Piece import Color
from Pawn import Pawn
from Knight import Knight
from Square import Square

# def make_move(move, board):
#     split_input = move.split(" ")
#     origin = split_input[0]
#     target = split_input[1]
#     color = board.square_at(origin).get_occupant().color
#     if color == Color.white:
#         white.make_move(origin, target)
#     else:
#         black.make_move(origin, target)


# _board = Board()
#
# white = Player(Color.white, _board)
# black = Player(Color.black, _board)
# white.opponent = black
# black.opponent = white
#
# white.make_move("e2", "e4")
# white.make_move("f1", "c4")
# white.make_move("g1", "h3")
# white.make_move("d1", "d2")
# white.make_move("d2", "d4")
# white.make_move("c1", "e3")
# white.make_move("b1", "a3")
# white.make_move("d1", "d2")
#
# black.make_move("d7", "d5")
# black.make_move("e7", "e5")
# black.make_move("c8", "f5")
# black.make_move("f8", "c5")
# black.make_move("b8", "c6")
# black.make_move("g8", "h6")
# black.make_move("d8", "d7")
#
# # White, Kingside
# # white.make_move("e1", "g1")
#
# # White, Queenside
# white.make_move("e1", "c1")
#
# # Black, Kingside
# # black.make_move("e8", "g8")
#
# # Black, Queenside
# black.make_move("e8", "c8")
#
# print(_board)

board = Board()
white = Player(Color.white, board)
black = Player(Color.black, board)
white.opponent = black
black.opponent = white

print(board)

white.make_move("a7", "a8")

if white.pawn_promotion():
    print(board)

for piece in white.pieces:
    print(f"{piece} at {piece.coord_string()}")
