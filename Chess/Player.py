from typing import Optional
from Board import Board
from Chess.Piece import Color
from Chess.pieces.King import King
from Chess.pieces.Queen import Queen
from Chess.pieces.Bishop import Bishop
from Chess.pieces.Rook import Rook
from Chess.pieces.Knight import Knight
from Chess.pieces.Pawn import Pawn
from enum import Enum, auto


class Pieces(Enum):
    KING = auto()
    QUEEN = auto()
    KINGSIDE_BISHOP = auto()
    QUEENSIDE_BISHOP = auto()
    KINGSIDE_KNIGHT = auto()
    QUEENSIDE_KNIGHT = auto()
    KINGSIDE_ROOK = auto()
    QUEENSIDE_ROOK = auto()


class Player:
    def __init__(self, color: Color, board: Board, pieces: list['Piece'] = None):
        self.color: Color = color
        # two players have the same board as part of their internal state
        self.board: Board = board
        # Each player's pieces are stored in a list for easy iteration
        self.pieces: list['Piece'] = []
        self.opponent: Optional[Player] = None
        self.king: Optional[King] = None
        self.is_valid_en_passant_target: bool = False

        if pieces is None:
            if self.color == Color.white:
                self.king = King(self.color, board.square_at("e1"))
                self.pieces.append(self.king)
                self.pieces.append(Queen(self.color, board.square_at("d1")))
                self.pieces.append(Bishop(self.color, board.square_at("f1")))
                self.pieces.append(Bishop(self.color, board.square_at("c1")))
                self.pieces.append(Knight(self.color, board.square_at("g1")))
                self.pieces.append(Knight(self.color, board.square_at("b1")))
                self.pieces.append(Rook(self.color, board.square_at("h1")))
                self.pieces.append(Rook(self.color, board.square_at("a1")))
                # Construct and place Pawns
                for file in range(8):
                    self.pieces.append(Pawn(self.color, board.square_at_index(1, file)))

            # If color is black
            else:
                self.king = King(self.color, board.square_at("e8"))
                self.pieces.append(self.king)
                self.pieces.append(Queen(self.color, board.square_at("d8")))
                self.pieces.append(Bishop(self.color, board.square_at("f8")))
                self.pieces.append(Bishop(self.color, board.square_at("c8")))
                self.pieces.append(Knight(self.color, board.square_at("g8")))
                self.pieces.append(Knight(self.color, board.square_at("b8")))
                self.pieces.append(Rook(self.color, board.square_at("h8")))
                self.pieces.append(Rook(self.color, board.square_at("a8")))
                # Construct and place Pawns
                for file in range(8):
                    self.pieces.append(Pawn(self.color, board.square_at_index(6, file)))

        else:
            self.pieces = pieces

    def copy(self) -> 'Player':
        """
        Returns a copy of the player.
        The player copy has a new opponent, which is a copy of the og player's opponent.
        The player copy has a new board, which has all the player copy's pieces in the same positions
        as the og players pieces
        The player copy has new pieces, which have the same internal state as the og players pieces (e.g. if the og
        player has not moved a pawn, then the player copy's pawn can still move forward 2 ranks).
        """
        # empty board to add the new pieces to
        # The new pieces come from the player copy, and then are put on to a blank board, so no need to copy the board,
        # which is why the board doesn't have a copy method.
        board_copy: Board = Board()
        self_copy: Player = Player(self.color, board_copy, [])
        self_copy.is_valid_en_passant_target = self.is_valid_en_passant_target
        opponent_copy: Player = Player(self.opponent.color, board_copy, [])
        opponent_copy.is_valid_en_passant_target = self.opponent.is_valid_en_passant_target
        self_copy.opponent = opponent_copy
        opponent_copy.opponent = self_copy

        # This loop copies each piece in the og player's piece list, copies it, adds it to the new (blank) board,
        # and then appends it to the player copy's piece list
        for piece in self.pieces:
            self_piece_position: 'Square' = piece.get_position()
            if piece.is_on_square():
                self_copy_piece_position = board_copy.square_at(self_piece_position.identifier())
            else:
                self_copy_piece_position = None
            self_copy.pieces.append(piece.copy(self_copy_piece_position))

        # This loop copies each piece in the og opponent's piece list, copies it, adds it to the new (blank) board
        # and then appends it to the opponent copy's piece list
        for piece in self.opponent.pieces:
            opponent_piece_position = piece.get_position()
            if piece.is_on_square():
                opponent_copy_piece_position = board_copy.square_at(opponent_piece_position.identifier())
            else:
                opponent_copy_piece_position = None
            opponent_copy.pieces.append(piece.copy(opponent_copy_piece_position))

        # Because players have a king variable in their internal state, they must be updated as well.
        self_copy.king = self_copy.pieces[0]
        opponent_copy.king = opponent_copy.pieces[0]

        # returns the player copy. The opponent copy is part of the player copy's internal state, so it doesn't need to
        # be returned
        return self_copy

    def can_make_move(self, origin, target) -> bool:
        """
        Checks whether this player can move from the specified origin to the specified target.
        :param origin: origin Square instance
        :param target: target Square instance
        :return: True if the player can make the move, otherwise False
        """
        result: bool = True
        origin_occupant: 'Piece' = origin.get_occupant()

        if not origin.is_occupied():
            return False

        # return true if the origin and target squares are valid, the move is clear, and if it's a legal move for the
        # piece at the origin square

        if not self.is_valid_origin(origin):
            result = False
        if not self.is_valid_target(target):
            result = False
        if not origin_occupant.can_move_to(target):
            result = False
        if not self.is_clear_move(origin, target):
            result = False

        return result

    def make_move(self, origin_id: str, target_id: str) -> bool:
        """
        Attempts to move the Piece at the origin Square to the target square.
        :param origin_id: origin square string identifier of intended move
        :param target_id: target square string identifier of intended move
        :return True if move executed successfully, else false
        """
        # use the origin square's string identifier to grab the origin Square instance
        origin: 'Square' = self.board.square_at(origin_id)
        # use the target square's string identifier to grab the target Square instance
        target: 'Square' = self.board.square_at(target_id)
        piece: 'Piece' = origin.get_occupant()
        result: bool = False

        # check if the intended move is a valid standard chess move
        if self.can_make_move(origin, target):
            piece.move_to(target)
            result = True
        # check if the intended move is a valid en passant
        elif self.can_make_en_passant(origin, target):
            self.make_en_passant(origin, target)
            result = True
        # check if the intended move is a valid castle move
        elif self.can_make_castle(origin, target):
            self.make_castle(origin, target)
            result = True
        #
        if self.is_pawn_move_by_two_ranks(origin, target, piece):
            self.is_valid_en_passant_target = True
        else:
            self.is_valid_en_passant_target = False

        return result

    def can_make_en_passant(self, origin: 'Square', target: 'Square') -> bool:
        """
        Checks whether this player can make the enpassant move.
        :param origin: origin Square instance
        :param target: target Square instance
        :return: True if the player can make the enpassant, otherwise False
        """
        if not origin.is_occupied() or target.is_occupied():
            return False
        if type(origin.get_occupant()) is not Pawn:
            return False
        if not self.opponent.is_valid_en_passant_target:
            return False
        if not self.board.is_clear_diagonal(origin, target):
            return False

        target_pawn_file: int = target.get_file()
        origin_occupant = origin.get_occupant()

        if self.color == Color.white:
            target_pawn_rank = target.get_rank() - 1
        else:
            target_pawn_rank = target.get_rank() + 1

        if target_pawn_rank > 7 or target_pawn_rank < 0:
            return False

        target_pawn: 'Piece' = self.board.square_at_index(target_pawn_rank, target_pawn_file).get_occupant()

        if type(target_pawn) is not Pawn:
            return False

        return origin_occupant.can_en_passant_to(target, target_pawn)

    def make_en_passant(self, origin: 'Square', target: 'Square'):
        """
        Attempts to make the enpassant move.
        :param origin: origin Square instance
        :param target: target Square instance
        :return: True if move executed successfully, otherwise False
        """
        origin_occupant = origin.get_occupant()
        if self.color == Color.white:
            target_pawn_rank = target.get_rank() - 1
        else:
            target_pawn_rank = target.get_rank() + 1

        target_pawn_file: int = target.get_file()
        target_pawn: 'Piece' = self.board.square_at_index(target_pawn_rank, target_pawn_file).get_occupant()

        origin_occupant.en_passant_to(target, target_pawn)

    def can_make_castle(self, origin: 'Square', target: 'Square') -> bool:
        """
        Checks whether this player can make the castle move.
        :param origin: origin Square instance
        :param target: target Square instance
        :return: True if the player can make the castle, otherwise False
        """
        if origin is not self.king.get_position():
            return False

        result: bool = False

        if self.color is Color.white:
            k_side_castle_target: 'Square' = self.board.square_at("g1")
            q_side_castle_target: 'Square' = self.board.square_at("c1")
        else:
            k_side_castle_target: 'Square' = self.board.square_at("g8")
            q_side_castle_target: 'Square' = self.board.square_at("c8")

        if target is k_side_castle_target:
            result = self.can_castle(True)
        elif target is q_side_castle_target:
            result = self.can_castle(False)
        return result

    def make_castle(self, origin: 'Square', target: 'Square') -> None:
        """
        Attempts to make the castle move.
        :param origin: origin Square instance
        :param target: target Square instance
        :return: True if move executed successfully, otherwise False
        """
        if origin is not self.king.get_position():
            return

        # White, kingside castle
        if self.color is Color.white and target is self.board.square_at("g1"):
            rook = self.board.square_at("h1").get_occupant()
            rook.move_to(self.board.square_at("f1"))
        # White, queenside castle
        elif self.color is Color.white and target is self.board.square_at("c1"):
            rook = self.board.square_at("a1").get_occupant()
            rook.move_to(self.board.square_at("d1"))
        # Black, kingside castle
        elif self.color is Color.black and target is self.board.square_at("g8"):
            rook = self.board.square_at("h8").get_occupant()
            rook.move_to(self.board.square_at("f8"))
        # Black, queenside castle
        elif self.color is Color.black and target is self.board.square_at("c8"):
            rook = self.board.square_at("a8").get_occupant()
            rook.move_to(self.board.square_at("d8"))
        self.king.move_to(target)

    def is_valid_origin(self, origin: 'Square') -> bool:
        """
        Checks whether the origin square is valid (i.e. whether the player has a piece at the origin).
        :param origin: origin Square instance
        :return: True if the origin square is valid, otherwise False
        """
        return origin.is_occupied() and origin.get_occupant().get_color() is self.color

    def is_valid_target(self, target: 'Square') -> bool:
        """
        Checks whether the intended target Square is valid.
        :param target: intended target Square
        :return: True if the target Square is unoccupied or is occupied by an opponent piece, else False
        """
        return not target.is_occupied() or target.get_occupant().get_color() is not self.color

    def is_clear_move(self, origin: 'Square', target: 'Square') -> bool:
        """
        Helper method to check if this player's intended move is clear or if the piece is a Knight
        :param origin: origin Square instance
        :param target: target Square instance
        :return: True if the intended move can be made successfully, else false
        """

        # Return True if any of the following conditions are met:
            # The intended move is clear file (up/down)
            # The intended move is clear rank (left/right)
            # The intended move is clear diagonal
            # The piece to move is a knight (since the knight moves in 'L' shape and can 'hop' over other pieces)
        # Otherwise, return False

        return (self.board.is_clear_rank(origin, target) or
            self.board.is_clear_file(origin, target) or
            self.board.is_clear_diagonal(origin, target) or
            type(origin.get_occupant()) is Knight)

    def pawn_promotion(self):
        """
        Promotes a pawn to another piece type
        :return: True if pawn promoted successfully, otherwise False
        """
        last_rank: int = 7 if self.color is Color.white else 0
        result: bool = False

        for file in range(8):
            current_square = self.board.square_at_index(last_rank, file)
            if type(current_square.get_occupant()) is Pawn:
                self.pieces.remove(current_square.get_occupant())
                self.prompt_promotion(current_square)
                result = True
        return result

    def prompt_promotion(self, position) -> None:
        """
        Prompts the player to specify what piece type to promote the pawn to using the console.
        :param position: position of the pawn
        """
        promotion_menu = ["Queen", "Bishop", "Knight", "Rook"]
        piece_type = input(f'{self.color}: Choose promotion piece \n({promotion_menu}): ').lower()
        new_piece = None
        # Assign Construct the new piece
        if piece_type == "queen":
            new_piece = Queen(self.color, position)
        elif piece_type == "bishop":
            new_piece = Bishop(self.color, position)
        elif piece_type == "knight":
            new_piece = Knight(self.color, position)
        elif piece_type == "rook":
            new_piece = Rook(self.color, position)
        else:
            print("Invalid input!")
            self.prompt_promotion(position)
        self.pieces.append(new_piece)

    def can_target_square(self, square) -> bool:
        """
        Checks whether this player can target a square.
        :param square: square to check
        :return: True if the square can be targeted, otherwise False
        """
        result = False
        for piece in self.pieces:
            if piece.is_on_square() and self.can_make_move(piece.get_position(), square) and piece.can_target(square):
                result = True
        return result

    def is_in_check(self) -> bool:
        """
        Checks whether this player is in check.
        :return: True if the player is in check, otherwise False
        """
        return self.opponent.can_target_square(self.king.get_position())

    def is_in_checkmate(self) -> bool:
        """
        Checks whether this player is in checkmate.
        :return: True if the player is in checkmate, otherwise False
        """
        result = True
        legal_moves = self.legal_moves()
        # for each piece:
        for piece in legal_moves:
            # for each legal target:
            for target in legal_moves[piece]:
                # simulate move to the target
                origin_id = piece.coord_string()
                target_id = target.identifier()
                self_copy = self.copy()
                self_copy.make_move(origin_id, target_id)
                # if this player is not in check:
                if not self_copy.is_in_check():
                    result = False
        return result

    def print_legal_moves(self) -> None:
        """
        Prints the player's legal moves to the console. (Helper method)
        """
        self_legal_moves = self.legal_moves()

        for piece in self_legal_moves:
            print(f"{piece} at {piece.get_position().identifier()}", end=": ")
            for target in self_legal_moves[piece]:
                print(target.identifier(), end=",")
            print()

    def legal_target_positions(self, piece) -> list:
        """
        Creates a list of a piece's legal target squares.
        :param piece: piece instance
        :return: list of legal target squares
        """
        legal_target_positions = []
        for file in range(8):
            for rank in range(8):
                origin = piece.get_position()
                target = self.board.squares[rank][file]
                if self.can_make_move(origin, target) or self.can_make_en_passant(origin, target):
                    legal_target_positions.append(target)
        return legal_target_positions

    def legal_moves(self) -> dict:
        """
        Creates a dictionary of all legal moves for the player.
        :return: dictionary of legal moves
        """
        legal_moves_dict: dict = {}
        for piece in self.pieces:
            if piece.is_on_square():
                legal_moves_dict[piece] = self.legal_target_positions(piece)
        return legal_moves_dict

    def is_white(self):
        """
        Checks whether this player is white.
        :return: True if the player is white, otherwise False
        """
        return self.color == Color.white

    def can_castle(self, kingside) -> bool:
        """
        Checks whether this player is castle.
        :param kingside: boolean parameter determining whether to check for kingside castle
        :return: True if the player can castle, otherwise False
        """
        rook = self.pieces[9] if kingside else self.pieces[8]
        result = True
        target_file = 6 if kingside else 2
        target_rank = 0 if self.is_white() else 7
        target = self.board.square_at_index(target_rank, target_file)

        # Conditions for castling:
        # player cannot be in check
        if self.is_in_check():
            result = False
        # King cannot have moved
        elif self.king.has_moved():
            result = False
        # Rook cannot have moved
        elif rook.has_moved():
            result = False
        # path between king and rook must be clear
        elif not self.board.is_clear_rank(self.king.get_position(), target):
            result = False
        return result

    def is_pawn_move_by_two_ranks(self, origin, target, piece) -> bool:
        """
        Checks whether a move is a pawn move by two ranks.
        :param origin: origin Square
        :param target: target Square
        :param piece: piece instance
        :return: True if the move is a pawn move by two ranks, otherwise False
        """
        origin_rank = origin.get_rank()
        origin_file = origin.get_file()
        target_rank = target.get_rank()
        target_file = target.get_file()
        result = True

        file_difference = abs(origin_file - target_file)
        rank_difference = abs(origin_rank - target_rank)

        if file_difference != 0:
            result = False
        elif rank_difference != 2:
            result = False
        elif type(piece) is not Pawn:
            result = False

        return result
