import os
import GoldyBot

MODULE_NAME = "FILES"

class File(object):
    """Goldy Bot's File Handler."""
    def __init__(self, path):
        self.file_path = path

        if self.exists() == False:
            GoldyBot.logging.print_and_log(f"[{MODULE_NAME}] Umm, that file doesn't exist, so I'm going to create it myself.")
            self.create()

    def read(self):
        """Commands Goldy to return the value of a file."""
        try:
            with self.get_file() as file:
                file_context = file.read()
                GoldyBot.logging.print_and_log(None, f"[{MODULE_NAME}] I've read the file '{self.file_path}'.")
                return file_context

        except Exception:
            GoldyBot.logging.print_and_log("warn", f"[{MODULE_NAME}] Oops, I Couldn't read the file '{self.file_path}', so I'm returning 'None'.")
            return None

    def write(self, value):
        """Commands Goldy to write to the file with the following value."""
        try:
            # Try to edit value of file.
            with self.get_file() as file:
                file.seek(0)
                file.write(str(value))
                file.truncate()

            GoldyBot.logging.print_and_log(None, f"[{MODULE_NAME}] I've written to '{self.file_path}'.")
        
        except Exception:
            GoldyBot.logging.print_and_log("error", f"[{MODULE_NAME}] I Couldn't edit '{self.file_path}' with the value '{value}'!")

    def create(self):
        """Commands Goldy to create a file or directory."""
        if self.file_path[-1] == "/": # Create directory.
            os.mkdir(self.file_path)
            GoldyBot.logging.print_and_log(f"[{MODULE_NAME}] I've created a directory at '{self.file_path}'.")
        else: # Create file.
            open(self.file_path, "a+")
            GoldyBot.logging.print_and_log(f"[{MODULE_NAME}] I've created a file at '{self.file_path}'.")

    def exists(self) -> bool:
        """Checks if the file exists."""
        if os.path.exists(self.file_path):
            return True
        else:
            return False

    def get_file(self, mode="r+"):
        """Commands Goldy to open the file."""
        return open(self.file_path, mode, encoding='utf-8')