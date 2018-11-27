##-- PrinterConfigScrape.ps1 ------------------------------
#
# Author:
#  David Martin
#
# Purpose:
#  Scrape HTML data pulled from web tool
# 
# Description:
#  This was written to test out web scraping and reorganising
#  of HTML table data. The program was written specifically for
#  an in-house print management tool which pulled its data from
#  a database. The URL and other identifying components of the script
#  have been removed for privacy reasons.
#
# Execution:
#  This code was specifically written for the HTML of the in-house printer tool
#  and this modified version is more a demonstration of the techniques
#  involved in web scraping.
#
##--------------------------------------------------


#-----------------------------------------
# Import libraries and declare variables
#-----------------------------------------

import requests
from requests_ntlm import HttpNtlmAuth
import pandas as pd
from bs4 import BeautifulSoup

# Get URL
url = Read-Host 'Enter URL to scrape...'

# Get HTTP auth username & password
username = Read-Host 'Enter username...'
password = Read-Host 'Enter password...'

# Define our arrays for column data storing
site_code = []
site = []
subnet = []
subnet_mask = []
legacy_ip = []
active = []
migrated = []



#-----------------------------------------------
# Perform HTTP request and parse returned data
#-----------------------------------------------

requests.packages.urllib3.disable_warnings()
r = requests.get(url, auth=HttpNtlmAuth(username, password), verify=False)

# Turn the HTML into a BS object
soup = BeautifulSoup(r.text, 'lxml')

# Create a table object for the HTML element
table = soup.find(class_='nowrap grid fullwidth')

# Find all the <tr> tag pairs and store the values
for row in table.find_all('tr')[1:]:
    col = row.find_all('td')

    column_1 = col[0].string.strip()
    site_code.append(column_1)

    column_2 = col[1].string.strip()
    site.append(column_2)

    column_3 = col[2].string.strip()
    subnet.append(column_3)

    column_4 = col[3].string.strip()
    subnet_mask.append(column_4)

    column_5 = col[4].string.strip()
    legacy_ip.append(column_5)

    column_6 = col[5].select("select > option[selected='selected']")[0].string.strip()
    active.append(column_6)

    column_7 = col[6].select("select > option[selected='selected']")[0].string.strip()
    migrated.append(column_7)
	


#-----------------------------------------------
# Organise data and present in console
#-----------------------------------------------

# Store our arrays in a dictionary object
columns = {'Site Code': site_code,
           'Site': site,
           'Subnet': subnet,
           'Subnet Mask': subnet_mask,
           'Legacy IP': legacy_ip,
           'Active': active,
           "Migrated": migrated
           }

# Change console width for display purposes
desired_width = 800
pd.set_option('display.width', desired_width)

# Organises table data into DataFrame for neat presentation
df = pd.DataFrame(columns)
df = df[['Site Code', 'Site', 'Subnet', 'Subnet Mask', 'Legacy IP', 'Active', 'Migrated']]
print(df)