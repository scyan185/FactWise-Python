import json
from dtos.teams import TeamDataLayer
from dtos.users import UserDataLayer
from models.teams import Team
from datetime import datetime
class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """
    def __init__(self, data_layer: TeamDataLayer, user_data_layer: UserDataLayer):
        """
                Initialize the TeamBase instance with data layer dependencies.
        """
        self.data_layer = data_layer
        self.user_data_layer = user_data_layer

    # create a team
    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        # Parse the request JSON
        data = json.loads(request)
        name = data.get("name")
        description = data.get('description')
        admin = data.get('admin')

        # Validate the required fields
        if not name or not description or not admin:
            return ("Invalid request format")

        if name and len(name) > 64:
            return ("Name should be max 64 characters")

        if description and len(description) > 128:
            return ("Description name should be max 128 characters")

        # Check if the team name is already taken
        teams = self.data_layer.read_teams()
        for team in teams:
            if team.name == name:
                return '{"error": "Name must be unique"}'

        # Generate a unique team ID
        team_id = str(len(teams) + 1)
        # Create the team instance
        team = Team(team_id, name, members=[], admin_id=admin, description=description)

        # Add the team to the existing teams
        teams.append(team)

        # Write the updated teams to the data layer
        self.data_layer.write_teams(teams)

        # Return the team ID as the response
        response = {"id": team_id}
        return json.dumps(response)

    # list all teams
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        teams_data = []
        teams = self.data_layer.read_teams()
        for team in teams:
            team_data = {
                "name": team.name,
                "description": team.description,
                "creation_time": datetime.utcfromtimestamp(team.creation_time).strftime("%Y-%m-%d %H:%M:%S"),
                "admin": team.admin_id
            }
            teams_data.append(team_data)
        return json.dumps(teams_data)

    # describe team
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        try:
            request_data = json.loads(request)
            id = request_data.get("team_id")
            if not id:
                return ("team_id is required")

            teams = self.data_layer.read_teams()
            for team in teams:
                if team.team_id == id:
                    description = team.description
                    response_data = {
                        "name": team.name,
                        "description": description,
                        "creation_time": datetime.utcfromtimestamp(team.creation_time).strftime("%Y-%m-%d %H:%M:%S"),
                        "admin": team.admin_id
                    }
                    return json.dumps(response_data)
            return json.dumps({"error": "Team not found"})
        except ValueError as e:
            return json.dumps({"error": str(e)})

    # update team
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        try:
            data = json.loads(request)
            id = data.get('id')
            team_data = data.get('team')

            if not id or not team_data:
                return ("Invalid request format")

            name = team_data.get('name')
            description = team_data.get('description')
            admin = team_data.get('admin')

            if not name or not description or not admin:
                return ("Invalid request data")

            if name and len(name) > 64:
                return ("Name should be max 64 characters")

            if description and len(description) > 128:
                return ("description should be max 128 characters")

            teams = self.data_layer.read_teams()
            for team in teams:
                if team.team_id == id:
                    team.description = description
                    self.data_layer.write_teams(teams)
                    return json.dumps({"id": id})
            return ("Team not found")
        except Exception as e:
            return json.dumps({"error": str(e)})

    # add users to team
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        data = json.loads(request)
        team_id = data.get('id')
        users = data.get('users')

        if not team_id or not users:
            raise Exception("Invalid request format")

        teams = self.data_layer.read_teams()

        # searches for a team in the teams list that matches the specified team_id. If a matching team is found,
        # it assigns that team object to the team variable; otherwise, it assigns None
        team = next((t for t in teams if t.team_id == team_id), None)

        if not team:
            return {"Error": "Team not found"}

        #existing_members creates a set containing distinct values everytime
        existing_members = set(team.members)
        #new_members produces a empty list based on the condition set
        new_members = [user_id for user_id in users if user_id not in existing_members]

        if len(team.members) + len(new_members) > 50:
            return {"Exception": "Cap cannot be extended beyond 50 users"}

        team.members.extend(new_members)

        self.data_layer.write_teams(teams)
        response = {"message": "Users added to team successfully"}
        return json.dumps(response)


    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        data = json.loads(request)
        team_id = data.get('id')
        users = data.get('users')

        if not team_id or not users:
            return {"Error": "Invalid request format"}

        teams = self.data_layer.read_teams()
        team = next((t for t in teams if t.team_id == team_id), None)

        if not team:
            return {"Error": "Team not found"}

        existing_members = set(team.members)
        #removed_members produces a list containing the IDs that we wanna remove
        removed_members = [user_id for user_id in users if user_id in existing_members]
        #team.members produces an empty list based on the condition set
        team.members = [user_id for user_id in team.members if user_id not in removed_members]
        #Finally writes to the data layer
        self.data_layer.write_teams(teams)
        response = {"message": "Users removed successfully"}
        return json.dumps(response)

    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        #Parsing the request
        data = json.loads(request)
        id = data.get('id')
        if not id:
            return {"Error": "Invalid request format"}
        teams = self.data_layer.read_teams()
        #Validating if team_id is present and suffice the condition
        team = next((t for t in teams if t.team_id == id), None)
        if not team:
            return {"Error": "Team not found"}
        user_details = []
        for user_id in team.members:
            users = self.user_data_layer.read_users()
            for user in users:
                if user_id == user.user_id:
                    user_data = {"id": user.user_id,
                                 "name": user.name,
                                 "display_name": user.display_name}
                    user_details.append(user_data)
        return user_details