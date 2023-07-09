#Description

My Application is a project management tool designed to facilitate collaboration and organization within teams. 
It provides a platform for managing users, teams, and boards with associated tasks. 
The main purpose of the application is to streamline project workflows, enhance communication, and track progress effectively.

Key Features:

User Management: The application allows creating, updating, and retrieving user information. Users can have unique names, display names, and are associated with specific teams.

Team Management: Teams can be created with a name, description, and an assigned administrator. The application supports adding and removing users from teams, as well as listing team members.

Board Management: Boards represent project boards and can be created with a name, description, team ID, and creation time. Boards serve as containers for tasks.

Task Management: Tasks can be added to boards with a title, description, assigned user ID, and creation time. Tasks are organized within boards and can be updated with status changes.

Board Export: The application offers the ability to export a board's information and tasks into a presentable view, which is saved as a text file.

With these features, My Application aims to provide a comprehensive project management solution that enables teams to collaborate, track tasks, and monitor project progress in an organized and efficient manner.


#File Structure Of the application:

my_application/
  ├── main.py
  ├── models/
  │   ├── users.py
  │   ├── teams.py
  │   ├── boards.py
  │   └── tasks.py
  ├── services/
  │   ├── user_base.py
  │   ├── team_base.py
  │   └── project_board_base.py
  ├── dtos/
  │   ├── users.py
  │   ├── teams.py
  │   └── boards.py
  ├── const/
  │   └── constants.py
  └── README.md

#A Brief Overview:

main.py: The entry point of the application. It contains the main function that orchestrates the execution and calls various services.

models/: This directory contains the model classes used in the application. The models represent entities such as users, teams, boards, and tasks.

services/: This directory contains the service classes responsible for handling the business logic and implementing the application's functionality.

user_base.py: Implements user-related operations and interactions.

team_base.py: Implements team-related operations and interactions.

project_board_base.py: Implements board-related operations and interactions.

dtos/: This directory contains the data transfer objects (DTOs) used for transferring data between different layers of the application.

users.py: Defines the user-related DTOs.

teams.py: Defines the team-related DTOs.

boards.py: Defines the board-related DTOs.

const/: This directory contains the constants used in the application.

constants.py: Defines constant values used throughout the application, such as file paths and status codes.

README.md: The README file that provides an overview of the application, installation instructions, usage examples, and other relevant information.

* Implementation of the APIs: (Note: I have built the use cases without even using frameworks.)

1) Create User: You have a create_user method in the UserBase class that handles creating a new user. It takes the necessary parameters such as name and display name, and adds the user to the user data layer.

2) List Users: The list_users method in the UserBase class retrieves the list of users from the user data layer and returns them.

3) Describe User: The describe_user method in the UserBase class takes the user ID as input and retrieves the details of the specified user from the user data layer.

4) Update User: The update_user method in the UserBase class allows updating the information of a specific user. It takes the user ID and the updated user object as input.

5) Get User Teams: The get_user_teams method in the UserBase class retrieves the teams associated with a specific user. It takes the user ID as input and returns the corresponding teams.

6) Create Team: The create_team method in the TeamBase class handles the creation of a new team. It takes the necessary parameters such as name, description, and admin ID, and adds the team to the team data layer.

7) List Teams: The list_teams method in the TeamBase class retrieves the list of teams from the team data layer and returns them.

8) Describe Team: The describe_team method in the TeamBase class takes the team ID as input and retrieves the details of the specified team from the team data layer.

9) Update Team: The update_team method in the TeamBase class allows updating the information of a specific team. It takes the team ID and the updated team object as input.

10) Add Users to Team: The add_users_to_team method in the TeamBase class handles adding users to a team. It takes the team ID and a list of user IDs as input.

11) Remove Users from Team: The remove_users_from_team method in the TeamBase class handles removing users from a team. It takes the team ID and a list of user IDs as input.

12) List Team Users: The list_team_users method in the TeamBase class retrieves the users belonging to a specific team. It takes the team ID as input and returns the corresponding users.

13) Create Board: The create_board method in the ProjectBoardBase class handles the creation of a new board. It takes the necessary parameters such as name, description, team ID, and creation time, and adds the board to the board data layer.

14) Add Task: The add_task method in the ProjectBoardBase class handles adding a new task to a board. It takes the necessary parameters such as title, description, user ID, and creation time. It ensures that the task title is unique for the board and adds the task to the board's task list.

15) Update Task Status: The update_task_status method in the ProjectBoardBase class allows updating the status of a task. It takes the task ID and the updated status as input.

16) Close Board: The close_board method in the ProjectBoardBase class handles closing a board. It sets the board's status to "CLOSED" if all tasks are marked as "COMPLETE".

17) List Boards: The list_boards method in the ProjectBoardBase class retrieves the boards associated with a specific team. It takes the team ID as input and returns the corresponding boards.

18) Export Board: The export_board method in the ProjectBoardBase class exports a board's information and tasks into a text file. It takes the board ID as input and returns the name of the created file.