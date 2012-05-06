from datetime import datetime
import sys

class NoaaCycle:
    """ Interface to the structure of NOAA METAR cycle files
    """
    @staticmethod
    def current_date():
        """Get a date string for the current cycle
        """
        if sys.version_info[2] > 4:
            return NoaaCycle.current_date25()
        else:
            return NoaaCycle.current_date24()

    @staticmethod
    def current_file():
        """Get the name of the current cycle file as defined by
        http://weather.noaa.gov/weather/metar.shtml
        The name of a current file is {<UTC hour>-1}Z.TXT
        """
        hour = (23 + int(datetime.utcnow().strftime("%H")))%24
        if hour < 10:
            return "0%dZ.TXT" % hour
        else:
            return "%dZ.TXT" % hour

    @staticmethod
    def current_date25():
        """Get a date string for the current cycle (version 2.5 or later)
        """
        current_date = datetime.utcnow() 
        if(current_date.hour == 24):
            # 23Z.txt belongs to previous day
            current_date = datetime.utcnow() - datetime.timedelta(1)
        return current_date.strftime("%Y-%m-%d")

    @staticmethod
    def current_date24():
        """Get a date string for the current cycle (version for Python 2.4)
        """
        current_date = datetime.utcnow() 
        # 2do also decrement when last day of the month, last month of the year
        datestr = current_date.strftime("%Y-%m")
        day = current_date.day()
        if(current_date.hour == 24):
            # 23Z.txt belongs to previous day
            day = (current_date.day() - 1)
        datestr = datestr + "-%02d" % day
        return datestr
    @staticmethod 
    def last_month():
        """ Get formatted YYYY-MM string for the previous month
        """
        # 2do decrement month; decrement year if needed
        last_month = datetime.utcnow().strftime("%Y-%m")
        return last_month

