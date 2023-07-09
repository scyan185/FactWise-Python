import json
from models.users import User
from const.constants import USERS_FIlE_PATH
class UserDataLayer:
    def __init__(self, USERS_FIlE_PATH):
        """
                Initialize the UserDataLayer with the path to the user data file.

                Args:
                    USERS_FIlE_PATH (str): Path to the user data file.
        """
        self.file_path = USERS_FIlE_PATH
    def read_users(self):
        """
                Read users from the file and return a list of User objects.

                Returns:
                    list: List of User objects representing the users.
        """
        try:
            with open(self.file_path) as file:
                data = json.load(file)
                users_data = data.get('users', [])
                users = []
                for user_data in users_data:
                    user_id = user_data.get('user_id')
                    name = user_data.get('name')
                    email = user_data.get('email')
                    creation_time = user_data.get('creation_time')
                    display_name = user_data.get('display_name')

                    user = User(user_id, name, email)
                    user.creation_time = creation_time
                    user.display_name = display_name
                    users.append(user)
                return users
        except FileNotFoundError:
            return []

    def write_users(self, users):
        """
                Write the list of User objects to the file.

                Args:
                    users (list): List of User objects to be written.

                Returns:
                    dict: Result of the write operation.

                Raises:
                    Exception: If failed to write the user data to the file.
        """
        users_data = [{"user_id": user.user_id, "name": user.name, "email": user.email, "display_name": user.display_name, "creation_time": user.creation_time} for user in users]
        data = {"users": users_data}
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent= 2)
        except IOError:
            return {"Exception": "Failed to write the User data"}