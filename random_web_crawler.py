#!/usr/bin/env python

import urllib
import re
import time
import os

website = 'https://en.wikipedia.org/'

# To get all the hyperlinks prefixed with wiki
# It is achieved through regular expression
def getAllLinksOnPage(link):
    keywordAnchorRegex  = '<a href="/wiki/(.+?)"'
    pattern         = re.compile(keywordAnchorRegex)
    print "Suspending for a second, politeness"
    time.sleep(1)
    htmlFile        = urllib.urlopen(link)
    htmlText        = htmlFile.read()
    newLinks        = re.findall(pattern,htmlText)
    return newLinks

# To get only the url from the string
# To get the full url from the string if it's a valid url as per specifications else return 'RejectedUrl'
def getIfValidUrl(link):
    potentialLink = link.split('"')[0]
    if ':' not in potentialLink and potentialLink != 'Main_Page':
        if '#' in potentialLink and 'cite' not in potentialLink.lower():
            if '/wiki/' in potentialLink.lower():
                potentialLink = website + potentialLink.split('#')[0]
            else:
                return 'RejectedUrl'
        else:
            potentialLink = website + 'wiki/' + potentialLink
        return potentialLink
    
    return 'RejectedUrl'

def crawler(url):
    fetchedUrls     = [url]
    seedLinks   = reversed(getAllLinksOnPage(url))  # Reversing the list since Top->Bottom is followed and above pages are more important
                                                    # During the pop from the list, the last element will be first link of the page
    toCrawl     = []
    toCrawl.extend(seedLinks)
    nextDepth   = [1]
    depth       = 1
    n_fetchedUrls   = 1

    print ("Start depth: %d" % depth)
    while toCrawl:
        link = getIfValidUrl(toCrawl.pop())
        if link != 'RejectedUrl' and link not in fetchedUrls:
            print "Added Url: " + link
            fetchedUrls.append(link) #Adding to the final url list

        if len(fetchedUrls) == 1000 or depth == 5:
            break
        if len(toCrawl) == 1:
            if n_fetchedUrls == nextDepth[depth-1]:             # Increasing the depth, if all urls on a particular depth is visited once
                nextDepth.append(len(fetchedUrls))
                depth += 1
                print ("Changed to depth: %d" % depth)
            toCrawl     = []
            toCrawl.extend(reversed(getAllLinksOnPage(fetchedUrls[n_fetchedUrls]))) #Adding new links to crawl
            n_fetchedUrls += 1
            

    print ("Ended at depth: %d" % depth)
    return fetchedUrls

#Main Function         
frontier    = crawler('https://en.wikipedia.org/wiki/Sustainable_energy')
writeFolder = os.getcwd() + '\\'
urlMode     = 'a+'
with open (writeFolder + 'wiki_urls_random.txt', urlMode) as u:  # Adding urls to text file
    for url in frontier:
        u.write(url + '\n')

print "No. of Urls fetched: %d" % len(frontier)

isDownload = raw_input("Do you want to download the webpages? 1.Yes 2.No: ")
if(isDownload == "1"):                                          # Downloading pages
    print "Downloading Pages....."
    nPage = 1
    for url in frontier:
        htmlFile        = urllib.urlopen(url)
        htmlText        = url + '\n' + htmlFile.read()
        with open (writeFolder + 'Corpus\\Task1\\%s.txt' % url.split('/')[len(url.split('/')) - 1], urlMode) as u:
            u.write(htmlText)
        nPage += 1
    print "Finished Downloading Pages....."
