import matplotlib
matplotlib.use('tkagg') # only needed for x-forwarding
import matplotlib.pyplot as p
import sqlite3
import pandas as pd
from urllib.parse import urlparse
from optparse import OptionParser
# based on https://applecrazy.github.io/blog/posts/analyzing-browser-hist-using-python/

# parse arguments
usage = "usage: %prog <SQLite file> [options]"
parser = OptionParser(usage=usage)
parser.add_option("-f","--firefox", action="store_true", dest="firefox",
                help="Switch for processing Firefox history file")
parser.add_option("-c","--chrome", action="store_true", dest="chrome",
                help="Switch for processing Chrome history file")
                
(browser, inputfile) = parser.parse_args()

try:
    inputfile = inputfile[0]
except IndexError:
    print("[!] You most likely forgot to give a filename as (SQLite) input")
    parser.print_help()
    exit(1)

db = sqlite3.connect(inputfile)
cursor = db.cursor()

# from http://forensicswiki.org/wiki/Mozilla_Firefox#History
# this will fetch all url's visited, with a timestamp in the (row) format of
# ('2016-10-12 10:17:21', 'http://nem.dcn.versatel.net/flow/devices')
if browser.firefox:
    cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id;''')
else:
    cursor.execute('''SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch'),url FROM  urls;''')
all_rows = cursor.fetchall()


data = pd.DataFrame(all_rows, columns=['datetime', 'url'])
# it can happen that Chrome messes up and registers timestamps of 1601-01-01 00:00:00
# pandas can't handle that so those entries are removed
if browser.chrome:
    print("[!] Will delete",len(data[data['datetime'] == '1601-01-01 00:00:00']),"rows with invalid 1601-01-01 00:00:00 timestamp")
    print(data[data['datetime'] == '1601-01-01 00:00:00'])
    data = data[data['datetime'] != '1601-01-01 00:00:00']
# convert datetime column to actual timestamps instead of strings
data.datetime = pd.to_datetime(data.datetime)

# only keep the (sub)domain from url's
parser = lambda u: urlparse(u).netloc
data.url = data.url.apply(parser)

# get visit counts per domain, in a new frame
site_frequencies = data.url.value_counts().to_frame()
site_frequencies = site_frequencies.reset_index()
site_frequencies.columns = ['domain', 'count']

# do some plotting
topN = 20
p.figure(1, figsize=(10,10))
p.title('Top $n sites visited'.replace('$n', str(topN)))
pie_data = site_frequencies['count'].head(topN).tolist()
pie_labels = None
pie_labels = site_frequencies['domain'].head(topN).tolist()
p.pie(pie_data, autopct='%1.1f%%', labels=pie_labels)
p.show()