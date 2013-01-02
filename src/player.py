################################################################################
# Part of piJukebox
###############################################################################

import subprocess
import signal
import time
import threading
import Queue


class Mpg123Controller:
	def __init__(self):
		self.pid = 0
		self.isRunning = False
		self._readerThread = None
		self._stopReading = False
		self._inputQueue = None

	def play(self, uri, isPlaylist=False):
		"""Plays the given URI."""
		if self.isRunning:
			return

		mpg123_bin = "mpg123"
		args = [mpg123_bin]
		if isPlaylist:
			args.append("-@")
		args.append(uri)

		self.mpg123 = subprocess.Popen(args,
									stdin=subprocess.PIPE,
									stdout=subprocess.PIPE,
									stderr=subprocess.STDOUT)
		#self.stdout, self.stderr = self.mpg123.communicate()
		#print self.stdout
		self._readerThread = threading.Thread(target=self._readOutput)
		#self._readerThread.setDaemon(True)
		self._stopReading = False
		self._readerThread.start()
		self.isRunning = True

	def stop(self):
		"""Stops the playback."""
		if not self.isRunning:
			return

		self._stopReading = True
		self._readerThread.join()
		self.mpg123.send_signal(signal.SIGINT)
		self.isRunning = False

	def _readOutput(self):
		while not self._stopReading:
			line = self.mpg123.stdout.readline()
			print "line: " + line.rstrip('\n')
			time.sleep(0.01)

	def _parseOutput(self):
		pass


if __name__ == '__main__':
	mpg123 = Mpg123Controller()
	mpg123.play("http://mp3stream1.apasf.apa.at:8000/listen.pls", True)
	time.sleep(5)
	mpg123.stop()