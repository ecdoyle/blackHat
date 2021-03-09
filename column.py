from itertools import permutations
import math
from englishFitnessFunction import scoreString, getFileText, scoreStringForTopN

# We know it is between 8 and 10 columns
# ~~~~~~ We know key length is between 10 and 20
text = getFileText('blackhat5')

def breakIntoColumnsPT(text, colNum):
    cols = [""] * colNum
    for k in range(len(text)):
        cols[k%colNum] += text[k]
    return cols    

def breakIntoColumnsCT(text, numCols):
    return [text[i:i+int(len(text)/numCols)] for i in range(0, len(text),int(len(text)/numCols) )]
 

def getPermutations(colNum):
    p = []
    for k in range(colNum):
        p.append(k)
    perms = set(list(permutations(p, colNum)))
    return perms

def assembleText(order, cols, origText):
    numCols = len(order)
    # Can only splice when string sequence is same length. This helps safe guard
    # so result string, a, is not too short
    rows = int(math.ceil(len(origText) / numCols))
    strLen = rows * numCols
    a = ['_'] * strLen

    for k in range(numCols):
        lenA = len(a[order.index(k)::numCols])
        lenColK = len(cols[k])
        # Protect against cols being too short to be sliced into a
        if lenColK < lenA:
            diff = lenA - lenColK
            for d in range(diff):
                cols[k] += ' '
        a[order.index(k)::numCols] = cols[k]
    return  "".join(a)

def testAssembleText():
    og = 'ebantownsisocute'
    order=[1,0,2,3,4,5,6,7]
    # should get beantown is so cute
    cl = breakIntoColumnsPT(og, 8)
    print(assembleText(order,cl , og))

def findFrames(window):
    centerWInd = int(len(window)/2)
    centerW = { centerWInd  : window[centerWInd ]}
    frameL = window[0:centerWInd]
    lenFrameL = len(frameL)
    centerFLInd = int(lenFrameL/2)
    centerFL = { centerFLInd  : window[centerFLInd ]}
    frameR=window[centerWInd+1:]
    lenFrameR = len(frameR)
    centerFRInd = int(lenFrameR/2)
    centerFR = { centerFRInd+ centerWInd  : window[centerFRInd + centerWInd ]}
    return centerW, centerFL, centerFR

    # score

def scoreFrameValues(window, centerWInd, centerFLInd, centerFRInd ):
    assembledString = assembleText(window[centerFLInd ], cols,text)
    scoreL = scoreString(assembledString)
    #print("L: ", scoreL,"~", assembledString)
    assembledString = assembleText(window[centerWInd ], cols,text)
    scoreC = scoreString(assembledString)
    #print("C: ",scoreC,"~", assembledString)
    assembledString = assembleText(window[centerFRInd ], cols,text)
    scoreR = scoreString(assembledString)
    #print("R: ",scoreR,"~", assembledString)
    return scoreL, scoreC, scoreR

def getFrameIndices(centerW, centerFL, centerFR ):
    return list(centerW.keys())[0], list(centerFL.keys())[0],list(centerFR.keys())[0]
    
def findNewWindow(window, scoreL,centerFLInd, scoreC,centerWInd, scoreR,centerFRInd ):
    if scoreL>scoreC and scoreL>scoreR:
        #if L is highest then make that the new center ( new window is 0 to center)
        window = window[:centerWInd]
        #print("Lhighest")
    elif scoreL<scoreC and scoreC>scoreR:
        # score C is largest. keep as center but shrink window,( new window is L to R)
        window = window[centerFLInd:centerFRInd]
        #print("chighest")
    elif scoreL<scoreR and scoreC<scoreR:
        # R is highest, make that the new center (new window is center to end)
        window = window[centerWInd:]
        #print("Rhighest")
    elif scoreL==scoreC and scoreC>scoreR:
        # L and C are tied, and greater than R so make them the new window (new window is L to C)
        window = window[centerFLInd:centerWInd]
        #print("LCtie")
    elif scoreL<scoreC and scoreC==scoreR:
        # C and R are tied, and greater than L so make them the new window (new window is C to R)
        window = window[centerWInd:centerFRInd]
        #print("crtie")
    #elif scoreL==scoreC and scoreC==scoreR:
        # all tied, offset and try window again
        #print("meep")
    else:
        print("Good fucking luck", scoreL, scoreC, scoreR) 
    print("scores", scoreL, scoreC, scoreR) 
    return window

def swapCols(cols, pos1, pos2):
    cols[pos1], cols[pos2] = cols[pos2], cols[pos1]
    return cols

def assembleTextAndScore(cols, text):
    assembledString = assembleText(range(len(cols)), cols,text)
    score = scoreString(assembledString)
    return score, assembledString

def printTextInCols(text, numCols):
    split = [text[i:i+numCols] for i in range(0, len(text), numCols)]
    for item in split:
        print(item)

testCt = 'evlnacdtesearofodeecwiree'
testPt= "wearediscoveredfleeatonce"

max = 0
scoreCutoff = 5900
for c in range(8,11):
    cols = breakIntoColumnsCT(text, c)
    print(cols)

    perms = getPermutations(c)
    print("Number permutations: ", len(perms))
    for p in perms:
        p = list(p)

        # assemble text and join
        assembledString = assembleText(p, cols,text)

        # score
        score = scoreStringForTopN(assembledString, 30)
        if score > max:
            max = score
        if score > scoreCutoff:
            print("Score: ", score, ", Permutation: ", p ,"Text: ", assembledString)
    
    print("Max for ",c , "~",max)

    """
    thebirdthatwouldsoarabovethelevelplainoftraditionandprejudicemusthavestrongwingsknavesdogrowgreatbybeinggreatmensapesthegreatsecretelizaisnothavingbadmannersorgoodmannersoranyotherparticularsortofmannersbuthavingthesamemannerforallhumansoulsinshortbehavingasifyouwereinheavenwheretherearenothirdclasscarriagesandonesoulisasgoodasanotherhappyaretheythatheartheirdetractionsandcanputthemtomendingitseemstomenowifiwastofindfatherathometonightishouldbehavedifferentbuttheresnoknowingperhapsnothingudbealessontousifitdidntcometoolateamindneedsbookasaswordneedsawhetstoneifitistokeepitsedge         

    Awakenings- the bird that would soar above the level plain of tradition and prejudice must have strong wings
    John Webster - knaves do grow great by being great mens apes
    Pygmalion- the great secret eliza is not having bad manners or good manners or any other particular sort of manners but having the same manner for all human souls in short behaving as if you were in heaven where there are no third class carriages and one soul is as good as another
    Much Ado about nothing (again) - happy are they that hear their detractions and can put them to mending
    George Elliot - it seems to me now if i was to find father at home tonight i should behave different but theres no knowing perhaps nothing ud be a lesson to us if it didnt come too late
    George R R Martin - a mind needs book as a sword needs a whetstone if it is to keep its edge         

    """
    """
    # Round 2 - attempting to use windows and frames in something that might be like hill climbing
    # assumbing that the permutations are ni some related order not yolo scattered
    # ideally would be like gray encoded so only 1 difference between perms

    perms = sorted(perms)
    window=perms
    print("len wind og ", len(window))
    i= 0
    while i<10:
        centerW, centerFL, centerFR = findFrames(window)
        #print(centerFL, centerW, centerFR)
        centerWInd, centerFLInd, centerFRInd = getFrameIndices(centerW, centerFL, centerFR)
        scoreL,scoreC, scoreR = scoreFrameValues(window, centerWInd, centerFLInd, centerFRInd  )
        if scoreL>5000 and scoreC>5000:
            options = window[centerFLInd: centerWInd]
            for option in options:
                assembledString = assembleText(p, cols,text)
                score = scoreString(assembledString)
                if score > scoreCutoff:
                    print("Score: ", score, ", Permutation: ", p ,"Text: ", assembledString)
        elif scoreC>5000 and scoreR>5000:
            options = window[ centerWInd:centerFRInd]
            for option in options:
                assembledString = assembleText(option, cols,text)
                score = scoreString(assembledString)
                if score > scoreCutoff:
                    print("Score: ", score, ", Permutation: ", option ,"Text: ", assembledString)
        else:    
            window = findNewWindow(window, scoreL, centerFLInd, scoreC, centerWInd, scoreR, centerFRInd)
        print(len(window))
        i+=1 



    # Round 3 - inspired by the eye dr - "1? or 2?"
    lastOptimalScore = 0
    lastOptimalText = text
    col = 0
    
    Straight swap highest in the 5600?
    while lastOptimalScore < scoreCutoff:
        curOptScore = 0
        curOptText= ''
        for k in range(len(cols)):
            if k == col:
                # dont swap with self
                continue
            cols = swapCols(cols, col, k)
            score, assembledString = assembleTextAndScore(cols, lastOptimalText)
            if score > curOptScore:
                curOptScore = score
                curOptText = assembledString
        
        if curOptScore > lastOptimalScore:
            lastOptimalScore = curOptScore
            lastOptimalText = curOptText
            print("cur: ", curOptScore, "~", curOptText)
        else: # curOptScore == lastOptimalScore:
            col += 1
            col = col % len(cols)
        #else:
        #    print("sos")

    while lastOptimalScore < scoreCutoff:
        curOptScore = 0
        curOptText= ''
        # score the orignial?  guess we dont have to since with either be the legit OG or 
        # it will be scored via the last round
        for k in range(1,len(cols)):
            cols = swapCols(cols, col+k-1, k) # need to adjust for different columns
            score, assembledString = assembleTextAndScore(cols, lastOptimalText)
            if score > curOptScore:
                curOptScore = score
                curOptText = assembledString
        
        if curOptScore > lastOptimalScore:
            lastOptimalScore = curOptScore
            lastOptimalText = curOptText
            print("cur: ", curOptScore, "~", curOptText)
        #else: # curOptScore == lastOptimalScore:
            #col += 1
            #col = col % len(cols)
        #else:
        #    print("sos")
        """

    

            

            

