A script that takes an SQLite db containing web browsing history as input, and outputs graphs showing most "popular" sites

Should make for a fun experiment to couple it to another program that generates fake web history entries

# Usage
The script is made to work over a sessionw with X-forwarding enabled.  
To avoid issues and disable this, comment out the first two lines:  
`import matplotlib`  
`matplotlib.use('tkagg')`

For Chrome history on a Windows machine, the SQLite file that Chrome stores browsing history in is at:  
C:\Users\\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\History

For Firefox history on a Windows machine:  
C:\Users\\%USERNAME%\AppData\Roaming\Mozilla\Firefox\Profiles\mq3xjipq.default\places.sqlite

Run with: `python history.py <SQLite file> [options]`  

Options:  
  -h, --help     show this help message and exit  
  -f, --firefox  Switch for processing Firefox history file  
  -c, --chrome   Switch for processing Chrome history file  
