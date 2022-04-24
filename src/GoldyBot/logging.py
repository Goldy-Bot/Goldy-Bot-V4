import os
import time
from datetime import date
import traceback

import GoldyBot

MODULE_NAME = "LOGGING"

def print_and_log(importance_level=None, text=None, no_traceback=False):
    """Goldy Bot's Print statement. PLEASE use this statement instead of the usual 'print()'."""
    if text == None: # Just makes a new line.
        if importance_level == None:
            print("")
            path_to_log = write_to_log("")
            return path_to_log

        if isinstance(importance_level, GoldyBot.errors.GoldyBotError):
            time = get_time_and_date("time")
            context = ("({}) [ERROR] {}".format(time, text))
            print(f"\u001b[31m{context} \n{traceback.format_exc()}\u001b[0m") #Red
            write_to_log(f"{context}\n\n{traceback.format_exc()}")
            return

        else:
            time = get_time_and_date("time")
            context = ("({}) {}".format(time, importance_level))

            print(f"\u001b[37m{context}\u001b[0m")
            
            path_to_log = write_to_log(context)
            return path_to_log

    if not text == None:
        if importance_level == None:
            time = get_time_and_date("time")
            context = ("({}) {}".format(time, text))

            print(f"\u001b[37m{context}\u001b[0m")
            write_to_log(context)
            return

        if importance_level.upper() == 'INFO':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[36m{context}\u001b[0m") # Blue
            write_to_log(context)
            return

        if importance_level.upper() == 'INFO_2':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[32m{context}\u001b[0m") # Green
            write_to_log(context)
            return

        if importance_level.upper() == 'INFO_3':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[38;5;51m{context}\u001b[0m") # Clay
            write_to_log(context)
            return

        if importance_level.upper() == 'INFO_4':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[38;5;200m{context}\u001b[0m") # Purple
            write_to_log(context)
            return

        if importance_level.upper() == 'INFO_5':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[38;5;139m{context}\u001b[0m") # Pink Grey
            write_to_log(context)
            return

        if importance_level.upper() == 'WARN':
            time = get_time_and_date("time")
            context = ("({}) [WARN] {}".format(time, text))
            
            if not no_traceback:
                print(f"\u001b[33m{context}\u001b[0m") #Yellow
            write_to_log(f"{context}\n\n{traceback.format_exc()}")
            return


        if importance_level.upper() == 'ERROR':
            time = get_time_and_date("time")
            context = ("({}) [ERROR] {}".format(time, text))
            if not no_traceback:
                print(f"\u001b[31m{context} \n{traceback.format_exc()}\u001b[0m") #Red
            write_to_log(f"{context}\n\n{traceback.format_exc()}")
            return

        if importance_level.upper() == 'APP_NAME':
            context = (text)

            print(f"\u001b[36m{context}\u001b[0m")
            write_to_log(context)
            return

log = print_and_log

# Date and time generator function.
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

log_date_and_time = get_time_and_date("both") #Time jsqp was started.

# Txt Logging Function
def write_to_log(text):
    #Create Logs Folder.
    paths = GoldyBot.paths

    try:
        os.mkdir(paths.LOGS)
    except FileExistsError as e:
        pass

    except Exception:
        print("^ Could not write_to_log that ^")
        return False

    f = open(f"{paths.LOGS}/{log_date_and_time}.txt", "a", encoding='utf-8')
    f.write(text + "\n")

    return f"{paths.LOGS}/{log_date_and_time}.txt"