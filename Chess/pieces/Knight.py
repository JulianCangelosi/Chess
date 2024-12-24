from Chess.Piece import Piece, Color


class Knight(Piece):
    def copy(self, position: 'Square') -> 'Knight':
        new_piece = Knight(self.color, position)
        new_piece.moved = self.moved
        return new_piece

    def value(self) -> int:
        return 3

    def can_move_to(self, target: 'Square') -> bool:
        origin: 'Square' = self.get_position()
        rank_difference: int = abs(origin.get_rank() - target.get_rank())
        file_difference: int = abs(origin.get_file() - target.get_file())

        # valid L-shaped moved
        return (file_difference == 1 and rank_difference == 2 or
                file_difference == 2 and rank_difference == 1)

    def can_target(self, square: 'Square') -> bool:
        return self.can_move_to(square)

    def __str__(self):
        if self.color is Color.white:
            return "n"
        else:
            return "N"
