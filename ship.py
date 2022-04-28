from microbit import *
import machine
import random
import radio

radio.on()

ml = \
[0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, \
4, 0, 0, 4, 4, \
0, 0, 0, 0, 0, \
0, 0, 0, 0, 0]

send = ["0", "0", "0", "0", "0", \
"0", "0", "0"]

p = 2

def handshake():
	string = tostring(ml)
	output(string)
	status = "a"
	sleep(100)
	while True:
		if button_a.was_pressed():
			singleplayer()
		if status == "a" and button_b.was_pressed():
			radio.send("b")
			display.set_pixel(3,2,9)
			display.set_pixel(4,2,9)
			while True:
				if radio.receive() == "c":
					return 7
				if button_a.was_pressed():
					singleplayer()
				sleep(100)
		if radio.receive() == "b":
			display.set_pixel(3,2,9)
			display.set_pixel(4,2,9)
			status = "b"
		if status == "b" and button_b.was_pressed():
			radio.send("c")
			return 8

def move_x_to_pos():
	reading = accelerometer.get_x()
	if reading <= -150:
		return 0
	elif reading >= -149 and reading <= -50:
		return 1
	elif reading > -49 and reading < 50:
		return 2
	elif reading >= 50 and reading < 150:
		return 3
	elif reading >= 150:
		return 4
	else:
		return 3

def tostring(m):
	i = 0
	frame = ""
	for x in m:
		if i == 4 or i == 9 or i == 14 or i == 19:
			frame = frame + str(x) + ":"
		else:
			frame = frame + str(x)	
		i = i + 1
	return frame

def output(fr):
	output = Image(fr)
	display.show(output)

def twoplayer(UP):
	p = 3
	recv = "00000000"
	sleep(150)
	countermax = 8
	ammo = 2
	counter = 0
	while True:
		sendstring = "".join(send)
		radio.send(sendstring)
		po = p
		if counter == countermax and ammo < 2:
			ammo += 1
		if recv is None:
			recv = "00000000"
		if recv[5] == "9":
			display.show(Image.YES)
			sleep(2000)
			machine.reset()
		for x in range(0,5):
			if x < ammo:
				ml[x+20] = 1
			else:
				ml[x+20] = 0
		for x in range(0,5):
			if ml[x] != 4:
				send[x] = "0"
			if ml[x] == 4:
				send[x] = "1"
				ml[x] = 0
		for x in range(0,5):
			if ml[x+5] == 4:
				ml[x] = 4
				ml[x+5] = 0
		for x in range(5,10):
			if ml[x+5] == 4:
				ml[x] = 4
				ml[x+5] = 0
		for x in range(10,15):
			if ml[x+5] == 4:
				ml[x] = 4
				ml[x+5] = 0
		for x in range(25,30):
			if ml[x-5] == 8:
				ml[x-5] = 0
		for x in range(20,25):
			if ml[x-5] == 8:
				ml[x] = 8
				ml[x-5] = 0
			if ml[x] == 8 and p+20 == x:
				display.show(Image.NO)
				send[5] = "9"
				sendstring = "".join(send)
				radio.send(sendstring)
				sleep(2000)
				machine.reset()
		for x in range(15,20):
			if ml[x-5] == 8:
				ml[x] = 8
				ml[x-5] = 0
		for x in range(10,15):
			if ml[x-5] == 8:
				ml[x] = 8
				ml[x-5] = 0
		for x in range(5,10):
			if ml[x-5] == 8:
				ml[x] = 8
				ml[x-5] = 0
		for x in range(0,5):
			if recv[x] == "1":
				ml[4-x] = 8
		if button_b.was_pressed() and ammo > 0:
			ml[p+15] = 4
			ammo -= 1
		p = move_x_to_pos()
		ml[20+p] = 9
		if po != p:
			ml[20+po] = 0
		string = tostring(ml)
		output(string)
		if counter <= countermax:
			counter += 1
		else:
			counter = 0
		sleep(30)
		recv = radio.receive()

player = handshake()
for x in range(10,15):
	ml[x] = 0
twoplayer(player)
