import time
import pygame
import os
import sys
import random
import binascii
import re

class Page:
	def __init__(self):
		# NOTE: Multiplier set to 23 to ignore first row (occupied by date/time and name of service)
		self.charList = ['20'] * (40*23)

	def parseTTV(file):
		with open(file, 'rb') as f:
			cont = f.read()
		hx = re.compile('(..)').findall(binascii.hexlify(cont))
		for x in range(40, 960):
			charList[x-40] = hx[x]

class System:
	def __init__(self, scrX, scrY, fullscreen=False):
		pygame.init()
		if fullscreen == True:
			self.screen = pygame.display.set_mode([scrX,scrY], pygame.FULLSCREEN)
		elif fullscreen == False:
			self.screen = pygame.display.set_mode([scrX,scrY])
		self.surfBase = pygame.Surface((768,768))
		self.surfBlink = pygame.Surface((768,768))
		self.surfFixed = pygame.Surface((768,768))
		self.fontSize = 32
		self.fontFace = pygame.font.Font('res/Bedstead.ttf', size)
		self.blink = True
		self.gameClock = pygame.time.Clock()
		self.magazine = []

	def oParity(hx):
		if (int(hx, 16) > 127):
		else:
			return hx

	def blitPage(charList):


	def showPages():
		