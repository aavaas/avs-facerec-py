import json
import urllib2
import speech

response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Kathmandu')
data_string = response.read()
decoded = json.loads(data_string)
str=decoded['main']['temp']-273.15


print str, "degree celsius"
speech.say("The Current Temperature is %s degree celsius" % str)


#for nepali
# nep=['०','१','२','३','४','५','६','७','८','९']
# finalStr=""
# for a in str(strr):
	# if(a=='.'):
		# finalStr+='.'
	# else:
		# finalStr+=nep[int(a)]
# finalStr=strr
# f=open('test.txt','w')
# f.write(finalStr)

