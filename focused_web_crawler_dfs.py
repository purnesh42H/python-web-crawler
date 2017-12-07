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
            if '/wiki/' in potentialLink:
                potentialLink = website + potentialLink.split('#')[0]
            else:
                return 'RejectedUrl'
        else:
            potentialLink = website + 'wiki/' + potentialLink
        return potentialLink
    
    return 'RejectedUrl'


# Focused Crawler with Depth First Search (Returns 1000 unique urls upto depth 5)
def dfsCrawler(url, keyword):
    fetchedUrls = [url]
    seedLinks   = getAllAnchorTexts(url)
    toCrawl     = []
    toCrawl.extend(reversed(seedLinks))                 # Reversing the list since Top->Bottom is followed and above pages are more important
                                                        # During the pop from the list, the last element will be first link of the page
    depth       = 1
    lastDepth   = [len(toCrawl)]
    n_fetchedUrls = 1
    
    while toCrawl:
        link = getIfValidUrl(toCrawl.pop(), keyword) 

        if link != 'RejectedUrl' and link not in fetchedUrls:
            print "At depth: %d" % depth
            print "Added url: " + link
            fetchedUrls.append(link)                    #Adding to the final url list

            if len(fetchedUrls) == 1000:
                break
                
            if depth < 5:
                newLinks = getAllAnchorTexts(link)          #Getting the links from current page, going deeper
                if len(newLinks) > 0:
                    toCrawl.extend(reversed(newLinks))      # Adding the new links to the list of pages to be crawled
                    lastDepth.append(len(toCrawl))
                    depth += 1                              # Increasing the depth

        if depth > 1 and len(toCrawl) < lastDepth[len(lastDepth) - 2]:     #Decreasing the depth, if all urls on a particular depth is visited once   
            lastDepth.remove(lastDepth[len(lastDepth) - 1])
            depth -= 1
                
    return fetchedUrls


# Main Function -> To call crawler and add download urls and pages            
frontier    = dfsCrawler('https://en.wikipedia.org/wiki/Sustainable_energy', 'solar')

writeFolder = os.getcwd() + '\\'
urlMode     = 'a+'
with open (writeFolder + 'wiki_urls_focused_dfs.txt', urlMode) as u: #Adding Urls to text files
    for url in frontier:
        u.write(url + '\n')

print "No. of Urls fetched: %d" % len(frontier)

isDownload = raw_input("Do you want to download the webpages? 1.Yes 2.No: ")
if(isDownload == "1"): #Downloading the pages
    print "Downloading Pages....."
    nPage = 1
    for url in frontier:
        htmlFile        = urllib.urlopen(url)
        htmlText        = htmlFile.read()
        with open (writeFolder + 'Task_2-B_Page_%d.txt' % nPage, urlMode) as u:
            u.write(htmlText)
        nPage += 1
    print "Finished Downloading Pages....."
