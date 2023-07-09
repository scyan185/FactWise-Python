from service.user_base import UserBase
from service.team_base import TeamBase
from service.project_board_base import ProjectBoardBase
from dtos.users import UserDataLayer
from dtos.teams import TeamDataLayer
from dtos.boards import BoardDataLayer
from const.constants import USERS_FIlE_PATH, TEAMS_FILE_PATH, BOARDS_FILE_PATH

# Entry point of the application
def main():

    # Create instances of UserBase, TeamBase, and ProjectBoardBase
    user_base = UserBase(UserDataLayer(USERS_FIlE_PATH),TeamDataLayer(TEAMS_FILE_PATH))
    team_base = TeamBase(TeamDataLayer(TEAMS_FILE_PATH), UserDataLayer(USERS_FIlE_PATH))
    board_base = ProjectBoardBase(BoardDataLayer(BOARDS_FILE_PATH))

    # UserBase API calls
    # Create a user
    request_create_user = '{"name": "Shreesh Chatterjee Mukherjee","display_name": "Shreesh"}'
    request_describe_user = '{"id" : "1"}'
    response_create_users = user_base.create_user(request_create_user)
    print(response_create_users)

    # List all users
    response_list_users = user_base.list_users()
    print(response_list_users)

    # Describe a user
    response_describe_users = user_base.describe_user(request_describe_user)
    print(response_describe_users)

    # Update a user
    request_update_user = '{"id":"1","user":{"name": "Saion Mukherjee", "display_name": "Shonta"}}'
    response_update_user = user_base.update_user(request_update_user)
    print(response_update_user)

    # Get teams associated with a user
    request_get_user_teams = '{"id":"1"}'
    response_get_user_teams = user_base.get_user_teams(request_get_user_teams)
    print(response_get_user_teams)

    # TeamBase API calls
    # Create a team
    request_create_team = '{"name":"A Team","description":"This is the A Team","admin":"1"}'
    response_create_team = team_base.create_team(request_create_team)
    print(response_create_team)

    # List all teams
    response_list_teams =  team_base.list_teams()
    print(response_list_teams)

    # Describe a team
    request_describe_teams = '{"id": "1"}'
    response_describe_teams = team_base.describe_team(request_describe_teams)
    print(response_describe_teams)

    # Update a team
    request_update_teams = '{"id":"1","team":{"name": "A Team", "description": "Hi, This is Team A again", "admin":"1"}}'
    response_update_teams = team_base.update_team(request_update_teams)
    print(response_update_teams)

    # Add users to a team
    request_add_users_to_teams = '{"id" : "1","users" : ["1", "2", "3"]}'
    response_add_users_to_teams = team_base.add_users_to_team(request_add_users_to_teams)
    print(response_add_users_to_teams)

    # Remove users from a team
    request_remove_users_from_teams = '{"id" : "1","users" : ["1", "2", "3"]}'
    response_remove_users_from_teams = team_base.remove_users_from_team(request_remove_users_from_teams)
    print(response_remove_users_from_teams)

    # List users in a team
    request_list_team_users = '{"id" : "1"}'
    response_list_team_users = team_base.list_team_users(request_list_team_users)
    print(response_list_team_users)

    # ProjectBoardBase API calls
    # Create a board
    request_create_board = '{"name" : "Board E","description" : "This is Board E",' \
                  '"team_id" : "2", "creation_time" : "2023-07-09 5:23:08"}'
    response_create_board = board_base.create_board(request_create_board)
    print(response_create_board)

    # Add tasks to a board
    request_add_tasks_to_board = '{"title": "Task 3", "description": "This is the first task", "user_id": "3", "creation_time": "2023-07-08 4:25:00"}'
    response_add_tasks_to_board = board_base.add_task(request_add_tasks_to_board)
    print(response_add_tasks_to_board)

    # Update task status
    request_update_task_status = '{"id" : "2","status" : "COMPLETE"}'
    response_update_task_status = board_base.update_task_status(request_update_task_status)
    print(response_update_task_status)

    # Close a board
    request_close_board = '{"id":"1"}'
    response_close_board = board_base.close_board(request_close_board)
    print(response_close_board)

    # List boards
    request_list_boards = '{"id":"2"}'
    response_list_boards = board_base.list_boards(request_list_boards)
    print(response_list_boards)

    # Export a board
    request_export_board = '{"id":"1"}'
    response_export_board = board_base.export_board(request_export_board)
    print(response_export_board)

# Call the main function to run the application
if __name__ == "__main__":
    main()


#------------------------------------------------------------------------------------------------------------#
    # request_body = '{"name": "Shreesh Chatterjee Mukherjee","display_name": "Shreesh"}'
    # request_body = '{"team_id": "1"}'
    # request_body = '{"id":"1","user":{"name": "Saion Mukherjee", "display_name": "Shonta"}}'
    # request_body = '{"id" : "1"}'
    # response = user_base.list_users()
    # request_body = '{"name":"A Team","description":"This is the A Team","admin":"1"}'
    # request_body = '{"team_id":"1"}'
    # request_body = '{"id":"1","team":{"name": "A Team", "description": "Hi, This is Team A again", "admin":"1"}}'
    # request_body = '{"id" : "1","users" : ["1", "2", "3"]}'
    # request_body = '{"id" : "1"}'
    #
    # response = team_base.list_team_users(request_body)
    # request_body = '{"name" : "Board E","description" : "This is Board E",' \
    #               '"team_id" : "2", "creation_time" : "2023-07-09 5:23:08"}'
    # request_body = '{"title": "Task 3", "description": "This is the first task", "user_id": "3", "creation_time": "2023-07-08 4:25:00"}'
    # request_body = '{"id" : "2","status" : "COMPLETE"}'
    # request_body = '{"id": "1"}'
    # request_body = '{"id":"1"}'
    # response = board_base.export_board(request_body)
    # print(response)


