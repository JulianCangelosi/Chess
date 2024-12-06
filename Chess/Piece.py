from abc import ABC, abstractmethod
from enum import Enum


class Color(Enum):
    white = 0
    black = 1

    def __str__(self) -> str:
        return "White" if self == Color.white else "Black"


def is_valid_rank(origin: 'Square', target: 'Square') -> bool:
    return origin.get_rank() == target.get_rank()


def is_valid_file(origin: 'Square', target: 'Square') -> bool:
    return origin.get_file() == target.get_file()


def is_valid_diagonal(origin: 'Square', target: 'Square') -> bool:
    rank_difference: int = abs(origin.get_rank() - target.get_rank())
    file_difference: int = abs(origin.get_file() - target.get_file())
    return rank_difference == file_difference


def rank_difference(origin: 'Square', target: 'Square') -> int:
    return abs(origin.get_rank() - target.get_rank())


def file_difference(origin: 'Square', target: 'Square') -> int:
    return abs(origin.get_file() - target.get_file())


class Piece(ABC):

    def __init__(self, color: Color, position: 'Square' = None):
        """
        Constructs a new Piece instance
        :param color: The color (black or white) of the new Piece
        :param position: the position (Square) of the new Piece
        """
        self.position = None
        if position is not None:
            self.set_position(position)
        self.color = color
        self.moved = False

    @abstractmethod
    def copy(self, position: 'Square') -> 'Piece':
        pass

    @abstractmethod
    def value(self) -> int:
        """
        Returns the relative piece value of this Piece.
        Pawn   = 1
        Knight = 3
        Bishop = 3
        Rook   = 5
        Queen  = 9
        King   = 200 (King's value is theoretically infinite but assigned 200 as arbitrary finite value)
        :return: the relative piece value of this Piece
        """
        pass

    @abstractmethod
    def can_move_to(self, target: 'Square') -> bool:
        """
        Checks if this Piece can move to the target square.
        :param target: target square to check if this piece can move to
        :return: True if this Piece can move to the target square, else False.
        """
        pass

    def move_to(self, target: 'Square'):
        """
        Attempts to move this piece to the user-specified target square.
        :param target: target square to move to
        :return: True
        """
        self.moved = True
        self.set_position(target)

    def is_on_square(self) -> bool:
        """
        Returns true if this Piece is on a square.
        :return: true if this Piece is on a square
        """
        return self.position is not None

    @abstractmethod
    def can_target(self, square: 'Square') -> bool:
        """
        Checks if this Piece can target the specified square.
        :param square: intended target Square instance
        :return: True if this Piece can target the specified square, else False
        """
        pass

    def capture(self) -> None:
        """
        Sets this piece's position's occupant to None.
        Sets this piece's position to None.
        :return: None
        """
        self.position.set_occupant(None)
        self.position = None

    def set_position(self, target: 'Square') -> None:
        """
        Sets the position of this Piece to the target square.
        :param target: target square
        """
        if self.get_position() is not None:
            self.get_position().set_occupant(None)

        if target.get_occupant() is not None:
            target.get_occupant().capture()

        target.set_occupant(self)
        self.position = target

    def get_position(self) -> 'Square':
        """
        Gets the position of this Piece.
        :return: this piece's position
        """
        return self.position

    def get_color(self) -> Color:
        """
        Returns the color of this Piece
        :return: the color of this Piece
        """
        return self.color

    def has_moved(self) -> bool:
        """
        Returns true if this Piece has moved, otherwise false.
        :return: true if this Piece has moved, otherwise false
        """
        return self.moved

    def coord_string(self) -> str:
        """
        Returns a string representation of this Piece's position Square.
        :return: A string representation of this Piece's position Square.
        """
        if not self.is_on_square():
            return ""

        return self.get_position().identifier()

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a single-letter string representation of this piece.
        Lowercase indicates white piece, uppercase indicates black piece
        :return: Returns a single-letter string representation of this piece
        """
        pass
