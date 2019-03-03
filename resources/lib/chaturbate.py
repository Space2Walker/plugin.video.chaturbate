# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 01.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcplugin
import resources.lib.helper as helper

#################################
#			get_cats			#
#################################
'''
crawls the Catergorys from xvideos.com
and returns them as a list of dicts

[{'category': 'Pornos auf Deutsch', 'link': 'https://xvideos.com/lang/deutsch'}, 
 {'category': '3d', 'link': 'https://xvideos.com/?k=3d&top'}]
'''
def get_cats():
	url = 'https://xvideos.com/'
	cats = []
	soup = helper.get_soup(url)
	divs = soup.find(id="main-cat-sub-list")

	for div in divs.find_all('a', href=True): 
		cats.append(
			dict([
				('category', div.text.lstrip(' ')),
				('link', url[:-1] + div.get('href'))
			]))

	return cats

#################################
#			get_vids			#
#################################
'''
crawls a given url form chaturbate.com for videos
and returns them as a list of dicts
if a catergory is given it will be added to the dict

a returnd dict looks like this
	 KEYS	 VALUE 
[{ 'title': 'BF HAVE 8 INC BUT YOUR ', 
    'link': 'https://chaturbate.com/nasty_girl_masturbate',
'duration': '5 min', 
   'thumb': 'https://img-hw.com/videos/thumbs169/a3/ed/36/a3ed367bcb5a69a9ad.14.jpg', 
     'res': '720p', 
   'views': '13k',
'uploader': 'hans',
'category': 'Grany'}]
'''
def get_vids(url, category='none'):

	hardcoded = 'https://chaturbate.com'
	video_info = []
	videos = [] 

	soup = helper.get_soup(url)

	videos = soup.find_all("li", class_="room_list_room")

	for info in videos:
		res = ''
		title = info.find("a", href=True).get('href')[1:-1]
		uploader = info.find("a", href=True).get('href')
		img = info.find("a", href=True).find('img').get('src')

		# views and time are only seperatot bei "," on the site
		duraview = info.find("li", class_="cams").text.split(",")
		views = duraview[1]

		if duraview[0].find("h") != -1:  #
			h = float(duraview[0][:-4])
			duration = (h * 60) * 60
		
		else: 
			duration = int(duraview[0][:-5]) * 60

		video_info.append(
			dict([
				('title', title),
				('link',  hardcoded + uploader),
				('duration', int(duration)),
				('thumb', img),
				('res', res),
				('views', views),
				('uploader', title),
				('category', category)
				]))
	return video_info


def play_video(_handle, video):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    soup = helper.get_soup(video)
    
    div = soup.find("div", id="video-player-bg")            #find div
    script_tag = div.find_all("script")[4]                  #find script tag in div
    
    tmp = script_tag.string.split("setVideoHLS('")[-1]      #cleanup request
    m3u_link = tmp.split("')", 1)[0]


    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=m3u_link)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

