#! python3

#downloads posts from /r/accidentalrenaissance

import requests, os, bs4, logging, sys, re
from enum import IntEnum


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class Upvotes(IntEnum):
	LOW = 1
	MEDIUM = 500
	HIGH = 900

def download_pic(link_array):
	logging.info(link_array)
	os.makedirs('renaissance', exist_ok=True)

	for link in link_array:
		try:
			req = requests.get(link)
			req.raise_for_status()
			image = open(os.path.join('renaissance',os.path.basename(req.url)),'wb')
			for chunk in req.iter_content(chunk_size=1024):
				image.write(chunk)
			image.close()
		except requests.exceptions.MissingSchema:
			continue



	




pic_list = []

#gets webpage
req = requests.get('https://www.reddit.com/r/accidentalrenaissance')
req.raise_for_status()

reddit_soup = bs4.BeautifulSoup(req.text,"html.parser")

linkElements = reddit_soup.find_all(class_="score likes")

logging.debug(len(linkElements))
logging.debug(linkElements[5].text)
logging.debug(linkElements[5].parent.parent.attrs['data-url'])

for link in linkElements:
	if link.text != "\u2022" and int(link.text) > Upvotes.LOW:
		logging.debug(link.text)
		logging.debug(link.parent.parent.attrs['data-url'])
		pic_list.append(link.parent.parent.attrs['data-url'])

logging.info(pic_list)
download_pic(pic_list)

