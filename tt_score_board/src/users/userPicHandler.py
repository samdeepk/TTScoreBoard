from __future__ import with_statement
from google.appengine.api import files,blobstore
import settings
import logging
import webapp2
from google.appengine.ext import webapp
from webapp2_extras import sessions_memcache
from models import Users,Pics
from baseServer import baseHandler, config
from django.utils import simplejson as json
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobInfo
import png

import urllib
from users.userManager import userHandler, getUserInfo,ignoreUserUpdate

from appRoot import getApproot
from google.appengine.ext import db
from webapp2 import Response

from StringIO import StringIO


		
class uploadPicData(baseHandler):
	@ignoreUserUpdate
	@getUserInfo
	def post(self,service=""):
		#logging.info(self.request.body)
		if self.request.body:
			pic = Pics(pic=db.Blob(str(self.request.POST.get('image'))),user=self.currentUser)
			
			
			
			
			y= pic.put()
			logging.info(y)
			self.response.clear()
			self.response.write({"key":str(y),'servingUrl' : "/users/pic/serve/d/"+str(y)})#+"/"+self.currentUser.userNickName})
			#response = Response(body='hello world!', content_type='text/plain')
			
			#self.response.write(y)
			
			return'''
			
			
			
			
			
			file_name = files.blobstore.create(mime_type='image/jpg')

			# Open the file and write to it
			with files.open(file_name, 'a') as f:
			  f.write(db.Blob(self.request.body))
			
			# Finalize the file. Do this before attempting to read it.
			files.finalize(file_name)
			
			# Get the file's blob key
			blob_key = files.blobstore.get_blob_key(file_name)
			
			
			logging.info(blob_key)
			
			
			#return webapp2.Response('Hello, returned response world!')
			#self.response.out.write(blob_key)
			self.response.out.write(json.dumps({"key":str(blob_key),'servingUrl' : "/users/pic/serve/d/"+str(blob_key)+"/"+self.currentUser.userNickName}))'''
class uploadPic(baseHandler):
	@ignoreUserUpdate
	@getUserInfo
	def post(self,service=""):
		#logging.info(self.request.body)
		if self.request.body:
			'''pic = Pics(pic=self.request.body)#,user=self.currentUser)
			
			y= pic.put()
			logging.info(y)
			self.response.clear()
			self.response.write({"key":str(pic),'servingUrl' : "/users/pic/"+str(pic)})#+"/"+self.currentUser.userNickName})
			response = Response(body='hello world!', content_type='text/plain')
			
			self.response.write(y)
			
			return'''
			file_name = files.blobstore.create(mime_type='image/jpg')

			# Open the file and write to it
			with files.open(file_name, 'a') as f:
			  f.write(db.Blob(self.request.body))
			
			# Finalize the file. Do this before attempting to read it.
			files.finalize(file_name)
			
			# Get the file's blob key
			blob_key = files.blobstore.get_blob_key(file_name)
			
			
			logging.info(blob_key)
			
			
			#return webapp2.Response('Hello, returned response world!')
			#self.response.out.write(blob_key)
			self.response.out.write(json.dumps({"key":str(blob_key),'servingUrl' : "/users/pic/serve/b/"+str(blob_key)+"/"+self.currentUser.userNickName}))

from google.appengine.api import images

class ServeHandlerFromData(baseHandler):
	def get(self, resource="",finlenME=""): 
		logging.info(resource)
		data = db.get(resource)	
		#self.response.headers['Content-Type'] = 'image/jpg'
		#img = images.Image(data.pic)
		#img.resize(width=80, height=100)
		#img.im_feeling_lucky()
		#thumbnail = img.execute_transforms(output_encoding=images.JPEG)
		f = StringIO()
		#w = png.Writer(len(s[0]), len(s), greyscale=True, bitdepth=1)
		#w.write(f, s)
		
		# binary PNG data
		#print f.getvalue()
		
		#r=png.Reader(data.pic)
		#r.read()
		
		#self.response.headers['Content-Type'] = 'image/jpeg'
		self.response.out.write(data.pic)#f.getvalue())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource="",finlenME=""): 
		logging.info(resource)
		#print resource
		#return
		resource = str(urllib.unquote(resource))
		logging.info(resource)
		blob_info = BlobInfo.get(resource)
		logging.info(blob_info)
		self.send_blob(blob_info)			
				
app = webapp2.WSGIApplication([
							
							('/users/pic/update', uploadPic),
							('/users/pic/update/data', uploadPicData),
							('/users/pic/serve/b/([^/]+)/(.*)', ServeHandler),
							('/users/pic/serve/d/([^/]+)/(.*)', ServeHandlerFromData),
							('/users/pic/s/([^/]+)/(.*)', ServeHandler),
							('/users/pic/([^/]+)/(.*)', ServeHandler),
							
							],config=config,
							  debug=True)
							  
							  
app2 = webapp.WSGIApplication([
							
							('/users/pic/serve/b/([^/]+)/(.*)', ServeHandler),
							('/users/pic/serve/d/([^/]+)/(.*)', ServeHandlerFromData),
							
							],config=config,
							  debug=True)
