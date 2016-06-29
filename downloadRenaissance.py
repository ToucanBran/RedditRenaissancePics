#! python3

#downloads posts from /r/accidentalrenaissance

import requests, os, bs4, logging, sys, re


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def download_pic(link_array):
	os.makedirs('renaissance', exist_ok=True)
	req = requests.get(link_array[0])
	req.raise_for_status()
	image = open(os.path.join('renaissance',))

	




pic_list = []
#gets webpage
req = requests.get('https://www.reddit.com/r/accidentalrenaissance')
req.raise_for_status()

reddit_soup = bs4.BeautifulSoup(req.text,"html.parser")

linkElements = reddit_soup.find_all(class_="score likes")

logging.info(len(linkElements))
logging.info(linkElements[5].text)
logging.info(linkElements[5].parent.parent.attrs['data-url'])

for link in linkElements:
	if link.text != "\u2022" and int(link.text) > 1000:
		logging.debug(link.text)
		pic_list.append(link.parent.parent.attrs['data-url'])

logging.info(pic_list)
download_pic(pic_list)

