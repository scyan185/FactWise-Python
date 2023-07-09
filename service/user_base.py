import json
from dtos.users import UserDataLayer
from dtos.teams import TeamDataLayer
from models.users import User
from datetime import datetime
class UserBase:
    """
    Base interface implementation for API's to manage users.
    """
    def __init__(self, data_layer: UserDataLayer, team_data_layer: TeamDataLayer):
        """
                        Initialize the TeamBase instance with data layer dependencies.
        """
        self.data_layer = data_layer
        self.team_data_layer = team_data_layer

    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        data = json.loads(request)
        name = data.get("name")
        display_name = data.get("display_name")
        if not name or not display_name:
            return ("Invalid request format")

        if name and len(name) > 64:
            return ("Name should be max 64 characters")

        if display_name and len(display_name) > 64:
            return ("Display name should be max 64 characters")

        users = self.data_layer.read_users()
        for user in users:
            if user.name == name:
                return '{"error": "Name must be unique"}'
        user_id = str(len(users) + 1)
        user = User(user_id, name, "")
        user.display_name = display_name
        users.append(user)
        self.data_layer.write_users(users)
        return json.dumps({"id": user_id})

    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        user_list = []
        users = self.data_layer.read_users()
        for user in users:
            user_data = {"name": user.name,
                         "display_name": user.display_name,
                         "creation_time": datetime.utcfromtimestamp(user.creation_time).strftime("%Y-%m-%d %H:%M:%S")}
            user_list.append(user_data)

        return user_list

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        try:
            request_data = json.loads(request)
            user_id = request_data.get("id")
            if not user_id:
                return ("Id is required")

            users = self.data_layer.read_users()
            for user in users:
                if user.user_id == user_id:
                    description = User.user_description(user)
                    response_data = {
                        "name": user.name,
                        "description": description,
                        "creation_time": datetime.utcfromtimestamp(user.creation_time).strftime("%Y-%m-%d %H:%M:%S")
                    }
                    return json.dumps(response_data)

            return json.dumps({"error": "User not found"})
        except ValueError as e:
            return json.dumps({"error": str(e)})

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        try:
            data = json.loads(request)
            user_id = data.get('id')
            user_data = data.get('user')

            if not user_id or not user_data:
                return ("Invalid request format")

            name = user_data.get('name')
            display_name = user_data.get('display_name')

            if not name or not display_name:
                return ("Invalid request data")

            if name and len(name) > 64:
                return ("Name should be max 64 characters")

            if display_name and len(display_name) > 128:
                return ("Display name should be max 128 characters")

            users = self.data_layer.read_users()
            for user in users:
                if user.user_id == user_id:
                    user.display_name = display_name
                    self.data_layer.write_users(users)
                    return json.dumps({"id": user_id})

            return ("User not found")

        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        data = json.loads(request)
        id = data.get('id')
        if not id:
            return ("Invalid request format")

        teams = self.team_data_layer.read_teams()
        team = next((t for t in teams if id in t.members), None)
        team_details = []
        for user_id in team.members:
            if id == user_id:
                team_data = {"name": team.name,
                             "description": team.description,
                             "creation_time": datetime.utcfromtimestamp(team.creation_time).strftime("%Y-%m-%d %H:%M:%S")}

                team_details.append(team_data)

        return team_details