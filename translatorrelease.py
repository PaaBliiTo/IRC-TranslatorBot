import sys
import time
import socket
import ssl
from textblob import TextBlob

server = ""
sslStr = ""
public = ""
port = 6667
botnick="translator"
channel=""
channelpwd=""
botpwd=""
username=""
inputLang=""
outputLang=""

def connectServ(server, port, sslStr):
	connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connexion.connect((server, port))
	if(sslStr=="y"):
		try:
			connexionssl = ssl.wrap_socket(connexion)
			return connexionssl
		except Exception as e:
			print("Impossible to connect to the server ! Check if you really need a SSL certificate");
	else:
		return connexion

def connectChan(irc):
	irc.setblocking(False)
	time.sleep(1)
	irc.send("USER "+botnick+" "+botnick+" "+botnick+" :Let's Translate !\r\n")
	time.sleep(1)
	irc.send("NICK "+botnick+"\r\n")
	if(botpwd!=""):
		time.sleep(2)
		irc.send("PRIVMSG NickServ :IDENTIFY "+botpwd+"\r\n")
	
	time.sleep(1)

	if(channelpwd!=""):
		irc.send("JOIN "+channel+" "+channelpwd+"\r\n")
	else:
		irc.send("JOIN "+channel+"\r\n")



while server=="":
	server = raw_input("\nUrl of the irc server : ")
	if(server==""):
		print("Can't be blank !")

while 1:
	try:
		port = raw_input("\nPort (leave blank for default 6667) : ")
		if(port == ""):
			port = 6667
			break
		port = int(port)
		break
	except Exception as e:
		print("Please enter an integer or leave blank")

botnick = raw_input("\nUsername of the bot (leave blank for default translator) : ")
if(botnick==""):
	botnick = "translator"

botpwd = raw_input("\nPassword of the bot's username (leave blank if it has none) : ")

print("\nDo you want the translations to be public ?")
print("Yes => translations are sent in the channel (better if more than one people need the translation)")
print("No => translations are sent only to a specific username (better for not spamming the channel)")

while 1:
	public = raw_input("(y/n) : ").lower()
	if(public != "y" and public != "n"):
		print("Please select y/n")
	else:
		break

if(public == "n"):
	while username=="":
		username = raw_input("\nThe username to whom the bot will send the translations : ")
		if(username == ""):
			print("Can't be blank !")

print("\nDo you need a SSL certificate to access your server ?")
while 1:
	sslStr = raw_input("(y/n) : ").lower()
	if(sslStr != "y" and sslStr != "n"):
		print("Please select y/n")
	else:
		break

print("\nFor the languages, type the language code (for example, en for English, fr for French, de for German etc.)")
print("Be careful : there is no verification of the language code. If you miswritten it, the translator might not work")
while (inputLang == ""):
	inputLang = raw_input("The language you want to translate (the incoming message) : ")
	if(inputLang==""):
		print("Can't be blank !")
while (outputLang == ""):
	outputLang = raw_input("The language you want as output : ")
	if(outputLang==""):
		print("Can't be blank !")

while (channel == ""):
	channel = raw_input("The channel you want your bot to join : ")
	if(channel == ""):
		print("Can't be blank !")

channelpwd = raw_input("The password of your channel (leave blank if none) : ")

irc = connectServ(server, port, sslStr)

connectChan(irc)

print("\nConnected to the server !")

once = True

while 1:

	text=""
	blob = None

	time.sleep(0.3)

	try:
		text=irc.recv(2040)
		textOriginal = text

		if(once):
			print("Connected to the channel !")
			once = False
		
		sender = text.split(':')[1].split('!')[0].upper()

		chunk = text.split(' ')

		indexColumn = text.find(":", 1)
		text = text[indexColumn+1:]

		if textOriginal.find('PING') != -1:
			irc.send("PONG\r\n")

		blob = TextBlob(text)

		if blob.detect_language() == inputLang:
			if(username!=""):
				message = "NOTICE "+username+" :"+sender+": "+str(blob.translate(to=outputLang))+"\r\n"
			else:
				message = "PRIVMSG "+channel+" :"+sender+": "+str(blob.translate(to=outputLang))+"\r\n"
			irc.send(message)
			time.sleep(0.1)

	except Exception:
		pass