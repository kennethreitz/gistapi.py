from fabric.api import *
from fabric.contrib.console import confirm

# Host settings (+ssh key credentials)

def publish():
	""" Deploys the Gist.py project to PyPi """
	pass


	# 			# webbrowser.open('http://172.16.158.131:8080')
	# def build():
	# 	""" Generates pages of documentation """
	# 	local('ronn -5 -b  man/pdfish.1.ronn')
	# 
	# def init():
	# 	'''Resolves project dependencies'''
	# 	local('virtualenv --distribute .')
	# 	local('./bin/pip install -r requirements.txt ')
	# 
	# def scrub():
	# 	'''Death to the bytecode!'''
	# 	local("find . -name \"*.pyc\" -exec rm '{}' ';'")
