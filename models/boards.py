import time
from const.constants import BOARD_STATUS_OPEN
class Board:
    def __init__(self, board_id: str, name: str, description: str, team_id: str, creation_time: str, tasks: list = None, status: str = BOARD_STATUS_OPEN):
        """
                Initialize a Board object.

                Args:
                    board_id (str): Unique identifier for the board.
                    name (str): Name of the board.
                    team_id (str): ID of the team the board belongs to.
                    description (str, optional): Description of the board. Defaults to "".
                    tasks (list, optional): List of Task objects associated with the board. Defaults to None.
                    status (str, optional): Status of the board. Can be "open", "progress", or "completed". Defaults to "open".
        """
        self.board_id = board_id
        self.name = name
        self.description = description
        self.team_id = team_id
        self.creation_time = creation_time
        self.tasks = tasks if tasks is not None else []
        self.status = status



