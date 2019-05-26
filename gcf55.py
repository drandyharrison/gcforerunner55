
# https://github.com/sirfoga/pygce

# Example of summary statistics, can we use them in analysing this data
#agg_summary = csvdata.groupby(['year', 'country']).agg({'accept': [sum, "mean", "count"]})
#print(agg_summary)

#summary = pandas.DataFrame(data=csvdata.groupby(['year', 'country'])['accept'].sum())
#summary = summary.assign(mean=csvdata.groupby(['year', 'country'])['accept'].mean(),
#                         count=csvdata.groupby(['year', 'country'])['accept'].count())
#print(summary)

# !/usr/bin/python3
# coding: utf-8

import os
import ast
import ash_utils
from datetime import datetime
from pygce.models.bot import GarminConnectBot

AVAILABLE_OUTPUT_FORMATS = ["json", "csv"]


def str2bool(v: str):
    """
    :param v: str
        boolean value
    :return: bool
        True if string holds a true value; otherwise False
    """
    assert(isinstance(v, str))
    return v.lower() in ("yes", "true", "t", "1")


def parse_yyyy_mm_dd(d):
    """
    :param d: str
        Date in the form yyyy-mm-dd to parse
    :return: datetime
        Date parsed
    """

    d = str(d).strip()  # discard jibberish
    return datetime.strptime(d, "%Y-%m-%d")


def check_args(user, password, url, chromedriver, days, out_dir):
    """
    :param user: str
        User to use
    :param password: str
        Password to use
    :param url: str
        Url to connect to
    :param chromedriver: str
        Path to chromedriver to use
    :param days: [] of datetime.date
        Days to save
    :param out_dir: str
        Directory to write to with output
    :return: bool
        True iff args are correct
    """

    assert (len(user) > 1)
    assert (len(password) > 1)
    assert ("https" in url and "garmin" in url)
    assert (os.path.exists(chromedriver))
    assert (2 == len(days))
    assert (isinstance(days[0], datetime))
    assert (days[0] <= days[1])  # start day <= end day

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)  # create necessary dir for output file

    return True


def get_gc_data(user: str, password: str, chromedriver: str, days: list, url: str = "https://connect.garmin.com/signin/",
                out_dir: str = ".", format_out: str = "csv", download_gpx: bool = False):
    """
    :param user: str
        User to use
    :param password: str
        Password to use
    :param chromedriver: str
        Path to chromedriver to use
    :param days: [] of datetime.date
        Days to save
    :param url: str
        Url to connect to
    :param out_dir: str
        Directory to write to with output
    :param format_out: str
        Output format: JSON or CSV
    :param download_gpx: bool
        download GPX activities
    :return: bool
        True iff args are correct
    """
    # not needed as not passing arguments from the command line
    # path_out = parse_args(create_args())

    if check_args(user, password, url, chromedriver, days, out_dir):
        bot = GarminConnectBot(user, password, download_gpx, chromedriver, url=url)

        arg_tuple = user, password, url, chromedriver, days, download_gpx, out_dir
        try:
            if format_out == "json":
                bot.save_json_days(days[0], days[1], arg_tuple)
            elif format_out == "csv":
                bot.save_csv_days(days[0], days[1], arg_tuple)

        except Exception as e:
            raise e
        finally:
            bot.close()
    else:
        print("Error while parsing args.")

# ===========================
# ====== main function ======
# ===========================


def main():
    # read config from a JSON
    jsonhndlr = ash_utils.JSONhandler("gcf55_config.json")
    if jsonhndlr.read_json():
        # read key values from config file (and cast as necessary)
        user = jsonhndlr.get_val('user')
        password = jsonhndlr.get_val('password')
        chromedriver = jsonhndlr.get_val('chromedriver')
        # ast.literal_eval() converts a string representation of a list into a list
        days = ast.literal_eval(jsonhndlr.get_val('days'))
        assert(2 == len(days))
        days = list(map(parse_yyyy_mm_dd, days))
        url = jsonhndlr.get_val('url')
        out_dir = jsonhndlr.get_val('out_dir')
        format_out = jsonhndlr.get_val('format_out')
        # convert to bool
        download_gpx = str2bool(jsonhndlr.get_val('download_gpx'))

    get_gc_data(user, password, chromedriver, days, url, out_dir, format_out, download_gpx)


if __name__ == "__main__":
    main()
