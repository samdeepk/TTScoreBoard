import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 
from appRoot import getApproot

from django.conf import settings
_ = settings.TEMPLATE_DIRS
settings.TEMPLATE_DIRS  = (getApproot(["templates"]))