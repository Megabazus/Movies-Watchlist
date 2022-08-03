import os.path
import json
from datetime import date

file_exists = os.path.exists('app.py')
print(file_exists)
today = date.today()
print(today)

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
print("d1 =", d1)

# Textual month, day and year
d2 = today.strftime("%B %d, %Y")
print("d2 =", d2)

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)

# Month abbreviation, day and year
d4 = today.strftime("%b-%d-%Y")
print("d4 =", d4)

# YYmmdd
d5 = today.strftime("%Y%m%d")
print("d5 =", d5)


# Load the daily file or extract it again if missing.
def daily_trend_extract(inputname):
    try:
        open_file = open('data/' + inputname)
        print("File exists")
        data = json.load(open_file)
        print(data)
        open_file.close()
    except:
        print("File does not exist")


daily_trend_extract('daily_trending_movies_%s.json' % d5)
