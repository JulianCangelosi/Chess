import tkinter as tk
from typing import Optional
from Chess.Piece import Color

from Square import Square


def is_valid_rank(origin: Square, target: Square) -> bool:
    return origin.get_rank() == target.get_rank()


def is_valid_file(origin: Square, target: Square) -> bool:
    return origin.get_file() == target.get_file()


def is_valid_diagonal(origin: Square, target: Square) -> bool:
    rank_difference: int = abs(origin.get_rank() - target.get_rank())
    file_difference: int = abs(origin.get_file() - target.get_file())
    return rank_difference == file_difference


class Board:
    def __init__(self, display: bool = False):
        self.squares: list[list[Optional[Square]]] = [[None for _ in range(8)] for _ in range(8)]
        for rank in range(8):
            for file in range(8):
                self.squares[rank][file] = Square(rank=rank, file=file, occupant=None)
        self.root = tk.Tk() if display else None
        self.root.title('Chess Board') if display else None
        self.board_frame = tk.Frame(self.root) if display else None
        self.board_frame.pack() if display else None
        self.selected_squares = [] if display else None
        self.images = self.load_images()
        # clear image for empty squares because for some reason the square dimensions are messed up if they don't
        # have an image.
        self.placeholder_image = tk.PhotoImage(width=64, height=64)

    def on_click(self, rank_no: int, file_no: int) -> None:
        """
        When the user clicks on a square, adds the
        """
        file_ids: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        file_id: str = file_ids[file_no]
        rank_id: str = f"{rank_no + 1}"
        square_id: str = f"{file_id}{rank_id}"
        self.selected_squares.append(square_id)

    def square_at_index(self, rank: int, file: int) -> Square:
        return self.squares[rank][file]

    def square_at(self, identifier: str) -> Square:
        file_char: str = identifier[0]
        rank_char: str = identifier[1]
        file_index: int = ord(file_char) - ord('a')
        rank_index: int = int(rank_char) - 1
        return self.square_at_index(rank_index, file_index)

    def is_clear_rank(self, origin: Square, target: Square) -> bool:
        is_clear: bool = is_valid_rank(origin, target)
        if is_clear:
            rank: int = origin.get_rank()
            for file in range(origin.get_file() + 1, target.get_file()):
                current = self.square_at_index(rank, file)
                if current.is_occupied():
                    is_clear = False
            for file in range(target.get_file() + 1, origin.get_file()):
                current = self.square_at_index(rank, file)
                if current.is_occupied():
                    is_clear = False
        return is_clear

    def is_clear_file(self, origin: Square, target: Square) -> bool:
        is_clear: bool = is_valid_file(origin, target)
        if is_clear:
            file: int = origin.get_file()
            for rank in range(origin.get_rank() + 1, target.get_rank()):
                current = self.square_at_index(rank, file)
                if current.is_occupied():
                    is_clear = False
            for rank in range(target.get_rank() + 1, origin.get_rank()):
                current = self.square_at_index(rank, file)
                if current.is_occupied():
                    is_clear = False
        return is_clear

    def is_clear_diagonal(self, origin: Square, target: Square) -> bool:
        rank_difference: int = abs(origin.get_rank() - target.get_rank())

        if not is_valid_diagonal(origin, target):
            return False

        rank_step = 1 if target.get_rank() > origin.get_rank() else -1
        file_step = 1 if target.get_file() > origin.get_file() else -1

        for i in range(1, rank_difference):
            rank = origin.get_rank() + i * rank_step
            file = origin.get_file() + i * file_step

            if self.square_at_index(rank, file).is_occupied():
                return False

        return True

    def load_images(self) -> dict[str, tk.PhotoImage]:
        """
        Load images for the chess pieces and return a dictionary mapping piece types to images.
        """
        images = {
            "white_king":   tk.PhotoImage(file="assets/White King.png"),
            "white_queen":  tk.PhotoImage(file="assets/White Queen.png"),
            "white_bishop": tk.PhotoImage(file="assets/White Bishop.png"),
            "white_knight": tk.PhotoImage(file="assets/White Knight.png"),
            "white_rook":   tk.PhotoImage(file="assets/White Rook.png"),
            "white_pawn":   tk.PhotoImage(file="assets/White Pawn.png"),
            "black_king":   tk.PhotoImage(file="assets/Black King.png"),
            "black_queen":  tk.PhotoImage(file="assets/Black Queen.png"),
            "black_bishop": tk.PhotoImage(file="assets/Black Bishop.png"),
            "black_knight": tk.PhotoImage(file="assets/Black Knight.png"),
            "black_rook":   tk.PhotoImage(file="assets/Black Rook.png"),
            "black_pawn":   tk.PhotoImage(file="assets/Black Pawn.png")
        }
        return images

    def update_display(self) -> None:
        light_color: str = '#F3CAAA'
        dark_color: str = '#B07F60'

        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for rank in range(8):
            for file in range(8):
                square: Square = self.squares[7 - rank][file]
                color: str = light_color if (rank + file) % 2 == 0 else dark_color

                if square.is_occupied():
                    occupant = square.get_occupant()
                    piece_color = "white" if occupant.get_color() == Color.white else "black"
                    piece_type = occupant.__class__.__name__.lower()  # Example: "king", "queen"
                    image_key = f"{piece_color}_{piece_type}"  # Example: "white_king"
                    piece_image = self.images.get(image_key)
                else:
                    # Use placeholder image for empty squares
                    piece_image = self.placeholder_image

                button = tk.Button(
                    self.board_frame,
                    image=piece_image,
                    height=64,
                    width=64,
                    bg=color,
                    command=lambda r=7 - rank, f=file: self.on_click(r, f),
                )
                button.image = piece_image  # Prevent image garbage collection
                button.grid(row=rank, column=file)

    def piece_at(self, identifier: str) -> 'Piece':
        return self.square_at(identifier).get_occupant()

    def __str__(self) -> str:
        rank = 7
        board_str = "     a   b   c   d   e   f   g   h\n"
        board_str += "   +---+---+---+---+---+---+---+---+\n"

        while rank >= 0:
            board_str += f" {rank + 1} |"
            for file in range(8):
                square = self.square_at_index(rank, file)
                board_str += square.__str__()
            board_str += f" {rank + 1}\n"
            board_str += "   +---+---+---+---+---+---+---+---+\n"
            rank -= 1

        board_str += "     a   b   c   d   e   f   g   h\n"
        return board_str
