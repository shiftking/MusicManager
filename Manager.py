#Main management Script
#This will scrape that data from a users account, peramiters can be set for downloading certains songs or entire playlists
#metadata is preserved as well as playlist or albumn structure
from gmusicapi import Mobileclient
import urllib

class GoogleMusicManager(object):
    def __init__(self):
        """Default construct"""#Main management Script
#This will scrape that data from a users account, peramiters can be set for downloading certains songs or entire playlists
#metadata is preserved as well as playlist or albumn structure
        self.api = [];
        self.activeSongList = []

    def Login(self, userName, userPassWord):
        """Login method to access you google play account"""
        self.api = Mobileclient()
        if(self.api.login(userName,userPassWord,Mobileclient.FROM_MAC_ADDRESS)):

            print "You have been logged in"
        else:
            print "Seems the login is incorect"


    def getAllSongs(self):
        """Get all songs that the user has listen too that are associated with the account"""
        print "Getting all Songs"
        self.activeSongList = self.api.get_all_songs(False)
            #Check to see if the song has been added before.
            #~~Maybe have it record the songs that have been downloaded already
            #~~if the time to check using the os library is long

            #Getting stream URL

            #Download file using the URL

            #Inject metadata into the now file

            #Check if file destination is created.
            #Structure: /BaseDir/Artist/Album/
            #If the file directory has not been create, call the method to set it up for
            #an new artist

            #Move file to new directory


    def getPlaylist(self,playlistName):
        """Gets a specific playlist by Name"""
        print "Getting " + playListName
