import json
from const.constants import BOARD_STATUS_OPEN, TASK_STATUS_OPEN, TASK_STATUS_PROGRESS, TASK_STATUS_CLOSED,BOARD_STATUS_CLOSED,OUTPUT_FILE_PATH
from dtos.boards import BoardDataLayer
from models.boards import Board
from models.tasks import Task
from datetime import  datetime
class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """
    def __init__(self, board_data_layer: BoardDataLayer):
        """
                        Initialize the ProjectBoardBase instance with data layer dependencies.
                """
        self.board_data_layer = board_data_layer

    # create a board
    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        data = json.loads(request)
        name = data.get('name')
        description = data.get('description')
        team_id = data.get('team_id')
        creation_time = data.get('creation_time')

        if not name or not description or not creation_time:
            return {"Invalid request format"}

        if name and len(name) > 64:
            return {"Name should be max 64 characters"}

        if description and len(description) > 128:
            return {"Description name should be max 128 characters"}

        boards = self.board_data_layer.read_boards()
        for board in boards:
            if board.name == name:
                return {"Name must be unique"}

        board_id = str(len(boards) + 1)
        board = Board(board_id, name, description, team_id, creation_time, status=BOARD_STATUS_OPEN)
        boards.append(board)
        self.board_data_layer.write_boards(boards)
        response = {"id":board_id}
        return json.dumps(response)

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        data = json.loads(request)
        board_id = data.get('id')

        if not board_id:
            return json.dumps({"Exception": "Invalid request format"})

        boards = self.board_data_layer.read_boards()
        for board in boards:
            if board.board_id == board_id:
                all_tasks_completed = all(task.status == TASK_STATUS_CLOSED.upper() for task in board.tasks)
                if all_tasks_completed:
                    board.status = BOARD_STATUS_CLOSED
                    # Set the end_time for the board here (current date:time)
                    board.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.board_data_layer.write_boards(boards)
                    return json.dumps({"Message": "Board closed successfully at {}".format(board.end_time)})
                else:
                    return json.dumps({"Exception": "Tasks are still open"})

        return json.dumps({"Exception": "Board not found"})

    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>",
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        data = json.loads(request)
        title = data.get('title')
        description = data.get('description')
        user_id = data.get('user_id')
        creation_time = data.get('creation_time')

        if not title or not description or not user_id or not creation_time:
            return json.dumps({"Exception": "Invalid request format"})

        if title and len(title) > 64:
            return json.dumps({"Exception": "Title should be max 64 characters"})

        if description and len(description) > 128:
            return json.dumps({"Exception": "Description should be max 128 characters"})

        boards = self.board_data_layer.read_boards()
        task_id = None
        for board in boards:
            if board.status != BOARD_STATUS_OPEN:
                return json.dumps({"Exception": "Can only add task to an OPEN board"})

            for task in board.tasks:
                if task.title == title:
                    return json.dumps({"Exception": "Task title must be unique for a board"})

            task_id = str(len(board.tasks) + 1)
            task = Task(task_id, title, description, user_id, creation_time, status=TASK_STATUS_OPEN)
            task.status = TASK_STATUS_OPEN
            board.tasks.append(task)

        if task_id:
            self.board_data_layer.write_boards(boards)
            return json.dumps({"id": task_id})
        else:
            return json.dumps({"Exception": "No open board found to add the task"})

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        data = json.loads(request)
        id = data.get('id')
        status = data.get('status')

        if not id or not status:
            return {"Exception": "Invalid request format"}
        boards = self.board_data_layer.read_boards()
        for board in boards:
            for task in board.tasks:
                if task.task_id == id:
                    if status not in [TASK_STATUS_OPEN.upper(), TASK_STATUS_PROGRESS.upper(), TASK_STATUS_CLOSED.upper()]:
                        return {"Exception": "Invalid task status"}
                    task.status = status
                    self.board_data_layer.write_boards(boards)
                    return {"Success": "Task status updated successfully"}
        return {"Exception": "Task not found"}

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        data = json.loads(request)
        id = data.get('id')
        boards = self.board_data_layer.read_boards()
        board_details = []
        for board in boards:
            if board.team_id == id:
                board_data = {
                    "id": board.board_id,
                    "name":board.name
                }
                board_details.append(board_data)
        return board_details

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        data = json.loads(request)
        board_id = data.get('id')

        if not board_id:
            return json.dumps({"Exception": "Invalid request format"})

        boards = self.board_data_layer.read_boards()
        for board in boards:
            if board.board_id == board_id:
                # Generate a visually appealing board view
                board_view = f"Board: {board.name}\n"
                board_view += f"Description: {board.description}\n\n"
                board_view += "Tasks:\n"

                for task in board.tasks:
                    task_view = f"Task ID: {task.task_id}\n"
                    task_view += f"Title: {task.title}\n"
                    task_view += f"Description: {task.description}\n"
                    task_view += f"User ID: {task.user_id}\n"
                    task_view += f"Creation Time: {task.creation_time}\n"
                    task_view += f"Status: {task.status}\n\n"

                    board_view += task_view

                # Generate a unique file name for the export
                file_name = f"board_export_{board_id}.txt"
                file_path = f"out/{file_name}"

                # Write the board view to a file
                with open(file_path, 'w') as file:
                    file.write(board_view)

                return json.dumps({OUTPUT_FILE_PATH: file_name})

        return json.dumps({"Exception": "Board not found"})