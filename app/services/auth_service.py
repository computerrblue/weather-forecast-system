import re

from app.models.user import User
from app.services.file_service import FileService


class AuthService:

    def __init__(self):

        self.file_service = FileService(
            "data/users.json"
        )


    def register_user(
        self,
        username: str,
        password: str
    ):

        users = self.file_service.load_json()

        if not username or not password:

            return {
                "error": "All fields are required"
            }

        if not re.match(r"^[a-zA-Z0-9_]+$", username):

            return {
                "error": "Invalid username"
            }

        for user in users:

            if user["username"] == username:

                return {
                    "error": "Username already exists"
                }

        new_user = User(
            username=username,
            password=password
        )

        users.append(new_user.to_dict())

        self.file_service.save_json(users)

        return {
            "success": "User registered"
        }


    def login_user(
        self,
        username: str,
        password: str
    ):

        users = self.file_service.load_json()

        for user in users:

            if (
                user["username"] == username
                and user["password"] == password
            ):

                return {
                    "success": "Login successful"
                }

        return {
            "error": "Invalid username or password"
        }