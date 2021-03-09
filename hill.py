import numpy as np
import string
from englishFitnessFunction import scoreString, getFileText, quadgramFreqs

def getKeyValuesFromMatrix(array):
    try:
        return [int(array.item(0)), int(array.item(2)), int(array.item(1)), int(array.item(3))]
    except:
        return [int(array.item(0)), int(array.item(1))]

def getWordFromMatrix(vals):
    keyword=''
    for k in vals:
        keyword += chr(k + 97)
    return keyword

def create2x2FromString(text):
    return np.array([[string.ascii_lowercase.index(text[0]), string.ascii_lowercase.index(text[2])],[ string.ascii_lowercase.index(text[1]), string.ascii_lowercase.index(text[3])]])

def create2x1FromString(text):
    return np.array([[string.ascii_lowercase.index(text[0])],[ string.ascii_lowercase.index(text[1])]])

def createMatrixFromString(text):
    if len(text) == 4:
        return create2x2FromString(text)
    elif len(text) == 2:
        return create2x1FromString(text)
    #else:
        #print("can't make matrix for Hills out of this:", text) first one has 3s and 1s

def adj2x2(matrix):
    vals = getKeyValuesFromMatrix(matrix)
    return np.array([[ vals[3], -1*vals[2]],[ -1*vals[1], vals[0]]])

# np lingalg det was not returning integers for some reason
# i.e. 260.9999999 instead of 261
def det2x2(matrix):
    vals = getKeyValuesFromMatrix(matrix)
    return (vals[0] * vals[3]) - (vals[1] * vals[2])

def getPossibleKeysPerQuadgram(text):
    possibleKeysPerQuadgram = {}
    # Use popular quadgrams to break this
    for q in quadgramFreqs.keys():
        print("Quadgram:", q)

        # create b based on most popular quadgram
        B = create2x2FromString(q)

        possibleKeysForQuad = {}
           
        for k in range(len(text) -3): # will have to do -3 beacuse last 3 will not be able to make a matrix so won't be able to glean info from
            # grab 4 chars
            chars = text[k:k+4]

            # create A
            A = createMatrixFromString(chars)

            try:
                invA = ((det2x2(A)%26)**-1)*adj2x2(A) 
            except:
                # if we can't find the inverse, they go on to next attempt b/c we certainly wont be able to find D
                continue

            # solve for D
            D = np.matmul(B,invA) %26

            valid = True
            # We toss them out at this point if they are not ints, because otherwise wouldnt make a valid key
            for m in range(4):
                if D.item(m).is_integer():
                    continue
                else:
                    valid = False
                    break

            if valid:
                possibleKeysForQuad[k] = D

        if len(possibleKeysForQuad) > 0:
            possibleKeysPerQuadgram[q] = possibleKeysForQuad
    return possibleKeysPerQuadgram

def decodeText(text, D, startingIndex):
    decodedText =''
    t = text[startingIndex :] + text[0:startingIndex]

    chunks = [t[i:i+4] for i in range(0,len(t), 4)]

    for chunk in chunks:
        if len(chunk) < 4:
            continue 
        # create A
        A = createMatrixFromString(chunk)
        B = (np.matmul(D,A)) % 26 
        decodedText += getWordFromMatrix(getKeyValuesFromMatrix(B))
    return decodedText

def findDecodeTextOption(text, D, k):
    return decodeText(text, D,k)

def test():
    t = 'fupcmtgzkyukbqfjhuktzkkixtta'
    key="fthe"
    D = np.array([ [ 17,5], [18,23] ])
    #print("D1", D)
    #possibleKeysPerQuadgram = getPossibleKeysPerQuadgram(t)
    possibleKeysPerQuadgram = {}
    possibleKeysPerQuadgram[key] = {18: D} # to sub in the provided correct key. remove this and above when go bac
    #print("poss", possibleKeysPerQuadgram)
    
    for item in possibleKeysPerQuadgram[key]:
        decodedStr = findDecodeTextOption(t,possibleKeysPerQuadgram[key][item], item )
        score = scoreString(decodedStr)
        print("SCORE",score)
        scoreCutoff = 1500
        if score > scoreCutoff:
            print("Score: ", score, ",Text: ", decodedStr)

# snag file
text = getFileText('blackhat4')
# Turns out it is a quote from Jane Eyre. Not sure exactly what the start of it is TBH 
# tiontheygrowtherefirmasweedsamongstonesmadnessingreatonesmustnotunwatchdgomadnessingreatonesmustnotunwatchdgothelifeofeverymanisadiaryinwhichhemeanstowriteonestoryandwritesanotherandhishumblesthouriswhenhecomparesthevolumeasitiswithwhathevowedtomakeittimeisthegreatphysiciantisnotthedyingforafaiththatssohardmasterharryeverymanofeverynationhasdonethattisthelivinguptoitthatisdifficultthereisnosuchthingasunmixedevilamanwholoseshismoneygainsatleastexperienceandsometimessomethingbetterprejudicesitiswellknownaremostdifficulttoeradicatefromtheheartwhosesoilhasneverbeenloosenedorfertilisedbyeduca
scoreCutoff = 13000

possibleKeysPerQuadgram = getPossibleKeysPerQuadgram(text)
print("D", possibleKeysPerQuadgram)

for key in possibleKeysPerQuadgram:
    print("Quadgram:", key)
    for item in possibleKeysPerQuadgram[key]:
        decodedStr = findDecodeTextOption(text,possibleKeysPerQuadgram[key][item], item )
        score = scoreString(decodedStr)
        if score > scoreCutoff:
            print("Score: ", score, ",Text: ", decodedStr)
