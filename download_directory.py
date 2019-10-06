import requests, json
from pprint import pprint
import urllib
import os

class Crawler:

    url = ""
    base = "./temp/"
    temp_url = ""
    level_in = 0
    current_url = {}

    def __init__(self, url):
        self.url = url
        self.temp_url = url

    def myMainMethod(self, url=None, level=0):
        self.level_in = level
        url = url if url else self.url
        hrefs = self.gettingAllHrefs(url)
        in_hrefs = self.gettingInsideHrefs(hrefs)
        filter_links = self.gettingFilteredLinks(in_hrefs)

        print "filter_links", filter_links

        for key,val in enumerate(filter_links):
            returnVerify = self.verifyHasFolder(val)
            print "returnVerify" , returnVerify
            if returnVerify[0]:
                self.current_url[level] = returnVerify[1]
                self.myMainMethod(returnVerify[1], level+1)
            else:
                self.current_url[level] = returnVerify[1]
                self.DownloadFileParsing(val)
        
        return level


    def verifyHasFolder(self, val):
        if val[-1] == '/':
            startfrom = 1 if val[0] == "/" else 0
            self.temp_url = self.url + val[startfrom:]
            return [1,self.url + val[startfrom:]]
        val = val.split('/')
        val.remove(val[-1])
        val = '/'.join(val)
        return [0, self.url + val.strip('/') +'/']


    def DownloadFileParsing(self, val):
        startfrom = 1 if val[0] == "/" else 0
        if val[-1] != '/':
            filename = val[startfrom:]
            filename = filename.split('/')
            filename = filename[-1]
            self.download_files(filename)

    def gettingAllHrefs(self, url):

        sessionRequest = requests.session()
        requestObj = requests.get(url)
        content = requestObj.content

        myFullLinks = []
        run = 1
        start_from = 0
        while (run):
            hrefs = content.find('<a href', start_from)
            if hrefs != -1:
                hrefs = hrefs + 1
                end_hrefs = content.find('</a>', hrefs)
                myFullLinks.append(content[hrefs - 1:end_hrefs + 4])
                start_from = hrefs
            else:
                run = 0

        return myFullLinks

    def gettingInsideHrefs(self, data):

        if len(data) < 1:
            return []

        in_hrefs = []
        for key, val in enumerate(data):
            occ = val.find('href=', 0)
            occ = occ + 5
            end = val.find('>', occ + 1)
            final = val[occ + 1: end - 1]
            in_hrefs.append(final)

        return in_hrefs

    def gettingFilteredLinks(self, data):
        if len(data) < 1:
            return []

        returnList = []
        urlParams = self.getUrlParams()
        hostname = urlParams[0] + '//' + urlParams[1]
        for key, val in enumerate(data):
            if "?" not in val and hostname + val not in self.temp_url:
                returnList.append(val)

        returnList = self.removeUrlExisting(returnList)

        return returnList

    def removeUrlExisting(self, links):
        for x, word in enumerate(links):
            for xx, rem in enumerate(self.getUrlParams()):
                if rem in word:
                    links[x] = links[x].replace("" + rem + "/", "")

        return links

    def getUrlParams(self):
        urlWords = self.url.split('/')
        urlWords = filter(None, urlWords)
        return urlWords
		

    def createDir(self, dir):
        base = ""
        dir = dir.split('/')
        for key,val in enumerate(dir):
            if not os.path.isdir(base+val):
                os.makedirs(base+val)
            base = base + val + "/"
                

    def download_files(self, filename):
        base = self.base
        folders = (self.current_url[self.level_in -1]).replace(self.url, "")
        downloadDir = base + folders.strip('/')
        self.createDir(downloadDir)
        filedownload = urllib.URLopener()
        print "downloading ",self.current_url[self.level_in -1] + filename
        filedownload.retrieve(self.current_url[self.level_in -1] + filename , downloadDir+"/"+filename)



mycall = Crawler("https://www.example.com/")
mycall.myMainMethod()