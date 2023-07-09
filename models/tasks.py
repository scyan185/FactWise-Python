import time
class Task:
    creation_time = int(time.time())
    def __init__(self, task_id: str, title: str, description: str, user_id: str, creation_time:str, status: str):
        """
                Initialize a Task object.

                Args:
                    task_id (str): Unique identifier for the task.
                    title (str): Title of the task.
                    description (str): Description of the task.
                    user_id (str): ID of the user assigned to the task.
                    creation_time (str): Creation time of the task.
                    status (str): Status of the task.
        """
        self.task_id = task_id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.creation_time = creation_time
        self.status = status


