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

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import json

Base = declarative_base()

class Configuration:
  """
  Configuration
  """
  def __init__(self):
    confDir = os.path.join(os.path.expanduser('~'), '.piJukebox')
    dbFile = os.path.join(confDir, 'piJukebox.db')
    rdStationsFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        '..', 'data', 'radio_stations.json')
    self._engine = create_engine('sqlite:///' + dbFile, convert_unicode=True)
    Session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=self._engine))
    self._dbSession = Session()

    if not os.path.exists(confDir):
      try:
        os.makedirs(confDir)
      except OSError, error:
        raise Exception(error)

    # If the DB doesn't exist, create the default config and populate the database
    if not os.path.exists(dbFile):
      Base.metadata.create_all(self._engine)
      self.create_default_config()
      self.populate_radioStations(rdStationsFile)

  class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    port = Column(Integer)
    google_music_user = Column(String(500))
    google_music_password = Column(String(500))

    def __init__(self):
      pass

  class RadioStation(Base):
    __tablename__ = 'radiostations'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(250))
    mrl = Column(String(500))
    website = Column(String(500))
    logo = Column(String(500))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("Genre")
    last_played = Column(Date)
    plays = Column(Integer)
    favorite = Column(Boolean)
    myStation = Column(Boolean)

    def __init__(self, name, mrl, website="", logo=""):
      if not name or not mrl:
        raise Exception

      self.name = name
      self.mrl = mrl
      self.website = website
      self.logo = logo
      self.plays = 0
      self.favorite = False
      self.myStation = False

  class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(500))

    def __init__(self):
      pass

    def __repr__(self):
      pass

  def app_settings(self):
    return self._dbSession.query(self.Settings).first()

  def create_default_config(self):
    settings = self.Settings()
    settings.port = 8080
    settings.google_music_user = ""
    settings.google_music_password = ""

    self._dbSession.add(settings)
    self._dbSession.commit()

  def add_radio_station(self, name, mrl, website="", logo=""):
    """Add a new radio station."""
    if not name or not mrl:
      return

    station = self.RadioStation(name, mrl, website, logo)
    self._dbSession.add(station)
    self._dbSession.commit()

    return station

  def add_category(self, name):
    pass

  def get_radio_stations(self):
    """Returns all radio stations."""
    return self._dbSession.query(self.RadioStation).all()

  radio_stations = property(get_radio_stations)

  def delete_radio_station(self, id):
    if not id:
      return

    #  Remove the radio station
    self._dbSession.query(self.RadioStation).filter(self.RadioStation.id == id).delete()
    self._dbSession.commit()

  def update_radio_station(self, data):
    """Updates a radio station"""
    if not data:
      return

    station = self._dbSession.query(self.RadioStation).filter(self.RadioStation.id == data['id'])[0]
    if not station:
      return

    station.name = data['name']
    station.mrl = data['mrl']
    station.website = data['website']
    station.logo = data['logo']
    #station.last_played = data['last_played']
    station.plays = int(data['plays'])
    station.favorite = bool(data['favorite'])
    station.myStation = bool(data['myStation'])

    self._dbSession.commit()

  def get_app_settings(self):
    settings = self.app_settings()

    if not settings:
      return {}

    data = {
      'gmUsername': settings.google_music_user,
      'gmPassword': settings.google_music_password
    }

    return data

  def save_app_settings(self, settings):
    appSettings = self.app_settings()
    appSettings.google_music_user = settings['gmUsername']
    appSettings.google_music_password = settings['gmPassword']
    self._dbSession.commit()

  def populate_radioStations(self, dataFile):
    """Populates the database with all available radio stations."""
    # Check if file exists
    if not os.path.exists(dataFile):
      raise Exception("Radion stations data file not found!")

    json_file = open(dataFile)
    data = json.load(json_file)
    json_file.close()

    for station in data:
      name = station['name']
      mrl = station['mrl']
      website = station['website']
      logo = station['logo']

      station = self.RadioStation(name, mrl, website, logo)
      self._dbSession.add(station)
      self._dbSession.commit()

  def add_test_radio_stations(self):
    self.add_radio_station("FM4",
        "http://mp3stream1.apasf.apa.at:8000/listen.pls",
        "http://fm4.orf.at/", "http://www.projectmooncircle.com/files/fm4logo.png")

