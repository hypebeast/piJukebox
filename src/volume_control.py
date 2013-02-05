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

import subprocess
import platform


class VolumeController:
	"""This class handles the volume control."""
	def __init__(self):
		self._volume = -1
		self._isMuted = False
		self._amixerbin = "amixer"
		self._soundDevice = "PCM"

		self._system = platform.system()

	def setVolume(self, volume):
		# if volume < 0 or volume > 100:
		# 	return

		self._volume = volume

		args = []
		if self._system == "Linux":
			args.append(self._amixerbin)
			args.append("-c0")
			args.append("set")
			args.append(self._soundDevice)
			args.append(str(volume)+"%")
		elif self._system == "Darwin":
			args.append('osascript')
			args.append('-e')	
			args.append('set volume ' + str((int(volume)/10)))

		if len(args) > 0:
			subprocess.Popen(args)

	def mute(self):
		self.setVolume(0)

	def unmute(self):
		if self._volume < 0:
			self.setVolume(65)
		else:
			self.setVolume(self._volume)