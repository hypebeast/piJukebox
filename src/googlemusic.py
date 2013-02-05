# -*- coding: utf-8 -*-

# Copyright (C) 2013 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import collections
from gmusicapi.api import Api
from operator import itemgetter


class GoogleMusic():
	"""This class handles the communication with Google Music."""
	def __init__(self, email, password):
		if not email or not password:
			raise Exception("Username and password needs to be given")

		self._library = None
		self._artists = None
		self._albums = None
		self._playlists = None

		self._email = email
		self._password = password

		# Initialize the Google Music API
		self._api_init(self._email, self._password)

		if not self._api.is_authenticated():
			raise Exception("Credentials were not accepted!")

		# Initial load of the library
		self.load_library()

	def _api_init(self, email, password):
		"""Inits the API object and login to Google Music"""
		self._api = Api()
		self._api.login(email, password)

	def load_library(self):
		"""
		This function downloads the music library from Google Music and
		processes it.
		"""
		self._library = self._api.get_all_songs()

		# Generate artists and albums trees
		self._gen_trees()

	def _gen_trees(self):
		"""
		This function generates trees of artists and albums from the library.

		Parts of this function are taken from: https://github.com/mstill/thunner/blob/master/thunner
		=> Thanks for the great code :)
		"""
		# Use defaultdict to group song dictionaries by artists
		artists_dict = collections.defaultdict(list)
		for i in self._library:
			artists_dict[i['artist']].append(i)

		artists = []
		albums =  []
		for artist, songs_of_artist in artists_dict.iteritems():
			albums_of_artists_dict = collections.defaultdict(list)
			for i in songs_of_artist:
				albums_of_artists_dict[i['album']].append(i)

			albums_of_artist = []
			for album,tracks in albums_of_artists_dict.iteritems():
				album_name = album
				if album == "":
					album_name = "Untitled album"

				albums_of_artist.append({
											"name": album_name,
											"subtree": sorted(tracks, key=itemgetter('track')),
											"subtreeline": 0
										})

			albums = albums + albums_of_artist
			artists.append({
								"name": artist,
								"subtree": sorted(albums_of_artist, key=lambda x: x['name'].lower()),
								"subtreeline": 0
							})

		self._artists = sorted(artists, key=lambda x: x['name'].lower())
		self._albums = sorted(albums, key=lambda x: x['name'].lower())

	def get_songs(self):
		"""This function returns all songs from the music library."""
		songs = []
		for entry in self._library:
			song = {
				'id': entry['id'],
				'title': entry['title'], 
				'artist': entry['artist'], 
				'album': entry['album'] 
			}
			songs.append(song)

		return songs

	def get_artists(self):
		pass

	def get_albums(self):
		pass 

	def get_stream_url(self, id):
		return self._api.get_stream_url(id)
