#!/usr/bin/python3
###############################################################################
###############################################################################
	# LICENSE: GNU General Public License, version 2 (GPLv2)
	# Copyright 2015, Charlie J. Smotherman
	#
	# This program is free software; you can redistribute it and/or
	# modify it under the terms of the GNU General Public License v2
	# as published by the Free Software Foundation.
	#
	# This program is distributed in the hope that it will be useful,
 	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.
	#
	# You should have received a copy of the GNU General Public License
	# along with this program; if not, write to the Free Software
	# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################
###############################################################################
import os, base64, glob
from PIL import Image
from pymongo import MongoClient, ASCENDING, DESCENDING
from pprint import pprint

client = MongoClient("mongodb://db:27017/ampnaodDB")
db = client.ampnadoDB
viewsdb = client.ampviewsDB

class Thumbnails():

	def get_smallthumb(self, size, location, filename):
		try:
			im2 = Image.open(filename)
			im2.load()
			im2.thumbnail(size, Image.ANTIALIAS)
			im2.save(location, "JPEG")
		except OSError:
			pass
		if os.path.exists(location):
			print("FUCK YEA LOCATION EXISTS I JUST MADE THE JPG")

	def get_thumb_size(self, location):
		try:
			return os.stat(location).st_size
		except FileNotFoundError:
			return 0 
		
	def get_b64_image(self, location):
		try:	
			with open(location, 'rb') as imagefile:
				return ''.join(('data:image/png;base64,', base64.b64encode(imagefile.read()).decode('utf-8')))
		except FileNotFoundError:
			print("FileNotFoundError: get_b64_image error")
			print(location)
			return "None"

	def create_thumbs(self, p):
		pprint(p)
		loc1 = os.environ["AMP_PROGRAM_PATH"] +" temp/" + p["PicId"] + ".jpg"
		if os.path.exists(loc1):
			print("yes loc1 exists removing")
			os.remove(loc1)
		d2thumb = (125, 125)
		if p["PicPath"] != None:
			if os.path.exists(p["PicPath"]):
				self.get_smallthumb(d2thumb, p["NewPicPath"], p["PicPath"])
				print("this is newpicpath")
				print(p["PicPath"])
				print(p["NewPicPath"])
			else:
		 		print("WTF\n WTF\n WTF\n %s" % p["NewPicPath"])
		
		# p['Image_Size'] = ""
		# p['Smallthumb'] = ""
		# if os.path.exists(p["NewPicPath"]):
		# 	print("p[NewPicPath] exists")
			
		p['Image_Size'] = self.get_thumb_size(p["NewPicPath"])
		print(p['Image_Size'])
		p['Smallthumb'] = self.get_b64_image(p["NewPicPath"])
		print(p['Smallthumb'])

		return p
		# if os.path.exists(loc1):
		# 	print("loc1 exists")
		# 	p['Image_Size'] = self.get_thumb_size(loc1)
		# 	p['Smallthumb'] = self.get_b64_image(loc1)
		# 	print(p['Image_Size'])
		# 	print(p['Smallthumb'])
		# 	return p
			
		# print("THIS IS SMALLTHUMB P \n")
		# print(p['Image_Size'])
		# print(p['Smallthumb'])
		# return p