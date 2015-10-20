# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 20:26:01 2015
Time taken: 590.886340908 seconds
@author: keyur

### Name: Keyur Doshi
### Student ID: 10405923
### BIA 660B Mid Term Project

Description:

Mid Term project which will perform the following:

Step 1: Select 4 different websites that include reviews on TVs. The reviews should include text, a date of submission, and a star rating.

Step 2: Collect at least 1000 TV reviews from each of the 4 websites. Use a different python script for each website.

Step 3: Store all the reviews from all 4 websites in a single file called "reviews.txt". The file should include the following TAB-separated columns:

: website where the review came from (e.g. amazon.com).
: the FULL review text, exactly as it appears on the website.
: the review's rating 
: the review's date of submission, as it appears on the website.

"""
#Importing libraries
import time,sys,urllib2
import requests
from lxml import html

#Function to replace new line in reviews
def remove_nextlinechar(text):
    return text.replace('\n', ' ')

#Capturing the start time of this program
start_time = time.clock()

#WebSite used for parsing
website = str('flipkart.com')

#Initializing browser
browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

#create a new file and open a connection to it.
fileWriter=open('reviews.txt','w')
fileReader=open('in.txt')

#Initiallizing index
index=0

#Creating the list to store all the records 
ReviewList = []
RatingList=[]
DateList=[]

for line in fileReader:
    #Fetch the url from file in.txt    
    reviewlink = line.strip()   
    print reviewlink
    page=0    
    while True:
        url = reviewlink + str(page)
        #Opening the url    
        try:
            myHtml=requests.get(url,timeout=(10.0))
            time.sleep(2) 
        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            print 'ERROR FOR URL:',url
            print error_type, 'Line:', error_info.tb_lineno
            continue
        
        tree = html.fromstring(myHtml.text)   
       
        #Will parse the Reviews and append it to the list        
        reviews = tree.xpath('//span[@class="review-text"]')
        for review in reviews:
            ReviewList.append((review.text_content()).encode('utf8'))

        #Will parse the Ratings and append it to the list        
        stars= tree.xpath('//div[@class="fk-stars"]/@title')
        for star in stars:
            RatingList.append(star)
        
        #Will parse the Dates and append it to the list    
        dates=tree.xpath('//div[@class="date line fk-font-small"]/text()')
        for date in dates:
            DateList.append(date)
            
        #Will check if reviews are available     
        stop = tree.xpath('//div[@class="fk-text-center fk-font-big"]/text()')
        if stop:
                print 'Exiting..No more reviews for this product'
                break
        
        page+=10
        #print 'Going to page',page
        print 'Reviews Collected',len(ReviewList)
        
        #Comparing length and writing data to file.
        if (len(ReviewList)==len(RatingList)==len(DateList)):
            while index < len(ReviewList):
                fileWriter.write(website + '\t' + str(remove_nextlinechar(ReviewList[index])) + '\t' + 
                str(RatingList[index]) + '\t' + str(remove_nextlinechar(DateList[index])) + '\n') 
                index+=1    
        else:
                print 'Some issue while writing data to file as records all records are not fetched.'

print 'Total Reviews Collected',len(ReviewList)

#Printing the running time   
print time.clock() - start_time, "seconds"

#Closing the FileReader    
fileReader.close()

#Closing the File Writer
fileWriter.close()