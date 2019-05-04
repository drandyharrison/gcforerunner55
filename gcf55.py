
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

import argparse
import os
from datetime import datetime
from pygce.models.bot import GarminConnectBot

AVAILABLE_OUTPUT_FORMATS = ["json", "csv"]

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
    assert (len(days) == 2)
    days[0] = parse_yyyy_mm_dd(days[0])
    days[1] = parse_yyyy_mm_dd(days[1])
    assert (isinstance(days[0], datetime))
    assert (days[0] <= days[1])  # start day <= end day

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)  # create necessary dir for output file

    return True

def get_gc_data(user:str, password:str, chromedriver:str, days:list, url:str="https://connect.garmin.com/signin/",
                out_dir:str=".", format_out:str="csv", download_gpx:bool=False):
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

# =======================
# ====== main body ======
# =======================
# TODO read these from a config JSON
user = "iam.andyharrison@gmail.com"
password = "Hog$ToRSING5"
chromedriver = "C:/Users/iaman/AppData/Local/Programs/Python/Python37/chromedriver-Windows"
days = ["2019-04-14", "2019-04-14"]
url = "https://connect.garmin.com/signin/"
out_dir = "./mygarmin/"
format_out = "csv"
download_gpx = False

get_gc_data(user, password, chromedriver, days, url, out_dir, format_out, download_gpx)
