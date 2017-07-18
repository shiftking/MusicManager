#Main management Script
#This will scrape that data from a users account, peramiters can be set for downloading certains songs or entire playlists
#metadata is preserved as well as playlist or albumn structure
from gmusicapi import Mobileclient
from urllib import urlopen
import urllib
import eyed3
from mutagen.id3 import ID3, TIT2
from mutagen.easyid3 import EasyID3
import os
#from MusicLibraryManager import MLM

class GoogleMusicManager(object):
    def __init__(self):
        """Default construct"""#Main management Script
#This will scrape that data from a users account, peramiters can be set for downloading certains songs or entire playlists
#metadata is preserved as well as playlist or albumn structure
        self.api = [];
        self.activeSongList = []
        self.activePlayList = []

    def Login(self, userName, userPassWord):
        """Login method to access you google play account"""
        self.api = Mobileclient()
        #reload(MusicLibraryManager)
        if(self.api.login(userName,userPassWord,Mobileclient.FROM_MAC_ADDRESS)):

            print "You have been logged in"
        else:
            print "Seems the login is incorect"

    def getAllRadioStations(self):
        """This will get all of the radiostations that I have saved"""
    def getAllSongs(self,playLists):

        if playLists == 1:
            """Keep Play list integrity"""
            print "Generating playlist structure"
            self.activePlayList = self.api.get_all_user_playlist_contents()
            for Playlits in self.activePlayList:
                print "Found a Play List called : " + Playlits['name']
                print "It contains "+str(len(Playlits['tracks'])) + " Songs"

        else:
            """Get all songs that the user has listen too that are associated with the account"""
            print "Getting all Songs"
            self.activeSongList = self.api.get_all_songs(False)
            #print str(self.activeSongList.count)
            baseDir = os.getcwd() + '/Music'
            print "Grabbed " + str(len(self.activeSongList)) +" Songs"
            #smallList = self.activeSongList[:3]
            for currentSong in self.activeSongList:
                #currentSong = self.activeSongList[0]
                #create a location sting for where the song will be saved.
                #check artist path
                artistPath = currentSong['artist'].strip().replace('/','')
                albumPath = currentSong['album'].strip().replace('/','')
                songTitle = currentSong['title'].replace('/','')
                print artistPath +" "+ albumPath
                songPath = '/'+ artistPath + '/'+ albumPath+ "/"
                if os.path.exists(baseDir+songPath):
                    print "Folder Structure exists"

                else:
                    print "Folder Structure does not exist"

                    if not os.path.exists(artistPath):
                        os.makedirs(baseDir+songPath)
                        print "created artitst and alartistPathbumn folder"
                    else:
                        os.makedirs(baseDir+songPath)
                print os.path.isfile(baseDir+songPath+songTitle+'.mp3')
                print baseDir+songPath+songTitle+'.mp3'
                if not os.path.isfile(baseDir+songPath+songTitle+'.mp3'):
                    #get stream url
                    streamUrl = self.api.get_stream_url(currentSong['id'])
                    urllib.urlretrieve(streamUrl,baseDir + songPath  + songTitle +'.mp3')

                    song = eyed3.load(baseDir + songPath + songTitle + '.mp3')
                    song.initTag()
                    song.tag.save()
                    song = eyed3.load(baseDir + songPath + songTitle + '.mp3')
                    song.tag.title = currentSong['title']
                    song.tag.artist = currentSong['artist']
                    song.tag.album = currentSong['album']
                    #song.tag.year = currentSong['year']
                    song.tag.genre = currentSong['genre']
                    song.tag.trackNumber = currentSong['trackNumber']
                    #song.tag.album = song['album']
                    #print song.tag.version
                    song.tag.save()
                    #print song.tag
                    #for song in self.activeSongList:
                else:
                    song = eyed3.load(baseDir + songPath + songTitle + '.mp3')
                    song.initTag()
                    song.tag.save()
                    song = eyed3.load(baseDir + songPath + songTitle + '.mp3')
                    song.tag.title = currentSong['title']
                    song.tag.artist = currentSong['artist']
                    song.tag.album = currentSong['album']
                    song.tag.genre = currentSong['genre']
                    #song.tag.year = currentSong['year']
                    song.tag.trackNumber = currentSong['trackNumber']
                    #song.tag.album = song['album']
                    #print song.tag.version
                    song.tag.save()



    def updateSongs(self):
        """Update locally stored music with any newly listened to or added"""



    def getPlaylist(self,playlistName):
        """Gets a specific playlist by Name"""
        print "Getting " + playListName
