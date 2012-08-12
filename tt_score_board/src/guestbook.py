#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import datetime
import webapp2
from appRoot import getApproot
import settings
from django.utils import simplejson as json

from google.appengine.ext import db
from google.appengine.api import users, memcache
from baseServer import baseHandler, config
from users.userManager import userHandler, getUserInfo

import copy
class Greeting(db.Model):
	author = db.UserProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
finalData = {"teams":[{'playerInfo':{'A1':{'names':" ",'img':" "},'A2':{'names':" ",'img':" "}},"win":False,"advantage":False,"Team_A_score":0,'playersPerformances':{'A1_score':0,"A2_score":0},'players':['A1',"A2"],"currentServing":True},{"Team_B_score":0,'playersPerformances':{'B1_score':0,"B2_score":0},'players':['B1',"B2"],"currentServing":False,"advantage":False,"win":False,'playerInfo':{'B1':{'names':" ",'img':" "},'B2':{'names':" ",'img':" "}}}]}

class show(baseHandler):
	
	def get(self,gameName=""):
		if gameName:
			cli = memcache.Client()
			toUpdate = cli.get("game-"+gameName)
			if   toUpdate:
				updatedData = toUpdate
                        	self.templateRender(template_values={"scores":{"teamA":updatedData['teams'][0],"teamB":updatedData['teams'][1]}},path=getApproot(["templates"]),template="userUpdate.html")
			else: self.response.out.write('Invalid Game Id or Game not found')

class update(baseHandler):
	ignoreUserUpdate = True
	
	@getUserInfo
	def post(self,gameName=""):
		
		if gameName:
			cli = memcache.Client()
			toUpdate = cli.get("game-"+gameName)
		   
			if not  toUpdate:
                                
				toUpdate = copy.copy(finalData)
			updatedData = toUpdate
             
			#self.response.out.write( "<br/><br/>Before -->")
			#self.response.out.write( updatedData)
			updateString = self.request.get('updateString').strip() if  self.request.get('updateString') else ""
			if updateString:
				updatedData = self.updateFinalData(toUpdate,updateString)	 
				if updatedData:cli.set("game-"+gameName,updatedData)
				
			#self.response.out.write( "<br/><br/>After-->")
			self.response.out.write( json.dumps(updatedData))
	@getUserInfo
	def get(self,gameName=""):
		#self.session = None
		#return
                
		if gameName:
                       	cli = memcache.Client()
			toUpdate = cli.get("game-"+gameName)
		   
			if not  toUpdate:
                                toUpdate = finalData
                                toUpdate['teams'][0]['playerInfo']['A1']['names']=self.request.get('a1') 
                                toUpdate['teams'][0]['playerInfo']['A2']['names']=self.request.get('a2') 
                                toUpdate['teams'][1]['playerInfo']['B1']['names']=self.request.get('b1') 
                                toUpdate['teams'][1]['playerInfo']['B2']['names']=self.request.get('b2')
                                toUpdate['teams'][0]['playerInfo']['A1']['img']=self.request.get('a1i')
                                toUpdate['teams'][0]['playerInfo']['A2']['img']=self.request.get('a2i')
                                toUpdate['teams'][1]['playerInfo']['B1']['img']=self.request.get('b1i') 
                                toUpdate['teams'][1]['playerInfo']['B2']['img']=self.request.get('b2i')
                                cli.set("game-"+gameName,toUpdate)
			updatedData = toUpdate
			self.templateRender(template_values={"scores":{"teamA":updatedData['teams'][0],"teamB":updatedData['teams'][1]}},path=getApproot(["templates"]),template="Scorefeeder.html")
			
			
		
	def updateFinalData(self,toUpdate={},updateString=""):
		
		self.finalData = toUpdate
		self.Team_A_score = 0
		self.Team_B_score = 0
		self.A1_score = 0
		self.A2_score = 0
		self.B1_score = 0
		self.B2_score = 0
		p='A1'
		o='A2'
		i='B1'
		u='B2'
		self.update_score(updateString)
		return self.finalData
	def update_score(self,r):
		self.str = r
		self.list = self.str.split()
		self.leng = len(self.list)
		for i in range(self.leng):
			self.value = self.list.pop()
			if self.value == 'a1+' or self.value == 'A1+':
				self.A1_score =1
			elif self.value =='b1+' or self.value == 'B1+':
				self.B1_score =1
			elif self.value == 'a1-' or self.value == 'A1-':
				self.A1_score -=1
			elif self.value == 'b1-' or self.value == 'B1-':
				self.B1_score -=1
			elif self.value == 'a2+' or self.value == 'A2+':
				self.A2_score =1
			elif self.value == 'b2+' or self.value == 'B2+':
				self.B2_score =1
			elif self.value == 'a2-' or self.value == 'A2-':
				self.A2_score -=1
			elif self.value == 'b2-' or self.value == 'B2-':
				self.B2_score -=1
			elif (self.value == 'a+' or self.value == 'A+') and self.Team_B_score ==0:
				self.Team_A_score =1
			elif (self.value == 'b+' or self.value == 'B+' ) and self.Team_A_score ==0:
				self.Team_B_score =1
		def swap(a,b):
			self.c = a
			self.a = b
			self.b = self.c
			return self.a,self.b
		if (self.finalData['teams'][0]['Team_A_score']== 20 and self.finalData['teams'][1]['Team_B_score']== 20):
                        self.list = self.str.split()
                        self.leng = len(self.list)
                        for i in range(self.leng):
                                self.value = self.list.pop()
                                if (self.value == 'a+' or self.value == 'A+'):
                                        if self.finalData['teams'][0]["advantage"] == True:
                                                self.finalData['teams'][0]["win"] == True
                                                self.finalData['teams'][0]['Team_A_score'] += self.Team_A_score
                                             #pass use win condition   
                                        self.finalData['teams'][0]["advantage"]=True
                                        self.finalData['teams'][1]["advantage"]=False
                                elif (self.value == 'b+' or self.value == 'B+' ):
                                        if self.finalData['teams'][1]["advantage"]==True:
                                                self.finalData['teams'][1]["win"]=True
                                                self.finalData['teams'][1]['Team_B_score'] += self.Team_B_score
                                        self.finalData['teams'][1]["advantage"]=True
                                        self.finalData['teams'][0]["advantage"]=False

                                        
                        self.finalData['teams'][0]['playersPerformances']['A2_score'] += self.A2_score
                        self.finalData['teams'][0]['playersPerformances']['A1_score'] += self.A1_score
                        self.finalData['teams'][1]['playersPerformances']['B2_score'] += self.B2_score
                        self.finalData['teams'][1]['playersPerformances']['B1_score'] += self.B1_score
                        
                        if self.finalData['teams'][0]['currentServing']:
                                        self.finalData['teams'][0]['players'][0],self.finalData['teams'][0]['players'][1] = swap(self.finalData['teams'][0]['players'][0],self.finalData['teams'][0]['players'][1])
                        if self.finalData['teams'][1]['currentServing']:
                                        self.finalData['teams'][1]['players'][0],self.finalData['teams'][1]['players'][1] = swap(self.finalData['teams'][1]['players'][0],self.finalData['teams'][1]['players'][1])
                        self.finalData['teams'][0]['currentServing'],self.finalData['teams'][1]['currentServing'] = swap(self.finalData['teams'][0]['currentServing'],self.finalData['teams'][1]['currentServing'])
                                
                elif (self.finalData['teams'][0]['Team_A_score']< 21 and self.finalData['teams'][1]['Team_B_score']< 21):
                        #self.finalData['teams'][0]['currentServing'] = self.current_Service_Status_Team_A
                        self.finalData['teams'][0]['playersPerformances']['A2_score'] += self.A2_score
                        self.finalData['teams'][0]['playersPerformances']['A1_score'] += self.A1_score
                        self.finalData['teams'][0]['Team_A_score'] += self.Team_A_score
                        #self.finalData['teams'][1]['currentServing'] = self.current_Service_Status_Team_B
                        self.finalData['teams'][1]['playersPerformances']['B2_score'] += self.B2_score
                        self.finalData['teams'][1]['playersPerformances']['B1_score'] += self.B1_score
                        self.finalData['teams'][1]['Team_B_score'] += self.Team_B_score
                        #print  (self.finalData['teams'][0]['Team_A_score'] + self.finalData['teams'][1]['Team_B_score'])/5
                        if (self.finalData['teams'][0]['Team_A_score'] + self.finalData['teams'][1]['Team_B_score'])%5 == 0:
                                #print 'inside Swap'
                                if self.finalData['teams'][0]['currentServing']:
                                        self.finalData['teams'][0]['players'][0],self.finalData['teams'][0]['players'][1] = swap(self.finalData['teams'][0]['players'][0],self.finalData['teams'][0]['players'][1])
                                if self.finalData['teams'][1]['currentServing']:
                                        self.finalData['teams'][1]['players'][0],self.finalData['teams'][1]['players'][1] = swap(self.finalData['teams'][1]['players'][0],self.finalData['teams'][1]['players'][1])
                                self.finalData['teams'][0]['currentServing'],self.finalData['teams'][1]['currentServing'] = swap(self.finalData['teams'][0]['currentServing'],self.finalData['teams'][1]['currentServing'])
                                        #print self.finalData
                		

app = webapp2.WSGIApplication([
	('/updateScore/(.*)', update),
	('/showScore/(.*)', show)
],config=config, debug=True)
