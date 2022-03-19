import json
import GoldyBot

MODULE_NAME = "CONFIG"

class Config(object):
    """A class that acts as an interface to manage enabling and disabling configs in json files."""
    
    def __init__(self, config_file:GoldyBot.files.File):
        self.config_file = config_file

        if not self.config_file.read() == "{}":
            print("debug")
            with self.config_file.get_file() as file:
                data = {}
                file.seek(0)
                json_string = json.dumps(data, indent=4)
                file.write(json_string)
                file.truncate()

    def write(self, config_name:str, value) -> None:
        """Method that edits a config's value or creates one with the value."""
        try:
            # Try to edit value of config.
            with self.config_file.get_file() as file:
                data = json.load(file)
                data[config_name.lower()] = value
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            GoldyBot.log(None, f"[{MODULE_NAME}] Written to config '{config_name.lower()}' in '{self.config_file.file_path}' with the value '{value}'.")
        
        except Exception:
            GoldyBot.log("error", f"[{MODULE_NAME}] Couldn't edit the config '{config_name}' in '{self.config_file.file_path}' with the value '{value}'!")

    def read(self, config_name:str):
        """Method that returns the value of a config."""
        try:
            with self.config_file.get_file() as file:
                data = json.loads(file.read())

                return data[config_name.lower()]

        except KeyError:
            return None

        except Exception:
            GoldyBot.log("warn", f"[{MODULE_NAME}] Couldn't read value in the config '{config_name.lower()}' from '{self.config_file.file_path}', so were returning 'None'.")
            return None

    def remove(self, config_name:str):
        """This method removes the config completly from the json file."""
        try:
            with self.config_file.get_file() as file:
                data = json.load(file)
                del data[config_name.lower()]
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            GoldyBot.log(None, f"[{MODULE_NAME}] Removed the config '{config_name.lower()}' from '{self.config_file.file_path}'!")

        except Exception:
            GoldyBot.log("error", f"[{MODULE_NAME}] Couldn't remove the config from the json file!")