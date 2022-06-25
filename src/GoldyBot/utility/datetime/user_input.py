import dateparser

def get_time(human_time_string_OwO:str, time_formats=["%H:%M"]):
    """A Goldy Bot util function to read human time string inputs and convert them to a datetime object."""

    return dateparser.parse(human_time_string_OwO, 
            date_formats=time_formats)

def get_date(human_date_string_UwU:str, date_formats=["%d/%m/%Y", "%Y/%m/%d"]):
    """A Goldy Bot util function to read human date string inputs and convert them to a datetime object."""

    return dateparser.parse(human_date_string_UwU, 
            date_formats=date_formats)

def get_time_and_date(human_time_date_string_UWU_OWO:str, datetime_formats=["%d/%m/%Y %H:%M", "%Y/%m/%d %H:%M"]):
    """A Goldy Bot util function to read both human date and time string inputs together and convert them to a datetime object."""

    return dateparser.parse(human_time_date_string_UWU_OWO, 
        date_formats=datetime_formats)