#! python3

#downloads posts from /r/accidentalrenaissance

import requests, os, bs4, logging, sys, re
from enum import IntEnum

#set logging up
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

#create enums for Upvote thresholds
class Upvotes(IntEnum):
	LOW = 0
	MEDIUM = 500
	HIGH = 900

#function: download_pic
#input: an array of links
#outputs: none but it will download pictures from the links to a specified folder
def download_pic(link_array):
	#logging this to make sure there's stuff in the array
	logging.info(link_array)

	#makes a directory called renaissance in the current working directory
	os.makedirs('renaissance', exist_ok=True)

	#loops through the links in the array for download
	for link in link_array:

		#sometimes the downloaded link is different than what I expect. For example,
		#some links were going to i.redd.it which was causing this program to
		#throw MissingSchema errors. I'll need to fix this in the future so I just
		#put in the exception to skip for now
		try:
			#uses requests to download the page from the link
			req = requests.get(link)
			req.raise_for_status()

			#opens a file that the image will be written to in 'write binary' mode
			#path will be ~\renaissance\__basename of url__
			image = open(os.path.join('renaissance',os.path.basename(req.url)),'wb')

			#starts writing chunks of the page to the image file.
			#100000 is a number I got from AutomateTheBoringStuff. Not sure why
			#this number specifically though.
			for chunk in req.iter_content(100000):
				image.write(chunk)

			#closes file	
			image.close()
		except requests.exceptions.MissingSchema:
			continue


#initialize array for holding links to pictures
pic_list = []

#downloads webpage and raises error if there is one
req = requests.get('https://www.reddit.com/r/accidentalrenaissance')
req.raise_for_status()

#set up parsed document 
reddit_soup = bs4.BeautifulSoup(req.text,"html.parser")

#This creates a list of all tags that have the class "score likes".
#Purpose is to loop through this to and find all tags that are above
#the amount of upvotes specified 
linkElements = reddit_soup.find_all(class_="score likes")

#logging these to make sure everything is working right
logging.debug(len(linkElements))
logging.debug(linkElements[5].text)
logging.debug(linkElements[5].parent.parent.attrs['data-url'])

#loops through all the score like elements
for link in linkElements:
	#If statement tests if the element's upvotes are greater than
	#the Upvotes threshold. I have to test for \u2022 because
	#reddit links use a dot symbol when they're brand new and I don't
	#want to pick those up at the moment
	if link.text != "\u2022" and int(link.text) > Upvotes.LOW:

		#logging these to make sure everythig is working right
		logging.debug(link.text)
		logging.debug(link.parent.parent.attrs['data-url'])

		#the actual URL of the picture is stored in the data-url attribute
		#about two elements up. If the element meets the if statement requirements,
		#then it's appended to the pic_list list.
		pic_list.append(link.parent.parent.attrs['data-url'])

#prints out the elements in the pic_list
logging.info(pic_list)

#call function to download pictures to computer
download_pic(pic_list)

