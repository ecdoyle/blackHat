import ssl
import urllib.error
from urllib.request import urlopen
import itertools
from englishFitnessFunction import scoreString, shiftBy, getFileText, unigramFreqs

def sortDictionaryDescending(dictionary):
	sortedDict = {}
	for key, value in sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True):
		sortedDict[key] =value
	return sortedDict

def createDecoderDict(sortedFrequencies, sortedNormalFrequencies):
	sortedKeys = list(sortedFrequencies.keys())
	normalKeys = list(sortedNormalFreq.keys())
	decoderDict = dict(zip(sortedKeys, normalKeys))
	#print(decoderDict)
	return decoderDict, sortedKeys

def decodeTextForFirstNChars(text, decoderDict, nChars, sortedKeys):	
	decoded = ''
	for char in text:
		if sortedKeys.index(char) < nChars:
			decoded += decoderDict[char]
		else:
			decoded += "_"
	print(decoded)
	return decoded

def decodeTextNChars(text, decoderDict, sortedKeys):	
	decoded = ''
	for char in text:
		if char in sortedKeys:
			decoded += decoderDict[char]
		else:
			decoded += "_"
	#print(decoded)
	return decoded

def decodeTextAll(text, decoderDict):
	return decodeTextForFirstNChars(text, decoderDict, 26)

loweronly = getFileText('blackhat2')
frequency = {}
encryptedList = list(loweronly)

for ascii in range(ord('a'), ord('a')+26):
	frequency[chr(ascii)] = float(encryptedList.count(chr(ascii)))/len(loweronly)

sum_freqs_squared = 0.0
for ltr in frequency:
	sum_freqs_squared += frequency[ltr]*frequency[ltr]

#print("Sum Square will be near .065: " + str(sum_freqs_squared))

sortedFrequencies = sortDictionaryDescending(frequency)
#print(sortedFrequencies)
sortedNormalFreq = sortDictionaryDescending(unigramFreqs)
#print(sortedNormalFreq)

scoreCutoff = 3245

sortedNormFreqKeys = list(sortedNormalFreq.keys())
sortedNormFreqVals = list(sortedNormalFreq.values())
sortedFreqVals = list(sortedFrequencies.values())
sortedFreqKeys = list(sortedFrequencies.keys())

""" 
# Original idea: go through and find what characters are a tolerance away from
# the expected normal character frequenices, and create combinations to serve as
# decode options. This didnt work out so hot. I mean it gave me options but nothing
# that resembled english that much. Kept increasing the tolerance which increased
# the option space and was just not getting the most useful output.
options = []
l = []

tolerance = 20 # percentage
threshold = 8 # number of letters to substitute in

for k in range(len(sortedFrequencies)):
	l =list(x for x in sortedNormFreqKeys if  abs(sortedNormalFreq[x] - sortedFreqVals[k]) <= ((tolerance /100)* sortedNormalFreq[x]) )
	options.append(l)

#possible subs has key of sorted frequencies from cipher text, and options for what it mightbe in the normal frequencies based on tolerance
possibleSubs = {}
possibleSubs = dict(zip(sortedFreqKeys, options))
#print(possibleSubs)

possibleOptions =list(itertools.product(*list(possibleSubs.values())[:threshold]))
# remove any with duplicates
uniqueOptions = []
for item in possibleOptions:
	if len(item) == len(set(item)):
		uniqueOptions.append(item)

print(len(uniqueOptions)) #," ~~~", uniqueOptions)

for option in uniqueOptions:
	decoderDict = {}
	sortedKeys = sortedFreqKeys
	decoderDict = dict(zip(sortedKeys[:threshold], option))
	#print("DD: ", decoderDict)
	#print(option)
	#decoderDict, sortedKeys = createDecoderDict(sortedFrequencies, sortedNormalFreq)
	decoded = decodeTextNChars(loweronly, decoderDict, sortedKeys[:threshold])
	#print(decoded[-19:])
	score = scoreString(decoded)
	if score > scoreCutoff:
		print("Score: ", score, ",Text: ", decoded)
 
"""
 # New idea: Just take top n number of most frequent letters of cipher and regular alphabet
 # and find all the combos of them. There seem to be a cluster of 15-20 letters all from
 # them at the end of the message so lets try to crack that first.
n = 8
nTopCip = sortedFreqKeys[:n]
nTopNorm = sortedNormFreqKeys[:n]
       
# find permutations	   
perms = itertools.permutations(nTopCip)

# May wish to commenting out if running, so doesnt bog down over and over, but this was the code that I used
for perm in list(perms):
	decoderDict = dict(zip(list(perm), nTopNorm))
	#print(decoderDict)
	decoded = decodeTextNChars(loweronly, decoderDict, nTopCip)
	#print(decoded[-19:])
	score = scoreString(decoded)
	if score > scoreCutoff:
		print(decoderDict)
		print("Score: ", score, ",Text: ", decoded)

# I can see what looks like too sustained, too concentrated or too direct  reserving
res = {'a': 'e', 'b': 't', 'f': 'a', 'w': 'o', 'q': 'n', 'p': 'i', 'x': 's', 'k': 'r'}

# Guessed these based on what looked like too sustained, too concentrated or too direct
initialSuspect = {'t' : 'c', 'c' : 'u', 'y': 'g', 'd':'v', 'v':'d'}
# other educated guesses 
secondarySuspect = { 'i':'j', 'l':'m', 'o':'f', 'r':'h', 'u':'p', 'y': 'y'}

decoderDict ={'h':'q', 'n':'w', 's':'z','g':'x','e':'l', 'j':'b','z':'k', 'a': 'e', 'b': 't', 'f': 'a', 'w': 'o', 'q': 'n', 'p': 'i', 'x': 's', 'k': 'r','t' : 'c', 'c' : 'u', 'm': 'g', 'd':'v', 'v': 'd', 'i':'j', 'l':'m', 'o':'f', 'r':'h', 'u':'p', 'y':'y'} 

decoded = decodeTextNChars(loweronly, decoderDict, decoderDict.keys())
score = scoreString(decoded)
print("OG: ", loweronly)
print("Score: ", score, ",Text: ", decoded)
""" Output:
Score:  21466 ,Text:  reservingjudgmentsisamatterofinfinitehope
allotherswindlersuponeartharenothingtotheselfswindlersandwithsuchpretencesdidicheatmyselfsurelyacuriousthingthatishouldinnocentlytakeabadhalfcrownofsomebodyelsesmanufactureisreasonableenoughbutthatishouldknowinglyreckonthespuriouscoinofmyownmakeasgoodmoney
discontentisthefirststepintheprogressofamanoranation
itisintheuncompromisingnesswithwhichdogmaisheldandnotinthedogmaorwantofdogmathatthedangerlies
byundueprofundityweperplexandenfeeblethoughtanditispossibletomakeevenvenusherselfvanishfromthefirmanentbyascrutinytoosustainedtooconcentratedortoodirect
"""
# So we got:
# The Great Gatsby - "Reserving judgment is a matter of infinite hope"
# Great Expectations - "All other swindlers upon earth are nothing to the self-swindlers, and with such pretences did I cheat myself. Surely a curious thing. That I should innocently take a bad half-crown of somebody else's manufacture, is reasonable enough; but that I should knowingly reckon the spurious coin of my own make, as good money!”
# Oscar Wilde - “Discontent is the first step in the progress of a man or a nation.”
# Samuel Butler -"It is in the uncompromisingness with which dogma is held and not in the dogma, or want of dogma, that the danger lies"
# Edgar Allen Poe - "By undue profundity, we perplex and enfeeble thought; and it is possible to make even Venus herself vanish from the firmament by a scrutiny too sustained, too concentrated, or too direct."
