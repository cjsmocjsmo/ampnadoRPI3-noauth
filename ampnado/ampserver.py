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
####To background this script invoke it with this command
####nohup python3 server.py &>/dev/null &

import os, random, hashlib, re, time, uuid, shutil
from urllib.parse import urlparse, parse_qs
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import pymongo
import functions as Fun

ampDBClient = pymongo.MongoClient("mongodb://db:27017/ampnadoDB")
db = ampDBClient.ampnadoDB

ampVDBClient = pymongo.MongoClient("mongodb://db:27017/ampviewsDB")
viewsdb = ampVDBClient.ampviewsDB

ampPDBClient = pymongo.MongoClient("mongodb://db:27017/picdb")
pdb = ampPDBClient.picdb

FUN = Fun.Functions()
RAND = Fun.RandomArtDb()


define('server_port',
	default= os.environ["AMP_SERVER_PORT"],
	help='run on the given port',
	type=int,
)

off_set = int(os.environ["AMP_OFFSET_SIZE"])

class Application(tornado.web.Application):
	def __init__(self):
		mpath = os.environ["AMP_MEDIA_PATH"]
		handlers = [
			(r"/Music/(.*)", tornado.web.StaticFileHandler, {'path': mpath}),
			(r"/ampnado", MainHandler),

			(r"/RandomPics", RandomPicsHandler),
			(r"/ArtistAlpha", ArtistAlphaHandler),

			(r"/ArtistInfo", ArtistInfoHandler),
			(r"/AlbumAlpha", AlbumAlphaHandler),

			(r"/AlbumInfo", AlbumInfoHandler),
			(r"/SongAlpha", SongAlphaHandler),

			(r"/SongInfo", SongInfoHandler),
			(r"/ImageSongsForAlbum", ImageSongsForAlbumHandler),
			(r"/PathArt", PathArtHandler),

			(r"/AllPlaylists", AllPlaylistsHandler),
			(r"/AllPlaylistSongsFromDB", AllPlaylistSongsFromDBHandler),
			(r"/Stats", StatsHandler),
			(r"/AddRandomPlaylist", AddRandomPlaylistHandler),
			(r"/AddPlayListNameToDB", AddPlayListNameToDBHandler),
			(r"/AddSongsToPlistDB", AddSongsToPlistDBHandler),
			(r"/CreatePlayerPlaylist", CreatePlayerPlaylistHandler),
			(r"/RandomAlbumPicPlaySong", RamdomAlbumPicPlaySongHandler),
			(r"/DeletePlaylistFromDB", DeletePlaylistFromDBHandler),
			(r"/DeleteSongFromPlaylist", DeleteSongFromPlaylistHandler),
			
			(r"/ArtistSearch", ArtistSearchHandler),
			(r"/AlbumSearch", AlbumSearchHandler),
			(r"/SongSearch", SongSearchHandler),
		]
		settings = dict(
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			# static_path = "./static",
			template_path = "./templates",
			login_url = "/login",
			cookie_secret = hashlib.sha512(str(random.randrange(100)).encode('utf-8')).hexdigest(),
			xsrf_cookies = False,
			debug = True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class MainHandler(BaseHandler):
	def get(self):
		self.render('ampnado.html')

class AllPlaylistsHandler(BaseHandler):
	@tornado.gen.coroutine
	def getpls(self):
		try: return [(d['playlistname'], d['playlistid']) for d in db.playlists.find({}).sort([('playlistname', pymongo.ASCENDING)])]
		except KeyError: return []
		
	@tornado.gen.coroutine
	def get(self):
		plname = yield self.getpls()
		plnamez = u"Please create a playlist"
		if plname != []: self.write(dict(plnames=plname))
		else: self.write(dict(plnames=plnamez))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class ArtistAlphaHandler(BaseHandler):
	@tornado.gen.coroutine
	def get(self):
		artal = viewsdb.artalpha.find_one({}, {'artalpha':1, '_id':0})
		artal = artal['artalpha']
		self.write(dict(artal=artal))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')
		
class ArtistInfoHandler(BaseHandler):
	@tornado.gen.coroutine
	def _get_art_info(self, sel):
		sel = str(sel)
		artinfo = [art for art in viewsdb.artistView.find({'Page': sel}, {'_id':0}).sort([('Artist', pymongo.ASCENDING)]).limit(off_set)]
		return artinfo

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		arts = yield self._get_art_info(int(p['selected'][0]))
		self.write(dict(arts=arts))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AlbumAlphaHandler(BaseHandler):
	@tornado.gen.coroutine
	def get(self):
		albal = viewsdb.albalpha.find_one({}, {'albalpha':1, '_id':0})
		albal = albal['albalpha']
		self.write(dict(albal=albal))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AlbumInfoHandler(BaseHandler):
	@tornado.gen.coroutine
	def _get_alb_info(self, sel):
		albinfo = [alb for alb in viewsdb.albumView.find({'Page': sel}, {'_id':0})]
		return albinfo

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		albs = yield self._get_alb_info(p['selected'][0])
		self.write(dict(albs=albs))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class SongAlphaHandler(BaseHandler):
	@tornado.gen.coroutine
	def get(self):
		songal = viewsdb.songalpha.find_one({}, {'songalpha':1, '_id':0})
		songal = songal['songalpha']
		self.write(dict(songal=songal))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class SongInfoHandler(BaseHandler):
	@tornado.gen.coroutine
	def _get_song_info(self, sel):
		songinfo = [song for song in viewsdb.songView.find({'Page': sel}, {'_id':0})]
		return songinfo

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		song = yield self._get_song_info(int(p['selected'][0]))
		self.write(dict(song=song))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class ImageSongsForAlbumHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_pic(self, aquery):
		picid = db.main.find_one({'AlbumId':aquery}, {"_id":0, "PicId":1})
		poo = pdb.pics.find_one({"PicId":picid["PicId"]}, {"_id":0, "Smallthumb":1})
		return poo["Smallthumb"]
		
	@tornado.gen.coroutine
	def getsongsongid(self, a_query):
		foo = {}
		foo['thumbnail'] = yield self.get_pic(a_query)
		foo['songs'] = [(t['Song'], t['SongId']) for t in db.main.find({'AlbumId':a_query}, {'Song':1, 'SongId':1, '_id':0})]			
		return foo

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		songs = yield self.getsongsongid(p['selected'][0])
		self.write(dict(getimgsonalb=songs))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class PathArtHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_file_info(self, asongid):
		return db.main.find_one({'SongId': asongid}, {'_id':0})
	
	@tornado.gen.coroutine
	def get_pic_info(self, a_picid):		
		return pdb.pics.find_one({'PicId':a_picid}, {'_id':0, 'Smallthumb':1})

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		selected = p['selected'][0]
		fileinfo = yield self.get_file_info(selected)
		#picinfo = yield self.get_pic_info(fileinfo["PicId"])
		#fileinfo['Smallthumb'] = picinfo['Smallthumb']
		self.write(fileinfo)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AllPlaylistSongsFromDBHandler(BaseHandler):
	@tornado.gen.coroutine
	def _get_songs_for_playlist(self, aplid):
		try:
			for playlist in db.playlists.find({'playlistid': aplid}):
			 return [[pl['Song'], pl['SongId']] for pl in playlist['songs']]
		except KeyError: return []
		except TypeError: return []

	@tornado.gen.coroutine		
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		taz = yield self._get_songs_for_playlist(p['playlistid'][0])
		self.write(dict(taz=taz))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class StatsHandler(BaseHandler):
	@tornado.gen.coroutine
	def _get_stats(self):
		return db.ampnado_stats.find_one({}, {'_id': 0})

	@tornado.gen.coroutine
	def get(self):
		stats = yield self._get_stats()
		self.write(dict(stats=stats))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AddPlayListNameToDBHandler(BaseHandler):
	@tornado.gen.coroutine	
	def _insert_plname(self, pln):
		db.playlists.insert({'playlistname': pln, 'playlistid': str(uuid.uuid4().hex)})

	@tornado.gen.coroutine
	def _get_playlists(self):
		return [{'playlistname': pl['playlistname'], 'playlistid': pl['playlistid']} for pl in db.playlists.find({})]

	@tornado.gen.coroutine		
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		yield self._insert_plname(p['playlistname'][0])
		pls = yield self._get_playlists()
		self.write(dict(pnames=pls))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AddSongsToPlistDBHandler(BaseHandler):
	@tornado.gen.coroutine	
	def insert_song_into_playlist(self, a_song_name, a_songid, a_plid):
		song = db.main.find_one({'SongId': a_songid})
		playlist = db.playlists.find_one({'playlistid': a_plid})
		try:
			playlist['songs'].append(song)
			db.playlists.update({'playlistid' : a_plid},
				{'playlistname' : playlist['playlistname'], 'playlistid' : a_plid, 'songs' : playlist['songs']})
		except KeyError:
			playlist['songs'] = [song]
			db.playlists.update({'playlistid': a_plid},
				{'playlistname' : playlist['playlistname'], 'playlistid' : a_plid, 'songs' : playlist['songs']})

	@tornado.gen.coroutine	
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		yield self.insert_song_into_playlist(p['songname'][0], p['songid'][0], p['playlistid'][0])
		self.write("Insertion complete")
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AddRandomPlaylistHandler(BaseHandler):
	@tornado.gen.coroutine	
	def create_random_playlist(self, aplname, aplcount):
		pl = {}
		aplcount = int(aplcount)
		ids = db.main.distinct('_id')
		random.shuffle(ids)
		random_ids = random.sample(ids, aplcount)
		new_song_list = []
		for r in random_ids:
			songs = db.main.find_one({'_id': r}, {'_id':0})
			new_song_list.append(songs)
		random.shuffle(new_song_list)
		pl['songs'] = new_song_list
		pl['playlistname'] = aplname
		pl['playlistid'] = str(uuid.uuid4().hex)
		db.playlists.insert(pl)
		return [{'playlistname': pl['playlistname'], 'playlistid': pl['playlistid']} for pl in db.playlists.find({}, {'_id':0})]

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		create_random_playlist = yield self.create_random_playlist(p['playlistname'][0], p['playlistcount'][0])
		self.write(dict(plists=create_random_playlist))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class CreatePlayerPlaylistHandler(BaseHandler):
	@tornado.gen.coroutine
	def _make_playlist(self, a_plid):
		playlist = db.playlists.find_one({'playlistid':a_plid})
		fart = []
		try:
			for pl in playlist['songs']:
				plp = pl['HttpMusicPath'].split('/', 1)
				plp = '/' + os.path.splitext(plp[1])[0]
				picinfo = [p for p in pdb.pics.find({"PicId": pl["PicId"]}, {"_id":0})]
				z = {
					'name': pl['Song'],
					'file': plp,
					'thumbnail': picinfo[0]['Smallthumb'],
					'album': pl['Album'],
					'artist': pl['Artist'],
				}
				fart.append(z)
			return fart
		except KeyError: return []

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		makePL = yield self._make_playlist(p['playlistid'][0])
		self.write(dict(makePL=makePL))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class DeletePlaylistFromDBHandler(BaseHandler):
	@tornado.gen.coroutine
	def _delete_playlist(self, plid):
		db.playlists.remove({'playlistid': plid})
		return u'Playlist Dropped From DB'

	@tornado.gen.coroutine
	def get_pl_list(self, plid):
		return [{'playlistname': pl['playlistname'], 'playlistid': pl['playlistid']} for pl in db.playlists.find({})]

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		yield self._delete_playlist(p['playlistid'][0])
		npl = yield self.get_pl_list(p['playlistid'][0])
		self.write(dict(npl=npl))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class DeleteSongFromPlaylistHandler(BaseHandler):
	@tornado.gen.coroutine
	def _get_rec_id(self, snameid):
		rec_id = db.tags.find_one({'songid': snameid})
		return rec_id['_id']
		
	@tornado.gen.coroutine
	def _get_playlist_info(self, plname):
		return db.playlists.find_one({'playlistname': plname})

	@tornado.gen.coroutine
	def _delete_song(self, pl, rid):
		pl['songs'] = [asong for asong in pl['songs'] if asong['_id'] != rid]
		db.playlists.update({'_id': pl['_id']}, {'$set': {'songs': pl['songs']}})

	@tornado.gen.coroutine
	def _get_new_playlist(self, pln):
		return [playlist['songs'] for playlist in db.playlists.find({'playlistname': pln}, {'songs.song':1, 'songs.songid':1})]

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		rec_id = yield self._get_rec_id(p['delsongid'][0])
		plist = yield self._get_playlist_info(p['playlistname'][0])
		yield self._delete_song(plist, rec_id)
		result = yield self._get_new_playlist(plist['playlistname'])
		self.write(dict(result=result))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class ArtistSearchHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_search(self, artsv):
		search = viewsdb.command('text', 'artistView', search=artsv)
		return [{ 'artist': sea['obj']['artist'],  'artistid': sea['obj']['artistid'], 'albums': sea['obj']['albums']} for sea in search['results']]

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		wsearch = yield self.get_search(p['artsearchval'][0])
		self.write(dict(wsearch=wsearch))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class AlbumSearchHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_search(self, albsv):
		search = viewsdb.command('text', 'albumView', search=albsv)
		return [{'artist': sea['obj']['artist'], 'album': sea['obj']['album'], 'albumid': sea['obj']['albumid'], 'thumbnail': sea['obj']['Smallthumb'], 'songs': sea['obj']['songs'], 'numsongs': sea['obj']['numsongs']} for sea in search['results']]

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		ysearch = yield self.get_search(p['albsearchval'][0])
		self.write(dict(ysearch=ysearch))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class SongSearchHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_search(self, sv):
		search = db.command('text', 'main', search=sv)
		return [{'artist': sea['obj']['Artist'], 'song': sea['obj']['Song'], 'songid': sea['obj']['SongId']} for sea in search['results']]

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		xsearch = yield self.get_search(p['searchval'][0])
		self.write(dict(xsearch=xsearch))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class RamdomAlbumPicPlaySongHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_song_info(self, apid):
		return db.main.find_one({'SongId':apid}, {'HttpMusicPath':1, 'Filename':1, 'PicId':1, 'Song':1, 'Album':1, 'Artist':1, '_id':0})

	@tornado.gen.coroutine
	def get_pic_info(self, pid):
		return pdb.pics.find_one({"PicId": pid['PicId']}, {"_id":0, "Smallthumb":1})

	@tornado.gen.coroutine
	def get(self):
		p = parse_qs(urlparse(self.request.full_url()).query)
		songid = p['sid'][0]
		foo = yield self.get_song_info(songid)
		boo = yield self.get_pic_info(foo)
		foo['Smallthumb'] = boo['Smallthumb']
		self.write(dict(soho=foo))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')

class RandomPicsHandler(BaseHandler):
	@tornado.gen.coroutine
	def get_count(self):
		return len([d['chunkid'] for d in db.randthumb.find({'displayed':'NOTSHOWN'})])

	@tornado.gen.coroutine
	def get_chunk(self):
		t5 = db.randthumb.find_one({'displayed': 'NOTSHOWN'})
		return t5['chunkid'], t5['chunk'], t5['displayed']

	@tornado.gen.coroutine
	def update_db(self, aid):
		db.randthumb.update({'chunkid': aid}, {'$set': {'displayed':'SHOWN'}})

	@tornado.gen.coroutine
	def reset_displayed(self):
		RAND.create_random_art_db()
		
	@tornado.gen.coroutine
	def get_rand_alb_list(self):
		count = yield self.get_count()
		if count < 2:
			yield self.reset_displayed()
			tid = yield self.get_chunk()
			yield self.update_db(tid[0])
			return tid[1]
		else:
			tid = yield self.get_chunk()
			yield self.update_db(tid[0])
			return tid[1]

	@tornado.gen.coroutine
	def get(self):
		rs = yield self.get_rand_alb_list()
		art = []
		for r in rs:
			x = {}
			pid = db.main.find_one({'AlbumId': r}, {'_id':0, 'PicId':1})
			ace = pdb.pics.find_one({'PicId':pid['PicId']}, {'Smallthumb':1, '_id':0})
			try:	
				x['thumbnail'] = ace['Smallthumb']
			except TypeError:
				print(r)
				#x["thumbnail"] = "./static/images/noartpic.jpg"
			x['songs'] = [(song['Song'], song['SongId']) for song in db.main.find({'AlbumId':r}, {'Song':1, 'SongId':1, '_id':0})]
			art.append(x)
		self.write(dict(rsamp=art))
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		self.set_header('Content-Type', 'application/json')
	
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.server_port)
	tornado.ioloop.IOLoop.instance().start()
	
if __name__ == "__main__":
	main()
