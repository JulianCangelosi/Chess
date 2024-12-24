from typing import Optional

from Player import Player
from Board import Board
from enum import Enum, auto
from Chess.Piece import Color


class State(Enum):
    SETUP = auto()
    PROMPT_MOVE_WHITE = auto()
    VALIDATE_INPUT_WHITE = auto()
    EXECUTE_MOVE_WHITE = auto()
    SURVEY_BOARD_WHITE = auto()
    INVALID_MOVE_WHITE = auto()
    PROMPT_MOVE_BLACK = auto()
    VALIDATE_INPUT_BLACK = auto()
    EXECUTE_MOVE_BLACK = auto()
    SURVEY_BOARD_BLACK = auto()
    INVALID_MOVE_BLACK = auto()
    GAME_OVER = auto()


def main():
    state: State = State.SETUP

    game_over: bool = False
    board: Board = Board(True)
    white: Player = Player(Color.white, board)
    black: Player = Player(Color.black, board)
    origin: Optional[str] = None
    target: Optional[str] = None
    
    while not game_over:
        match state:
            case State.SETUP:
                # print the board
                print(board)
                state = State.PROMPT_MOVE_WHITE
            # ======================================================================
            #                          WHITE'S TURN
            # ======================================================================
            # Prompt white to input a move
            case State.PROMPT_MOVE_WHITE:
                origin, target = prompt("White")
                state = State.VALIDATE_INPUT_WHITE
            # Ensure white's input is a valid format.
            # If the input is invalid, set state to INVALID_MOVE_WHITE,
            # else set state to EXECUTE_MOVE_WHITE
            case State.VALIDATE_INPUT_WHITE:
                if origin == target or len(origin) != 2 or len(target) != 2:
                    state = State.INVALID_MOVE_WHITE
                else:
                    state = State.EXECUTE_MOVE_WHITE
            # Print an invalid move message
            # set the state to INVALID_MOVE_WHITE
            case State.INVALID_MOVE_WHITE:
                print("Invalid move! Try again")
                state = State.PROMPT_MOVE_WHITE
            # Attempt to execute the player's move.
            # If the move is executed successfully, set state to SURVEY_BOARD_WHITE
            # else, set the state to INVALID_MOVE_WHITE
            case State.EXECUTE_MOVE_WHITE:
                if white.make_move(origin, target):
                    print(board)
                    state = State.SURVEY_BOARD_WHITE
                else:
                    state = State.INVALID_MOVE_WHITE
            case State.SURVEY_BOARD_WHITE:
                if white.pawn_promotion():
                    print(board)
                state = State.PROMPT_MOVE_BLACK
            # ======================================================================
            #                          BLACK'S TURN
            # ======================================================================
            case State.PROMPT_MOVE_BLACK:
                print(f"Current: {state}")
                origin, target = prompt("Black")
                state = State.VALIDATE_INPUT_BLACK
            case State.VALIDATE_INPUT_BLACK:
                print(f"Current: {state}")
                if origin == target or len(origin) != 2 or len(target) != 2:
                    state = State.INVALID_MOVE_BLACK
                else:
                    state = State.EXECUTE_MOVE_BLACK
            case State.EXECUTE_MOVE_BLACK:
                print(f"Current: {state}")
                if black.make_move(origin, target):
                    print(board)
                    state = State.SURVEY_BOARD_BLACK
                else:
                    state = State.INVALID_MOVE_BLACK
            case State.SURVEY_BOARD_BLACK:
                print(f"Current: {state}")
                if black.pawn_promotion():
                    print(board)
                state = State.PROMPT_MOVE_WHITE
            case State.INVALID_MOVE_BLACK:
                print(f"Current: {state}")
                print("Invalid move! Try again")
                state = State.PROMPT_MOVE_BLACK


def prompt(color):
    input_string = input(f"{color}: Enter a move (e.g. 'a2 c4'): ")
    split_input = input_string.split(" ")
    origin = split_input[0]
    target = split_input[1]
    return origin, target

if __name__ == "__main__":
    main()
