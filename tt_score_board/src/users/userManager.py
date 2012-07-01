
from google.appengine.api import users

import settings
import logging
import webapp2
from webapp2_extras import sessions_memcache
from models import Users
from baseServer import baseHandler, config
from appRoot import getApproot
from google.appengine.ext import db, webapp
from webob.response import Response

from google.appengine.api import files,blobstore


def ignoreUserUpdate(handler_method):
		def check_login(self, *args, **kwargs):
			self.ignoreUserUpdate =True
			handler_method(self, *args, **kwargs)
				
				
		return check_login
def ignoreUserLogin(handler_method):
		def check_login(self, *args, **kwargs):
			self.ignoreUserLogin =True
			handler_method(self, *args, **kwargs)
				
				
		return check_login


def getUserInfo(handler_method):
	def check_login(self, *args, **kwargs):
		self.currentUser = self.session.get('currentUser')
		if self.currentUser: self.currentUser= db.get(self.currentUser)
		if not self.currentUser:
			
			userX = userHandler().getUserFromUnique()
			self.session['currentUser'] = str(userX[1].key()) if userX[1] else ""
			self.currentUser = userX[1]#self.session['currentUser'] 
		
#		print 
#		print self.ignoreUserLogin , "self.ignoreUserLogin"
#		print self.ignoreUserUpdate , "self.ignoreUserUpdate"
		logging.info( self.ignoreUserUpdate)
		logging.info( self.ignoreUserLogin)
		if not( self.currentUser ) and  not self.ignoreUserLogin:
			logging.info(self.request.path)
			return self.redirect('/login'+(("?next="+self.request.uri) if self.request.uri else "") )
		else:
			logging.info("hei")
			if self.currentUser and self.currentUser.requestSettingsUpdate and   not self.ignoreUserUpdate:
				
				self.redirect('/users/update'+(("?next="+self.request.uri) if self.request.uri else "") )
			handler_method(self, *args, **kwargs)
			#logging.info("hei")

			
	return check_login
FIDS = {}		
def getFIURL(service):
	
	if not service: return "www.google.com/accounts/o8/id"
	else :
		return FIDS[service] if service in FIDS else "www.google.com/accounts/o8/id"
					
class userHandler(baseHandler):
	currentUser = None
	def getUserFromUnique(self):
		user = users.get_current_user()
		logging.info(user)
		ruser= None
		if user:
			ruser = Users.get_or_insert(user.federated_identity() or (user.user_id()+":"+user.email()))
			if not ruser.userInfo:
				ruser.userInfo = user
				ruser.userNickName = user.nickname()
				ruser.put()
		return (user,ruser) if user else (None,None)
#		if get_session:
#			users.get_current_user()


class loginHandler(baseHandler):
	@ignoreUserLogin 
	@getUserInfo
	def get(self,service=""):
		self.redirect(users.create_login_url(self.request.get('next') or "/", federated_identity = getFIURL(service)) )

class logoutHandler(baseHandler):
	@getUserInfo
	def get(self):
		self.session['currentUser'] = None
		self.redirect(users.create_logout_url("/"))
		#response = Response(body='hello world!', content_type='text/plain')
	
defaultExpressions =[
					
					{"type":"smile",'defaultMsg':"Smile Please ! :)","defaultPic":"/static/images/icon/set1/okHappy.png",'updatedPic':""},
					{"type":"worried",'defaultMsg':"Your results are going to be out at any moment ...","defaultPic":"/static/images/icon/set1/worried.png",'updatedPic':""},
					{"type":"winner",'defaultMsg':"Congratulation you got 1C at KBC, we are here to capture your expression.","defaultPic":"/static/images/icon/set1/winner.png",'updatedPic':""},
					{"type":"unHappy",'defaultMsg':"unHappy Please ! :(","defaultPic":"/static/images/icon/set1/unHappy.png",'updatedPic':""},
					{"type":"shocked",'defaultMsg':"shocked Please ! ","defaultPic":"/static/images/icon/set1/shocked.png",'updatedPic':""},
					{"type":"serious",'defaultMsg':"I am serious now.. please every one be serious.! :-|","defaultPic":"/static/images/icon/set1/serious.png",'updatedPic':""},
					{"type":"pleased",'defaultMsg':"pleased Please ! :)","defaultPic":"/static/images/icon/set1/pleased.png",'updatedPic':""},
					{"type":"looser",'defaultMsg':"looser looser looser looser :P","defaultPic":"/static/images/icon/set1/looser.png",'updatedPic':""},
					{"type":"LaughLoud",'defaultMsg':"LOL !!!!!","defaultPic":"/static/images/icon/set1/LaughLoud.png",'updatedPic':""},
					{"type":"kinky",'defaultMsg':"kinky ! ;)","defaultPic":"/static/images/icon/set1/kinky.png",'updatedPic':""},
					{"type":"cunningSmart",'defaultMsg':"cunningSmart ! ;)","defaultPic":"/static/images/icon/set1/cunningSmart.png",'updatedPic':""},
					{"type":"angry",'defaultMsg':"angry Please ! :X","defaultPic":"/static/images/icon/set1/angry.png",'updatedPic':""},
					
					
					]	
class userUpdate(baseHandler):
	@ignoreUserUpdate
	@getUserInfo
	def get(self,service=""):
		if self.currentUser:
			template_values= {'user':self.currentUser,'defaultExpressions':defaultExpressions}
			self.templateRender(template_values=template_values,path=getApproot(["templates","users"]),template="userUpdate.html",render=True)
		
app = webapp2.WSGIApplication([
							
							('/users/update', userUpdate),
							('/login', loginHandler),
							('/logout', logoutHandler),
							
							],config=config,
							  debug=True)

