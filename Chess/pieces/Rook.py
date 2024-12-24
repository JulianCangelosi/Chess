from Chess.Piece import Piece, Color, is_valid_rank, is_valid_file


class Rook(Piece):
    def copy(self, location: 'Square'):
        new_piece = Rook(self.color, location)
        new_piece.moved = self.moved
        return new_piece

    def value(self) -> int:
        return 5

    def can_move_to(self, target: 'Square') -> bool:
        origin = self.get_position()
        # valid rank
        return is_valid_rank(origin, target) or is_valid_file(origin, target)

    def can_target(self, square) -> bool:
        return self.can_move_to(square)

    def __str__(self) -> str:
        if self.color == Color.white:
            return "r"
        else:
            return "R"
