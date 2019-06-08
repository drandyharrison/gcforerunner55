
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

import ash_utils

# ===========================
# ====== main function ======
# ===========================


def main():
    gcf = ash_utils.GarminHandler("gcf55_config.yml")
    gcf.get_gc_data()


if __name__ == "__main__":
    main()
