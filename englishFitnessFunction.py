import warnings
import ssl
from urllib.request import urlopen
import numpy as np
import matplotlib.pyplot as plt

print("~~~~~~~~ stupid ass warnings that wont go away no matter what I try from stack overflow ~~~~~~~~~~")

# get words from the dictionary
f=open('dictionary.txt', 'r')
words = [word.strip() for word in f]
f.close() 

res = urlopen('https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt')
sortedWords = res.read().split()

def getCorrespondingLetter(number):
    return chr(ord('`')+number)

def shiftBy(c, n):
    return chr(((ord(c) - ord('a') + n) % 26) + ord('a'))
	
def sumSquared(freqs):
	sumSquared = 0
	sum = 0
	for key in freqs:
		sum += freqs[key]
		sumSquared += freqs[key]* freqs[key]
	return sum, sumSquared

# nominal in this case would be the normal uni, bi or quadgram frequencies
def sumSqWithNominal(freqs, nominal):
	sumSq = 0.0
	for item in freqs:
		sumSq += freqs[item] * nominal[item]
	return sumSq

def singleCharFreq(lowercaseStr):
	freq = {}
	for ascii in range(ord('a'), ord('a')+26):
		freq[chr(ascii)] = float(lowercaseStr.count(chr(ascii)))/len(lowercaseStr)
	return sortDictionaryDescending(freq)

# how does the length fit in... is it string length or number of bigrams within it? compare to moby dick
def ngramFreq(lowercaseStr, ngramExpected):
	freq ={}
	for ngram in ngramExpected.keys():
		freq[ngram] = float(lowercaseStr.count(ngram))/len(lowercaseStr)
	return sortDictionaryDescending(freq)

def formatLowerCharOnlyStr(text):
	onlyLetters = "".join(filter(str.isalpha, str(text)))
	lowerOnly = onlyLetters.lower()
	return lowerOnly
	
def percentDiff(expected, experimental):
	return ((experimental - expected) / expected) * 100

def getFileText(filename):
	f = open(filename, 'r')
	ftxt = f.read()
	f.close()
	return formatLowerCharOnlyStr(ftxt)

def multiBarChart(title, reference, data1,data2,  data3, data4, data5):
	plt.subplot(2,3,1)
	plt.bar(list(reference.keys()), reference.values())
	plt.title(title)
	
	plt.subplot(2,3,2)
	plt.bar(list(data1.keys()), data1.values())
	plt.title('File 1')

	plt.subplot(2,3,3)
	plt.bar(list(data2.keys()), data2.values())
	plt.title('File 2')
	
	plt.subplot(2,3,4)
	plt.bar(list(data3.keys()), data3.values())
	plt.title('File 3')

	plt.subplot(2,3,5)
	plt.bar(list(data4.keys()), data4.values())
	plt.title('File 4')

	plt.subplot(2,3,6)
	plt.bar(list(data5.keys()), data5.values())
	plt.title('File 5')
	plt.show()

def getSingleCharStats(text):
	singleFreq = singleCharFreq(text)
	singleSum, singleSumSq = sumSquared(singleFreq)
	return singleFreq, singleSum, singleSumSq

def getNgramStats(text, normalNgramFreq):
	freq = ngramFreq(text, normalNgramFreq)
	# TODO: not sure if this is useful since only partial knowledge
	singleSum, singleSumSq = sumSquared(freq)
	return freq

def triLevelScoring(levels,scores, value ):
	score = 0
	if value < levels[0]:
		#print("level0")
		score += scores[0]
	elif value < levels[1]:
		#print("level1")
		score += scores[1]
	elif value < levels[2]:
		#print("level2")
		score += scores[2]
	return score

def scoreFile(text, uniFreq, biFreq, quadFreq):
	score = 0
	# TODO - adjust level scores for bi and quad to be reflective
	# score single letter frequencies 
	u = sumSqWithNominal(uniFreq, unigramFreqs)
	diff = abs(u - sumSqUnigram)
	score += triLevelScoring([0.005, 0.01, 0.015], [300, 200,100], diff)

	# score bigram frequencies 
	u = sumSqWithNominal(biFreq, bigramFreqs)
	diff = abs(u - sumSqBigram)
	score += triLevelScoring([0.005, 0.01, 0.015], [600, 400,300], diff)

	# score quadgram frequencies 
	u = sumSqWithNominal(quadFreq, quadgramFreqs)
	diff = abs(u - sumSqQuadgram)
	score += triLevelScoring([0.005, 0.01, 0.015], [900, 800,700], diff)

	# score words in dictionary
	baseWordValue = 20
	for word in words:
		if len(word) < 3:
			# skip 1 and 2 letter words because they could just happen in ciphered text and be misleading
			continue
		#score component per word is based on a base value for any found word and then an 
		#additional component based on the length of the word. Additional component is an
		#exponential of 2 because each additional letter in the word increases the complexity
		#significantly and wanted that at least somewhat represented in the score
		score += text.count(word) * (baseWordValue + (2**(len(word)-2)))
	return score

def scoreFileForTopN(text, uniFreq, biFreq, quadFreq,n):
	score = 0
	# TODO - adjust level scores for bi and quad to be reflective
	# score single letter frequencies 
	u = sumSqWithNominal(uniFreq, unigramFreqs)
	diff = abs(u - sumSqUnigram)
	score += triLevelScoring([0.005, 0.01, 0.015], [300, 200,100], diff)

	# score bigram frequencies 
	u = sumSqWithNominal(biFreq, bigramFreqs)
	diff = abs(u - sumSqBigram)
	score += triLevelScoring([0.005, 0.01, 0.015], [600, 400,300], diff)

	# score quadgram frequencies 
	u = sumSqWithNominal(quadFreq, quadgramFreqs)
	diff = abs(u - sumSqQuadgram)
	score += triLevelScoring([0.005, 0.01, 0.015], [900, 800,700], diff)

	# score words in dictionary
	baseWordValue = 20
	for word in sortedWords[:n]:
		word = word.decode("utf-8")
		score += text.count(word) * (baseWordValue + (2**(len(word))))
	return score


def sortDictionaryDescending(dictionary):
	sortedDict = {}
	for key, value in sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True):
		sortedDict[key] =value
	return sortedDict

def scoreString(string):
	singleFreq, singleSum, singleSumSq = getSingleCharStats(string)
	biFreq = getNgramStats(string, bigramFreqs)
	quadFreq = getNgramStats(string, quadgramFreqs)
	return scoreFile(string, singleFreq, biFreq, quadFreq)

def scoreStringForTopN(string, n):
	singleFreq, singleSum, singleSumSq = getSingleCharStats(string)
	biFreq = getNgramStats(string, bigramFreqs)
	quadFreq = getNgramStats(string, quadgramFreqs)
	return scoreFileForTopN(string, singleFreq, biFreq, quadFreq, n)

unigramFreqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
sumUnigram, sumSqUnigram = sumSquared(unigramFreqs)

# bigrams, quadgrams from https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html
# sum and sum squared will not be crazy useful most likely since it is only top 20 of each,
#Test run with moby dick gave us bigram sum of 0.25, sum sq of 0.003952. THese frequencies gave sum of .322 and sq of 0.00669
# moby dick quadgram gave us sum of 0.024917, squared of 4.49e-5.  These frequencies gave a sum of 0.06932, and square of 2.83e-4

bigramFreqs = { 'th': 0.03882543, 'he': 0.03681391, 'in': 0.02283899, 'er': 0.02178042, 'an': 0.02140460, 're': 0.01749394, 'nd':0.01571977, 'on': 0.01418244, 'en':0.01383239, 'at':0.01335523, 'ou':0.012854854, 'ed':0.01275779, 'ha':0.01274742, 'to':0.01169655, 'or':0.01151094, 'it':0.0134891, 'is':0.01109877, 'hi': 0.01092302, 'ed':0.01092301, 'ng':0.01053385}
sumBigram, sumSqBigram = sumSquared(bigramFreqs)

quadgramFreqs = {'that':0.00761242, 'ther':0.00604501, 'with':0.00573866, 'tion':0.00551919, 'here':0.00374549, 'ould':0.00369920, 'ight':0.00309440, 'have':0.00290544, 'hich': 0.00284292, 'whic':0.00283826, 'this': 0.00276333, 'thin':0.00270413, 'they':0.00262421, 'atio': 0.00262386, 'ever':0.00260695, 'from':0.00258580, 'ough':0.00253447, 'were':0.00231089, 'hing':0.00229944, 'ment':0.00223347}
sumQuadgram, sumSqQuadgram = sumSquared(quadgramFreqs)
# should we include most common words? http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/


#response =urlopen("https://vip.udel.edu/crypto/mobydick.txt", context=ssl._create_unverified_context())
#mobytext = response.read()

#lowerOnly = formatLowerCharOnlyStr(mobytext)
#singleFreq = singleCharFreq(lowerOnly)
#singleSum, singleSumSq = sumSquared(singleFreq)
#print(singleSumSq)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#biFreq = ngramFreq(lowerOnly, bigramFreqs)
#biSum, biSumSq = sumSquared(biFreq)
#print(biFreq)

#print(biSum, biSumSq)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#quadFreq = ngramFreq(lowerOnly, quadgramFreqs)
#quadSum, quadSumSq = sumSquared(quadFreq)
#print(quadFreq)
#print(quadSum, quadSumSq)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#bitestsum, bitestsq = sumSquared(bigramFreqs)
#print(bitestsum, bitestsq)
#qtestsum, qtestsq = sumSquared(quadgramFreqs)
#print(qtestsum, qtestsq) 

#data ={}
#data["moby"] = singleFreq
#multiBarChart('single',unigramFreqs,singleFreq , singleFreq, singleFreq, singleFreq, singleFreq ) 
