import requests, json
from pprint import pprint
import urllib
import os

class Crawler:

    url = ""
    base = "./temp/"
    temp_url = ""

    def __init__(self, url):
        self.url = url
        self.temp_url = url

    def myMainMethod(self, url=None):
        
        url = url if url else self.url
        hrefs = self.gettingAllHrefs(url)
        in_hrefs = self.gettingInsideHrefs(hrefs)
        filter_links = self.gettingFilteredLinks(in_hrefs)

        for key,val in enumerate(filter_links):
            returnVerify = self.verifyHasFolder(val)
            if returnVerify:
                self.myMainMethod(returnVerify)
            else:
                self.createFolderAndDownloadFile([val])
        
        print "completed"


    def verifyHasFolder(self, val):
        if val[-1] == '/':
            self.createDir(val[1:-1])
            self.temp_url = self.url + val[1:]
            return self.url + val[1:]
        return 0


    def createFolderAndDownloadFile(self, filter_links):

        for key, val in enumerate(filter_links):
            if val[-1] == '/':
                self.createDir(val[1:-1])
            else:
                filename = val[1:]
                self.download_files(self.url+filename, self.base+filename)
        return []

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
        base = self.base
        dir = dir.split('/')
        for key,val in enumerate(dir):
            if not os.path.isdir(base+val):
                os.makedirs(base+val)
            base = base + val + "/"
                

    def download_files(self, url, dir):
        filedownload = urllib.URLopener()
        filedownload.retrieve(url, dir)
        print "download_files", url


mycall = Crawler("http://example.com/package")
mycall.myMainMethod()