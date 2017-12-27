#Main management Script
#This will scrape that data from a users account, peramiters can be set for downloading certains songs or entire playlists
#metadata is preserved as well as playlist or albumn structure
from gmusicapi import Mobileclient
import urlopen
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
        self.api.logout()
        #reload(MusicLibraryManager)
        if(self.api.login(userName,userPassWord,Mobileclient.FROM_MAC_ADDRESS)):

            print("You have been logged in")
        else:
            print("Seems the login is incorect")

    def getAllRadioStations(self):
        """This will get all of the radiostations that I have saved"""
        print ("Collecting Radio Station Contents")
        #Generate base directory
        #check to see if a playlist directory exists
        baseDir = os.getcwd() + '/RadioStations'
        #if not os.path.exists(baseDir):
        #    raise ValueError(baseDir + " does not exist")


        self.activeRadioStations= self.api.get_all_stations()
        for Station in self.activeRadioStations:
            print ("Found a RadioStation called : " + Station['name'])
            #get radioContent
            RadioStationSongs = self.api.get_station_tracks(Station['id'],1000,{})
            print ("It contains "+str(len(RadioStationSongs)) + " Songs")
            print ("downloading songs")
            stationName = Station['name']
            #create a dir for the radiostation
            activeDir = baseDir + "/"+ stationName +"/"
            #check to see if the radio station folder exists
            if not os.path.exists(activeDir):
                #radiostation doesn't exist so we create it
                os.makedirs(activeDir)

            for Song in RadioStationSongs:
                print (str(Song))

                if not os.path.exists(activeDir + Song['title'] +".mp3"):
                    #it doesn't exists in the playlist yet, so we need to add it
                    songTitle = Song['title']
                    streamUrl = self.api.get_stream_url(Song['storeId'])
                    urllib.urlretrieve(streamUrl,activeDir + songTitle +'.mp3')
                    song = eyed3.load(activeDir + songTitle + '.mp3')
                    song.initTag()
                    song.tag.save()
                    song = eyed3.load(activeDir + songTitle + '.mp3')
                    if "title" in Song:
                        song.tag.title = Song['title']
                    if "artist" in Song:
                        song.tag.artist = Song['artist']
                    if "album" in Song:
                        song.tag.album = Song['album']
                    #song.tag.year = currentSong['year']

                    if "genre" in song.tag:

                        song.tag.genre = Song['genre']
                    if "trackNumber" in Song:
                        song.tag.trackNumber = Song['trackNumber']
                    #song.tag.album = song['album']
                    #print song.tag.version
                    song.tag.save()
                    #print song.tag
                    #for song in self.activeSongList:

    def getAllPlaylists(self):
        """Gets all of the users playlists that they have created"""
        print ("Getting all PLaylist contents")
        self.activePlayList = self.api.get_all_user_playlist_contents()
        baseDir = os.getcwd() + '/Playlists'
        for Playlist in self.activePlayList:
            playlistName = Playlist['name']
            print (playlistName)
            playlistSongs = Playlist['tracks']
            activeDir = baseDir + '/' + playlistName +'/'
            if not os.path.exists(activeDir):
                os.makedirs(activeDir)

            for Song in playlistSongs:
                #print Song
                if 'track' in Song:
                    activeSong = Song['track']
                    print ('getting song : ' + activeSong['title'])
                    if not os.path.exists(activeDir + activeSong['title'] + 'mp3'):
                        #it doesn't exists in the playlist yet, so we need to add it
                        songTitle = activeSong['title']
                        streamUrl = self.api.get_stream_url(activeSong['storeId'])
                        urllib.request.urlretrieve(streamUrl,activeDir + songTitle +'.mp3')
                        song = eyed3.load(activeDir + songTitle + '.mp3')
                        song.initTag()
                        song.tag.save()
                        song = eyed3.load(activeDir + songTitle + '.mp3')
                        if "title" in activeSong:
                            song.tag.title = activeSong['title']
                        if "artist" in activeSong:
                            song.tag.artist = activeSong['artist']
                        if "album" in activeSong:
                            song.tag.album = activeSong['album']
                        #song.tag.year = currentSong['year']
                        if "genre" in activeSong:
                            song.tag.genre = activeSong['genre']
                        if "trackNumber" in activeSong:
                            song.tag.trackNumber = activeSong['trackNumber']
                        #song.tag.album = song['album']
                        #print song.tag.version
                        song.tag.save()

    def getAllSongs(self):


        """Get all songs that the user has listen too that are associated with the account"""
        print ("Getting all Songs")
        self.activeSongList = self.api.get_all_songs(False)
        #print str(self.activeSongList.count)
        baseDir = os.getcwd() + '/Music'
        print ("Grabbed " + str(len(self.activeSongList)) +" Songs")
        #smallList = self.activeSongList[:3]
        for currentSong in self.activeSongList:
            #currentSong = self.activeSongList[0]
            #create a location sting for where the song will be saved.
            #check artist path
            artistPath = currentSong['artist'].strip().replace('/','')
            albumPath = currentSong['album'].strip().replace('/','')
            songTitle = currentSong['title'].replace('/','')
            print (artistPath +" "+ albumPath)
            songPath = '/'+ artistPath + '/'+ albumPath+ "/"
            if os.path.exists(baseDir+songPath):
                print ("Folder Structure exists")

            else:
                print ("Folder Structure does not exist")

                if not os.path.exists(artistPath):
                    os.makedirs(baseDir+songPath)
                    print ("created artitst and alartistPathbumn folder")
                else:
                    os.makedirs(baseDir+songPath)
            print (os.path.isfile(baseDir+songPath+songTitle+'.mp3'))
            print (baseDir+songPath+songTitle+'.mp3')
            if not os.path.isfile(baseDir+songPath+songTitle+'.mp3'):
                #get stream url
                streamUrl = self.api.get_stream_url(currentSong['id'])
                urllib.request.urlretrieve(streamUrl,baseDir + songPath  + songTitle +'.mp3')

                song = eyed3.load(baseDir + songPath + songTitle + '.mp3')
                song.initTag()
                song.tag.save()
                song = eyed3.load(baseDir + songPath + songTitle + '.mp3')
                song.tag.title = currentSong['title']
                song.tag.artist = currentSong['artist']
                song.tag.album = currentSong['album']
                #song.tag.year = currentSong['year']
                if 'genre' in currentSong:
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
                if 'genre' in currentSong:
                    song.tag.genre = currentSong['genre']
                #song.tag.year = currentSong['year']
                song.tag.trackNumber = currentSong['trackNumber']
                #song.tag.album = song['album']
                #print song.tag.version
                song.tag.save()

    def Logout(self):
	    self.api.logout()
    def updateSongs(self):
        """Update locally stored music with any newly listened to or added"""



    def getPlaylist(self,playlistName):
        """Gets a specific playlist by Name"""
        print ("Getting " + playlistName)
