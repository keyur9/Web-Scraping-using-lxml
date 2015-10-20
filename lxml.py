# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 20:26:01 2015

@author: keyur
"""

import time,sys,urllib2
import requests
from lxml import html

def remove_nextlinechar(text):
    return text.replace('\n', ' ')

start_time = time.clock()
website = str('flipkart.com')
browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]
fileWriter=open('reviews.txt','w')
fileReader=open('in.txt')
index=0

Reviews = []
Rating=[]
Date=[]

for line in fileReader:
    reviewlink = line.strip()   
    print reviewlink
    page=0    
    while True:
        #url='http://www.flipkart.com/sony-bravia-klv-22p402b-54-7-cm-22-led-tv/product-reviews/ITMDV8ZAZVDNHRTQ?pid=TVSDV8J7S3EHY5BQ&rating=1,2,3,4,5&reviewers=all&type=top&sort=most_helpful&start='+str(page)
        
        #print url
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
        reviews = tree.xpath('//span[@class="review-text"]')
        for review in reviews:
            Reviews.append((review.text_content()).encode('utf8'))
        stars= tree.xpath('//div[@class="fk-stars"]/@title')
        for star in stars:
            Rating.append(star)
        dates=tree.xpath('//div[@class="date line fk-font-small"]/text()')
        for date in dates:
            Date.append(date)
            
        stop = tree.xpath('//div[@class="fk-text-center fk-font-big"]/text()')
        if stop:
                print 'Exiting..No more reviews for this product'
                break
        
        page+=10
        #print 'Going to page',page
        print 'Reviews Collected',len(Reviews)
        
        if (len(Reviews)==len(Rating)==len(Date)):
            while index < len(Reviews):
                fileWriter.write(website + '\t' + str(remove_nextlinechar(Reviews[index])) + '\t' + 
                str(Rating[index]) + '\t' + str(remove_nextlinechar(Date[index])) + '\n') 
                index+=1    
        else:
                print 'Some issue while writing data to file as records all records are not fetched.'

print 'Total Reviews Collected',len(Reviews)
print time.clock() - start_time, "seconds"
fileReader.close()
fileWriter.close()