import time
import pygame
import os
import sys
import random
import binascii
import re

pygame.init()

scrX = pygame.display.Info().current_w
scrY = pygame.display.Info().current_h

# Insert base64 teletext string here
super64 = 'BQt-_Xtw8taDpo080HDDnyoOm9Bzw9sqDzv68kHffy1oECAo4cOHCAl4KKHDhw4cOHDhw4cOHDhw4cOHDhw4cOHDhw4cOCn79-JKH69IUXbnyZEq_fv379-_fv379-_fv379-_fv379-Kf__96T0f1hLwgI-P_Qor3________________________8ovXryWTwsXJyPj9____rAovXr169evXr169evXr169evXryvx4RwfPn7__fp1e____pSvz58-fPnz58-fPnz58-fPnz58KtyPj___r05Ph86Ed_9iVXL16_-vXr169ev___________8pwI736cns-f____1Ir_7wt__tUGr_q_6v5TgV__0Hz58KcCn_6wJrvvLf_____96sKfC39GhQav-Lnq_lN5X__Qf__8p_Kf_5NctJ7______rViwp_Lf_7X9__6v-r__QFf_9B_alFn8p__l9_sn6____9A-XrSn8t_QIP6D_q_6v5dYV__0H___Kfyn_-9J8PH_____y-zu_Kfy3_-1___-r_q__yqD__Qf2pTh_Kf_5P8vT4eH7ur28OHgp_Lf_7Vfv_6v6r__KoP_9B_alP_8p__k9_dmjVr163oyV_yn_hw4EfRThw4cOHDh04cOHDhw__yqxYkJq__zgR2vSfv-lKqFixIRalVCxYsWLFixYsWLFixYsKIECAv0Jo1__58_P05RAgQICOpCgB1IsyLUi2KiBAgQIECAogQF1X_-9WLMHxgUQIC6BAgItySAGgixJNSfSQIECBAgQICqwv4a7_5L99L__6rpw-fyf9p8KrFixYsWLFixYsWLFixYsKF_X_-yTkv78v__tWX___J_Wm8oa-fPnz58-fPnz58-fPnwvo_6v_9uS-F9rJfoaol-8mvRlPBr__________________y65KuXryS5etLr169eUWLFixYvXml69evXr169evXr169evInSaQHQ5ZefNBFpw0CtBaB9N6DHsy4eSDpo080HPHyy5dyAidJpAdDll580EWnDQK0D8Hm38kHTRlQaMuzgg54-WXLuQICJ0ukDwuufmgw7siDll49cvPpzQd8uzHv25ciDD0dIECBAgInS6APo6dOHN0vX59PTR1xLse_av5Ye-zLzX5cmnot6ZkCA'

# Branding
name = '*NEW* SUPERTEXT'

screen = pygame.display.set_mode([scrX,scrY], pygame.FULLSCREEN)
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

# RFC4648-compliant base64 index
index64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'

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
			xs -= 3
			ys -= 3
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
# Added parameter to render base64 teletext strings
def textBlit(data, type=0):
	# Type 0: TTV file input
	# Type 1: base64 string input
	rangeLim = 25
	if type == 0:
		printBool(("Opening TTV file: " + data), runOnce)
		with open(data, 'rb') as f:
			cont = f.read()
		hx = re.compile('(..)').findall(binascii.hexlify(cont))
		if len(hx) < 1000:
			rangeLim = 24
	# Special thanks to Mr Rawles for the url2raw.pl at https://github.com/rawles/edit-tf
	elif type == 1:
		printBool("Parsing base64 string...", runOnce)
		if len(data) == 1120:
			rangeLim = 24
		hx = []
		for s in range(0,(40*rangeLim)):
			hx.append('00')
		for r in range(0,len(data)):
			try:
				val = index64.index(data[r])
			except ValueError:
				printBool(("ERROR: Character at position " + r + " should be one from the base64 alphabet!"), runOnce)
			else:
				printBool(("NOW EXAMINING " + data[r] + " (value is " + str(val) + ")"), runOnce)
				for b in range(0,6):
					bit = val & (1<<(5-b))
					if bit > 0:
						cbit = (r*6) + b
						printBool(("cbit set to " + str(cbit)), runOnce)
						cpos = cbit % 7
						printBool(("cpos set to " + str(cpos)), runOnce)
						cloc = (cbit-cpos)/7
						printBool(("cloc set to " + str(cloc)), runOnce)
						ctrip = int(hx[cloc], 16) | 1 << (6-cpos)
						hx[cloc] = format(ctrip, 'x').zfill(2)
						printBool(("hx["+str(cloc)+"] changed to " + hx[cloc]), runOnce)
			printBool("===NEXT===", runOnce)
		printBool(("hx output:"), runOnce)
		for z in range(0,len(hx)):
			printBool(hx[z], runOnce)
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

pygame.mixer.music.load('bgm/jazz.ogg')
pygame.time.delay(500)
pygame.mixer.music.play(-1)
while onRun:
	surf.fill((0,0,0))
	textBlit(super64, 1)
	if blink == True:
		surf.blit(surfBlink, (0,0))
		blink = False
	elif blink == False:
		surf.blit(surfSte, (0,0))
		blink = True
	pygame.draw.rect(surf, (0,0,0), pygame.Rect(coords(0, 0), (19*40, 32)))
	surf.blit(font.render(time.strftime(" " + '{:>16}'.format(name)[:16] + " %a %d %b "), False, (255,255,255)), coords(0, 0))
	surf.blit(font.render(time.strftime("%I:%M/%S%p"), False, (255,255,0)), coords(29, 0))
	pygame.transform.scale(surf, (scrX,scrY), screen)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if (pygame.key.get_pressed()[pygame.K_PAGEUP] != 0 and pygame.mixer.music.get_volume < 1.0):
				pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
			if (pygame.key.get_pressed()[pygame.K_PAGEDOWN] != 0 and pygame.mixer.music.get_volume > 0.0):
				pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
			if (pygame.key.get_pressed()[pygame.K_END] != 0):
				onRun = False
		if event.type == pygame.QUIT:
			onRun = False
	pygame.display.flip()
	if runOnce == True:
		runOnce = False
	gameClock.tick(2)