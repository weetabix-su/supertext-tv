# Import declarations
import time
import pygame
import os
import sys
import random
import binascii
import re

class Settings:
	# branding, only 16 characters
	self.name = "SUPERTEXT"
	# screen height and width
	self.screenHeight = 720
	self.screenWidth = 576
	# fullscreen ignores screen height and width
	self.fullScreen = True
	# forces letterboxing on non-4:3 displays when fullscreen
	self.letterBox = False
	# sets screen to display only 24 rows, [false] sets it to 25
	self.lessRows = False
	# sets font (located in [res])
	self.fontFace = 'Bedstead.ttf'
	# sets font size
	self.fontSize = 32
	# alphabet for Page class base64 parser
	self.index64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'

class Display:
	def __init__(self):
		pygame.init()
		if Settings.fullScreen == False:
			self.screen = pygame.display.set_mode([Settings.screenHeight, Settings.screenWidth])
		else:
			if Settings.letterBox == False:
				self.screen = pygame.display.set_mode([pygame.display.Info().current_w, pygame.display.Info().current_h], pygame.FULLSCREEN)
			else:
				if ((pygame.display.Info().current_w / 4) >= (pygame.display.Info().current_h / 3)):
					self.screen = pygame.display.set_mode([((pygame.display.Info().current_h/3)*4), pygame.display.Info().current_h], pygame.FULLSCREEN)
				else:
					self.screen = pygame.display.set_mode([pygame.display.Info().current_w, ((pygame.display.Info().current_w/4)*3)], pygame.FULLSCREEN)
		if Settings.lessRows:
			self.surfaceBase = pygame.Surface((768,768))
			self.surfaceBlink = pygame.Surface((768,768))
			self.surfaceFixed = pygame.Surface((768,768))
		else:
			self.surfaceBase = pygame.Surface((768,800))
			self.surfaceBlink = pygame.Surface((768,800))
			self.surfaceFixed = pygame.Surface((768,800))
		self.font = pygame.font.Font(('res/' + Settings.fontFace), Settings.fontSize)
		self.clock = pygame.time.Clock()
		self.blink = True

class Page:
	def __init__(self):
		# charlist defaults to 25 even if Settings.lessRows is enabled
		self.charList = ['00'] * (40*25)

	def parseTTV(file):
		with open(file, 'rb') as f:
			cont = f.read()
		hx = re.compile('(..)').findall(binascii.hexlify(cont))
		for x in range(0, 1000):
			charList[x] = hx[x]

	def parseB64(data):
		for r in range(0,len(data)):
			try:
				val = index64.index(data[r])
			except ValueError:
				print ("ERROR: Character at position " + r + " should be one from the base64 alphabet!")
			else:
				for b in range(0,6):
					bit = val & (1<<(5-b))
					if bit > 0:
						cbit = (r*6) + b
						cpos = cbit % 7
						cloc = (cbit-cpos)/7
						ctrip = int(hx[cloc], 16) | 1 << (6-cpos)
						charList[cloc] = format(ctrip, 'x').zfill(2)