import time
class User:
    # Class variable to store the current creation time
    creation_time = int(time.time())
    def __init__(self, user_id: str, name: str, email: str):
        """
                Initialize a User object.

                Args:
                    user_id (str): Unique identifier for the user.
                    name (str): Name of the user.
                    email (str): Email address of the user.
        """
        self.user_id = user_id
        self.name = name
        self.display_name = ""
        self.email = email
        self.creation_time = self.generate_unique_creation_time()
    @classmethod
    def generate_unique_creation_time(cls):
        """
                Generate a unique creation time for the User object.

                Returns:
                    int: Unique creation time.
        """
        cls.creation_time += 1
        return cls.creation_time

    @staticmethod
    def user_description(User):
        """
                Generate a description for the User object.

                Args:
                    User (User): User object for which the description is generated.

                Returns:
                    str: User description.
        """
        description = f"User: {User.name}"
        if User.display_name:
            description += f", Display Name: {User.display_name}"
        else:
            description += f", creation time: {User.creation_time}"
        return description