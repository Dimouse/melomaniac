# -*- coding: utf-8 -*-
"""This module contains the controller classes of the application."""

# symbols which are imported by "from music.controllers import *"
__all__ = ['Root']

# standard library imports
# import logging
import datetime
from sqlalchemy import or_
from sqlalchemy import desc
from sqlalchemy.sql import func
from operator import itemgetter

# third-party imports
from turbogears import controllers, expose, flash, redirect

# project specific imports
# from music import model
# from music import json

from music.model import *

# log = logging.getLogger("music.controllers")

class TrackInfo(object):
    id = int
    name = unicode
    artist = unicode
    album = unicode
    number = int
    length = int
    bitrate = int
    path = str

    def __init__(self, id):
        self.id = id

class Root(controllers.RootController):
    """The root controller of the application."""

    @expose(template="music.templates.welcome")
    def index(self):
        """"Show the welcome page."""
        # log.debug("Happy TurboGears Controller Responding For Duty")
        flash(_(u"Your application is now running"))
        return dict(now=datetime.datetime.now())

    @expose("music.templates.edit")
    def edit(self,album_id):
        a = session.query(Album).get(album_id)
        g = session.query(Genre).all()
        ar= session.query(Artist).all()
        return dict(album = a, genres = g, artists = ar)

    @expose("music.templates.editartist")
    def editartist(self,id):
        a = session.query(Artist).get(id)
        g = session.query(Genre).all()
        return dict(artist = a, genres = g)

    @expose("music.templates.newalbum")
    def newalbum(self, title = u"", artist_id=0, genre_id=0, year=0, have=1, rating=-1, atype=0, submit=0):
	artist_id = int(artist_id)
	genre_id = int(genre_id)
	year = int(year)
	have = int(have)
	rating = int(rating)
	atype = int(atype)
	id = session.query(Album).order_by(Album.album_id.desc()).first().album_id + 1
        g = session.query(Genre).all()
        ar= session.query(Artist).all()
#	print artist_id
        return dict(id = id, title = title, artist_id = artist_id, genre_id = genre_id, year = year, have = have, rating = rating, atype = atype, genres = g, artists = ar)

    @expose("music.templates.newartist")
    def newartist(self):

	id = session.query(Artist).order_by(Artist.artist_id.desc()).first().artist_id + 1
        g = session.query(Genre).all()

        return dict(id = id,  genres = g)

    @expose("music.templates.newgenre")
    def newgenre(self):

	id = session.query(Genre).order_by(Genre.genre_id.desc()).first().genre_id + 1
        g = session.query(Genre).all()

        return dict(id = id,  genres = g)

    @expose()
    def save(self, album_id, title, artist_id, genre_id, year, have, rating, atype, submit):
        album = session.query(Album).get(album_id)
	album.title = title
	album.artist_id = artist_id
	album.genre_id = genre_id
	album.year = year
	album.have = have
	album.rating = rating
	album.atype = atype
	album.date = datetime.datetime.now()

        session.flush()
        return "Entry edited, you may close the page"

    @expose()
    def get_genres(self):
#        total=session.query(func.count(Album.album_id)).first()
#        total=str(total).replace("(","").replace(",)","")

        genres = session.query(Genre,func.count(Album.album_id)).filter(Genre.genre_id==Album.genre_id).group_by(Genre).all()
	gstr=""
	
	for g in genres:
	  num=str(g[1]).replace("(","").replace(")","")
	  if(int(num)>50):
	    gstr+=str(g[0].name)+","+str(num)+"; "
	
        return gstr

    @expose()
    def get_countries(self):
#        total=session.query(func.count(Album.album_id)).first()
#        total=str(total).replace("(","").replace(",)","")

        countries = session.query(Artist,func.count(Album.album_id)).filter(Artist.artist_id==Album.artist_id).group_by(Artist.country).all()
	gstr=""
	
	for g in countries:
	  num=str(g[1]).replace("(","").replace(")","")
	  if(int(num)>20):
	    gstr+=str(g[0].country)+","+str(num)+"; "
	
        return gstr

    @expose()
    def get_countries2(self):
#        total=session.query(func.count(Album.album_id)).first()
#        total=str(total).replace("(","").replace(",)","")

        countries = session.query(Artist,func.count(Artist.artist_id)).group_by(Artist.country).all()
	gstr=""
	
	for g in countries:
	  num=str(g[1]).replace("(","").replace(")","")
	  if(int(num)>5):
	    gstr+=str(g[0].country)+","+str(num)+"; "
	
        return gstr

    @expose()
    def get_years(self,genre):
#        g=session.query(Genre).all()
	res=""
	for y in range(1950,2020):	
          c = session.query(func.count(Album.year)).filter(Album.year==y)
          if genre!="-1":
            c=c.filter(Album.genre_id==genre)
          c=c.first()
	  c = str(c).replace("(","").replace(")","")
	  res+=str(y)+","+str(c)+"; "
	
        return res

    @expose()
    def get_dates(self,genre):
#        g=session.query(Genre).all()
	res=""
	now = datetime.datetime.now()
	
	for y in range(now.year-4,now.year+1):
	  for m in range(1,13):	
	    begin = datetime.date(y,m,1)
	    if m!=12:
	      end = datetime.date(y,m+1,1)
	    else:
	      end = datetime.date(y+1,1,1)	    
            c = session.query(func.count(Album.year)).filter(Album.date>=begin).filter(Album.date<end)
            if genre!="-1":
              c=c.filter(Album.genre_id==genre)
            c=c.first()
	    c = str(c).replace("(","").replace(")","")
	    res+=str(m)+"."+str(y)+","+str(c)+"; "
	
        return res

    @expose()
    def get_ratings(self,genre):
#        g=session.query(Genre).all()
	res=""
	for y in range(0,11):	
          c = session.query(func.count(Album.year)).filter(Album.rating==y)
          if genre!="-1":
            c=c.filter(Album.genre_id==genre)
          c=c.first()
	  c = str(c).replace("(","").replace(")","")
	  res+=str(y)+","+str(c)+"; "
	
        return res
                                
    @expose()
    def savenew(self, album_id, title, artist_id, genre_id, year, have, rating, atype, submit):
        album = Album(album_id,title,artist_id,genre_id,year,have,rating,atype,datetime.datetime.now())

        session.add(album)
        session.flush()
        return "Entry added, you may close the page"

    @expose()
    def saveartist(self, artist_id, name, genre_id, country, descr, submit):
	ar = session.query(Artist).get(artist_id)
	if ar:
	  ar.name = name
	  ar.genre_id = genre_id
	  ar.country = country
	  ar.descr = descr
	else:
          artist = Artist(artist_id,name,genre_id,country,descr)
          session.add(artist)
          session.flush()
        return "Entry added, you may close the page"

    @expose()
    def savegenre(self, genre_id, name, main_id, submit):
	g = session.query(Genre).get(genre_id)
	if g:
	  g.genre_id = genre_id
	  g.name = name
	  g.main_genre_id = main_id
	else:
          genre = Genre(genre_id,name,main_id)
          session.add(genre)
          session.flush()
        return "Entry added, you may close the page"

    @expose("music.templates.artists")
    def artists(self, sort=0, country="", genre=-1):
	sort=int(sort)
	genre=int(genre)
	
        a=session.query(Artist)
	score=[]
	newx=[]
	i=0

	if country!="":
	  a=a.filter(Artist.country==country)
	if genre!=-1:
	  a=a.filter(Artist.genre_id==genre)

	if sort==2:
	  a=a.order_by(Artist.country)
	if sort==3:
	  a=a.order_by(Artist.name)
	if sort==4:
	  a=a.order_by(Artist.genre_id)
	         
	a=a.all()	                       
	for x in a:
	  s=session.query(func.avg(Album.rating)).filter(Album.rating>-1).filter(Album.artist_id == x.artist_id).scalar()
	  s2=session.query(Album).filter(Album.rating>-1).filter(Album.artist_id == x.artist_id).count()
	  s3=session.query(Album).filter(Album.rating>5).filter(Album.artist_id == x.artist_id).count()
	  ss = 0
	  if s:
	    ss=s+s2*0.02+s3*0.02 #add 0.01 for each album with rating <= 5 and 0.02 for each album with rating > 5
	  newx.append([x,ss])
	  score.append(ss)
	if sort==1:
	  newx=sorted(newx, key=itemgetter(1))
	  a = [i[0] for i in newx]
	  score = [i[1] for i in newx]

        return dict(artists=a, score=score)

    @expose("music.templates.genres")
    def genres(self, page=1):
#        g=session.query(Genre).all()
        g = session.query(Genre,func.count(Album.album_id)).outerjoin(Album,Album.genre_id==Genre.genre_id).group_by(Genre)
        return dict(genres=g)

    @expose("music.templates.albums_byyear")
    def albums_byyear(self, genre=-1):
	genres = session.query(Genre).all()
	
	genre=int(genre)
	max=210
	if genre!=-1:
	  max=35
#        g=session.query(Genre).all()
	name = "All"
	if genre!=-1:
	  g = session.query(Genre).get(genre)
	  if g:
	    name = g.name
#        g = session.query(Genre,func.count(Album.album_id)).filter(Genre.genre_id==Album.genre_id).group_by(Genre)
        return dict(genres=genres,genre=genre,name=name,max=max)

    @expose("music.templates.albums_bydate")
    def albums_bydate(self, genre=-1):
	genres = session.query(Genre).all()
	
	genre=int(genre)
	max=210
	if genre!=-1:
	  max=35
#        g=session.query(Genre).all()
	name = "All"
	if genre!=-1:
	  g = session.query(Genre).get(genre)
	  if g:
	    name = g.name
#        g = session.query(Genre,func.count(Album.album_id)).filter(Genre.genre_id==Album.genre_id).group_by(Genre)
        return dict(genres=genres,genre=genre,name=name,max=max)

    @expose("music.templates.albums_byrating")
    def albums_byrating(self, genre=-1):
	genres = session.query(Genre).all()
	
	genre=int(genre)
	max=210*6
	if genre!=-1:
	  max=280
#        g=session.query(Genre).all()
	name = "All"
	if genre!=-1:
	  g = session.query(Genre).get(genre)
	  if g:
	    name = g.name
#        g = session.query(Genre,func.count(Album.album_id)).filter(Genre.genre_id==Album.genre_id).group_by(Genre)
        return dict(genres=genres,genre=genre,name=name,max=max)

    @expose("music.templates.albums_bygenre")
    def albums_bygenre(self, page=1):
#        g=session.query(Genre).all()
        g = session.query(Genre,func.count(Album.album_id)).filter(Genre.genre_id==Album.genre_id).group_by(Genre)
        return dict(genres=g)

    @expose("music.templates.albums_bycountry")
    def albums_bycountry(self, page=1):
#        g=session.query(Genre).all()
#        g = session.query(Artist,func.count(Album.album_id)).filter(Artist.artist_id==Album.artist_id).group_by(Artist.country)
        return dict()

    @expose("music.templates.artists_bycountry")
    def artists_bycountry(self, page=1):
#        g=session.query(Genre).all()
#        g = session.query(Artist,func.count(Album.album_id)).filter(Artist.artist_id==Album.artist_id).group_by(Artist.country)
        return dict()
        
    @expose("music.templates.albums")
    def albums(self, artist=0, year=0, rating=0, genre=0, have=0, sort=0, period=0, printed=0):

	artist=int(artist)
	year=int(year)
	rating=int(rating)
	genre=int(genre)
	have=int(have)
        sort=int(sort)
        period=int(period)
        printed=int(printed)

        a=session.query(Album)

        if artist != 0:
          a=a.filter_by(artist_id = artist)

        if year != 0:
          a=a.filter_by(year = year)

        if rating != 0:
          a=a.filter_by(rating = rating)

        if genre != 0:
          a=a.filter_by(genre_id = genre)

        if have != 0 and have < 10:
          a=a.filter_by(have = have)
	elif have !=0 and have == 10: #no mp3
	  a=a.filter(or_(Album.have == 0, Album.have == 2, Album.have == 4, Album.have == 6))
	elif have !=0 and have == 11: #mp3
	  a=a.filter(or_(Album.have == 1, Album.have == 3, Album.have == 5, Album.have == 7, Album.have == 8, Album.have == 9))
	elif have !=0 and have == 12: #cd
	  a=a.filter(or_(Album.have == 2, Album.have == 3, Album.have == 4, Album.have == 5, Album.have == 8, Album.have == 9))
	elif have !=0 and have == 13: #lp
	  a=a.filter(or_(Album.have == 6, Album.have == 7, Album.have == 8, Album.have == 9))

        from datetime import timedelta

	if period !=0:
	  d = timedelta(days = period)
	  a=a.filter(Album.date >= datetime.datetime.now() - d)

	if sort == 0:
          a=a.order_by(Album.album_id)
	if sort == 1:
          a=a.join(Album.artist).order_by(Artist.name)
	if sort == 2:
          a=a.order_by(Album.title)
	if sort == 3:
          a=a.order_by(Album.genre_id)
	if sort == 4:
          a=a.order_by(Album.year)
	if sort == 5:
          a=a.order_by(Album.rating)
	if sort == 6:
          a=a.order_by(Album.have)
	if sort == 7:
          a=a.order_by(Album.date)

	num=a.count()

	if printed == 1:
          return dict(albums=a, num=num, uri_artist=artist, uri_year=year, uri_rating=rating, uri_genre=genre, uri_have=have, uri_sort=sort, uri_period=period, tg_template='music.templates.albums_print')
        return dict(albums=a, num=num, uri_artist=artist, uri_year=year, uri_rating=rating, uri_genre=genre, uri_have=have, uri_sort=sort, uri_period=period)

    @expose()
    def saveuni(self, path="Z:\\"):
	import os, sys
	import traceback
	from mutagen.easyid3 import EasyID3

        from traceback import print_exc
        from mutagen.mp3 import MP3
        print "Scanning", path
	t = []
        i=0

        for path, dirs, files in os.walk(path):
          files.sort()
          for fn in files:
            if not fn.lower().endswith('.mp3'): continue
            ffn = os.path.join(path, fn)
            try:
                mp3 = MP3(ffn)
            except KeyboardInterrupt:
                raise
            except Exception, err:
                print "ERROR!"
            else:
                if mp3.tags is None:
                    print "ERROR: No mp3 tags here"
                else:
                    id3 = EasyID3(ffn)
                    if id3:
#                      print ffn, id3["title"], id3["artist"]
		      encoding = 'CP1251'
		      print i
                      t2 = TrackInfo(i)
#		      t2.name = id3["title"]
	              try:
   		        uni = id3["title"][0]
	  	        name = uni.encode('iso-8859-1').decode(encoding)
			id3["title"] = name
	              except (UnicodeError, LookupError):
                        pass
	              try:
   		        uni = id3["artist"][0]
	  	        name = uni.encode('iso-8859-1').decode(encoding)
			id3["artist"] = name
	              except (UnicodeError, LookupError):
                        pass
	              try:
   		        uni = id3["album"][0]
	  	        name = uni.encode('iso-8859-1').decode(encoding)
			id3["album"] = name
	              except (UnicodeError, LookupError):
                        pass

		      id3.save(ffn)
		      i += 1
        raise redirect("/")

    @expose("music.templates.checkdir")
    def checkdir(self, path, submit):
	import os, sys
	import traceback
	from mutagen.easyid3 import EasyID3

        from traceback import print_exc
        from mutagen.mp3 import MP3
        print "Scanning", path
	t = []
        i=0

        for path, dirs, files in os.walk(path):
          files.sort()
          for fn in files:
            if not fn.lower().endswith('.mp3'): continue
            ffn = os.path.join(path, fn)
            try:
                mp3 = MP3(ffn)
            except KeyboardInterrupt:
                raise
            except Exception, err:
                rep.error(ffn)
            else:
                if mp3.tags is None:
                    print "ERROR: No mp3 tags here"
                else:
#    	            print ffn
                    id3 = EasyID3(ffn)
                    if id3:
#                      print id3["title"], id3["artist"]
                      t2 = TrackInfo(i)
		      t2.name = id3["title"]
		      t2.artist = id3["artist"]
		      t2.album = id3["album"]
		      t2.length = mp3.info.length
		      t2.bitrate = mp3.info.bitrate
		      t2.path = ffn
		      t.append(t2)
		      i += 1
        print "DONE"
        return dict(tracks=t)


    @expose("music.templates.checkdir2")
    def checkdir2(self, path, submit):
	import os, sys
	import traceback
	from mutagen.easyid3 import EasyID3
	from mutagen.id3 import ID3

        from traceback import print_exc
        from mutagen.mp3 import MP3

        print "Scanning", path
	found = []
        found_name = []
	notfound = []
        notfound_name = []
	found_artist = []
        i=0

        for path, dirs, files in os.walk(path):
          files.sort()
          for fn in files:
            if not fn.lower().endswith('.mp3'): continue
            ffn = os.path.join(path, fn)
            try:
                mp3 = MP3(ffn)
            except KeyboardInterrupt:
                raise
            except Exception, err:
                rep.error(ffn)
            else:
                if mp3.tags is None:
                    print "ERROR: No mp3 tags here"
                else:
#    	            print ffn
                    id3 = EasyID3(ffn)
		    fid3 = ID3(ffn)
                    if id3:
#                      print id3["title"], id3["artist"]
		      ar = session.query(Artist).filter_by(name = id3["artist"][0]).all()
		      if ar:
                        al = session.query(Album).filter_by(artist_id = ar[0].artist_id).filter_by(title = id3["album"][0]).all()
		        if al:
		          if id3["album"] not in found_name:
			    found.append(al[0])
			    found_name.append(id3["album"])
		        else:
		          if id3["album"] not in notfound_name:
			    title = id3["album"][0]
			    title = title.replace("'","\\'")
			    title = title.replace("?","_")

#			    print title
			    album = Album(100000,unicode(title),ar[0].artist_id,ar[0].genre_id,fid3["TDRC"].text,1,-1,0,datetime.datetime.now())
			    notfound.append(album)
			    notfound_name.append(id3["album"])
			    found_artist.append(ar[0])
		      else:
			print "ERROR: Artist not found!"
        print "DONE"
        return dict(found=found, notfound=notfound, artists = found_artist)