# Welsh Academy

"Welsh Academy" is an application dedicated to provide recipes to cheddar lovers around the world.

## Installation

Clone the project:
```sh
git clone git@github.com:entissar12/welsh_academy.git
```
Move into the project:
```sh
cd welsh_academy
```

Build the docker image:
```sh
docker build --tag welsh_app .
```
Run the docker imageas a container: 

```sh
docker run -d -p 5000:5000 welsh_app
```
Access app throw : 

```sh
http://localhost:5000
```
## Available Endpoints
| Endpoint | Request Method| Authorization in header | Example of Body | Description|
| ------ | ------ | ----------| ------------| ----------- |
| /users | POST | |  ```{"username" :  "username", "password": "password123"} ```|Create user |
| /login | POST | |  ``` {"username" :  "username", "password": "password123"}  ``` |Login user |
|/ingredients | POST | ```{"Authorization": "Bearer {token_resulted_from_login}" ``` | ``` {"name" :  "Ingredient1"} ``` | Create ingredient |
| /ingredients | GET |  ```{"Authorization": "Bearer {token_resulted_from_login}" ``` | | List all ingredients |
| /recipes | POST |  ```{"Authorization": "Bearer {token_resulted_from_login}" ``` |  ``` {"name" :  "Recipe1"}  ``` | Create recipe |
| /recipes | GET |  ```{"Authorization": "Bearer {token_resulted_from_login}" ``` | | List all recipes |
| /users | GET |  ```{"Authorization": "Bearer {token_resulted_from_login}" ``` | | Get data of current user with his favorite recipes |
| /users | PATCH |  ```{"Authorization": "Bearer {token_resulted_from_login}" ``` | ``` {"recipe_id": 2} ``` |Flag recipe if not flagged / Unflag recipe if already flagged (for current user) |
