import json
from const.constants import BOARDS_FILE_PATH
from models.boards import Board
from models.tasks import Task

class BoardDataLayer:
    def __init__(self, BOARDS_FILE_PATH):
        self.file_path = BOARDS_FILE_PATH

    def read_boards(self):
        """
                Read boards from the file and return a list of Board objects.

                Returns:
                    list: List of Board objects representing the boards.
        """
        try:
            with open(self.file_path) as file:
                data = json.load(file)
                boards_data = data.get('boards', [])
                boards = []
                for board_data in boards_data:
                    board_id = board_data.get('board_id')
                    name = board_data.get('name')
                    team_id = board_data.get('team_id')
                    description = board_data.get('description')
                    creation_time = board_data.get('creation_time')
                    status = board_data.get('status')

                    tasks_data = board_data.get('tasks', [])
                    tasks = []
                    for task_data in tasks_data:
                        task_id = task_data.get('task_id')
                        title = task_data.get('title')
                        description = task_data.get('description')
                        user_id = task_data.get('user_id')
                        creation_time = task_data.get('creation_time')
                        status = task_data.get('status')

                        task = Task(task_id, title, description, user_id, creation_time, status)
                        tasks.append(task)

                    board = Board(board_id, name, description, team_id, creation_time, tasks, status)
                    board.creation_time = creation_time
                    boards.append(board)
                return boards
        except FileNotFoundError:
            return []

    def write_boards(self, boards):

        """
                Write the list of Board objects to the file.

                Args:
                    boards (list): List of Board objects to be written.

                Raises:
                    Exception: If failed to write the board data to the file.
        """
        boards_data = []
        for board in boards:
            tasks_data = []
            for task in board.tasks:
                task_data = {
                    "task_id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "user_id": task.user_id,
                    "creation_time": task.creation_time,
                    "status": task.status
                }
                tasks_data.append(task_data)

            board_data = {
                "board_id": board.board_id,
                "name": board.name,
                "team_id": board.team_id,
                "description": board.description,
                "creation_time": board.creation_time,
                "status": board.status,
                "tasks": tasks_data
            }
            boards_data.append(board_data)
        data = {"boards": boards_data}
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=2)
        except IOError:
            return {"Exception": "Failed to write the Board data"}