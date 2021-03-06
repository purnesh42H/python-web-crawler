#!/usr/bin/env python

import urllib
import re
import time
import os

website = 'https://en.wikipedia.org/'

# To get the anchor text links in the page
# It is achieved through regular expression
def getAllAnchorTexts(link):
    keywordAnchorRegex  = '<a href="/wiki/(.+?)</a>'                    # Regular expression to get urls which has keyword
    pattern         = re.compile(keywordAnchorRegex, re.IGNORECASE)
    print "Suspending for a second, politeness"
    time.sleep(1)                                                       #Delay of 1 second before requesting web page
    htmlFile        = urllib.urlopen(link)
    htmlText        = htmlFile.read()
    newLinks        = re.findall(pattern,htmlText)
    return newLinks



# To get the full url from the string if it's a valid url as per specifications else return 'RejectedUrl'
def getIfValidUrl(link, keyword):
    if keyword.lower() not in link.lower():
        return 'RejectedUrl'
    
    potentialLink = link.split('"')[0]
    if ':' not in potentialLink:
        if '#' in potentialLink and 'cite' not in potentialLink.lower():
            if '/wiki/' in potentialLink.lower():
                potentialLink = website + potentialLink.split('#')[0]
            else:
                return 'RejectedUrl'
        else:
            potentialLink = website + 'wiki/' + potentialLink
        return potentialLink
    
    return 'RejectedUrl'

# Focused Crawler with Breadth First Search (Returns top 1000 unique urls upto depth 5)
def bfsCrawler(url, keyword):
    fetchedUrls     = [url]
    seedLinks       = reversed(getAllAnchorTexts(url)) # Reversing the list since Top->Bottom is followed and above pages are more important
                                                                # During the pop from the list, the last element will be first link of the page
    toCrawl         = []

    toCrawl.extend(seedLinks)
    nextDepth       = [1]
    depth           = 1
    n_fetchedUrls   = 1

    print ("Start depth: %d" % depth)
    while toCrawl:
        link = getIfValidUrl(toCrawl.pop(), keyword)
        if link != 'RejectedUrl' and link not in fetchedUrls:
            print "Added Url: " + link
            fetchedUrls.append(link)

        if len(fetchedUrls)  == 1000 or depth == 5:              # Break if 1000 unique urls are found
            break
        while len(toCrawl)   == 1 and n_fetchedUrls < len(fetchedUrls): #Loop until a url with anchor text is found
            if n_fetchedUrls == nextDepth[depth-1]:
                nextDepth.append(len(fetchedUrls))
                depth += 1
                print ("Changed to depth: %d" % depth)
            toCrawl.extend(reversed(getAllAnchorTexts(fetchedUrls[n_fetchedUrls]))) #Adding new links to toCrawl
            n_fetchedUrls += 1

    print ("Ended at depth: %d" % depth)
    return fetchedUrls

#Main Function -> To call crawler and download urls and pages
frontier    = bfsCrawler('https://en.wikipedia.org/wiki/Sustainable_energy', 'solar')
writeFolder = os.getcwd() + '\\'
urlMode     = 'a+'
with open (writeFolder + 'wiki_urls_focused_bfs.txt', urlMode) as u:
    for url in frontier:
        u.write(url + '\n')

print "No. of Urls fetched: %d" % len(frontier)

isDownload = raw_input("Do you want to download the webpages? 1.Yes 2.No: ")
if(isDownload == "1"):
    print "Downloading Pages....."
    nPage = 1
    for url in frontier:
        htmlFile        = urllib.urlopen(url)
        htmlText        = htmlFile.read()
        with open (writeFolder + 'Task_2-A_Page_%d.txt' % nPage, urlMode) as u:
            u.write(htmlText)
        nPage += 1
    print "Finished Downloading Pages....."
