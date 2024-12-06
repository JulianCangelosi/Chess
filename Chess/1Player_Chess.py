from Player import Player
from Board import Board
from enum import Enum, auto
from Piece import Color
import random


class State(Enum):
    SETUP = auto()
    PROMPT_MOVE_WHITE = auto()
    SIMULATE_MOVE_WHITE = auto()
    CHECK_DETECT_WHITE = auto()
    EXECUTE_MOVE_WHITE = auto()
    SURVEY_BOARD_WHITE = auto()
    PROMPT_MOVE_BLACK = auto()
    SIMULATE_MOVE_BLACK = auto()
    CHECK_DETECT_BLACK = auto()
    EXECUTE_MOVE_BLACK = auto()
    SURVEY_BOARD_BLACK = auto()
    GAME_OVER = auto()


def main() -> None:
    state: State = State.SETUP

    game_over: bool = False
    board: Board = Board(True)
    white: Player = Player(Color.white, board)
    black: Player = Player(Color.black, board)
    white.opponent = black
    black.opponent = white

    while not game_over:
        match state:
            case State.SETUP:
                board.update_display()
                state = State.PROMPT_MOVE_WHITE
            case State.PROMPT_MOVE_WHITE:
                if len(board.selected_squares) == 1:
                    origin_sqr = board.square_at(board.selected_squares[0])
                    if (not origin_sqr.is_occupied() or
                            origin_sqr.get_occupant().get_color() != Color.white):
                        board.selected_squares.clear()

                if len(board.selected_squares) >= 2:
                    target_sqr = board.square_at(board.selected_squares[1])
                    if target_sqr.get_occupant_color() is Color.white:
                        board.selected_squares[0] = board.selected_squares[1]
                        board.selected_squares.remove(board.selected_squares[1])
                    else:
                        origin_str = board.selected_squares[0]
                        target_str = board.selected_squares[1]
                        board.selected_squares.clear()
                        state = State.SIMULATE_MOVE_WHITE
                else:
                    board.root.update()
            case State.SIMULATE_MOVE_WHITE:
                white_copy = white.copy()
                if white_copy.make_move(origin_str, target_str):
                    piece = board.square_at(origin_str).get_occupant()
                    state = State.CHECK_DETECT_WHITE
                else:
                    state = State.PROMPT_MOVE_WHITE
            case State.CHECK_DETECT_WHITE:
                if white_copy.is_in_check():
                    state = State.PROMPT_MOVE_WHITE
                else:
                    state = State.EXECUTE_MOVE_WHITE
                del white_copy
            case State.EXECUTE_MOVE_WHITE:
                if white.make_move(origin_str, target_str):
                    board.update_display()
                    print(f"White: {piece} from {origin_str} to {target_str}")
                    state = State.SURVEY_BOARD_WHITE
                else:
                    state = State.PROMPT_MOVE_WHITE
            case State.SURVEY_BOARD_WHITE:
                if white.pawn_promotion():
                    board.update_display()
                if black.is_in_checkmate():
                    print("BLACK IS IN CHECKMATE")
                    state = State.GAME_OVER
                else:
                    if black.is_in_check():
                        print("BLACK IS IN CHECK")
                    print("Black's turn")
                    state = State.PROMPT_MOVE_BLACK
            case State.PROMPT_MOVE_BLACK:
                moves_dict = black.legal_moves()
                piece_list = list(moves_dict.keys())

                if piece_list:
                    piece = random.choice(piece_list)
                    moves_list = moves_dict[piece]
                    if moves_list:
                        origin_str = piece.coord_string()
                        target = random.choice(moves_list)
                        target_str = target.identifier()
                        state = State.SIMULATE_MOVE_BLACK
                    else:
                        state = State.PROMPT_MOVE_BLACK
                else:
                    state = State.GAME_OVER

            case State.SIMULATE_MOVE_BLACK:
                black_copy = black.copy()
                if black_copy.make_move(origin_str, target_str):
                    state = State.CHECK_DETECT_BLACK
                else:
                    state = State.PROMPT_MOVE_BLACK
            case State.CHECK_DETECT_BLACK:
                if black_copy.is_in_check():
                    print(f"main: Cannot move from {origin_str} to {target_str}")
                    state = State.PROMPT_MOVE_BLACK
                else:
                    state = State.EXECUTE_MOVE_BLACK
                del black_copy
            case State.EXECUTE_MOVE_BLACK:
                if black.make_move(origin_str, target_str):
                    board.root.after(2000, board.update_display)
                    print(f"Black: {piece} from {origin_str} to {target_str}")
                    state = State.SURVEY_BOARD_BLACK
                else:
                    state = State.PROMPT_MOVE_BLACK
            case State.SURVEY_BOARD_BLACK:
                if black.pawn_promotion():
                    board.update_display()
                if white.is_in_checkmate():
                    print("WHITE IS IN CHECKMATE")
                    state = State.GAME_OVER
                else:
                    if white.is_in_check():
                        print("WHITE IS IN CHECK")
                    print("White's turn")
                    state = State.PROMPT_MOVE_WHITE
            case State.GAME_OVER:
                game_over = True

    board.root.mainloop()

if __name__ == "__main__":
    main()
