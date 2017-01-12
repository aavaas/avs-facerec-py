import json
import speech
import urllib2

devicelisturi ="http://localhost/deviceslist.htm"
response = urllib2.urlopen(devicelisturi);

data = response.read()
data =data.strip()
data =data.split("-")
devices ={}
for str in data:
	new= str.split("_")
	devices[new[0]]= new[1]
print devices

command = [
	["batti baala" , "Lamp", "on" ],
	["Batti baala" , "Lamp", "on" ],
	["Batti nivau" , "Lamp", "off"],
	["batti nivau" , "Lamp", "off"],
	["TV khola" , "TV", "on"],
	["tv khola", "TV", "on"],
	["TV nivau" , "TV", "off"],
	["tv nivau", "TV", "off"],
	#["pankha khola", "Fridge", "on"] 
	]



	
ctrluri ="http://192.168.43.151:8001/sync/"
def response(phrase, listener):	
	#print("You said %s" % phrase)
	if phrase == "turn off":
		listener.stoplistening()
		return
		
	if phrase.upper() == "AAJAKO TAPKRAM":		
		# response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Kathmandu')
		# data_string = response.read()
		# decoded = json.loads(data_string)
		# str=decoded['main']['temp']-273.15

		print str, "degree celsius"
		speech.say("The Current Temperature is 24 degree celsius") # str)
		
	if phrase.upper() == "URJA BACHAT SURU":
		print "Urja bachat suru initiated"
		speech.say("safe mode initiated")
		response = urllib2.urlopen("http://192.168.43.151:8001/sync/invertermode");
	
	for id in range(len(command)):
		print phrase.upper() , command[id][0].upper()
		if (phrase.upper() == command[id][0].upper()):
			print ("initiated "+ command[id][0])
			speech.say("command initiated %s" % command[id][1]+command[id][2])
			urllib2.urlopen(ctrluri+command[id][2]+"/"+devices[command[id][1]]);
			print (ctrluri+command[id][2]+"/"+devices[command[id][1]]);
			break
	
voice = [x[0] for x in command]
voice.append('turn off')
voice.append('aajako tapkram')
voice.append('urja bachat suru')
voice.append('Urja bachat suru')

print voice
listener = speech.listenfor(voice,response)

# response() will be called on a seOther parate thread happens over and over until listener hasn't been stopped.
import time
while listener.islistening():
	time.sleep(1)
	print "Listning..."