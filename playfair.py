from englishFitnessFunction import scoreString, getFileText, formatLowerCharOnlyStr, getNgramStats, bigramFreqs, scoreStringForTopN
import numpy as np
import random
from urllib.request import urlopen
import itertools
text = getFileText('blackhat3')

def createGrid(key):
    # Alphabet padding does not have j. If not dropping
    # j then swap out for whatever
    alphabetPad="abcdefghiklmnopqrstuvwxyz"
    gridList = []
    letters = key  + alphabetPad
    for k in range(len(letters)):
        if len(gridList) < 25:
            if letters[k] not in gridList:
                gridList.append(letters[k])
        else:
            break
    grid = np.reshape(gridList, (5,5))
    return grid

def checkIfInColumn(c1, c2, grid):
    indC1 = np.where(grid == c1)
    if c2 in grid[:, indC1[1][0]]:
        return True
    else:
        return False

def encodeBigramCol(c1, c2, grid):
    indC1 = np.where(grid == c1)
    col = grid[:, indC1[1]]
    indC2 = np.where(grid == c2)
    newC1 = col[(indC1[0][0] +1) %5][0]
    newC2 = col[(indC2[0][0] +1) %5][0]
    return newC1, newC2

def decodeBigramCol(c1, c2, grid):
    indC1 = np.where(grid == c1)
    col = grid[:, indC1[1]]
    indC2 = np.where(grid == c2)
    newC1 = col[(indC1[0][0] -1) %5][0]
    newC2 = col[(indC2[0][0] -1) %5][0]
    return newC1, newC2

def checkIfInRow(c1, c2, grid):
    indC1 = np.where(grid == c1)
    if c2 in grid[ indC1[0][0],:]:
        return True
    else:
        return False

def encodeBigramRow(c1, c2, grid):
    indC1 = np.where(grid == c1)
    col = grid[indC1[0],:]
    indC2 = np.where(grid == c2)
    newC1 = col[0][(indC1[1][0] +1) %5]
    newC2 = col[0][(indC2[1][0] +1) %5]
    return newC1, newC2

def decodeBigramRow(c1, c2, grid):
    indC1 = np.where(grid == c1)
    col = grid[indC1[0],:]
    indC2 = np.where(grid == c2)
    newC1 = col[0][(indC1[1][0] -1) %5]
    newC2 = col[0][(indC2[1][0] -1) %5]
    return newC1, newC2

# also serves for decode too
def encodeBigramRect(c1, c2, grid):
    indC1 = np.where(grid == c1)
    indC2 = np.where(grid == c2)
    rowC1 = indC1[0][0]
    rowC2 = indC2[0][0]
    colC1 = indC1[1][0]
    colC2 = indC2[1][0]
    rowContainingC1 = grid[indC1[0],:]
    rowContainingC2 = grid[indC2[0],:]
    rectWidth = abs(colC1- colC2)
    if colC1 >colC2:
        newC1 = rowContainingC1[0][indC1[1][0] - rectWidth]
        newC2 = rowContainingC2[0][indC2[1][0] + rectWidth]
    else:
        newC1 = rowContainingC1[0][indC1[1][0] + rectWidth]
        newC2 = rowContainingC2[0][indC2[1][0] - rectWidth]
    return newC1, newC2

def encodeBigram(c1, c2, grid):
    # check if same letter - what if is both x?
    if c1 == c2:
        c2 = 'x'
        
    if checkIfInColumn(c1, c2, grid):
        nc1, nc2 = encodeBigramCol(c1,c2, grid)
    elif checkIfInRow(c1, c2, grid):
        nc1, nc2 = encodeBigramRow(c1,c2, grid)
    else:
        nc1, nc2 = encodeBigramRect(c1, c2, grid)
    return nc1, nc2

def decodeBigram(c1, c2, grid):
    if checkIfInColumn(c1, c2, grid):
        nc1, nc2 = decodeBigramCol(c1,c2, grid)
    elif checkIfInRow(c1, c2, grid):
        nc1, nc2 = decodeBigramRow(c1,c2, grid)
    else:
        nc1, nc2 = encodeBigramRect(c1, c2, grid)

    if nc2 == 'x':
        nc2 = nc1
    return nc1, nc2

def encodeBigrams(bigrams, grid):
    encodedTxt=""
    for bigram in bigrams:
        chars = list(bigram)
        nc1, nc2 = encodeBigram(chars[0], chars[1], grid)
        encodedTxt += (nc1 + nc2)
    return encodedTxt

def decodeBigrams(bigrams, grid):
    decodedTxt=""
    for bigram in bigrams:
        chars = list(bigram)
        nc1, nc2 = decodeBigram(chars[0], chars[1], grid)
        decodedTxt += (nc1 + nc2)
    return decodedTxt

def createBigrams(text):
    bigrams =[]
    for i in range(0, len(text),2):
        bigrams.append(text[i:i+2]) 
    return bigrams

def test():
    key = "playfair example"
    key = formatLowerCharOnlyStr(key)
    grid = createGrid(key)
    print(grid)
    #print(encodeBigramRect('a', 'n', grid))
    #print(encodeBigramRect('h', 'i', grid))
    text = "andyhowwould"
    bigrams = createBigrams(text)
    #print(bigrams)
    ct = encodeBigrams(bigrams, grid)
    print(ct)
    cipherTxt = "logadsygnvac"
    bigrams = createBigrams(cipherTxt)
    pt = decodeBigrams( bigrams, grid)
    print(pt)

#test()
def freqTest():
    bigramFreq = getNgramStats(text, bigramFreqs)
    print(bigramFreq)
    bigrams = createBigrams(text)
    dec = ""
    ctBigramFreqList = list(bigramFreq.keys())
    for bigram in bigrams:
        if bigram in ctBigramFreqList[:5]:
            dec += list(bigramFreqs.keys())[ctBigramFreqList.index(bigram)]
        else:
            dec +="_-"
    print(dec)

res = urlopen('https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt')
words = res.read().split()
max = 0
for k in range(1000000):
    random.shuffle(words)
    seed=""
    for word in words[:10]:
        seed  += word.decode("utf-8").replace('j', 'i')
    #seed = "".join(words[:10]).replace('j','i')
    #print(seed)
    key = seed#"playfair example"
    key = formatLowerCharOnlyStr(key)
    #print(key)
    grid = createGrid(key)
    #print(grid)
    bigrams = createBigrams(text)
    pt = decodeBigrams( bigrams, grid)
    score = scoreStringForTopN(pt, 10)
    if score> max:
        max = score
    if score > 1588:
        print(seed, "~",grid, "~", score, "~", pt)
print(max)
# thats a lot
#print(len(list(itertools.permutations(words, 10))))