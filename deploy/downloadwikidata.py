import requests
from BeautifulSoup import BeautifulSoup
from subprocess import call


print "Downloading links"
response = requests.get("http://dumps.wikimedia.org/other/wikidata/")
soup = BeautifulSoup(response.content)
link = "http://dumps.wikimedia.org/other/wikidata/" + str(soup.findAll('a')[-1].get("href"))

print "Downloding last dump: " + str(link)
call(["wget",link])

print "Decompressing last dump"
call(['gunzip', '-d', str(soup.findAll('a')[-1].get("href"))])

