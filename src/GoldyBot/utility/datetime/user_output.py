import datetime

def make_time_human(datetime:datetime.datetime, time_format:str="%I:%M%p"):
    """A Goldy Bot util function to convert datetime object to human readable form so dumb humans can read it, smh!"""

    return datetime.strftime(time_format)

def make_date_human(datetime:datetime.datetime, date_format:str="%d/%m/%Y"):
    """A Goldy Bot util function to convert datetime object to human readable form so dumb humans can read it, smh!"""

    return datetime.strftime(date_format)

def make_date_and_time_human(datetime:datetime.datetime, datetime_format:str="%d/%m/%Y - %H:%M"):
    """A Goldy Bot util function to convert datetime object to human readable form so dumb humans can read it, smh!"""

    return datetime.strftime(datetime_format)