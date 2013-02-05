################################################################################
# This file is part of piJukebox.
###############################################################################

from mpg123 import Mpg123
from mplayer import MPlayer


class Player:
  def __init__(self):
    self.availablePlayers = ['mpg123']
    self.pid = 0
    self.isPlaying = False
    self.isPaused = False
    #self.mpg123 = Mpg123()
    self.mplayer = MPlayer()
    self.activePlayer = self.availablePlayers[0]

  def play_stream(self, url):
    """Plays the given stream."""
    if not url:
      return

    self.mplayer.play(url)
    self.isPlaying = True
    self.isPaused = False

  def stop(self):
    """Stops the playback."""
    if not self.isPlaying:
      return

    self.mplayer.stop()
    self.isPlaying = False
    self.isPaused = False

  def pause(self):
    """Pauses the playback."""
    if self.isPaused:
      return
    self.mplayer.pause()
    self.isPaused = True

  def resume(self):
    """Resumes the playback."""
    if not self.isPaused:
      return
    self.mplayer.resume()
    self.isPaused = False

  def get_rd_station(self):
    """Returns the current playing radio station."""
    #if not self.isPlaying:
    #  return ""

    return self.mplayer.stationName

  def get_song_title(self):
    """Returns the current playing song title"""
    #if not self.isPlaying or not self.isPaused:
    #  return ""

    return self.mplayer.currentTrackName

  def get_info(self):
    pass


if __name__ == '__main__':
  player = Player()
  player.play_stream("http://mp3stream1.apasf.apa.at:8000/listen.pls", True)
  time.sleep(5)
  player.stop()
