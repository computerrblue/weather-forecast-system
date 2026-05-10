import json
from pathlib import Path


class FileService:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.write_text("[]")


    def load_json(self):

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except json.JSONDecodeError:
            return []

        except FileNotFoundError:
            return []


    def save_json(self, data):

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

        except Exception as error:
            print(f"Error saving file: {error}")


    def append_history(self, weather_data):

        data = self.load_json()

        data.append(weather_data)

        self.save_json(data)