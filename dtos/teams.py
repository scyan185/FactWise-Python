import json
from models.teams import Team
from const.constants import TEAMS_FILE_PATH
class TeamDataLayer:
    def __init__(self, TEAMS_FILE_PATH):
        self.file_path = TEAMS_FILE_PATH
    def read_teams(self):
        """
                Read teams from the file and return a list of Team objects.

                Returns:
                    list: List of Team objects representing the teams.
        """
        try:
            with open(self.file_path) as file:
                data = json.load(file)
                teams_data = data.get('teams', [])
                teams = []
                for team_data in teams_data:
                    team_id = team_data.get('team_id')
                    name = team_data.get('name')
                    members = team_data.get('members')
                    admin = team_data.get('admin')
                    creation_time = team_data.get('creation_time')
                    display_name = team_data.get('display_name')
                    description = team_data.get('description')
                    # Create Team object and populate attributes
                    team = Team(team_id, name, members, admin_id=admin, description=description)
                    team.creation_time = creation_time
                    team.display_name = display_name
                    team.description = description
                    teams.append(team)
                return teams
        except FileNotFoundError:
            return []
    def write_teams(self, teams):
        """
                Write the list of Team objects to the file.

                Args:
                    teams (list): List of Team objects to be written.

                Raises:
                    Exception: If failed to write the team data to the file.
        """
        teams_data = [
            {
                "team_id": team.team_id,
                "name": team.name,
                "members": team.members,
                "display_name": team.display_name,
                "creation_time": team.creation_time,
                "description": team.description,
                "admin": team.admin_id
            }
            for team in teams
        ]
        data = {"teams": teams_data}
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=2)
        except IOError:
            return {"Exception": "Failed to write the Team data"}