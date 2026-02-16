# Add the lib folder to the Python path
import sys
from os.path import join, dirname
import os

# Now import your libraries
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc
import requests

sys.path.insert(0, join(dirname(__file__), 'libs'))
import json
import bs4
import random
from urllib import parse
import urllib



# Get addon info
BeautifulSoup = bs4.BeautifulSoup
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = parse.parse_qs(sys.argv[2][1:])

# Provided variables
Website = "https://www.desitellybox.to/"
TVSearchWebsite = "https://www.themoviedb.org/search/tv?query="
ImageNormalSearchWebsite = \
    "https://www.themoviedb.org/search?query="
HDIMAGEURL = "https://image.tmdb.org/t/p/w1280/"
CACHE_FILE = "image_cache.json"

Channels = [
  {"name": "And TV", "url": f"{Website}and-tv/"},
  {"name": "Colors", "url": f"{Website}colors-tv/"},
  {"name": "MTV", "url": f"{Website}mtv-channel/"},
  {"name": "Sab TV", "url": f"{Website}sab-tv/"},
  {"name": "Sony TV", "url": f"{Website}sony-tv/"},
  {"name": "Star Bharat", "url": f"{Website}star-bharat/"},
  {"name": "Star Plus", "url": f"{Website}star-plus/"},
  {"name": "Zee TV", "url": f"{Website}zee-tv/"},
  {"name": "MORE", "url": "more"}, # MORE channel might need special handling or indicate more categories
]
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

osWin = xbmc.getCondVisibility('system.platform.windows')
osOsx = xbmc.getCondVisibility('system.platform.osx')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osAndroid = xbmc.getCondVisibility('System.Platform.Android')

#Config Variables
browserApp = addon.getSetting("app")

MORES=[
    {
        "channel_name": "Alt Balaji Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/altbalaji.png",
        "shows": [
            {
                "name": "Apharan",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/apharan/"
            },
            {
                "name": "Average Dating Time Before Second Marriage",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/average-dating-time-before-second-marriage/"
            },
            {
                "name": "Baarish",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/baarish-alt-balaji-web-series/"
            },
            {
                "name": "Baarish Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/baarish-season-2/"
            },
            {
                "name": "Baby Come Naa",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/baby-come-naa/"
            },
            {
                "name": "Bang Baang: The Sound Of Crimes",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bang-baang-the-sound-of-crimes/"
            },
            {
                "name": "Bebaakee",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bebaakee/"
            },
            {
                "name": "Bekaaboo",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bekaaboo/"
            },
            {
                "name": "Bekaaboo Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bekaaboo-season-2/"
            },
            {
                "name": "Bewafaa Sii Wafaa",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bewafaa-sii-wafaa/"
            },
            {
                "name": "Bicchoo Ka Khel",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bicchoo-ka-khel/"
            },
            {
                "name": "Booo Sabki Phategi",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/booo-sabki-phategi/"
            },
            {
                "name": "Bose \u2013 Dead or Alive",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/bose-dead-or-alive/"
            },
            {
                "name": "Boss Baap of Special Services",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/boss-baap-of-special-services/"
            },
            {
                "name": "Boygiri",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/boygiri/"
            },
            {
                "name": "Broken But Beautiful Season 1",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/broken-but-beautiful-season-1/"
            },
            {
                "name": "Broken But Beautiful Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/broken-but-beautiful-season-2/"
            },
            {
                "name": "Broken But Beautiful Season 3",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/broken-but-beautiful-season-3/"
            },
            {
                "name": "Cartel",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/cartel/"
            },
            {
                "name": "Class Of 2017",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/class-of-2017/"
            },
            {
                "name": "Class of 2020",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/class-of-2020/"
            },
            {
                "name": "Code M",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/code-m/"
            },
            {
                "name": "Coldd Lassi Aur Chicken Masala",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/coldd-lassi-aur-chicken-masala/"
            },
            {
                "name": "Crashh",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/crashh/"
            },
            {
                "name": "Crimes And Confessions",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/crimes-and-confessions/"
            },
            {
                "name": "Cyber Squad",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/cyber-squad/"
            },
            {
                "name": "Dark 7 White",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/dark-7-white/"
            },
            {
                "name": "Dev DD",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/dev-dd/"
            },
            {
                "name": "Dev DD Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/dev-dd-season-2/"
            },
            {
                "name": "Dil Hi Toh Hai 3",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/dil-hi-toh-hai-3/"
            },
            {
                "name": "Dil Hi Toh Hai Season 1",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/dil-hi-toh-hai-season-1/"
            },
            {
                "name": "Dil Hi Toh Hai Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/dil-hi-toh-hai-season-2/"
            },
            {
                "name": "Fittrat",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/fittrat/"
            },
            {
                "name": "Fixerr",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/fixerr/"
            },
            {
                "name": "Fourplay",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/fourplay/"
            },
            {
                "name": "Gandii Baat Season 01",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/gandii-baat-season-01/"
            },
            {
                "name": "Gandii Baat Season 02",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/gandii-baat-season-02/"
            },
            {
                "name": "Gandii Baat Season 03",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/gandii-baat-season-03/"
            },
            {
                "name": "Gandii Baat Season 04",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/gandii-baat-season-04/"
            },
            {
                "name": "Gandii Baat Season 5",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/gandii-baat-season-5/"
            },
            {
                "name": "Gandii Baat Season 6",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/gandii-baat-season-6/"
            },
            {
                "name": "Girgit",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/girgit/"
            },
            {
                "name": "Hai Taubba",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/hai-taubba/"
            },
            {
                "name": "Hai Taubba Chapter 3",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/hai-taubba-chapter-3/"
            },
            {
                "name": "Hai Taubba: Chapter 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/hai-taubba-chapter-2/"
            },
            {
                "name": "Haq Se",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/haq-se/"
            },
            {
                "name": "Helllo Jee",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/helllo-jee/"
            },
            {
                "name": "His Storyy",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/his-storyy/"
            },
            {
                "name": "Home",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/home/"
            },
            {
                "name": "Hum",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/hum/"
            },
            {
                "name": "Hum Tum and Them",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/hum-tum-and-them/"
            },
            {
                "name": "It Happened In Calcutta",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/it-happened-in-calcutta/"
            },
            {
                "name": "Karrle Tu Bhi Mohabbat Season 1",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/karrle-tu-bhi-mohabbat-season-1/"
            },
            {
                "name": "Karrle Tu Bhi Mohabbat Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/karrle-tu-bhi-mohabbat-season-2/"
            },
            {
                "name": "Karrle Tu Bhi Mohabbat Season 3",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/karrle-tu-bhi-mohabbat-season-3/"
            },
            {
                "name": "Kehne Ko Humsafar Hain",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/kehne-ko-humsafar-hain-alt-balaji-web-series/"
            },
            {
                "name": "Kehne Ko HumSafar Hain Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/kehne-ko-humsafar-hain-season-2/"
            },
            {
                "name": "Kehne Ko Humsafar Hain Season 3",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/kehne-ko-humsafar-hain-season-3/"
            },
            {
                "name": "Lock Upp",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/lock-upp/"
            },
            {
                "name": "LSD: Love, Scandal & Doctors",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/lsd-love-scandal-doctors/"
            },
            {
                "name": "Mai Hero Boll Raha Hu",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/mai-hero-boll-raha-hu/"
            },
            {
                "name": "Medically Yourrs",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/medically-yourrs/"
            },
            {
                "name": "Mentalhood",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/mentalhood/"
            },
            {
                "name": "Mission Over Mars",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/mission-over-mars/"
            },
            {
                "name": "Mum Bhai",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/mum-bhai/"
            },
            {
                "name": "Paurashpur",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/paurashpur/"
            },
            {
                "name": "PM Selfiewallie",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/pm-selfiewallie/"
            },
            {
                "name": "Puncch Beat",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/puncch-beat/"
            },
            {
                "name": "Punch Beat Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/punch-beat-season-2/"
            },
            {
                "name": "Ragini MMS Returns",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/ragini-mms-returns/"
            },
            {
                "name": "Ragini MMS Returns Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/ragini-mms-returns-season-2/"
            },
            {
                "name": "Romil and Jugal",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/romil-and-jugal/"
            },
            {
                "name": "The Great Indian Dysfunctional Family",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/the-great-indian-dysfunctional-family/"
            },
            {
                "name": "The Married Woman",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/the-married-woman/"
            },
            {
                "name": "The Test Case",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/the-test-case/"
            },
            {
                "name": "The Verdict \u2013 State Vs Nanavat",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/the-verdict-state-vs-nanavat/"
            },
            {
                "name": "Virgin Bhasskar",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/virgin-bhasskar/"
            },
            {
                "name": "Virgin Bhasskar Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/virgin-bhasskar-season-2/"
            },
            {
                "name": "Whos Your Daddy",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/whos-your-daddy/"
            },
            {
                "name": "Whos Your Daddy Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/whos-your-daddy-season-2/"
            },
            {
                "name": "XXX Uncensored Season 1",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/xxx-uncensored-season-1/"
            },
            {
                "name": "XXX Uncensored Season 2",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/xxx-uncensored-season-2/"
            },
            {
                "name": "Zaban Sambhal Ke",
                "link": "https://www.desitellybox.to/category/alt-balaji-web-series/zaban-sambhal-ke/"
            }
        ]
    },
    {
        "channel_name": "Hotstar Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/hotstar.png",
        "shows": [
            {
                "name": "1962 The War In The Hills",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/1962-the-war-in-the-hills/"
            },
            {
                "name": "9 Hours",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/9-hours/"
            },
            {
                "name": "Aarya",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/aarya/"
            },
            {
                "name": "Aarya Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/aarya-season-2/"
            },
            {
                "name": "Aashiqana",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/aashiqana/"
            },
            {
                "name": "Ankahi Ansuni",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/ankahi-ansuni/"
            },
            {
                "name": "Bamini and Boys",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/bamini-and-boys/"
            },
            {
                "name": "Bamini and Boys Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/bamini-and-boys-season-2/"
            },
            {
                "name": "Bhopal to Vegas",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/bhopal-to-vegas/"
            },
            {
                "name": "Chattis Aur Maina",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/chattis-aur-maina/"
            },
            {
                "name": "City of Dreams",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/city-of-dreams/"
            },
            {
                "name": "City of Dreams Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/city-of-dreams-season-2/"
            },
            {
                "name": "Crime Next Door",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/crime-next-door/"
            },
            {
                "name": "Criminal Justice",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/criminal-justice/"
            },
            {
                "name": "Criminal Justice Season 3",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/criminal-justice-season-3/"
            },
            {
                "name": "Criminal Justice: Behind Closed Doors",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/criminal-justice-behind-closed-doors/"
            },
            {
                "name": "Daav",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/daav/"
            },
            {
                "name": "Emotional Atyachaar",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/emotional-atyachaar-hotstar-web-series/"
            },
            {
                "name": "Escaype Live",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/escaype-live/"
            },
            {
                "name": "Ghar Waapsi",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/ghar-waapsi/"
            },
            {
                "name": "Grahan",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/grahan/"
            },
            {
                "name": "Gumrah (Quix)",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/gumrah-quix/"
            },
            {
                "name": "Hamara Bar Happy Hour",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/hamara-bar-happy-hour/"
            },
            {
                "name": "Home Shanti",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/home-shanti/"
            },
            {
                "name": "Hostages",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/hostages/"
            },
            {
                "name": "Hostages Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/hostages-season-2/"
            },
            {
                "name": "Human",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/human/"
            },
            {
                "name": "Hundred",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/hundred/"
            },
            {
                "name": "Kamathipura",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/kamathipura/"
            },
            {
                "name": "Kota Toppers",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/kota-toppers-hotstar-web-series/"
            },
            {
                "name": "Life Love Siyaapa",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/life-love-siyaapa/"
            },
            {
                "name": "Live Telecast",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/live-telecast/"
            },
            {
                "name": "Loki (Hindi)",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/loki-hindi/"
            },
            {
                "name": "Masoom",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/masoom/"
            },
            {
                "name": "Mukesh Jasoos",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/mukesh-jasoos/"
            },
            {
                "name": "Murder Meri Jaan",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/murder-meri-jaan/"
            },
            {
                "name": "November Story",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/november-story/"
            },
            {
                "name": "OK Computer",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/ok-computer/"
            },
            {
                "name": "Out of Love",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/out-of-love/"
            },
            {
                "name": "Out Of Love Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/out-of-love-season-2/"
            },
            {
                "name": "Pariwar",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/pariwar/"
            },
            {
                "name": "Risky Ishq",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/risky-ishq/"
            },
            {
                "name": "Rudra \u2013 The Edge Of Darkness",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/rudra-the-edge-of-darkness/"
            },
            {
                "name": "Sarabhai Vs Sarabhai Season 2 (Hotstar)",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/sarabhai-vs-sarabhai-season-2-hotstar/"
            },
            {
                "name": "Shit Yaar",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/shit-yaar/"
            },
            {
                "name": "Six",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/six/"
            },
            {
                "name": "Special Ops 1.5",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/special-ops-1-5/"
            },
            {
                "name": "Special Ops 2020",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/special-ops-2020/"
            },
            {
                "name": "Target",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/target/"
            },
            {
                "name": "Teen Do Paanch",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/teen-do-paanch/"
            },
            {
                "name": "The Empire",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-empire/"
            },
            {
                "name": "The Great Indian Murder",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-great-indian-murder/"
            },
            {
                "name": "The Hunt",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-hunt/"
            },
            {
                "name": "The Legend of Hanuman",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-legend-of-hanuman/"
            },
            {
                "name": "The Legend Of Hanuman Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-legend-of-hanuman-season-2/"
            },
            {
                "name": "The Office",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-office/"
            },
            {
                "name": "The Office Season 2",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-office-season-2/"
            },
            {
                "name": "The Return",
                "link": "https://www.desitellybox.to/category/hotstar-web-series/the-return/"
            },
            {
                "name": "7 Kadam",
                "link": "https://www.desitellybox.to/category/eros-now/7-kadam/"
            },
            {
                "name": "Date Gone Wrong 2",
                "link": "https://www.desitellybox.to/category/eros-now/date-gone-wrong-2/"
            },
            {
                "name": "Enaaya",
                "link": "https://www.desitellybox.to/category/eros-now/enaaya/"
            },
            {
                "name": "Eros Orignals",
                "link": "https://www.desitellybox.to/category/eros-now/eros-orignals/"
            },
            {
                "name": "Flesh",
                "link": "https://www.desitellybox.to/category/eros-now/flesh/"
            },
            {
                "name": "Flip",
                "link": "https://www.desitellybox.to/category/eros-now/flip/"
            },
            {
                "name": "Hindmata",
                "link": "https://www.desitellybox.to/category/eros-now/hindmata/"
            },
            {
                "name": "Metro Park",
                "link": "https://www.desitellybox.to/category/eros-now/metro-park/"
            },
            {
                "name": "Metro Park \u2013 Quarantine Edition",
                "link": "https://www.desitellybox.to/category/eros-now/metro-park-quarantine-edition/"
            },
            {
                "name": "Metro Park Season 2",
                "link": "https://www.desitellybox.to/category/eros-now/metro-park-season-2/"
            },
            {
                "name": "Modi CM to PM Season 2",
                "link": "https://www.desitellybox.to/category/eros-now/modi-cm-to-pm-season-2/"
            },
            {
                "name": "Modi: Journey of a common man",
                "link": "https://www.desitellybox.to/category/eros-now/modi-journey-of-a-common-man/"
            },
            {
                "name": "My Name Is Sheela",
                "link": "https://www.desitellybox.to/category/eros-now/my-name-is-sheela/"
            },
            {
                "name": "Operation Cobra",
                "link": "https://www.desitellybox.to/category/eros-now/operation-cobra/"
            },
            {
                "name": "Paisa Fek Tamasha Dekh",
                "link": "https://www.desitellybox.to/category/eros-now/paisa-fek-tamasha-dekh/"
            },
            {
                "name": "Side Hero",
                "link": "https://www.desitellybox.to/category/eros-now/side-hero/"
            },
            {
                "name": "Smoke",
                "link": "https://www.desitellybox.to/category/eros-now/smoke/"
            },
            {
                "name": "The Investigation",
                "link": "https://www.desitellybox.to/category/eros-now/the-investigation/"
            }
        ]
    },
    {
        "channel_name": "Zee5 Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/zee5.jpg",
        "shows": [
            {
                "name": "Abhay",
                "link": "https://www.desitellybox.to/category/zee5-web-series/abhay/"
            },
            {
                "name": "Abhay Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/abhay-season-2/"
            },
            {
                "name": "Abhay Season 3",
                "link": "https://www.desitellybox.to/category/zee5-web-series/abhay-season-3/"
            },
            {
                "name": "Akoori",
                "link": "https://www.desitellybox.to/category/zee5-web-series/akoori/"
            },
            {
                "name": "Anaganaga Once Upon A Time",
                "link": "https://www.desitellybox.to/category/zee5-web-series/anaganaga-once-upon-a-time/"
            },
            {
                "name": "Auto Shankar",
                "link": "https://www.desitellybox.to/category/zee5-web-series/auto-shankar/"
            },
            {
                "name": "Bhalla Calling Bhalla",
                "link": "https://www.desitellybox.to/category/zee5-web-series/bhalla-calling-bhalla/"
            },
            {
                "name": "Bhanwar",
                "link": "https://www.desitellybox.to/category/zee5-web-series/bhanwar-zee5-web-series/"
            },
            {
                "name": "Bhoot Purva",
                "link": "https://www.desitellybox.to/category/zee5-web-series/bhoot-purva/"
            },
            {
                "name": "Bhram",
                "link": "https://www.desitellybox.to/category/zee5-web-series/bhram/"
            },
            {
                "name": "Black Widows",
                "link": "https://www.desitellybox.to/category/zee5-web-series/black-widows/"
            },
            {
                "name": "Bombers",
                "link": "https://www.desitellybox.to/category/zee5-web-series/bombers/"
            },
            {
                "name": "Break Point Web Series",
                "link": "https://www.desitellybox.to/category/zee5-web-series/break-point-web-series/"
            },
            {
                "name": "Chadarangam",
                "link": "https://www.desitellybox.to/category/zee5-web-series/chadarangam/"
            },
            {
                "name": "Churails",
                "link": "https://www.desitellybox.to/category/zee5-web-series/churails/"
            },
            {
                "name": "Codename Gondya",
                "link": "https://www.desitellybox.to/category/zee5-web-series/codename-gondya/"
            },
            {
                "name": "D7",
                "link": "https://www.desitellybox.to/category/zee5-web-series/d7/"
            },
            {
                "name": "Dhoop Ki Deewar",
                "link": "https://www.desitellybox.to/category/zee5-web-series/dhoop-ki-deewar/"
            },
            {
                "name": "Duranga",
                "link": "https://www.desitellybox.to/category/zee5-web-series/duranga/"
            },
            {
                "name": "Ek Jhoothi Love Story",
                "link": "https://www.desitellybox.to/category/zee5-web-series/ek-jhoothi-love-story/"
            },
            {
                "name": "Engineering Girls Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/engineering-girls-season-2/"
            },
            {
                "name": "Expiry Date",
                "link": "https://www.desitellybox.to/category/zee5-web-series/expiry-date/"
            },
            {
                "name": "Fingertip",
                "link": "https://www.desitellybox.to/category/zee5-web-series/fingertip/"
            },
            {
                "name": "Forbidden Love",
                "link": "https://www.desitellybox.to/category/zee5-web-series/forbidden-love/"
            },
            {
                "name": "Gods Of Dharmapuri",
                "link": "https://www.desitellybox.to/category/zee5-web-series/gods-of-dharmapuri/"
            },
            {
                "name": "Hawala",
                "link": "https://www.desitellybox.to/category/zee5-web-series/hawala/"
            },
            {
                "name": "High Priestess",
                "link": "https://www.desitellybox.to/category/zee5-web-series/high-priestess/"
            },
            {
                "name": "Hutatma",
                "link": "https://www.desitellybox.to/category/zee5-web-series/hutatma/"
            },
            {
                "name": "Hutatma Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/hutatma-season-2/"
            },
            {
                "name": "Ishq Aaj Kal Season 01",
                "link": "https://www.desitellybox.to/category/zee5-web-series/ishq-aaj-kal-season-01/"
            },
            {
                "name": "Ishq Aaj Kal Season 02",
                "link": "https://www.desitellybox.to/category/zee5-web-series/ishq-aaj-kal-season-02/"
            },
            {
                "name": "Ishq Aaj Kal Season 3",
                "link": "https://www.desitellybox.to/category/zee5-web-series/ishq-aaj-kal-season-3/"
            },
            {
                "name": "Ishq Aaj Kal Season 4",
                "link": "https://www.desitellybox.to/category/zee5-web-series/ishq-aaj-kal-season-4/"
            },
            {
                "name": "Jamai 2.0",
                "link": "https://www.desitellybox.to/category/zee5-web-series/jamai-2-0/"
            },
            {
                "name": "Jamai 2.0 Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/jamai-2-0-season-2/"
            },
            {
                "name": "Jeet Ki Zidd",
                "link": "https://www.desitellybox.to/category/zee5-web-series/jeet-ki-zidd/"
            },
            {
                "name": "Judgement Day",
                "link": "https://www.desitellybox.to/category/zee5-web-series/judgement-day/"
            },
            {
                "name": "Kaafir",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kaafir/"
            },
            {
                "name": "Kaale Dhande",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kaale-dhande/"
            },
            {
                "name": "Kaali",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kaali-zee5-web-series/"
            },
            {
                "name": "Kaali Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kaali-season-2/"
            },
            {
                "name": "Kailasapuram",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kailasapuram/"
            },
            {
                "name": "Kannamoochi",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kannamoochi/"
            },
            {
                "name": "Karenjit Kaur \u2013 The Untold Story of Sunny Leone",
                "link": "https://www.desitellybox.to/category/zee5-web-series/karenjit-kaur-the-untold-story-of-sunny-leone/"
            },
            {
                "name": "Karenjit Kaur \u2013 The Untold Story of Sunny Leone 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/karenjit-kaur-the-untold-story-of-sunny-leone-2/"
            },
            {
                "name": "Karenjit Kaur \u2013 The Untold Story of Sunny Leone 3",
                "link": "https://www.desitellybox.to/category/zee5-web-series/karenjit-kaur-the-untold-story-of-sunny-leone-3/"
            },
            {
                "name": "Kark Rogue",
                "link": "https://www.desitellybox.to/category/zee5-web-series/kark-rogue/"
            },
            {
                "name": "Krishanu Krishanu",
                "link": "https://www.desitellybox.to/category/zee5-web-series/krishanu-krishanu/"
            },
            {
                "name": "Lalbazaar",
                "link": "https://www.desitellybox.to/category/zee5-web-series/lalbazaar/"
            },
            {
                "name": "Life Sahi Hai Season 1",
                "link": "https://www.desitellybox.to/category/zee5-web-series/life-sahi-hai-season-1/"
            },
            {
                "name": "Life Sahi Hai Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/life-sahi-hai-season-2/"
            },
            {
                "name": "Love Bites",
                "link": "https://www.desitellybox.to/category/zee5-web-series/love-bites/"
            },
            {
                "name": "Love Sleep Repeat",
                "link": "https://www.desitellybox.to/category/zee5-web-series/love-sleep-repeat/"
            },
            {
                "name": "Mafia",
                "link": "https://www.desitellybox.to/category/zee5-web-series/mafia/"
            },
            {
                "name": "Mrs & Mr Shameem",
                "link": "https://www.desitellybox.to/category/zee5-web-series/mrs-mr-shameem/"
            },
            {
                "name": "Naxalbari",
                "link": "https://www.desitellybox.to/category/zee5-web-series/naxalbari/"
            },
            {
                "name": "NERD \u2013 Neither Either Really Dead",
                "link": "https://www.desitellybox.to/category/zee5-web-series/nerd-neither-either-really-dead/"
            },
            {
                "name": "Never Kiss Your Best Friend",
                "link": "https://www.desitellybox.to/category/zee5-web-series/never-kiss-your-best-friend/"
            },
            {
                "name": "Never Kiss Your Best Friend \u2013 Lockdown Special",
                "link": "https://www.desitellybox.to/category/zee5-web-series/never-kiss-your-best-friend-lockdown-special/"
            },
            {
                "name": "Never Kiss Your Best Friend Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/never-kiss-your-best-friend-season-2/"
            },
            {
                "name": "Nisha",
                "link": "https://www.desitellybox.to/category/zee5-web-series/nisha/"
            },
            {
                "name": "Parchhayee",
                "link": "https://www.desitellybox.to/category/zee5-web-series/parchhayee/"
            },
            {
                "name": "Pavitra Rishta 2.0 \u2013 It's Never Too Late",
                "link": "https://www.desitellybox.to/category/zee5-web-series/pavitra-rishta-2-0-its-never-too-late/"
            },
            {
                "name": "Phone A Friend",
                "link": "https://www.desitellybox.to/category/zee5-web-series/phone-a-friend/"
            },
            {
                "name": "Poison",
                "link": "https://www.desitellybox.to/category/zee5-web-series/poison/"
            },
            {
                "name": "Poison Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/poison-season-2/"
            },
            {
                "name": "Police Diary 2.0",
                "link": "https://www.desitellybox.to/category/zee5-web-series/police-diary-2-0/"
            },
            {
                "name": "Postman",
                "link": "https://www.desitellybox.to/category/zee5-web-series/postman/"
            },
            {
                "name": "Qatil Haseenaon Ke Naam",
                "link": "https://www.desitellybox.to/category/zee5-web-series/qatil-haseenaon-ke-naam/"
            },
            {
                "name": "Qubool Hai 2.0",
                "link": "https://www.desitellybox.to/category/zee5-web-series/qubool-hai-2-0/"
            },
            {
                "name": "Rangbaaz",
                "link": "https://www.desitellybox.to/category/zee5-web-series/rangbaaz/"
            },
            {
                "name": "Rangbaaz Phirse",
                "link": "https://www.desitellybox.to/category/zee5-web-series/rangbaaz-phirse/"
            },
            {
                "name": "RejctX",
                "link": "https://www.desitellybox.to/category/zee5-web-series/rejctx/"
            },
            {
                "name": "RejctX Season 2",
                "link": "https://www.desitellybox.to/category/zee5-web-series/rejctx-season-2/"
            },
            {
                "name": "Sex Drugs & Theatre",
                "link": "https://www.desitellybox.to/category/zee5-web-series/sex-drugs-theatre/"
            },
            {
                "name": "Sharate Aaj",
                "link": "https://www.desitellybox.to/category/zee5-web-series/sharate-aaj/"
            },
            {
                "name": "Skyfire",
                "link": "https://www.desitellybox.to/category/zee5-web-series/skyfire/"
            },
            {
                "name": "State of Siege 2611",
                "link": "https://www.desitellybox.to/category/zee5-web-series/state-of-siege-2611/"
            },
            {
                "name": "Sunflower",
                "link": "https://www.desitellybox.to/category/zee5-web-series/sunflower/"
            },
            {
                "name": "Sutliyan",
                "link": "https://www.desitellybox.to/category/zee5-web-series/sutliyan/"
            },
            {
                "name": "Table No. 5",
                "link": "https://www.desitellybox.to/category/zee5-web-series/table-no-5/"
            },
            {
                "name": "Taish",
                "link": "https://www.desitellybox.to/category/zee5-web-series/taish/"
            },
            {
                "name": "The Broken News",
                "link": "https://www.desitellybox.to/category/zee5-web-series/the-broken-news/"
            },
            {
                "name": "The Casino",
                "link": "https://www.desitellybox.to/category/zee5-web-series/the-casino/"
            },
            {
                "name": "The Chargesheet",
                "link": "https://www.desitellybox.to/category/zee5-web-series/the-chargesheet/"
            },
            {
                "name": "The Final Call",
                "link": "https://www.desitellybox.to/category/zee5-web-series/the-final-call/"
            },
            {
                "name": "Three Half Bottles",
                "link": "https://www.desitellybox.to/category/zee5-web-series/three-half-bottles/"
            },
            {
                "name": "Water Bottle",
                "link": "https://www.desitellybox.to/category/zee5-web-series/water-bottle/"
            },
            {
                "name": "Zee 5 Shortfilm Festival (2020)",
                "link": "https://www.desitellybox.to/category/zee5-web-series/zee-5-shortfilm-festival-2020/"
            },
            {
                "name": "Zee5 Originals",
                "link": "https://www.desitellybox.to/category/zee5-web-series/zee5-originals/"
            },
            {
                "name": "Zero KMS",
                "link": "https://www.desitellybox.to/category/zee5-web-series/zero-kms/"
            }
        ]
    },
    {
        "channel_name": "Amazon Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/amazon.png",
        "shows": [
            {
                "name": "Afsos",
                "link": "https://www.desitellybox.to/category/amazon-web-series/afsos/"
            },
            {
                "name": "Akkad Bakkad Rafu Chakkar",
                "link": "https://www.desitellybox.to/category/amazon-web-series/akkad-bakkad-rafu-chakkar/"
            },
            {
                "name": "Amazon Originals",
                "link": "https://www.desitellybox.to/category/amazon-web-series/amazon-originals/"
            },
            {
                "name": "Bestseller",
                "link": "https://www.desitellybox.to/category/amazon-web-series/bestseller/"
            },
            {
                "name": "Breathe",
                "link": "https://www.desitellybox.to/category/amazon-web-series/breathe/"
            },
            {
                "name": "Breathe \u2013 Into the Shadows",
                "link": "https://www.desitellybox.to/category/amazon-web-series/breathe-into-the-shadows/"
            },
            {
                "name": "Chacha Vidhayak Hain Humare Season 1",
                "link": "https://www.desitellybox.to/category/amazon-web-series/chacha-vidhayak-hain-humare-season-1/"
            },
            {
                "name": "Chacha Vidhayak Hain Humare Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/chacha-vidhayak-hain-humare-season-2/"
            },
            {
                "name": "Comicstaan Season 1",
                "link": "https://www.desitellybox.to/category/amazon-web-series/comicstaan-season-1/"
            },
            {
                "name": "Comicstaan Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/comicstaan-season-2/"
            },
            {
                "name": "Drishtibhram",
                "link": "https://www.desitellybox.to/category/amazon-web-series/drishtibhram/"
            },
            {
                "name": "Four More Shots Please!",
                "link": "https://www.desitellybox.to/category/amazon-web-series/four-more-shots-please/"
            },
            {
                "name": "Four More Shots Please! Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/four-more-shots-please-season-2/"
            },
            {
                "name": "Guilty Minds",
                "link": "https://www.desitellybox.to/category/amazon-web-series/guilty-minds/"
            },
            {
                "name": "Hostel Daze",
                "link": "https://www.desitellybox.to/category/amazon-web-series/hostel-daze/"
            },
            {
                "name": "Hostel Daze Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/hostel-daze-season-2/"
            },
            {
                "name": "Inside Edge Season 1",
                "link": "https://www.desitellybox.to/category/amazon-web-series/inside-edge-season-1/"
            },
            {
                "name": "Inside Edge Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/inside-edge/"
            },
            {
                "name": "Jestination Unknown",
                "link": "https://www.desitellybox.to/category/amazon-web-series/jestination-unknown/"
            },
            {
                "name": "Kaali Peeli Tales",
                "link": "https://www.desitellybox.to/category/amazon-web-series/kaali-peeli-tales/"
            },
            {
                "name": "Laakhon Mein Ek Season 1",
                "link": "https://www.desitellybox.to/category/amazon-web-series/laakhon-mein-ek-season-1/"
            },
            {
                "name": "Laakhon Mein Ek Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/laakhon-mein-ek-season-2/"
            },
            {
                "name": "LOL \u2013 Hasee Toh Phasee",
                "link": "https://www.desitellybox.to/category/amazon-web-series/lol-hasee-toh-phasee/"
            },
            {
                "name": "Made in Heaven",
                "link": "https://www.desitellybox.to/category/amazon-web-series/made-in-heaven/"
            },
            {
                "name": "McMafia",
                "link": "https://www.desitellybox.to/category/amazon-web-series/mcmafia/"
            },
            {
                "name": "Mind The Malhotras",
                "link": "https://www.desitellybox.to/category/amazon-web-series/mind-the-malhotras/"
            },
            {
                "name": "Mind The Malhotras Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/mind-the-malhotras-season-2/"
            },
            {
                "name": "Mirzapur",
                "link": "https://www.desitellybox.to/category/amazon-web-series/mirzapur/"
            },
            {
                "name": "Mirzapur Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/mirzapur-season-2/"
            },
            {
                "name": "Mumbai Diaries 26/11",
                "link": "https://www.desitellybox.to/category/amazon-web-series/mumbai-diaries-26-11/"
            },
            {
                "name": "Paatal Lok",
                "link": "https://www.desitellybox.to/category/amazon-web-series/paatal-lok/"
            },
            {
                "name": "Panchayat",
                "link": "https://www.desitellybox.to/category/amazon-web-series/panchayat/"
            },
            {
                "name": "Panchayat Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/panchayat-season-2/"
            },
            {
                "name": "Pushpavalli Season 1",
                "link": "https://www.desitellybox.to/category/amazon-web-series/pushpavalli-season-1/"
            },
            {
                "name": "Pushpavalli Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/pushpavalli-season-2/"
            },
            {
                "name": "Rasbhari",
                "link": "https://www.desitellybox.to/category/amazon-web-series/rasbhari/"
            },
            {
                "name": "Say Yes to the Dress India",
                "link": "https://www.desitellybox.to/category/amazon-web-series/say-yes-to-the-dress-india/"
            },
            {
                "name": "Sons Of The Soil",
                "link": "https://www.desitellybox.to/category/amazon-web-series/sons-of-the-soil/"
            },
            {
                "name": "Tandav",
                "link": "https://www.desitellybox.to/category/amazon-web-series/tandav/"
            },
            {
                "name": "The Family Man",
                "link": "https://www.desitellybox.to/category/amazon-web-series/the-family-man/"
            },
            {
                "name": "The Family Man Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/the-family-man-season-2/"
            },
            {
                "name": "The Forgotten Army \u2013 Azaadi Ke Liye",
                "link": "https://www.desitellybox.to/category/amazon-web-series/the-forgotten-army-azaadi-ke-liye/"
            },
            {
                "name": "The Last Hour",
                "link": "https://www.desitellybox.to/category/amazon-web-series/the-last-hour/"
            },
            {
                "name": "Transparency Pardarshita",
                "link": "https://www.desitellybox.to/category/amazon-web-series/transparency-pardarshita/"
            },
            {
                "name": "Udan Patolas",
                "link": "https://www.desitellybox.to/category/amazon-web-series/udan-patolas/"
            },
            {
                "name": "Udan Patolas Season 2",
                "link": "https://www.desitellybox.to/category/amazon-web-series/udan-patolas-season-2/"
            },
            {
                "name": "Wakaalat from Home",
                "link": "https://www.desitellybox.to/category/amazon-web-series/wakaalat-from-home/"
            }
        ]
    },
    {
        "channel_name": "Voot Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/voot.jpg",
        "shows": [
            {
                "name": "24 Season 2",
                "link": "https://www.desitellybox.to/category/voot-web-series/24-season-2/"
            },
            {
                "name": "Apharan Season 2",
                "link": "https://www.desitellybox.to/category/voot-web-series/apharan-season-2/"
            },
            {
                "name": "Asur",
                "link": "https://www.desitellybox.to/category/voot-web-series/asur/"
            },
            {
                "name": "Badman",
                "link": "https://www.desitellybox.to/category/voot-web-series/badman/"
            },
            {
                "name": "Baked Season 1",
                "link": "https://www.desitellybox.to/category/voot-web-series/baked-season-1/"
            },
            {
                "name": "Baked Season 2",
                "link": "https://www.desitellybox.to/category/voot-web-series/baked-season-2/"
            },
            {
                "name": "Baked Season 3",
                "link": "https://www.desitellybox.to/category/voot-web-series/baked-season-3/"
            },
            {
                "name": "Bandon Mein Tha Dum",
                "link": "https://www.desitellybox.to/category/voot-web-series/bandon-mein-tha-dum/"
            },
            {
                "name": "Banned",
                "link": "https://www.desitellybox.to/category/voot-web-series/banned/"
            },
            {
                "name": "Candy",
                "link": "https://www.desitellybox.to/category/voot-web-series/candy/"
            },
            {
                "name": "Chinese Bhasad",
                "link": "https://www.desitellybox.to/category/voot-web-series/chinese-bhasad/"
            },
            {
                "name": "Code M Season 2",
                "link": "https://www.desitellybox.to/category/voot-web-series/code-m-season-2/"
            },
            {
                "name": "Crackdown",
                "link": "https://www.desitellybox.to/category/voot-web-series/crackdown/"
            },
            {
                "name": "Doon Kaand",
                "link": "https://www.desitellybox.to/category/voot-web-series/doon-kaand/"
            },
            {
                "name": "Fuh Se Fantasy",
                "link": "https://www.desitellybox.to/category/voot-web-series/fuh-se-fantasy/"
            },
            {
                "name": "Illegal",
                "link": "https://www.desitellybox.to/category/voot-web-series/illegal/"
            },
            {
                "name": "Illegal season 2",
                "link": "https://www.desitellybox.to/category/voot-web-series/illegal-season-2/"
            },
            {
                "name": "It's Not That Simple",
                "link": "https://www.desitellybox.to/category/voot-web-series/its-not-that-simple/"
            },
            {
                "name": "Its Not That Simple Season 2",
                "link": "https://www.desitellybox.to/category/voot-web-series/its-not-that-simple-season-2/"
            },
            {
                "name": "Khwabon Ke Parindey",
                "link": "https://www.desitellybox.to/category/voot-web-series/khwabon-ke-parindey/"
            },
            {
                "name": "London Files",
                "link": "https://www.desitellybox.to/category/voot-web-series/london-files/"
            },
            {
                "name": "Marzi",
                "link": "https://www.desitellybox.to/category/voot-web-series/marzi/"
            },
            {
                "name": "Memories",
                "link": "https://www.desitellybox.to/category/voot-web-series/memories/"
            },
            {
                "name": "NRI Haadsa",
                "link": "https://www.desitellybox.to/category/voot-web-series/nri-haadsa/"
            },
            {
                "name": "Ranjish Hi Sahi",
                "link": "https://www.desitellybox.to/category/voot-web-series/ranjish-hi-sahi/"
            },
            {
                "name": "Shaadi Boys",
                "link": "https://www.desitellybox.to/category/voot-web-series/shaadi-boys/"
            },
            {
                "name": "Shortcuts",
                "link": "https://www.desitellybox.to/category/voot-web-series/shortcuts/"
            },
            {
                "name": "Soadies",
                "link": "https://www.desitellybox.to/category/voot-web-series/soadies/"
            },
            {
                "name": "Sumer Singh Case Files: Girlfriends",
                "link": "https://www.desitellybox.to/category/voot-web-series/sumer-singh-case-files-girlfriends/"
            },
            {
                "name": "The Gone Game",
                "link": "https://www.desitellybox.to/category/voot-web-series/the-gone-game/"
            },
            {
                "name": "The Raikar Case",
                "link": "https://www.desitellybox.to/category/voot-web-series/the-raikar-case/"
            },
            {
                "name": "Time Out",
                "link": "https://www.desitellybox.to/category/voot-web-series/time-out/"
            },
            {
                "name": "Untag",
                "link": "https://www.desitellybox.to/category/voot-web-series/untag/"
            },
            {
                "name": "Voot Originals",
                "link": "https://www.desitellybox.to/category/voot-web-series/voot-originals/"
            },
            {
                "name": "Yo Ke Hua Bro",
                "link": "https://www.desitellybox.to/category/voot-web-series/yo-ke-hua-bro/"
            }
        ]
    },
    {
        "channel_name": "Netflix Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/netflix.png",
        "shows": [
            {
                "name": "A Suitable Boy",
                "link": "https://www.desitellybox.to/category/netflix/a-suitable-boy/"
            },
            {
                "name": "Alma Matters",
                "link": "https://www.desitellybox.to/category/netflix/alma-matters/"
            },
            {
                "name": "Aranyak",
                "link": "https://www.desitellybox.to/category/netflix/aranyak/"
            },
            {
                "name": "Bad Boy Billionaires: India",
                "link": "https://www.desitellybox.to/category/netflix/bad-boy-billionaires-india/"
            },
            {
                "name": "Bard of Blood",
                "link": "https://www.desitellybox.to/category/netflix/bard-of-blood/"
            },
            {
                "name": "Betaal",
                "link": "https://www.desitellybox.to/category/netflix/betaal/"
            },
            {
                "name": "Bhaag Beanie Bhaag",
                "link": "https://www.desitellybox.to/category/netflix/bhaag-beanie-bhaag/"
            },
            {
                "name": "Bombay Begums",
                "link": "https://www.desitellybox.to/category/netflix/bombay-begums/"
            },
            {
                "name": "Call My Agent Bollywood",
                "link": "https://www.desitellybox.to/category/netflix/call-my-agent-bollywood/"
            },
            {
                "name": "Comedy Premium League",
                "link": "https://www.desitellybox.to/category/netflix/comedy-premium-league/"
            },
            {
                "name": "Crime Stories: India Detectives",
                "link": "https://www.desitellybox.to/category/netflix/crime-stories-india-detectives/"
            },
            {
                "name": "Delhi Crime",
                "link": "https://www.desitellybox.to/category/netflix/delhi-crime/"
            },
            {
                "name": "Delhi Crime Season 2",
                "link": "https://www.desitellybox.to/category/netflix/delhi-crime-season-2/"
            },
            {
                "name": "Engineering Girls",
                "link": "https://www.desitellybox.to/category/netflix/engineering-girls/"
            },
            {
                "name": "Fabulous Lives of Bollywood Wives",
                "link": "https://www.desitellybox.to/category/netflix/fabulous-lives-of-bollywood-wives/"
            },
            {
                "name": "Feels Like Ishq",
                "link": "https://www.desitellybox.to/category/netflix/feels-like-ishq/"
            },
            {
                "name": "Ghoul",
                "link": "https://www.desitellybox.to/category/netflix/ghoul/"
            },
            {
                "name": "Hasmukh",
                "link": "https://www.desitellybox.to/category/netflix/hasmukh/"
            },
            {
                "name": "House of Secrets: The Burari Deaths",
                "link": "https://www.desitellybox.to/category/netflix/house-of-secrets-the-burari-deaths/"
            },
            {
                "name": "Indian Matchmaking",
                "link": "https://www.desitellybox.to/category/netflix/indian-matchmaking/"
            },
            {
                "name": "Jamtara Sabka Number Ayega",
                "link": "https://www.desitellybox.to/category/netflix/jamtara-sabka-number-ayega/"
            },
            {
                "name": "Kota Factory Season 2",
                "link": "https://www.desitellybox.to/category/netflix/kota-factory-season-2/"
            },
            {
                "name": "Lava Ka Dhaava",
                "link": "https://www.desitellybox.to/category/netflix/lava-ka-dhaava/"
            },
            {
                "name": "Leila",
                "link": "https://www.desitellybox.to/category/netflix/leila/"
            },
            {
                "name": "Little Things S01",
                "link": "https://www.desitellybox.to/category/netflix/little-things-s01/"
            },
            {
                "name": "Little Things S02",
                "link": "https://www.desitellybox.to/category/netflix/little-things-s02/"
            },
            {
                "name": "Little Things S03",
                "link": "https://www.desitellybox.to/category/netflix/little-things-s03/"
            },
            {
                "name": "Little Things Season 4",
                "link": "https://www.desitellybox.to/category/netflix/little-things-season-4/"
            },
            {
                "name": "Masaba Masaba",
                "link": "https://www.desitellybox.to/category/netflix/masaba-masaba/"
            },
            {
                "name": "Mismatched",
                "link": "https://www.desitellybox.to/category/netflix/mismatched/"
            },
            {
                "name": "mixed bag",
                "link": "https://www.desitellybox.to/category/netflix/mixed-bag/"
            },
            {
                "name": "Netflix Originals",
                "link": "https://www.desitellybox.to/category/netflix/netflix-originals/"
            },
            {
                "name": "Never Have I Ever",
                "link": "https://www.desitellybox.to/category/netflix/never-have-i-ever/"
            },
            {
                "name": "Ray",
                "link": "https://www.desitellybox.to/category/netflix/ray/"
            },
            {
                "name": "Sacred Games S01",
                "link": "https://www.desitellybox.to/category/netflix/sacred-games-s01/"
            },
            {
                "name": "Sacred Games S02",
                "link": "https://www.desitellybox.to/category/netflix/sacred-games-s02/"
            },
            {
                "name": "Selection Day",
                "link": "https://www.desitellybox.to/category/netflix/selection-day/"
            },
            {
                "name": "SHE",
                "link": "https://www.desitellybox.to/category/netflix/she/"
            },
            {
                "name": "She Season 2",
                "link": "https://www.desitellybox.to/category/netflix/she-season-2/"
            },
            {
                "name": "Stories by Rabindranath Tagore",
                "link": "https://www.desitellybox.to/category/netflix/stories-by-rabindranath-tagore/"
            },
            {
                "name": "Taj Mahal 1989",
                "link": "https://www.desitellybox.to/category/netflix/taj-mahal-1989/"
            },
            {
                "name": "Typewriter",
                "link": "https://www.desitellybox.to/category/netflix/typewriter/"
            },
            {
                "name": "What The Love With Karan Johar",
                "link": "https://www.desitellybox.to/category/netflix/what-the-love-with-karan-johar/"
            },
            {
                "name": "Yeh Kaali Kaali Ankhein",
                "link": "https://www.desitellybox.to/category/netflix/yeh-kaali-kaali-ankhein/"
            },
            {
                "name": "Yeh Meri Family",
                "link": "https://www.desitellybox.to/category/netflix/yeh-meri-family/"
            }
        ]
    },
    {
        "channel_name": "VB Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/vb.jpg",
        "shows": [
            {
                "name": "Faceless",
                "link": "https://www.desitellybox.to/category/vb-web-series/faceless/"
            },
            {
                "name": "Gehraiyaan",
                "link": "https://www.desitellybox.to/category/vb-web-series/gehraiyaan/"
            },
            {
                "name": "Hadh",
                "link": "https://www.desitellybox.to/category/vb-web-series/hadh/"
            },
            {
                "name": "Maaya 1",
                "link": "https://www.desitellybox.to/category/vb-web-series/maaya-1/"
            },
            {
                "name": "Maaya 2",
                "link": "https://www.desitellybox.to/category/vb-web-series/maaya-2/"
            },
            {
                "name": "Maaya 3",
                "link": "https://www.desitellybox.to/category/vb-web-series/maaya-3/"
            },
            {
                "name": "Rain",
                "link": "https://www.desitellybox.to/category/vb-web-series/rain/"
            },
            {
                "name": "Spotlight Season 1",
                "link": "https://www.desitellybox.to/category/vb-web-series/spotlight-season-1/"
            },
            {
                "name": "Spotlight Season 2",
                "link": "https://www.desitellybox.to/category/vb-web-series/spotlight-season-2/"
            },
            {
                "name": "Twisted Season 1",
                "link": "https://www.desitellybox.to/category/vb-web-series/twisted-season-1/"
            },
            {
                "name": "Twisted Season 2",
                "link": "https://www.desitellybox.to/category/vb-web-series/twisted-season-2/"
            },
            {
                "name": "Twisted Season 3",
                "link": "https://www.desitellybox.to/category/vb-web-series/twisted-season-3/"
            },
            {
                "name": "Untouchables",
                "link": "https://www.desitellybox.to/category/vb-web-series/untouchables/"
            },
            {
                "name": "Zakhmi",
                "link": "https://www.desitellybox.to/category/vb-web-series/zakhmi/"
            },
            {
                "name": "Zindabaad",
                "link": "https://www.desitellybox.to/category/vb-web-series/zindabaad/"
            }
        ]
    },
    {
        "channel_name": "MX Player Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/mxplayer.png",
        "shows": [
            {
                "name": "Aafat",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/aafat/"
            },
            {
                "name": "Aani Kay Hava",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/aani-kay-hava/"
            },
            {
                "name": "Aapkey Kamrey Mein Koi Rehta Hai",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/aapkey-kamrey-mein-koi-rehta-hai/"
            },
            {
                "name": "Aashram",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/aashram/"
            },
            {
                "name": "Aashram Chapter 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/aashram-chapter-2/"
            },
            {
                "name": "Aashram Chapter 3",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/aashram-chapter-3/"
            },
            {
                "name": "Anamika",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/anamika-mx-player-web-series/"
            },
            {
                "name": "Beehad Ka Baghi",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/beehad-ka-baghi/"
            },
            {
                "name": "Bhaukaal",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/bhaukaal/"
            },
            {
                "name": "Bhootiyagiri",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/bhootiyagiri/"
            },
            {
                "name": "Bisaat",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/bisaat/"
            },
            {
                "name": "Bullets",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/bullets/"
            },
            {
                "name": "Chakravyuh",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/chakravyuh/"
            },
            {
                "name": "Cheesecake",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/cheesecake/"
            },
            {
                "name": "Chhatrasal",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/chhatrasal/"
            },
            {
                "name": "Dangerous",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/dangerous/"
            },
            {
                "name": "Delhi Khabbar",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/delhi-khabbar/"
            },
            {
                "name": "Ek Thi Begum",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/ek-thi-begum/"
            },
            {
                "name": "Ek Thi Begum 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/ek-thi-begum-2/"
            },
            {
                "name": "Ek Thi Begum2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/ek-thi-begum2/"
            },
            {
                "name": "Girlfriend Chor",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/girlfriend-chor/"
            },
            {
                "name": "Hello Mini",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/hello-mini/"
            },
            {
                "name": "Hello Mini 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/hello-mini-2/"
            },
            {
                "name": "Hello Mini 3",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/hello-mini-3/"
            },
            {
                "name": "Hey Prabhu Season 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/hey-prabhu-season-2/"
            },
            {
                "name": "Hey Prabhu!",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/hey-prabhu/"
            },
            {
                "name": "High (Mx)",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/high-mx/"
            },
            {
                "name": "I'm Mature",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/im-mature/"
            },
            {
                "name": "Indori Ishq",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/indori-ishq/"
            },
            {
                "name": "Koi Hai",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/koi-hai/"
            },
            {
                "name": "Lockdown Rishtey",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/lockdown-rishtey/"
            },
            {
                "name": "Locked in Love",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/locked-in-love/"
            },
            {
                "name": "Love Ok Please",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/love-ok-please/"
            },
            {
                "name": "Mastram",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/mastram/"
            },
            {
                "name": "Mrs And Mr Kohli",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/mrs-and-mr-kohli/"
            },
            {
                "name": "Nakaab",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/nakaab/"
            },
            {
                "name": "Naked",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/naked/"
            },
            {
                "name": "Only For Singles",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/only-for-singles/"
            },
            {
                "name": "Pati Patni Aur Panga",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/pati-patni-aur-panga/"
            },
            {
                "name": "Pati Patni Aur Woh",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/pati-patni-aur-woh/"
            },
            {
                "name": "Pawan and Pooja",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/pawan-and-pooja/"
            },
            {
                "name": "Queen",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/queen/"
            },
            {
                "name": "Raktanchal",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/raktanchal/"
            },
            {
                "name": "Raktanchal Season 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/raktanchal-season-2/"
            },
            {
                "name": "Ramyug",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/ramyug/"
            },
            {
                "name": "Ratri Ke Yatri",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/ratri-ke-yatri/"
            },
            {
                "name": "Roohaniyat",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/roohaniyat/"
            },
            {
                "name": "Roohaniyat Season 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/roohaniyat-season-2/"
            },
            {
                "name": "Runaway Lugaai",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/runaway-lugaai/"
            },
            {
                "name": "Samantar",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/samantar/"
            },
            {
                "name": "Samantar Season 2",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/samantar-season-2/"
            },
            {
                "name": "Sanak \u2013 Ek Junoon",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/sanak-ek-junoon/"
            },
            {
                "name": "Split Ends",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/split-ends/"
            },
            {
                "name": "Spotlight",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/spotlight/"
            },
            {
                "name": "The Cobweb",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/the-cobweb/"
            },
            {
                "name": "The Holiday",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/the-holiday/"
            },
            {
                "name": "The Missing Stone",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/the-missing-stone/"
            },
            {
                "name": "Thinkistan",
                "link": "https://www.desitellybox.to/category/mx-player-web-series/thinkistan/"
            }
        ]
    },
    {
        "channel_name": "Hoichoi Web Series",
        "channel_image": "https://www.desitellybox.to//images/channels/hoichoi.png",
        "shows": [
            {
                "name": "Astey Ladies",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/astey-ladies/"
            },
            {
                "name": "Black Diamond (Nokol Heere)",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/black-diamond-nokol-heere/"
            },
            {
                "name": "Byomkesh",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/byomkesh/"
            },
            {
                "name": "Calm Sutra",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/calm-sutra/"
            },
            {
                "name": "Calm Sutra Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/calm-sutra-season-2/"
            },
            {
                "name": "Charitraheen",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/charitraheen/"
            },
            {
                "name": "Charitraheen Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/charitraheen-season-2/"
            },
            {
                "name": "Charitraheen Season 3",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/charitraheen-season-3/"
            },
            {
                "name": "Crime of Desire (Bonyo Premer Golpo 2)",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/crime-of-desire-bonyo-premer-golpo-2/"
            },
            {
                "name": "Daastan-E-Love",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/daastan-e-love/"
            },
            {
                "name": "Daastan-E-Love (Paanch Phoron) Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/daastan-e-love-paanch-phoron-season-2/"
            },
            {
                "name": "Damayanti",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/damayanti/"
            },
            {
                "name": "Hello",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/hello/"
            },
            {
                "name": "Hello Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/hello-season-2/"
            },
            {
                "name": "Hello Season 3",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/hello-season-3/"
            },
            {
                "name": "Holy Crap Season 1",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/holy-crap-season-1/"
            },
            {
                "name": "Holy Crap Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/holy-crap-season-2/"
            },
            {
                "name": "Hushhh 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/hushhh-2/"
            },
            {
                "name": "Kamini",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/kamini/"
            },
            {
                "name": "Love and Affairs",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/love-and-affairs/"
            },
            {
                "name": "Madhushala",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/madhushala/"
            },
            {
                "name": "Mahanagar",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/mahanagar/"
            },
            {
                "name": "Mismatch Season 3",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/mismatch-season-3/"
            },
            {
                "name": "Mrs. Jasoos",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/mrs-jasoos/"
            },
            {
                "name": "Once Upon a Crime",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/once-upon-a-crime/"
            },
            {
                "name": "Once Upon a Crime (Shobdo Jobdo)",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/once-upon-a-crime-shobdo-jobdo/"
            },
            {
                "name": "Paap",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/paap/"
            },
            {
                "name": "Paap Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/paap-season-2/"
            },
            {
                "name": "Tales of Mystery And Thrill Season 1",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/tales-of-mystery-and-thrill-season-1/"
            },
            {
                "name": "Tales of Mystery And Thrill Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/tales-of-mystery-and-thrill-season-2/"
            },
            {
                "name": "Tales of Mystery and Thrill Season 3",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/tales-of-mystery-and-thrill-season-3/"
            },
            {
                "name": "Tansen ka Tanpura",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/tansen-ka-tanpura/"
            },
            {
                "name": "Taqdeer",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/taqdeer/"
            },
            {
                "name": "Taranath Tantrik",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/taranath-tantrik/"
            },
            {
                "name": "The Stoneman Murder",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/the-stoneman-murder/"
            },
            {
                "name": "Vaidehi (Shei Je Holud Pakhi) Season 1",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/vaidehi-shei-je-holud-pakhi-season-1/"
            },
            {
                "name": "Vaidehi (Shei Je Holud Pakhi) Season 2",
                "link": "https://www.desitellybox.to/category/hoichoi-web-series/vaidehi-shei-je-holud-pakhi-season-2/"
            }
        ]
    }
]



def openbrowser(url):
    if osOsx:
        # ___ Open the url with the default web browser
        xbmc.executebuiltin("System.Exec(open "+url+")")
    elif osWin:
        # ___ Open the url with the default web browser
        xbmc.executebuiltin("System.Exec(cmd.exe /c start "+url+")")
    elif osLinux and not osAndroid:
        # ___ Need the xdk-utils package
        xbmc.executebuiltin("System.Exec(xdg-open "+url+")")
    elif osAndroid:
        # ___ Open media with configured web browser in addon settings
        xbmc.executebuiltin("StartAndroidActivity("+browserApp+",android.intent.action.VIEW,,"+url+")")
    


def get_a_header():
    """
    Returns a dictionary containing a randomly selected User-Agent header.

    Returns:
        dict: A dictionary with the "User-Agent" key and a random user agent as the value.
    """
    user_agents = [
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x86) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 Edge/16.16299",
      "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 12; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 13; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 14; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 15; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 16; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
      "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
      "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
      "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPad; CPU OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1",
    ]

    # Shuffle and select a random user agent
    user_agent = random.choice(user_agents)
    return {"User-Agent": user_agent}


def log(message, level=xbmc.LOGDEBUG):
    """Log a message to Kodi's log file."""
    xbmc.log(f"{addon_name}: {message}", level)

def build_url(query):
    """Build a plugin URL for Kodi."""
    return base_url + '?' + urllib.parse.urlencode(query)

def get_html(url,head=None):
    """Fetch HTML content from a URL with a basic User-Agent."""
    try:
        headers = head or get_a_header()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        log(f"Error fetching URL {url}: {e}", xbmc.LOGERROR)
        return None

def list_channels():
    log("Listing channels")
    for channel in Channels:
        # Skip the 'MORE' channel for now if it doesn't have a direct URL
        if channel['url']:
            list_item = xbmcgui.ListItem(label=channel['name'])
            thumbnail = google_search_image(channel['name']+" hd logo")
            list_item.setArt({'thumb': thumbnail})
            url = build_url({'mode': 'list_shows', 'channel_url': channel['url']})
            xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)
        else:
            log(f"Skipping channel without URL: {channel['name']}")
    clearcachelist_item = xbmcgui.ListItem(label="Clear Cache")
    url = build_url({'mode': 'list_shows', 'channel_url': "clearcache"})
    xbmcplugin.addDirectoryItem(addon_handle, url, clearcachelist_item, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)
    
    log("Finished listing channels")

def fetch_more_data():
    try:
        with open("./MoreContent.json", 'r') as cache_file:
            return json.load(cache_file)
    except FileNotFoundError:
        xbmcgui.Dialog().notification('Error', 'Failed to fetch data', xbmcgui.NOTIFICATION_ERROR, 5000)
        
    
    # if ("more" in cache_data.keys()):
    #     if (len(cache_data["more"])>0):
    #         return cache_data["more"]
    
    channels = []
    try:
        html = get_html(Website)
        if (not html):
            xbmcgui.Dialog().notification('Error', 'Failed to fetch data', xbmcgui.NOTIFICATION_ERROR, 5000)
            return
        
        soup = BeautifulSoup(html, 'html.parser')

        # Find all sections with class 'colm'
        sections = soup.select('div.colm')

        for section in sections:
            # Extract channel name
            channel_name_element = section.select_one('strong')
            channel_name = channel_name_element.text.strip() if channel_name_element else ''

            # Extract channel image
            img_tag = section.select_one('img')
            channel_image = img_tag.get('src', '').strip() if img_tag else ''

            # Extract shows and links
            shows = []
            show_list = section.select('li.cat-item')
            for item in show_list:
                show_name_element = item.select_one('a')
                show_name = show_name_element.text.strip() if show_name_element else ''
                show_link = show_name_element.get('href', '').strip() if show_name_element else ''

                if show_name and show_link:
                    shows.append({'name': show_name, 'url': show_link})

            channels.append({
                'channel_name': channel_name,
                'channel_image': google_search_image(channel_name+" hd logo"),  # Assuming channel image is relative
                'shows': shows,
            })
        # cache_data["more"] = channels
        # with open(CACHE_FILE, 'w') as cache_file:
        #     json.dump(cache_data, cache_file)

    except requests.exceptions.RequestException as e:
        xbmcgui.Dialog().notification('Error', 'Broke! Failed to fetch data', xbmcgui.NOTIFICATION_ERROR, 5000)

    except Exception as e:
        xbmcgui.Dialog().notification('Error', 'Failed to prasing data', xbmcgui.NOTIFICATION_ERROR, 5000)

    return channels

def more_shows(channel_name):
    Shows = [i["shows"] for i in MORES if i["channel_name"]==channel_name]
    for show in Shows[0]:
        list_item = xbmcgui.ListItem(label=show['name'])
        thumbnail = scrape_hd_image(show["name"],channel_name) 
        list_item.setArt({'thumb': thumbnail})          
        url = build_url({'mode': 'list_episodes', 'show_url': show['link'],'image_url':thumbnail})
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)





def list_shows(channel_url):
    if channel_url == "clearcache":
        os.remove(CACHE_FILE)
        xbmcgui.Dialog().notification('Done', 'Cache is clear.', xbmcgui.NOTIFICATION_INFO, 5000)
        return
    if (channel_url == "more"):
        for ott in MORES:
            list_item = xbmcgui.ListItem(label=ott['channel_name'])
            # TODO: Add artwork scraping later if needed
            list_item.setArt({'thumb': ott['channel_image']})          
            url = build_url({'mode': 'more_shows', 'channel_name': ott['channel_name'],'image_url': ott['channel_image']})
            xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)
        return
        
    
    log(f"Listing shows for channel: {channel_url}")
    html_content = get_html(channel_url)
    shows = []
    Channel_name=channel_url.split("/")[-2]
    log(f"Channel name is:{Channel_name}")
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Based on your Dart code, shows might be in div.entry_content a
        entry_content = soup.select_one("div.entry_content")
        if entry_content:
            links = entry_content.select("a")
            # Assuming the first link might be different, like in your Dart code
            if links:
                 
                for link in links[1:]:
                    title = link.text.strip()
                    href = link.get('href')
                    if ("completed" in href):
                        continue
                    if title and href:
                        thumbnail = scrape_hd_image(title,Channel_name)
                        shows.append({'name': title, 'url': href,'thumbnail': thumbnail})
    if (len(shows)==0):
        xbmcgui.Dialog().notification('Content not found', 'This is usual sometime. Try Again.', xbmcgui.NOTIFICATION_INFO, 5000)
        return

    for show in shows:
        list_item = xbmcgui.ListItem(label=show['name'])
        # TODO: Add artwork scraping later if needed
        list_item.setArt({'thumb': show['thumbnail']})
        list_item.setInfo("folder", {"description": show['name'],"title":show["name"]})
        
        url = build_url({'mode': 'list_episodes', 'show_url': show['url'],'image_url':show["thumbnail"]})
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
    log(f"Finished listing shows for channel: {channel_url}. Found {len(shows)} shows.")


# Function to fetch HTML data
def fetch_html_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Function to extract image using custom logic
def pro_image_extractor(query):
    try:
        search_url = f"{TVSearchWebsite}{query}"
        html = fetch_html_data(search_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the first card
        first_card = soup.select_one('div.card.v4.tight')
        if first_card:
            img_tag = first_card.select_one('img.poster.w-full')
            if img_tag:
                img_url = img_tag.get('src')
                if img_url:
                    image_file = img_url.split('/')[-1]
                    return HDIMAGEURL + image_file
    except Exception as e:
        print(f"Error in ProImageExtractor: {e}")
    return None

# Function to fetch Google image thumbnail
def google_search_image(query):
    try:
        search_query = f"{query} FULL HD image"
        search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}&tbm=isch"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = soup.select('img')
        for img in images[1:]:  # Skip the first image (logo)
            src = img.get('src')
            if src and src.startswith('http') and not ("social" in src or "icon" in src):
                return src
    except Exception as e:
        print(f"Error fetching Google image: {e}")
    return "https://parinamlaw.com/wp-content/themes/lawcounsel/images/no-image/No-Image-Found-400x264.png"

# Function to scrape HD image
def scrape_hd_image(show, channel):
    try:
        

        # Try custom scraper
        img1 = pro_image_extractor(show)
        if img1:
            image_url = img1
        else:
            # Fallback to Google search
            img2 = google_search_image(f"{show} show in {channel}")
            image_url = img2

        return image_url
    except Exception as e:
        print(f"Error scraping HD image: {e}")
        return "https://parinamlaw.com/wp-content/themes/lawcounsel/images/no-image/No-Image-Found-400x264.png"

def fetch_pagination_pages(show_url, response=None):
    pages = []
    
    try:
        if response is None or not response.text:
            response = requests.get(show_url,headers=get_a_header())
            
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all li elements inside ul with class page-numbers
            list_items = soup.select('ul.page-numbers li')
            
            for li in list_items:
                # Skip if contains dots class
                if li.select_one('.dots'):
                    continue
                    
                # Check if it's the current page
                current = li.select_one('span.current')
                if current:
                    pages.append({
                        "text": current.text.strip(),
                        "url": None,
                        "current": True
                    })
                else:
                    # Get the link if it exists
                    a_tag = li.select_one('a')
                    if a_tag:
                        text = a_tag.text.strip() if a_tag.text.strip() else a_tag.get('class', [''])[0]
                        pages.append({
                            "text": text,
                            "url": a_tag.get('href'),
                            "current": False
                        })
                        
    except Exception as e:
        print(f"Error fetching pagination pages: {e}")
        
    return pages


def list_episodes(show_url,image_url):  
    log(f"Listing episodes for show: {show_url}")
    episodes = []
    pages = fetch_pagination_pages(show_url)
    log(f"Pages: {pages}")
    nextpage = [i for i in pages if i["text"]=="next"]
    prepage = [i for i in pages if i["text"]=="prev"]
    
    # TODO: Implement scraping based on div.item_content h4 a and handle pagination (ul.page-numbers li)
    html_content = get_html(show_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        episode_links = soup.select('div.item_content h4 a')
        
            
        for ep in episode_links:
            title = ep.text.strip()
            href = ep.get('href')
            # Filter out 'preview' links if necessary, based on your Dart code
            if title and href and 'preview' not in title.lower():
                episodes.append({'name': title, 'url': href})

        # TODO: Implement pagination handling here
        # Look for ul.page-numbers li and extract links
        
    if (len(prepage)>0):
        prepage = prepage[0]
        list_item = xbmcgui.ListItem(label="Previous")
        url = build_url({'mode': 'list_episodes', 'show_url': prepage['url'],'image_url':image_url})
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)
    
    if (len(episodes)==0):
        xbmcgui.Dialog().notification('Content not found', 'This is usual sometime. Try Again.', xbmcgui.NOTIFICATION_INFO, 5000)
        return
        
    for episode in episodes:
        list_item = xbmcgui.ListItem(label=episode['name'])
        # Set video info if available (plot, duration, etc.)
        if (image_url !="none"):
            list_item.setArt({'thumb': image_url})
        list_item.setInfo('video', {'title': episode['name']}) # Need to scrape plot if available
        url = build_url({'mode': 'play_video', 'episode_url': episode['url']})
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)
        
    if (len(nextpage)>0):
        nextpage = nextpage[0]
        list_item = xbmcgui.ListItem(label="Next")
        url = build_url({'mode': 'list_episodes', 'show_url': nextpage['url'],'image_url':image_url})
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
    log(f"Finished listing episodes for show: {show_url}. Found {len(episodes)} episodes.")


def extract_entry_content_urls(watch_page_url, headers):
    """
    Extracts URLs from a specific div with class 'entry_content' on the given page.

    Args:
        watch_page_url (str): The URL of the page to scrape.
        headers (dict): The headers to include in the HTTP request.

    Returns:
        list: A list of URLs extracted from the page.
    """
    try:
        # Fetch HTML data
        response = requests.get(watch_page_url, headers=headers)
        if response.status_code != 200:
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the 'entry_content' div
        entry_content_div = soup.find('div', class_='entry_content')
        if entry_content_div:
            # Extract all anchor tags with href attributes
            urls = [
                a['href']
                for a in entry_content_div.find_all('a', href=True)
                if a['href']
            ]

            # Remove the last URL if the list has more than 5 URLs
            if len(urls) > 5:
                urls.pop()

            return urls

    except Exception as e:
        print(f"Error extracting entry content URLs: {e}")

    return []

def open_browser_link_with_prompt(url):
    """
    Prompt the user with a dialog and open the browser link if confirmed.

    Args:
        url (str): The URL to open in the browser.
    """
    dialog = xbmcgui.Dialog()
    user_choice = dialog.yesno("Open Link", f"Do you want to open this link?\n{url}")
    
    if user_choice:
        try:
            # For Android
            if xbmcgui.getCondVisibility("System.Platform.Android"):
                xbmcgui.executebuiltin(f'StartAndroidActivity("android.intent.action.VIEW", "{url}")')
            else:
                # For other platforms, log or use alternative methods
                log("Opening link: " + url, xbmc.LOGINFO)
        except Exception as e:
            log(f"Error opening browser: {e}", xbmc.LOGERROR)
    else:
        log("User declined to open the link.", xbmc.LOGINFO)



def play_video(episode_url):
    log(f"Attempting to play video from: {episode_url}")
    video_url = None
    Videoheader = get_a_header()

    VideosUrl = extract_entry_content_urls(episode_url,Videoheader)
    vkprime_video_url = [url for url in VideosUrl if "vkprime" in url]
    log (f"Vkprimeurl: {vkprime_video_url}")
    if (len(vkprime_video_url)!=0):
        html_content = get_html(vkprime_video_url[0],Videoheader)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            entry_content = soup.select_one("div.entry_content")
            if entry_content:
                iframe = entry_content.select_one('iframe')
                if iframe and 'src' in iframe.attrs:
                    iframe_url = iframe['src']
                    log(f"Found iframe with src: {iframe_url}")
                    # Now fetch and parse the iframe_url to find the video source
                    # This often requires more advanced parsing or handling redirects/javascript
                    # For many sites, the iframe src might be the direct video URL or a page containing it
                    # You might need to investigate the structure of the iframe source page
                    # As a simple example, let's assume the iframe src IS the video URL (unlikely for complex sites)
                    video_url = iframe_url # This is a placeholder, replace with actual extraction logic

                    # If the iframe src is not the direct video, you would need to call get_html(iframe_url) and parse that content.
                    # This can get complicated if the video URL is generated by JavaScript within the iframe.


    if video_url:
        log(f"Found video URL: {video_url}")
        xbmcgui.Player().play(video_url)
        log("Resolved video URL for playback")
    else:
        if (len(VideosUrl)!=0):
            for idx,videourl in enumerate(VideosUrl):
                list_item = xbmcgui.ListItem(label=f"Server {idx+1}")
                # TODO: Add artwork scraping later if needed                
                url = build_url({'mode': 'serverplay', 'videourl': videourl})
                xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)
        else:
            xbmcgui.Dialog().notification('Content not found', 'This is usual sometime. Try Again.', xbmcgui.NOTIFICATION_INFO, 5000)
            log(f"Could not extract playable video URL from {episode_url}", xbmc.LOGERROR)
            xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem()) # Indicate failure
            return
            # xbmcgui.Dialog().ok(addon_name, "Could not find a playable video link for this episode.Try Again.")

if __name__ == '__main__':
    log(f"Addon started with args: {sys.argv}")
    mode = args.get('mode', None)

    if mode is None:
        list_channels()
    elif mode[0] == 'list_shows':
        channel_url = args['channel_url'][0]
        list_shows(channel_url)
    elif mode[0]=="more_shows":
        cname = args["channel_name"][0]
        imgurl=args['image_url'][0]
        more_shows(cname)
        
    elif mode[0] == 'list_episodes':
        show_url = args['show_url'][0]
        image_url = args['image_url'][0]
        list_episodes(show_url,image_url)
    elif mode[0] == 'play_video':
        episode_url = args['episode_url'][0]
        play_video(episode_url)
    elif mode[0] == "serverplay":
        url = args["videourl"][0]
        openbrowser(url)

    log("Addon finished")
