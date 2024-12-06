from Piece import Piece, Color


class Bishop(Piece):
    def copy(self, position) -> 'Bishop':
        new_bishop: Bishop = Bishop(self.color, position)
        new_bishop.moved = self.moved
        return new_bishop

    def value(self) -> int:
        return 3

    def can_move_to(self, target) -> bool:
        origin: 'Square' = self.get_position()
        rank_difference: int = abs(origin.get_rank() - target.get_rank())
        file_difference: int = abs(origin.get_file() - target.get_file())

        # valid diagonal
        return file_difference == rank_difference

    def can_target(self, square) -> bool:
        return self.can_move_to(square)

    #
    def __str__(self) -> str:
        if self.color is Color.white:
            return "b"
        else:
            return "B"
