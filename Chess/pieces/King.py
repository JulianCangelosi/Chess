from Chess.Piece import Piece, Color


class King(Piece):
    def copy(self, position: 'Square') -> 'King':
        """
        Returns a copy of the piece with
        """
        new_piece: 'King' = King(self.color, position)
        new_piece.moved = self.moved
        return new_piece

    def value(self) -> int:
        return 200

    def can_move_to(self, target: 'Square') -> bool:
        origin: 'Square' = self.get_position()
        rank_difference: int = abs(origin.get_rank() - target.get_rank())
        file_difference: int = abs(origin.get_file() - target.get_file())

        return rank_difference <= 1 and file_difference <= 1

    def can_target(self, square: 'Square') -> bool:
        return self.can_move_to(square)

    def __str__(self) -> str:
        if self.color is Color.white:
            return "k"
        else:
            return "K"
