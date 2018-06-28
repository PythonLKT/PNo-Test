import pandas as pd
import re

df = pd.read_csv("C:\\Users\\ChrisR\\Desktop\\test.csv")

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def aextraction(varinput):
    if hasNumbers(varinput) == True:
        tempfindlen = re.search("\d", varinput)
        findlen = tempfindlen.start()
        OutNumber =  varinput[findlen:]
    elif varinput.isdigit() == False:
        OutNumber = varinput
    return OutNumber

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

PA = []

for row in df["POWELL"]:
    var = row.split('-')[3]
    PAitem = aextraction(var)
    PA.append(PAitem)

df['PowellAngle'] = PA

df.to_csv('C:\\Users\\ChrisR\\Desktop\\output1.csv', sep=',')