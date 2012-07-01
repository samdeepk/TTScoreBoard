from google.appengine.ext import db



class bDataModel(db.Model):
#	lastUpdatedBY = db.ReferenceProperty()
#	createdBy = db.ReferenceProperty()
	updateInfo = db.TextProperty()
	lastUpdatedOn = db.DateTimeProperty(auto_now=True)
	createdOn = db.DateTimeProperty(auto_now=True)


class Users(db.Model):
	userInfo = db.UserProperty()
	userNickName = db.StringProperty()
	faceExpressions =  db.TextProperty(default="{'smile':'','sand':'','cry':'','laugh':'','think':'','confused';'','angry':'','aggressive':''}")
	requestSettingsUpdate = db.BooleanProperty(default=True)
	loginCount = db.IntegerProperty(default=0)
	currentStatus = db.IntegerProperty(default=0)#{0:OFFILNE,1:ONILNE,3:AWAY,4;NOTRESPONDING}

	