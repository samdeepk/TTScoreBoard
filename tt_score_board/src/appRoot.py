import os

def getApproot(part=[""]):
	return  os.path.join(os.path.dirname(__file__),*part)