import numpy as np
import itertools
from englishFitnessFunction import scoreString, getFileText, unigramFreqs, shiftBy, getCorrespondingLetter

# ~~~~~~ We know key length is between 10 and 20
encryptedUnknownKeyLength = getFileText('blackhat1')

# make sure letters is a list so can use count
# letter is not really a letter, it is a list of letters.probs should rename
def determinePossibleKeysForLetter(letters, tolerance):
    frequency = {}
    possibleKeys=[]

    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(letters.count(chr(ascii)))/len(letters)

    sum_freqs_squared = 0.0
    for ltr in frequency:
        sum_freqs_squared += frequency[ltr]*frequency[ltr] #print("Will be near .065 despite Caesar: " + str(sum_freqs_squared))
    
    for possible_key in range(1, 26):
        sum_f_sqr = 0.0
        for ltr in unigramFreqs:
            caesar_guess = shiftBy(ltr, possible_key)
            sum_f_sqr += unigramFreqs[ltr]*frequency[caesar_guess]
        if abs(sum_f_sqr - .065) < tolerance:
            possibleKeys.append(possible_key)
    return possibleKeys

def determinePossibleKeysForWord( encryptedText, wordLength, tolerance):
    keysForWord=[]
    for k in range(0, wordLength):
        # find list
        letters = list(encryptedText[k:len(encryptedText):wordLength])

        # find possible key for that list
        possibleKeys = determinePossibleKeysForLetter(letters, tolerance)
        #print(possibleKey)
        keysForWord.append(possibleKeys)
    return keysForWord

def getKeyWordFromKeyValues(keys):
    asciiLetters = []
    for key in keys:
        asciiLetters.append(getCorrespondingLetter(key))
    return "".join(asciiLetters)
        
def decodeTextBasedOnKeys(encryptedText, keysForWord): 
    decryptedText = []

    # decode letters
    for k in range(0,len(encryptedText)):
        decryptedText.append(shiftBy(encryptedText[k], 26 - keysForWord[k%len(keysForWord)]))
    return decryptedText

def decryptForKeyLength(encryptedText, keyLength, tolerance, scoreCutoff):
    possibleDecryptions = {}
    keysForWord =determinePossibleKeysForWord(encryptedText, keyLength, tolerance)
    possibleKeys =list(itertools.product(*keysForWord))
    if len(possibleKeys) >0:
        print("# Possible keys: ", len(possibleKeys))
    for key in possibleKeys:
        decryptedText = decodeTextBasedOnKeys(encryptedText, key)
        decryptedString = "".join(decryptedText)
        score = scoreString(decryptedString)
        if score > scoreCutoff:
            keyword = getKeyWordFromKeyValues(key)
            print("Score: ", score, ", Keyword: ", keyword ,"Text: ", decryptedString)
            possibleDecryptions[keyword] = decryptedString
    return possibleDecryptions
   
tolerance = 0.011
scoreCutoff = 13000
for k in range(10,21):
    print("Key Length: ", k)
    try:
        possibleDecryptions = decryptForKeyLength(encryptedUnknownKeyLength, k, tolerance, scoreCutoff)
        #if len(possibleDecryptions) >0:
            #print("Decryption Options:",possibleDecryptions)
    except TypeError:
        continue

    # Score:  1800 , Keyword:  kknghnrbunmpccttb Text:  appyaretheythatheartheirdetractionsandcanputthemtomendingitwasthebestoftimesitwastheworstoftimesitwastheageofwisdomitwastheageoffoolishnessitwastheepochofbeliefitwastheepochofincredulityitwastheseasonoflightitwastheseasonofdarknessitwasthespringofhopeitwasthewinterofdespairwehadeverythingbeforeuswehadnothingbeforeuswewereallgoingdirecttoheavenwewereallgoingdirecttheotherwayinshorttheperiodwassofarlikethepresentperiodthatsomeofitsnoisiestauthoritiesinsistedonitsbeingreceivedforgoodorforevilinthesuperlativedegreeofcomparisononlyadifferenceoftasteinjokesisagreatstrainontheaffectionsh
