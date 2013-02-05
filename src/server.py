# -*- coding: utf-8 -*-

# Copyright (C) 2012 Sebastian Ruml <sebastian.ruml@gmail.com>
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

from bottle import route, run, debug, template, request, validate, error, static_file, get
from bottle import response
from json import dumps
from player import Player
from configuration import Configuration
from volume_control import VolumeController
from googlemusic import GoogleMusic

# Player object
player = Player()

# Config object
config = Configuration()

# Volume Control object
volume_control = VolumeController()

# Google Music
google_music = GoogleMusic(config.app_settings().google_music_user,
                            config.app_settings().google_music_password)

####
# UI
####

@route('/')
def index():
  return template('index')

@route('/about')
def about():
  return template('about')


####
# Mobile UI
####

@route('/mobile')
def index_mobile():
  return template('index_mobile')


####
# API
####

@route('/api/start')
def start_playback():
  player.resume()
  success = { 'success': True }
  return success

@route('/api/pause')
def pause_playback():
  player.pause()
  success = { 'success': True }
  return success

@route('/api/play_station', method="POST")
def play_stream():
  url = request.forms.get('mrl','')
  player.play_stream(url)

@route('/api/play_gm_song', method="POST")
def play_gm_song():
  song_id = request.forms.get('id', '')
  player.play_stream(google_music.get_stream_url(song_id))

@route('/api/song')
def get_song():
  """Returns infos of the currently playing song or radio station."""
  rd_station = player.get_rd_station()
  song = player.get_song_title()
  data = { 'station': rd_station, 'song': song}
  return data

@route('/api/stations', method="GET")
def get_stations():
  stations = config.radio_stations
  data = []
  for station in stations:
    data.append({
                  'id': station.id,
                  'name': station.name,
                  'mrl': station.mrl,
                  'website': station.website,
                  'logo': station.logo,
                  'genre': "",
                  'last_played': station.last_played,
                  'plays': station.plays,
                  'favorite': station.favorite,
                  'myStation': station.myStation
                })

  response.content_type = 'application/json'
  return dumps(data)

@route('/api/stations', method="POST")
def create_station():
  name = request.forms.get('name', '')
  mrl = request.forms.get('mrl', '')
  website = request.forms.get('website', '')
  logo = request.forms.get('logo', '')

  # Add the new radio station
  station = config.add_radio_station(name, mrl, website, logo)
  station.myStation = True
  data = {
            'id': station.id,
            'name': station.name,
            'mrl': station.mrl,
            'website': station.website,
            'logo': station.logo,
            'genre': "",
            'last_played': station.last_played,
            'plays': station.plays,
            'favorite': station.favorite,
            'myStation': station.myStation
         }
  return data

@route('/api/stations/<id:int>', method="PUT")
def update_station(id):
  assert isinstance(id, int)

  station = {
              'id': id,
              'name': request.forms.get('name', ''),
              'mrl': request.forms.get('mrl', ''),
              'website': request.forms.get('website', ''),
              'logo': request.forms.get('logo', ''),
              'genre': "",
              'last_played': request.forms.get('lastPlayed', ''),
              'plays': int(request.forms.get('plays', '')),
              'favorite': bool(request.forms.get('favorite', '')),
              'myStation': bool(request.forms.get('myStation', ''))
            }

  config.update_radio_station(station)

@route('/api/stations/<id:int>', method="DELETE")
def delete_station(id):
  assert isinstance(id, int)
  config.delete_radio_station(id)

@route('/api/stations/genres', method="GET")
def get_rd_genres():
  pass

@route('/api/gm', method="GET")
def get_gm_library():
  """Returns the google music library"""
  stations = google_music.get_songs()

  response.content_type = 'application/json'
  return dumps(stations)

@route('/api/settings', method="GET")
def get_settings():
  return config.get_app_settings()

@route('/api/settings', method="POST")
def save_settings():
  data = {
    'gmUsername': request.forms.get('gmUsername', ''),
    'gmPassword': request.forms.get('gmPassword', '')
  }
  config.save_app_settings(data)

@route('/api/volume', method="POST")
def set_volume():
  volume = request.forms.get('volume', '')
  volume_control.setVolume(volume)

@route('/api/volume/mute', method="GET")
def mute_volume():
  volume_control.mute()

@route('/api/volume/unmute', method="GET")
def unmute_volume():
  volume_control.unmute()

# Static
@route('/public/:path#.+#', name='static')
def static(path):
    return static_file(path, root='public')

@route('/templates/:path#.+#', name='static')
def static_templates(path):
    return static_file(path, root='public/templates')

@error(404)
def error404(error):
    return 'Nothing here, sorry'

# Run the server
def run_server(host, port):
  run(host=host, port=port, reloader=True, debug=True)
