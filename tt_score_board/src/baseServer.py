
from django.template import Template as TR
import os

import webapp2

from webapp2_extras import sessions
from django.template.loader import get_template
from django.template.context import Context


config = {}
config['webapp2_extras.sessions'] = {
            'secret_key': 'my-super-secret-key',
        }

class baseHandler(webapp2.RequestHandler):
	
	
	
	ignoreUserUpdate =False
	ignoreUserLogin =False
	def templateRender(self,template_values={},path="",template="",render=True):
		
		
		template_values.update({'currentUser':self.currentUser if hasattr(self, "currentUser") else None,})
		
		path = os.path.join((path or os.path.dirname(__file__)), template)
		TR = get_template(path)
		finalRendered = TR.render(Context(template_values))
		if render: self.response.out.write(finalRendered)
		else: return finalRendered
		
	def dispatch(self):
		# Get a session store for this request.
		self.session_store = sessions.get_store(request=self.request)

		try:
			# Dispatch the request.
			webapp2.RequestHandler.dispatch(self)
		finally:
			# Save all sessions.
			self.session_store.save_sessions(self.response)

	@webapp2.cached_property
	def session(self):
		# Returns a session using the default cookie key.
		return self.session_store.get_session()