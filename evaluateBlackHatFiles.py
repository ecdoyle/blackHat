from englishFitnessFunction import *


# BlackHat Files
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
f1txt = getFileText('blackHat1')
#print('File 1: ',f1txt)
f2txt = getFileText('blackHat2')
#print('File 2: ', f2txt)
f3txt = getFileText('blackHat3')
#print('File 2: ', f3txt)
f4txt = getFileText('blackHat4')
#print('File 4: ', f4txt)
f5txt = getFileText('blackHat5')
#print('File 5: ', f5txt)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Single Character Frequencies
f1SingleFreq, f1SingleSum, f1SingleSumSq = getSingleCharStats(f1txt)
f2SingleFreq, f2SingleSum, f2SingleSumSq = getSingleCharStats(f2txt)
f3SingleFreq, f3SingleSum, f3SingleSumSq = getSingleCharStats(f3txt)
f4SingleFreq, f4SingleSum, f4SingleSumSq = getSingleCharStats(f4txt)
f5SingleFreq, f5SingleSum, f5SingleSumSq = getSingleCharStats(f5txt)
multiBarChart('Single Character Frequency', sortDictionaryDescending(unigramFreqs), f1SingleFreq, f2SingleFreq, f3SingleFreq, f4SingleFreq, f5SingleFreq)
# Based off of that it looks like #5 is substitution cipher

# Bigram
f1BiFreq = getNgramStats(f1txt, bigramFreqs)
f2BiFreq = getNgramStats(f2txt, bigramFreqs)
f3BiFreq = getNgramStats(f3txt, bigramFreqs)
f4BiFreq = getNgramStats(f4txt, bigramFreqs)
f5BiFreq = getNgramStats(f5txt, bigramFreqs)
multiBarChart('Top 20 Bigram Frequencies', bigramFreqs, f1BiFreq, f2BiFreq, f3BiFreq, f4BiFreq, f5BiFreq)
# This didn't seem particularly useful. Thought would be able to idetify playfair based onthis, but I already know it is 3

# Quadgram
f1QuadFreq = getNgramStats(f1txt, quadgramFreqs)
f2QuadFreq = getNgramStats(f2txt, quadgramFreqs)
f3QuadFreq = getNgramStats(f3txt, quadgramFreqs)
f4QuadFreq = getNgramStats(f4txt, quadgramFreqs)
f5QuadFreq = getNgramStats(f5txt, quadgramFreqs)
multiBarChart('Top 20 Quadgram Frequencies', quadgramFreqs, f1QuadFreq, f2QuadFreq, f3QuadFreq, f4QuadFreq, f5QuadFreq)

# scoring
s1 = scoreFile(f1txt, f1SingleFreq, f1BiFreq, f1QuadFreq)
print(s1)
s2 = scoreFile(f2txt, f2SingleFreq, f2BiFreq, f2QuadFreq)
print(s2)
s3 = scoreFile(f3txt, f3SingleFreq, f3BiFreq, f3QuadFreq)
print(s3)
s4 = scoreFile(f4txt, f4SingleFreq, f4BiFreq, f4QuadFreq)
print(s4)
s5 = scoreFile(f5txt, f5SingleFreq, f5BiFreq, f5QuadFreq)
print(s5)