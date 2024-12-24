from typing import Optional
from Chess.Piece import Piece, Color


class Square:

    def __init__(self, rank: int, file: int, occupant: 'Piece' = None):
        self.rank = rank    # rank = Row
        self.file = file    # file = Column
        self.occupant = occupant

    def copy(self) -> 'Square':
        square_copy = Square(self.rank, self.file)
        if self.is_occupied():
            occupant_copy = self.occupant.copy()
            occupant_copy.set_position(square_copy)
        else:
            occupant_copy = None
        square_copy.set_occupant(occupant_copy)
        return square_copy

    def get_rank(self) -> int:
        return self.rank

    def get_file(self) -> int:
        return self.file

    def set_occupant(self, new_occupant: Piece) -> None:
        self.occupant = new_occupant

    def is_occupied(self) -> bool:
        return self.occupant is not None

    def get_occupant(self) -> Piece:
        return self.occupant

    def get_occupant_color(self) -> Optional[Color]:
        if not self.is_occupied():
            return None
        else:
            return self.occupant.get_color()

    def identifier(self) -> str:
        files: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks: list[str] = ['1', '2', '3', '4', '5', '6', '7', '8']
        file_id: int = files[self.file]
        rank_id: int = ranks[self.rank]
        return f"{file_id}{rank_id}"

    def display(self) -> str:
        return f"{self.get_occupant()}" if self.is_occupied() else ""

    def occupant_is_white(self) -> bool:
        result: bool = False
        if self.is_occupied():
            if self.get_occupant().get_color() == Color.white:
                result = True
        return result

    def __str__(self) -> str:
        if self.is_occupied():
            return f" {self.get_occupant()} |"
        else:
            return f"   |"
