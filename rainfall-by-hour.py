import csv
from datetime import datetime, timedelta
from calendar import monthrange


def fifteen_minutes_before(date):
    '''For each row, we need to subtract fifteen minutes from the date because we
    really want to count each rain measurement for the fifteen minute period before it.
    For example, rain measured at 0:00:00 actually counts towards the amount it rained
    since 23:45 the previous day.'''
    return (datetime.strptime(date, "%m/%d/%Y %H:%M:%S") -
            timedelta(minutes=15)).timetuple()

# load data
f = open("data/tblModelRain.csv")
csv = csv.reader(f, delimiter=',', quotechar='"')

# skip header row
next(csv)

# construct bin for storing data
bin = {}
for gauge in range(1, 25):
    bin[gauge] = {}
    for year in range(1990, 2014):
        bin[gauge][year] = {}
        for month in range(1, 13):
            bin[gauge][year][month] = {}
            for day in range(1, monthrange(year, month)[1]+1):
                bin[gauge][year][month][day] = 0

# loop through all rows in csv
for row in csv:
    gauge = int(row[0])
    rainfall = float(row[2])
    date = fifteen_minutes_before(row[1])
    year, month, day = date[0], date[1], date[2]
    bin[gauge][year][month][day] += rainfall
    print gauge, year, month, day, bin[gauge][year][month][day]

output = open("data/output.txt", "w")
output.write(str(bin))
output.close()
