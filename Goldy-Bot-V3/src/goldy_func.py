import os
import time
from datetime import date
import json
import stat
import shutil

def get_time_and_date(option):

    if option.lower() == 'date':
        today = date.today()
        # dd/mm/YY
        current_date = today.strftime("%d-%m-%Y")
        return current_date

    if option.lower() == 'time':
        t = time.localtime()
        # hh/mm/ss
        current_time = time.strftime("%H.%M.%S", t)
        return current_time

    if option.lower() == 'both':
        #Date
        today = date.today()
        current_date = today.strftime("%d-%m-%Y")

        #Time
        t = time.localtime()
        current_time = time.strftime("%H.%M.%S", t)

        both = "({}) [{}]".format(current_date, current_time)
        return both

log_date_and_time = get_time_and_date("both") #Time run file was ran.

def print_and_log(importance_level=None, text=None, arg1=None, arg2=None):
    
    if text == None: #Just makes a new line.
        print("")
        path_to_log = log("")
        return path_to_log

    if not text == None:
        if importance_level == None:
            time = get_time_and_date("time")
            context = ("({}) {}".format(time, text))

            print(f"\u001b[37m{context}\u001b[0m")
            log(context)
            return

        if importance_level.upper() == 'INFO':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[36m{context}\u001b[0m") #Clay
            log(context)
            return

        if importance_level.upper() == 'INFO_2':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[32m{context}\u001b[0m") #Green
            log(context)
            return

        if importance_level.upper() == 'NO_GUILD_CONFIG_VALUE':
            time = get_time_and_date("time")
            context = ("({}) [INFO] '{}' is not available in '{}'s config so I'm just going to use the default value.".format(time, text, arg1))

            print(f"\u001b[32m{context}\u001b[0m") #Red
            log(context)
            return

        if importance_level.upper() == 'WARN':
            time = get_time_and_date("time")
            context = ("({}) [WARN] {}".format(time, text))

            print(f"\u001b[33m{context}\u001b[0m") #Yellow
            log(context)
            return


        if importance_level.upper() == 'ERROR':
            time = get_time_and_date("time")
            context = ("({}) [ERROR] {}".format(time, text))

            print(f"\u001b[31m{context}\u001b[0m") #Red
            log(context)
            return

        if importance_level.upper() == 'ERROR_COG':
            time = get_time_and_date("time")
            context = ("({}) [ERROR] Exception occured in {} '{}' method. >>> {}".format(time, text, arg1, arg2))

            print(f"\u001b[31m{context}\u001b[0m") #Red
            log(context)
            return

        if importance_level.upper() == 'APP_NAME':
            context = (text)

            print(f"\u001b[36m{context}\u001b[0m")
            log(context)
            return

def log(text):
    import settings

    #Create Logs Folder.
    try:
        os.mkdir(settings.path_to_logs)

    except FileExistsError as e:
        live_installer_status = "[Log Folder Already Exists]"

    f = open(f"{settings.path_to_logs}{log_date_and_time}.txt", "a", encoding='utf-8')
    f.write(text + "\n")

    return f"{settings.path_to_logs}{log_date_and_time}.txt"


def get_token():
    PATH = "./config/bot_token.txt"

    try:
        f = open(PATH, "r") #Opens text file containing bot token but creates if it doesn't exist.
        token = f.read()

        if token == "":
            print_and_log("error", "Please enter your discord token in the 'token.txt' file and run 'bot.py' again.")
            return False

        if token == "{ENTER BOT TOKEN HERE}":
            print_and_log("error", "Please enter your discord token in the 'token.txt' file and run 'bot.py' again.")
            return False

        else:
            f.close()
            return token

    except FileNotFoundError:
        f = open(PATH, "x")
        f = open(PATH, "w")
        f.write("{ENTER BOT TOKEN HERE}")
        print_and_log("warn", "'token.txt' did not exist so we created the file for you, now please enter your discord token in the text file and run 'bot.py' again.")

def get_database_url():
    PATH = "./config/database_url.txt"
    try:
        f = open(PATH, "r") #Opens text file containing bot token but creates if it doesn't exist.
        token = f.read()

        if token == "":
            print_and_log("warn", "Please enter your database URL in the 'database_url.txt' file and reload database.")
            print_and_log()
            f.close()
            return False

        if token.lower() == "none":
            f.close()
            return None

        if token == "{ENTER MONGODB CONNECTION URL HERE}":
            print_and_log("warn", "Please enter your database URL in the 'database_url.txt' file and reload database.")
            f.close()
            return False

        else:
            f.close()
            return token

    except FileNotFoundError:
        f = open(PATH, "x")
        f = open(PATH, "w")
        f.write("{ENTER MONGODB CONNECTION URL HERE}")
        print_and_log("warn", "'database_url.txt' did not exist so we created the file for you, now please enter your database URL in the text file and run 'bot.py' again.")

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

async def check_range(num, x_range, y_range): #Check if number is in range of x_range and y_range.
    if num in range(x_range, y_range):
        return True #Number is in range.
    else:
        return False #Number is not in range.


class json():
    async def get(path_to_file):
        try:
            f = open (path_to_file, "r")
            json_file = json.loads(f.read())

        except FileNotFoundError as e:
            print_and_log("warn", f"'{os.path.basename(path_to_file)}' was not found. Running update function and trying again. >>> {e}")
            from . import goldy_utility
            await goldy_utility.servers.update()

            f = open (path_to_file, "r")
            json_file = json.loads(f.read())

        return json_file

def create_folder(path):
    live_installer_status = "Creating a Folder..."
    print_and_log(None, "Creating Folder '" + path + "'")
    try:
        os.mkdir(path)
        os.chmod(path, stat.S_IWRITE)
        print_and_log(None, "[DONE]")
        print_and_log()
        return path

    except FileExistsError as e:
        live_installer_status = "[Folder Already Exists]"
        print_and_log("INFO", "This Folder Already Exists.")
        print_and_log()
        return path

def delete_file(file):
    live_installer_status = f"Deleting {file}..."
    print_and_log(None, f"Deleting {file}...")

    try:
        try:
            os.remove(file) #Deleting as fiile
        except OSError as e:
            shutil.rmtree(file) #If not file delete as directory with it's contexts.
        print_and_log(None, "[Done]")
        live_installer_status = "[Done]"

        print_and_log()
        return True

    except OSError as e:
        print_and_log("ERROR", f"Error occured while removing {file} \n {e}")
        live_installer_status = e
        return False

def move_files(from_dir, target_dir, text_label=None, replace=False): #Move multiple files from a directory.
    files = os.listdir(from_dir)

    for f in files:
        try:
            print(f)
            print_and_log(None, f"Moving {f} to {target_dir}")
            if not text_label == None:
                text_label.config(text=f"Moving {f} to {target_dir}")

            shutil.move(from_dir + f"/{f}", target_dir)
            print_and_log(None, "[Done]")

            if not text_label == None:
                text_label.config(text="[Done]")

        except Exception as e:
            if replace == True: #Deletes File and replaces it with new file. (Basically overwrites the file.)
                print_and_log("INFO", "Deleting file '{}'...".format(f))
                if not text_label == None:
                    text_label.config(text="Deleting file '{}'...".format(f))
                delete_file(target_dir + "/" + f)

                print_and_log(None, "[DONE]")
                if not text_label == None:
                    text_label.config(text="[DONE]")

                #Try moving again
                print_and_log(None, f"Moving {f} to {target_dir}")
                if not text_label == None:
                    text_label.config(text=f"Moving {f} to {target_dir}")

                try:
                    shutil.move(from_dir + f, target_dir)
                except Exception as e:
                    print_and_log("WARN", f"Could not replace {f}, so we skiping the file.")
                    pass

                print_and_log(None, "[Done]")

                if not text_label == None:
                    text_label.config(text="[Done]")

            else:
                print_and_log("ERROR", e)
                print_and_log()
                if not text_label == None:
                    text_label.config(text=e)


    print_and_log()
    return True

def move_file(path_to_file, target_dir, file_name=None, text_label=None, replace=False): #Move a single file
    try:
        print_and_log(None, f"Moving {path_to_file} to {target_dir}")
        shutil.move(path_to_file, target_dir)

        print_and_log(None, "[Done]")
        print_and_log()
        return True

    except Exception as e:
        if replace == True: #Deletes File and replaces it with new file. (Basically overwrites the file.)
            print_and_log("INFO", "Deleting file '{}'...".format(path_to_file))
            if not text_label == None:
                text_label.config(text="Deleting file '{}'...".format(path_to_file))
            delete_file(target_dir + "/" + file_name)

            print_and_log(None, "[DONE]")
            if not text_label == None:
                text_label.config(text="[DONE]")

            #Try moving again
            print_and_log(None, f"Moving {file_name} to {target_dir}")
            if not text_label == None:
                text_label.config(text=f"Moving {file_name} to {target_dir}")

            try:
                shutil.move(path_to_file, target_dir)
            except Exception as e:
                print_and_log("WARN", f"Could not replace {path_to_file}, so we skiping the file.")
                pass

            print_and_log(None, "[Done]")

            if not text_label == None:
                text_label.config(text="[Done]")

        else:
            print_and_log("ERROR", e)
            print_and_log()
            if not text_label == None:
                text_label.config(text=e)