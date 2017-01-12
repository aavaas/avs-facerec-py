import urllib2

uri ="http://localhost/deviceslist.htm"

response = urllib2.urlopen(uri);
data = response.read()
data =data.strip()
data =data.split("-")
devices ={}
for str in data:
	new= str.split("_")
	devices[new[0]]= new[1]
print devices

command = [
	["batti bala" , "Lamp" ],
	["TV khola" , "TV" ],
	["Fridge khola", "Fridge"] 
	]

ctrluri ="/sync/"

print (ctrluri+"on"+"/"+devices[command[0][1]]);