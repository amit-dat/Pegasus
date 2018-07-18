
'''
BeautifulSoup Instagram Scraper that gets all pictures posted by celebrities yesterday (max 12 pictures per celeb)
'''

import requests
import json
import os
import pprint
import sys
import milpy
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from accounts import accounts
#from emoji import emoji

#Configuration
instagram = 'http://www.instagram.com/' 
yesterday = (datetime.today()- timedelta(days=1)).strftime('%Y-%m-%d') 
limiting_date = "2018-03-15"
pictureFolder = os.path.join('.','Instagram_Pictures',yesterday)


        
for p in [pictureFolder]: #makes the prequiste folders, if they don't already exits
    if os.path.exists(p) == False:
        os.makedirs(p)


def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

def picFinder(account):    
    try:
        rgram = requests.get(instagram + account) #accesses the instagram account
        rgram.raise_for_status()
    except requests.exceptions.HTTPError: #this handles exceptions if accounts get deleted or suspended. Does not handle exceptions for accounts made private
        print('\t \t ### ACCOUNT MISSING ###')
    else:        
        selenaSoup=BeautifulSoup(rgram.text,'html.parser')
        print(selenaSoup)
        pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
        for i, j in enumerate(pageJS): #Converts pageJS to list of strings so i can calculate length for below. If BS4 has a neater way of doing this, I haven't found it.
            pageJS[i]=str(j)
        picInfo= sorted(pageJS,key=len, reverse=True)[0] #finds the longest bit of JavaScript on the page, which always contains the image data
        #print(picInfo)
        allPics = json.loads(str(picInfo)[52:-10])['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']#['media']['nodes']

    return allPics



def picDownloader(account):
    for picture in picFinder(account):
        if datetime.fromtimestamp(picture['node']['taken_at_timestamp']).strftime('%Y-%m-%d') < yesterday and datetime.fromtimestamp(picture['node']['taken_at_timestamp']).strftime('%Y-%m-%d') >  limiting_date: #finds pictures from yesterday
                print('\tDownloading picture '+DateStamp(picture['node']['taken_at_timestamp']))
                picRes = requests.get(picture['node']['display_url'])
                picFileName = os.path.join(pictureFolder, account+'_'+DateStamp(picture['node']['taken_at_timestamp'])+'.jpg')
                picFile = open(picFileName,'wb')

                for chunk in picRes.iter_content(100000):
                    picFile.write(chunk)

                picFile.close()
                


    
def main():
    print('downloading pictures:')
    for c, account in enumerate(accounts,1):
        print(c,'Pictures from today on '+account+'\'s Instagram')
        picDownloader(account)
    print('finding dominant colour')
    milpy.directory_image_average(pictureFolder, '.jpg')



if __name__ == '__main__':
    main()