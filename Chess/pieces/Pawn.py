from Chess.Piece import Piece, Color, is_valid_diagonal, is_valid_file


class Pawn(Piece):

    def __init__(self, color, position):
        self.valid_en_passant_target = False
        super().__init__(color, position)

    def copy(self, position: 'Square') -> 'Pawn':
        new_piece: Pawn = Pawn(self.color, position)
        new_piece.moved = self.moved
        new_piece.valid_en_passant_target = self.valid_en_passant_target
        return new_piece

    def value(self) -> int:
        return 1

    def can_move_to(self, target: 'Square'):
        """
        Checks whether this Pawn can move to the user-specified target.
        :param target: target Square object
        :return: true if the Pawn can move to the user-specified target, otherwise false
        """
        origin: 'Square' = self.position
        result: bool = False
        if self.color is Color.white:
            # White Pawns capture diagonally up by one rank
            if target.is_occupied():
                if is_valid_diagonal(origin, target) and origin.get_rank() + 1 == target.get_rank():
                    result = True
                    self.valid_en_passant_target = False
            # White pawns can always move up one rank (row)
            elif is_valid_file(origin, target) and origin.get_rank() + 1 == target.get_rank():
                result = True
                self.valid_en_passant_target = False
            # White pawns can move up two ranks (rows) on first move
            elif is_valid_file(origin, target) and origin.get_rank() + 2 == target.get_rank() and not self.moved:
                result = True
                self.valid_en_passant_target = True
        else:
            # Black Pawns capture diagonally down by one rank
            if target.is_occupied():
                if is_valid_diagonal(origin, target) and origin.get_rank() - 1 == target.get_rank():
                    result = True
                    self.valid_en_passant_target = False
            # Black pawns can always move down one rank (row)
            elif is_valid_file(origin, target) and origin.get_rank() - 1 == target.get_rank():
                result = True
                self.valid_en_passant_target = False
            # Black pawns can move down two ranks (rows) on first move
            elif is_valid_file(origin, target) and origin.get_rank() - 2 == target.get_rank() and not self.moved:
                result = True
                self.valid_en_passant_target = True

        return result

    def can_target(self, square: 'Square'):
        origin: 'Square' = self.position
        result: bool = False
        if self.color is Color.white:
            # White Pawns capture diagonally up by one rank
            if is_valid_diagonal(origin, square) and origin.get_rank() + 1 == square.get_rank():
                result = True
        else:
            if is_valid_diagonal(origin, square) and origin.get_rank() - 1 == square.get_rank():
                result = True

        return result

    def can_en_passant_to(self, target_square: 'Square', target_pawn: 'Pawn') -> bool:
        # if the target pawn is None or if the target square is occupied, return False
        if type(target_pawn) is not Pawn or target_square.is_occupied():
            return False

        target_square_rank: int = target_square.get_rank()
        target_square_file: int = target_square.get_file()
        target_pawn_rank: int = target_pawn.get_position().get_rank()
        target_pawn_file: int = target_pawn.get_position().get_file()
        result: bool = False

        # If self is a white pawn:
        if self.color == Color.white:
            # if it is moving up one rank
            if (target_square_rank - 1 == target_pawn_rank and
                    # if it is moving by one file (either left OR right)
                    abs(target_square_file - self.get_position().get_file()) == 1 and
                    # if the target pawn is in the correct position for en passant
                    target_pawn_rank == target_square_rank - 1 and target_pawn_file == target_square_file and
                    # if the target pawn is a black pawn
                    target_pawn.get_color() == Color.black):
                result = True
        # Else if self is a black pawn
        else:
            # if it is moving down one rank
            if (target_square_rank + 1 == target_pawn_rank and
                    # if it is moving by one file (either left OR right)
                    abs(target_square_file - self.get_position().get_file()) == 1 and
                    # if the target pawn is in the correct position for en passant
                    target_pawn_rank == target_square_rank + 1 and target_pawn_file == target_square_file and
                    # if the target pawn is a white pawn
                    target_pawn.get_color() == Color.white):
                result = True
        return result

    def en_passant_to(self, target_square: 'Square', target_pawn: 'Pawn') -> None:
        self.move_to(target_square)
        target_pawn.capture()
        self.valid_en_passant_target = False

    def __str__(self) -> str:
        if self.color is Color.white:
            # white pieces are lowercase
            return "p"
        else:
            # black pieces are uppercase
            return "P"
