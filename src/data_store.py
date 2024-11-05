from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board

class DataStore:

    def add_board(self, model) -> None:
        raise NotImplementedError

    def get_board(self, id) -> "Board":
        raise NotImplementedError

    def get_boards(self) -> list["Board"]:
        raise NotImplementedError

    def update_board(self, model, update):
        raise NotImplementedError

    def remove_board(self, board) -> None:
        raise NotImplementedError
