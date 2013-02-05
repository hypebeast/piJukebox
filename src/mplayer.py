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

import time
import threading
import subprocess
import signal


class MPlayer(object):
  """
  Wrapper class for working with mplayer.
  """
  def __init__(self):
    self.isRunning = False
    self.isPaused = False
    self._pid = 0
    self._readerThread = None
    self._stopReading = False
    self._mplayerbin= "mplayer"
    self._mplayer = None

    self.stationUrl = ""
    self.stationName = ""
    self.currentTrackName = ""

  def play(self, url):
    """Plays the given URL."""
    if not url:
      return

    # Save the current active URL
    self.stationUrl = url

    # Stop the currently running stream if one is running
    if self.isRunning:
      self.stop()

    args = [self._mplayerbin]
    args.append("-noconfig")
    args.append("all")
    args.append("-quiet")
    # Check for playlist
    if self.stationUrl.endswith('m3u') or self.stationUrl.endswith('pls'):
      args.append("-playlist")
    args.append(self.stationUrl)

    self._mplayer = subprocess.Popen(args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    #self.stdout, self.stderr = self.mpg123.communicate()
    #print self.stdout
    self._readerThread = threading.Thread(target=self._readOutput)
    self._readerThread.setDaemon(True)
    self._stopReading = False
    self._readerThread.start()
    self.isRunning = True
    self.isPaused = False

  def stop(self):
    if not self.isRunning:
      return

    self._stopReading = True
    #self._readerThread.join()
    self._mplayer.send_signal(signal.SIGINT)
    self.isRunning = False
    self.isPaused = False

  def pause(self):
    if self.isPaused:
      return

    self.stop()
    self.isPaused = True

  def resume(self):
    if not self.isPaused or len(self.stationUrl) == 0:
      return

    self.play(self.stationUrl)
    self.isPaused = False

  def _readOutput(self):
    while not self._stopReading:
      line = self._mplayer.stdout.readline()
      self._parseOutput(line)
      time.sleep(0.1)

  def _parseOutput(self, line):
    if not line:
      return

    if line.startswith("Name"):
      self.stationName = line[(len("Name   :")):].strip()
    elif line.startswith("ICY Info:"):
      if "StreamTitle=" in line:
        startIndex = line.find("'", line.find("StreamTitle=")+len("StreamTitle="))+1
        endIndex = line.find("'", startIndex)
        self.currentTrackName = line[startIndex:endIndex]
