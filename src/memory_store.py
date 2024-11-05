from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board

from data_store import DataStore

class InMemoryStore(DataStore):
    def __init__(self):
        self.boards: dict[int, "Board"] = {}

    def add_board(self, board: "Board"):
        self.boards[board.board_id] = board

    def get_board(self, id: int):
        return self.boards[id]

    def update_board(self, board: "Board", update: dict):
        for k in update:
            setattr(board, k, update[k])

    def get_boards(self):
        return [self.boards[b] for b in self.boards]

    def remove_board(self, board: "Board"):
        del self.boards[board.board_id]
