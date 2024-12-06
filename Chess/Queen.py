from Square import Square
from Piece import Piece, Color, is_valid_file, is_valid_rank, is_valid_diagonal


class Queen(Piece):
    def copy(self, location: Square):
        new_piece = Queen(self.color, location)
        new_piece.moved = self.moved
        return new_piece

    def value(self) -> int:
        return 9

    def can_move_to(self, target: Square) -> bool:
        origin: Square = self.get_position()
        rank_difference: int = abs(origin.get_rank() - target.get_rank())
        file_difference: int = abs(origin.get_file() - target.get_file())

        if origin == target:
            return False

        return (is_valid_file(origin, target) or
                is_valid_rank(origin, target) or
                is_valid_diagonal(origin, target))

    def can_target(self, square: Square) -> bool:
        return self.can_move_to(square)

    def __str__(self) -> str:
        if self.color is Color.white:
            return "q"
        else:
            return "Q"
