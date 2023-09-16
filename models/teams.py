import time
class Team:
    # Class variable to store the current creation time
    creation_time = int(time.time())
    def __init__(self, team_id: str, name: str, members: list, admin_id: str = "", description: str = ""):
        """
                Initialize a Team object.

                Args:
                    team_id (str): Unique identifier for the team.
                    name (str): Name of the team.
                    members (list): List of members in the team.
                    admin_id (str, optional): ID of the team administrator. Defaults to "".
                    description (str, optional): Optional description for the team. Defaults to "".
        """
        self.team_id = team_id
        self.name = name
        self.members = members
        self.display_name = ""
        self.admin_id = admin_id
        self.creation_time = self.generate_unique_creation_time()
        self.description= description
    @classmethod
    def generate_unique_creation_time(cls):
        """
                Generate a unique creation time for the Team object.

                Returns:
                    int: Unique creation time.
        """
        cls.creation_time += 1
        return cls.creation_time

