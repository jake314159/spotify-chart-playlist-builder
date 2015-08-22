from lxml import html
import time
import requests
import spotify
import sys

class ChartPlaylistBuilder:
	def __init__(self, playlistURI):

		self.RATE_LIMIT_DELAY = 1		

		self.playlist_uri = playlistURI

		username_file = open('spotify_username.txt', 'r')
		username = username_file.read();
		username_file.close()

		password_file = open('spotify_password.txt', 'r')
		password = password_file.read();
		password_file.close()

		self.session = spotify.Session()
		self.session.login(username, password)

		while self.session.connection.state != spotify.ConnectionState.LOGGED_IN:
		    self.session.process_events()

		self.count = 0

	# Scrape the offical charts page and pull out the charts in order
	def getCharts(self):
		page = requests.get("http://www.officialcharts.com/charts/")
		tree = html.fromstring(page.text)

		artists = tree.xpath('//div[@class="artist"]')
		titles = tree.xpath('//div[@class="title"]')

		songs = []

		for i in range(0,min(len(artists), len(titles))):
			a = artists[i].getchildren()[0].text
			t = titles[i].getchildren()[0].text
			songs.append({'artist':a, 'title':t})

		return songs

	def deleteAllTracks(self, playlist):
		playlist.remove_tracks(range(0,len(playlist.tracks)))
		self.session.process_events()
		while playlist.has_pending_changes:
			self.session.process_events()

	# Take a song dict and find it's spotify ID
	def getSpotifyUID(self, song):
		self.count = self.count+1
		query = 'artist:"%s" title:"%s"' % (song.get("artist"), song.get("title"))
		s = self.session.search(query)
		s.load()

		time.sleep(self.RATE_LIMIT_DELAY)

		if len(s.tracks) > 0:
			print "     %d Found '%s'"%(self.count, query)
			return s.tracks[0]
			
		# Attempt with just the title
		query = 'title:"%s"' % (song.get("title"))
		s = self.session.search(query)
		s.load()
		time.sleep(self.RATE_LIMIT_DELAY)

		if len(s.tracks) > 0:
			print "!    %d Found '%s' by title only"%(self.count, query)
			return s.tracks[0]
		else:
			print "!!!! %d Can't find the song '%s'"%(self.count, query)
			return None

	def run(self):

		print "Looking up the current charts..."

		songs = self.getCharts()

		print "I have %d songs from the charts"%len(songs)
		print "Time to get the spotify ids..."

		tracks = map(self.getSpotifyUID, songs)
		tracks = [x for x in tracks if x is not None]

		print "I have %d spotify IDs"%len(tracks)

		if len(tracks) == 0:
			print "Didn't find any tracks, exiting with error"
			sys.exit(1)

		print "\n\n"

		playlist = self.session.get_playlist(self.playlist_uri)
		playlist.load()
		self.deleteAllTracks(playlist)
		playlist.load()
		print "Now i'm going to add %d tracks to the playlist"%len(tracks)
		playlist = self.session.get_playlist(self.playlist_uri)
		playlist.load()
		playlist.add_tracks(tracks)
		count = 0
		self.session.process_events()
		while playlist.has_pending_changes or count < len(tracks)+10:
			count = count+1
			self.session.process_events()
		print "Done after processing %d events"%count

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Please supply a playlist URI as the first argument"
		sys.exit(2)
	playlistBuilder = ChartPlaylistBuilder(sys.argv[1])
	playlistBuilder.run()