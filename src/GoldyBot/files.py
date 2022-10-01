from __future__ import annotations
import io
import os
import re
import threading
import time
from typing import IO, Any, Callable

import GoldyBot
import requests

MODULE_NAME = "FILES"

class File(object):
    """Goldy Bot's File Handler."""
    def __init__(self, path):
        self.file_path = path

        if self.exists() == False:
            GoldyBot.logging.print_and_log(f"[{MODULE_NAME}] Umm, that file doesn't exist, so I'm going to create it myself.")
            self.create()

    def read(self) -> Any|None:
        """Commands Goldy to return the value of a file."""
        try:
            with self.get_file() as file:
                file_context = file.read()
                GoldyBot.logging.print_and_log(None, f"[{MODULE_NAME}] I've read the file '{self.file_path}'.")
                return file_context

        except Exception as e:
            GoldyBot.logging.print_and_log("error", f"[{MODULE_NAME}] Oops, I Couldn't read the file '{self.file_path}', so I'm returning 'None'. \nError --> {e}")
            return None

    def write(self, value) -> None:
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

    def create(self) -> None:
        """Commands Goldy to create a file or directory."""
        if self.file_path[-1] == "/": # Create directory.
            os.mkdir(self.file_path)
            GoldyBot.logging.print_and_log(f"[{MODULE_NAME}] I've created a directory at '{self.file_path}'.")
        else: # Create file.
            open(self.file_path, "a+")
            GoldyBot.logging.print_and_log(f"[{MODULE_NAME}] I've created a file at '{self.file_path}'.")

    def delete(self) -> None:
        """Commands Goldy to delete this file."""
        if self.file_path[-1] == "/": # Delete as directly.
            os.rmdir(self.file_path)
            GoldyBot.logging.print_and_log("info_5", f"[{MODULE_NAME}] I've removed the directory at '{self.file_path}'.")
        else: # Delete as file.
            os.remove(self.file_path)
            GoldyBot.logging.print_and_log("info_5", f"[{MODULE_NAME}] I've removed the file at '{self.file_path}'.")
        

    def exists(self) -> bool:
        """Checks if the file exists."""
        if os.path.exists(self.file_path):
            return True
        else:
            return False

    def get_file(self, mode="r+") -> IO:
        """Commands Goldy to open the file."""
        if mode == "wb": return open(self.file_path, mode) # For writing binary.

        return open(self.file_path, mode, encoding='utf-8')

class WebFile():
    """A web file is a class that partially inherits the GoldyBot.File() class but instead of taking in file path it takes in a URL of a file on the web."""
    def __init__(self, url:str, download_to_disk:bool=False, time_until_deletion:int|float=10):
        self._url = url
        self._download_to_disk = download_to_disk
        self._time_until_deletion = time_until_deletion
        self._request = requests.get(self._url, stream=True)
        self._request.raw.decode_content = True # Content-Encoding

        self.file_path = self._url

        self._file_object = io.BytesIO(self._request.content)

        # Getting file name.
        try:
            self._file_object.name = re.findall("filename=(.+)", self._request.headers['Content-Disposition'])[0]

        except KeyError: # If fail to get file name then fallback to default.
            GoldyBot.logging.log("warn", f"[{MODULE_NAME}] Failed to find the web file's file name so I'm giving it a default name.")

            content_type = self._request.headers['Content-Type']
            self._file_object.name = f"uwu_file.{content_type[content_type.index('/')+1:]}"

        # Download to disk temporary if 'download_to_disk' is True.
        if download_to_disk:
            self.download_to_disk(self._time_until_deletion)

    @property
    def url(self) -> str:
        """Returns url of file."""
        return self._url

    @property
    def downloaded_to_disk(self) -> bool:
        """Has this file been downloaded to disk."""
        return self._download_to_disk

    @property
    def file_name(self) -> str:
        """Returns name of file."""
        return self._file_object.name

    @property
    def raw_bytes(self) -> bytes:
        """Returns 🥩raw bytes of file. Sometimes this is more preferred by other libraries."""
        return self._request.content

    def download_to_disk(self, time_until_deletion:int|float=10) -> None:
        """Downloads file to disk temporary. The file deletes itself by default in 5 seconds."""
        File("./temp/") # Create temp folder.
        
        self.temp_file = File(f"./temp/{self._file_object.name}")

        with self.temp_file.get_file(mode="wb") as file:
            file.seek(0)
            file.write(self._file_object.getvalue())
            file.truncate()
            file.close()

        def delete_file_later(): time.sleep(time_until_deletion); self.temp_file.delete()

        threading.Thread(target=delete_file_later).start()

    def get_file(self) -> io.BytesIO|str:
        """Returns file IO object but if 'download_to_disk' is True this will return the temporary path to the file."""
        if self.downloaded_to_disk:
            return f"./temp/{self._file_object.name}"
        else:
            return self._file_object
    
    # Inheriting read method from GoldyBot.File class.
    read:Callable[[], Any|None] = File.__dict__["read"]
    """Commands Goldy to return the value of a file."""