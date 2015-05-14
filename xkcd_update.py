"""

When run, the program will check what comics have already been downloaded, which at first will be 0. 
It will then continue to download all xKCD comics up to the most recent one.

After this, whenever the program is run, it will check if any new xKCD comics have been uploaded and 
will then download them and launch the image in your default image-opening program.


"""

import requests
from bs4 import BeautifulSoup
import urllib.request
#For finding max filenumber:
import glob
import re
import win32api
global dlSession
import subprocess
import os
dlSession = 0
errors = 0


def findHighestComic():


	directory = "comics"
	#Creates a 'comics' folder if non-existant
	if not os.path.exists(directory):
		os.makedirs(directory)

	allfiles = []
	allfiles1 = []
	allfiles2 = []

	for filename in glob.glob("comics/**"):
		name = filename.split('xkcd_',1)
		allfiles += name

	
		
	#Extract numbers from filenames
	for filename in allfiles:
		filename = str(filename)
		numo = re.findall('\d+', filename)
		allfiles1 += numo

	for numoo in allfiles1:
		numoo = int(numoo)
		allfiles2.append(numoo)
		


	try:
		return(max(allfiles2))
	except:
		return(0)


def downloadComics(downloadFromNo):
	global dlSession
	global errors
	comicNo = (downloadFromNo)
	while comicNo != -1:
		#Chosen page to scrape
		try:
			page = requests.get("http://xkcd.com/" + str(comicNo)).content
			#Creates a 'soup' object from the page
			soup = BeautifulSoup(page)
			#Searches the soup object for a div tag that contains an id with a value of "comic"
			comicImageBlock = soup.find("div",{"id":"comic"})
			#Searches the 'comic' div for the attrivute 'img'
			comicImageTag = comicImageBlock.find("img")
			#Searches the 'img' tag for the attribute 'src' and saves the value as 'comicURL'
			comicURL = comicImageTag['src']
			#Adds "http:" to the start of the ComicURL so that it will  be recognised as a valid URL
			comicURL = "http:" +  str(comicURL)
			fileName = "comics/xkcd_" + str(comicNo) + ".jpg"

			print("DL: " + str(fileName))

			
			# Download the file from `url` and save it locally under `fileName`:
			urllib.request.urlretrieve(comicURL, fileName)
			comicNo += 1
			dlSession += 1

		except:
			errors += 1

			#The number of attemps that will be made to downlaod an image:
			if errors >= 15:

				if dlSession ==0:
					win32api.MessageBox(0, 'No comics were downloaded. \nLibrary is already up-to-date.', 'xKCD Comic Downloader')
				elif dlSession >= 1:
					win32api.MessageBox(0, str(dlSession) + ' comics were downloaded.', 'xKCD Comic Downloader')
				else:
					win32api.MessageBox(0, 'An issue occurred with the xKCD site.', 'xKCD Comic Downloader')
				comicNo = -1
				return comicNo
				break
			else:
				comicNo += 1


def openFolder(path):
	subprocess.check_call(['explorer', path])



def openImage(filename):
	os.system("start "+ filename)




def main():
	#Main:
	mostRecentComicDownloaded = findHighestComic()+1
	downloadComics( mostRecentComicDownloaded )
	#openFolder("C:\py\Python_+_Web\download_all_xkcd")

	toOpen = findHighestComic()

	fileName = "comics/xkcd_" + str(toOpen) + ".jpg"

	try:
		openImage(fileName)
	except:
		os.system("open "+ fileName)

if __name__ == "__main__":
    main() 

