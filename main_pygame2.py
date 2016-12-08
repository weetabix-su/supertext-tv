import time
import pygame
import os
import sys
import random
import binascii
import re

pygame.init()

scrX = 720
scrY = 576

screen = pygame.display.set_mode([scrX,scrY])	#, pygame.FULLSCREEN)
surf = pygame.Surface((768,800))
surfBlink = pygame.Surface((768,800))
surfSte = pygame.Surface((768,800))
testcard = pygame.image.load('res/testcard.png').convert()
size = 32
font = pygame.font.Font('res/Bedstead.ttf', size)
keys = pygame.key.get_pressed()
onRun=True
onAir=False
cock = 0
gameClock = pygame.time.Clock()
blink = True

#FUNCTIONS!

# Print only if true
def printBool(str, yes):
	if yes == True:
		print str

runOnce = True

# Returns color tuple according to hex code
def color(hxs):
	col = list(hxs)[1]
	if col == '0':
		return (0,0,0)
	elif col == '1':
		return (255,0,0)
	elif col == '2':
		return (0,255,0)
	elif col == '3':
		return (255,255,0)
	elif col == '4':
		return (0,0,255)
	elif col == '5':
		return (255,0,255)
	elif col == '6':
		return (0,255,255)
	elif col == '7':
		return (255,255,255)
	else:
		printBool(("Invalid color code ("+hxs+") detected! Returning black."), runOnce)
		return (0,0,0)

# Returns XY coordinates configured to 40x24 map
def coords(a, b):
	a = (3 + (a*19))
	b = (3 + (b*32))
	return (a, b)

# Returns streched font render
def x2str(cha, col):
	return pygame.transform.scale(font.render(cha, False, col), (19, 64))
	
# Blits hex characters to screen
def blitChar(cha, xy, cBG, cFG, blink=False, dBG=False, dFG=False):
	if dBG == False:
		pygame.draw.rect(surfSte, cBG, pygame.Rect(xy, (19, 32)))
		pygame.draw.rect(surfBlink, cBG, pygame.Rect(xy, (19, 32)))
	elif dBG == True:
		pygame.draw.rect(surfSte, cBG, pygame.Rect(xy, (19, 64)))
		pygame.draw.rect(surfBlink, cBG, pygame.Rect(xy, (19, 64)))
	if blink == False:
		if dFG == False:
			surfSte.blit(font.render(cha, False, cFG), xy)
			surfBlink.blit(font.render(cha, False, cFG), xy)
		elif dFG == True:
			surfSte.blit(x2str(cha, cFG), xy)
			surfBlink.blit(x2str(cha, cFG), xy)
	elif blink == True:
		if dFG == False:
			surfBlink.blit(font.render(cha, False, cFG), xy)
		if dFG == True:
			surfBlink.blit(x2str(cha, cFG), xy)

def gPos(inc, xy, sep=False, dub=False):
	xPlus = 0
	yPlus = 0
	if sep == True:
		xPlus += 1
		yPlus += 1
	if inc % 2 == 0:
		xPlus += 10
	if inc < 2:
		yPlus += 11
	if inc < 4:
		yPlus += 11
	if dub == True:
		yPlus = yPlus * 2
	printBool((xy[0]+xPlus, xy[1]+yPlus), runOnce)
	return (xy[0]+xPlus, xy[1]+yPlus)
			
def blitG(cha, xy, cBG, cFG, sep=False, blink=False, dBG=False, dFG=False):
	printBool("cha: " + cha, runOnce)
	chu = int(cha, 16) - 32
	if chu > int('3f', 16):
		chu = chu - 32
	printBool("chu: " + str(chu), runOnce)
	switch = list(str(bin(chu)[2:].zfill(6)))
	printBool(switch, runOnce)
	if dBG == False:
		pygame.draw.rect(surfSte, cBG, pygame.Rect(xy, (19, 32)))
		pygame.draw.rect(surfBlink, cBG, pygame.Rect(xy, (19, 32)))
	elif dBG == True:
		pygame.draw.rect(surfSte, cBG, pygame.Rect(xy, (19, 64)))
		pygame.draw.rect(surfBlink, cBG, pygame.Rect(xy, (19, 64)))
	cnt = 0
	for sw in switch:
		sw = int(sw)
		xs = 10
		ys = 11
		if cnt < 2:
			ys = 10
		if cnt % 2 == 0:
			xs = 9
		if sep == True:
			xs -= 2
			ys -= 2
		if dFG == True:
			ys = ys * 2
		if sw == 1:
			if blink == False:
				pygame.draw.rect(surfSte, cFG, pygame.Rect(gPos(cnt, xy, sep, dFG), (xs, ys)))
				pygame.draw.rect(surfBlink, cFG, pygame.Rect(gPos(cnt, xy, sep, dFG), (xs, ys)))
			elif blink == True:
				pygame.draw.rect(surfBlink, cFG, pygame.Rect(gPos(cnt, xy, sep, dFG), (xs, ys)))
		cnt += 1
		
# Parity checking
def oParity(hx, runOnce):
	if (int(hx, 16) > 127):
		printBool("Parity byte may have been detected.", runOnce)
		switch = list(str(bin(int(hx, 16))[2:].zfill(8)))
		printBool(switch, runOnce)
		parity = int(switch[0])
		pCh = 0
		for x in switch:
			pCh += int(x)
		pCh -= parity
		printBool(str(pCh), runOnce)
		if pCh % 2 != parity:
			printBool("Parity check passed! It is ODD.", runOnce)
			switch.pop(0)
			return format(int("".join(switch), 2), 'x').zfill(2)
		else:
			printBool("Parity check passed! It is EVEN.", runOnce)
			switch.pop(0)
			return format(int("".join(switch), 2), 'x').zfill(2)
	else:
		return hx

# Blits TTV file to surface
def ttvBlit(file):
	printBool(("Opening TTV file: " + file), runOnce)
	with open(file, 'rb') as f:
		cont = f.read()
	hx = re.compile('(..)').findall(binascii.hexlify(cont))
	dSkip = False
	rangeLim = 25
	if len(hx) < 1000:
		rangeLim = 24
	for c in range(0,rangeLim):
		bg = color('00')
		fg = color('07')
		blinker = False
		s2 = False
		gMode = False
		gSep = False
		if dSkip == True:
			dSkip = False
		elif dSkip == False:
			for d in range(0, 40):
				printBool("[POSITION "+str(d)+","+str(c)+"]", runOnce)
				cha = ' '
				char = hx[(40*c)+d]
				chee = oParity(char, runOnce)
				if chee == False:
					break
				else:
					char = chee
				if char == '00' or char == '01' or char == '02' or char == '03' or char == '04' or char == '05' or char == '06' or char == '07':
					gMode = False
					fg = color(char)
				elif char == '08':
					blinker = True
				elif char == '09':
					blinker = False
				elif char == '0c':
					s2 = False
				elif char == '0d':
					if c > 0:
						s2 = True
						if dSkip == False:
							dSkip = True
					else:
						printBool("Not permitted to write double text on top row.", runOnce)
				elif char == '10' or char == '11' or char == '12' or char == '13' or char == '14' or char == '15' or char == '16' or char == '17':
					gMode = True
					fg = color(char)
				elif char == '18':
					printBool("Conceal Display code called at ("+str(d)+", "+str(c)+"). SUPERTEXT does not support this code as of this moment.", runOnce)
				elif char == '19':
					if gSep == True:
						gSep = False
				elif char == '1a':
					if gSep == False:
						gSep = True
				elif char == '1c':
					bg = color('00')
				elif char == '1d':
					bg = fg
				elif char == '1e':
					printBool("Hold Graphics code called at ("+str(d)+", "+str(c)+"). SUPERTEXT does not support this code as of this moment.", runOnce)
				elif char == '1f':
					printBool("Release Graphics code called at ("+str(d)+", "+str(c)+"). SUPERTEXT does not support this code as of this moment.", runOnce)
				else:
					printBool("Code called: "+char, runOnce)
					cha = binascii.unhexlify(char)
				if gMode == False:
					blitChar(cha, coords(d, c), bg, fg, blinker, dSkip, s2)
				elif gMode == True:
					if ((int(char, 16) > int('0x20', 0) and int(char, 16) < int('0x40', 0)) or (int(char, 16) > int('0x5F', 0) and int(char, 16) < int('0x80', 0))):
						blitG(char, coords(d,c), bg, fg, gSep, blinker, dSkip, s2)
					else:
						blitChar(cha, coords(d, c), bg, fg, blinker, dSkip, s2)		

pygame.mixer.music.load('res/jazz.ogg')
pygame.time.delay(4000)
pygame.mixer.music.play(-1)
while onRun:
	surf.fill((0,0,0))
	ttvBlit('pages/tsty.ttv')
	if blink == True:
		surf.blit(surfBlink, (0,0))
		blink = False
	elif blink == False:
		surf.blit(surfSte, (0,0))
		blink = True
	pygame.draw.rect(surf, (0,0,0), pygame.Rect(coords(0, 0), (19*40, 32)))
	#pygame.draw.rect(surf, (0,0,255), pygame.Rect(coords(0, 23), (19*40, 32)))
	surf.blit(font.render(time.strftime("    SUPERTEXT BGC %a %d %b "), False, (255,255,255)), coords(0, 0))
	surf.blit(font.render(time.strftime("%I:%M/%S%p"), False, (255,255,0)), coords(29, 0))
	#surf.blit(font.render("   GREETINGS FROM KAIJU BLUE COUNTRY   ", False, (255,255,255)), coords(0, 23))
	pygame.transform.scale(surf, (scrX,scrY), screen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			onRub = False
	pygame.display.flip()
	if runOnce == True:
		runOnce = False
	gameClock.tick(2)