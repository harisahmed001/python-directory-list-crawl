import requests, json, urllib, os, shutil
from pprint import pprint

class Crawler:

    url = ""
    base = "./temp/"
    temp_url = ""
    myUrls = []

    def __init__(self, url):
        self.url = url
        self.temp_url = url

    def handle(self):
        url = self.url
        hrefs = self.gettingAllHrefs(url)
        in_hrefs = self.gettingInsideHrefs(hrefs)
        filter_links = self.gettingFilteredLinks(in_hrefs)

        for key, val in enumerate(filter_links):
            returnVerify = self.verifyHasFolder(val)
            if returnVerify[0]:
                self.processDepth(returnVerify[1])
            else:
                self.download_files(self.DownloadFileParsing(val))
        self.createZip()

        print "completed"

    def createZip(self):
        name = self.url
        name = name.replace("http://", "")
        name = name.replace("https://", "")
        name = name.replace("www.", "")
        name = name.strip("/")
        name = name.replace(".", "_")
        name = name.replace("/", "_")
        self.createDir('outputs')
        shutil.make_archive('outputs/'+name, 'zip', 'temp/')

    def processDepth(self, depthCheck):
        url = self.url + depthCheck
        hrefs = self.gettingAllHrefs(url)
        in_hrefs = self.gettingInsideHrefs(hrefs)
        filter_links = self.gettingFilteredLinks(in_hrefs)

        for key, val in enumerate(filter_links):
            returnVerify = self.verifyHasFolder(val)
            if returnVerify[0]:
                self.processDepth(returnVerify[1])
            else:
                self.download_files(depthCheck + self.DownloadFileParsing(val))

    def verifyHasFolder(self, val):
        if val[-1] == '/':
            startfrom = 1 if val[0] == "/" else 0
            self.temp_url = self.url + val[startfrom:]
            return [1, val[startfrom:]]
        val = val.split('/')
        val.remove(val[-1])
        val = '/'.join(val)
        return [0, val.strip('/') +'/']


    def DownloadFileParsing(self, val):
        startfrom = 1 if val[0] == "/" else 0
        filename = val[startfrom:]
        filename = filename.split('/')
        filename = filename[-1]
        return filename

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
        for key, val in enumerate(dir):
            if not os.path.isdir(base + val):
                os.makedirs(base + val)
            base = base + val + "/"

    def download_files(self, filename):
        base = self.base
        folders = filename.split('/')
        folders.remove(folders[-1])
        folders = '/'.join(folders)
        self.createDir(base + folders)
        filedownload = urllib.URLopener()
        print "downloading ", self.url + filename
        filedownload.retrieve(self.url + filename, base + "/" + filename)


mycall = Crawler("http://example,com/name/")
mycall.handle()