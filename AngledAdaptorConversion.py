import pandas as pd
import numpy as np
import re



    # Translation index list between POWEEL & HOSEMASTER
tsindex = {'JCFX': '18',
           'TW': '16',
           'BPMB': '29',
           'MPM': '75',
           'DHMB': '58',
           'DLMB': '56',
           'JCMB': '19',
           'NSFX': '46',
           'OFMB': '40',
           'UNF': '43',
           'IM-JCFX': '18',
           'JSFX': '18',
           'JCFS': '18',
           'JCM': '19',
           'JCF': '20',
           'BBNJ': '23',
           'BBNJB': '23',
           'BPFX': '24',
           'BTM': '25',
           'BTF': '27',
           'BFFX': '31',
           'BPM': '29',
           'BFM': '32',
           'BPF': '35',
           'OFFX': '39',
           'OFM': '40',
           'UNM': '43',
           'NPMX': '47',
           'NPM': '47',
           'NPF': '48',
           'SFFX': '50',
           'SFM': '51',
           'DLFX': '55',
           'DLM': '56',
           'DHFX': '57',
           'DHM': '58',
           'KMM': '60',
           'FL': '61',
           'DG-FL': '61',
           'FH': '62',
           'FL': '61',
           'DG-FH': '62',
           'CF': '63',
           'MBNJ': '92',
           'MBNJB': '92'
           }
tsTubeSize = {'55': 'light',
              '56': 'light',
              '57': 'heavy',
              '58': 'heavy'
              }
tubeSizeWeight = {'extralight': {'08': '04',
                                 '10': '06',
                                 '12': '08'},
                  'light': {'12': '06',
                            '14': '08',
                            '16': '10',
                            '18': '12',
                            '22': '15',
                            '26': '18',
                            '30': '22',
                            '36': '28',
                            '45': '35',
                            '52': '42',
                            },
                  'heavy': {'14': '06',
                            '16': '08',
                            '18': '10',
                            '20': '12',
                            '22': '14',
                            '24': '16',
                            '30': '20',
                            '36': '25',
                            '42': '30',
                            '45': '30',
                            '52': '38'
                            }
                  }
UMNSizeIndex = { '03': '06',
'04': '07',
'05': '08',
'06': '09',
'08': '12',
'10': '14',
'12': '17',
'14': '19',
'16': '21',
'20': '26',
'24': '30',
'32': '40'
}
adaptorAngle = {'90LO': 'CL',
'45LO': 'BL',
'90': 'C-',
'90B': 'CN',
'45': 'B-',
'45B': 'BN',
'45S': 'D-',
'90S': 'E-',
'90L': 'F-',
'180': 'A-',
'180B': 'AN'
}

# HTS1&HTS1S is smaller one; HTS2&HTS2S is biger one
# PTSS: POWELL 5th part number
# PTS1: POWELL 3rd part number, PTS2: POWELL 4th part number
HTS1 = []
HTS2 = []
HTS1S = []
HTS2S = []
HA = []

def main():
    for row in df["POWELL"]:
        PA1 = row.split('-')[3]
        HA1 = adaptorAngle[aextraction(PA1)]
        HA.append(HA1)
        PTS1 = row.split('-')[2]    # separte number by '-' & get 3rd part of it
        PTS2 = row.split('-')[3]    # separte number by '-' & get 4rd part of it
        PTS1A = tsindex[textraction(PTS1)]       # translate the character by tsindex, like 'JCM' to '19'
        PTS2A = tsindex[textraction(PTS2)]
        if (PTS1A <= PTS2A):           # compare two number and make sure smaller one in the first place
            HTS1.append(PTS1A)
            HTS2.append(PTS2A)
            PTSS = row.split('-')[4]
            HTS1S.append(UNMSizeAlter(PTS1A,filtrate(PTSS[0:2], PTS1A))) # don't need to change place
            HTS2S.append(UNMSizeAlter(PTS2A,filtrate(PTSS[2:4], PTS2A))) # such as '1314' to '13' '14' ## if it is UNM, the size will be changed by UMNSizeIndex
        else:
            HTS2.append(PTS1A)
            HTS1.append(PTS2A)
            PTSS = row.split('-')[4]
            HTS2S.append(UNMSizeAlter(PTS1A,filtrate(PTSS[0:2], PTS1A))) # get number from 5th part of POWELL and exchange its place with second part
            HTS1S.append(UNMSizeAlter(PTS2A,filtrate(PTSS[2:4], PTS2A))) # such as '1314' to '14' '13'
    df['HTS1'] = HTS1               # input the list of HTS1 to df new column 'HTS1'
    df['HTS2'] = HTS2
    df['HTS1S'] = HTS1S
    df['HTS2S'] = HTS2S
    df['HA'] = HA

def output():
    # Compare with 'HMIINPUT' column, then get the result
    df['COMPARE'] = (df['HA'] + (df['HTS1'] + ' ') + (df['HTS1S'] + ' ') + (df['HTS2'] + ' ') + df['HTS2S'] + ' PO')
    #df['EXACT'] = np.where(df['HOSEMASTERS'] == df['COMPARE'], 'TRUE', 'FALSE')    # Output the result to a csv document
    print(df)
    df.to_csv('F:\\Dropbox\Python\\Part No Conversion\\Batch2.1\\Adaptor_Comparison.csv', sep=',')

def filtrate(size, threadstyle):
    if threadstyle in tsTubeSize:
        weight = tsTubeSize.get(threadstyle)
        weightvalue = tubeSizeWeight.get(weight)
        finalsize = weightvalue.get(size)
    else:
        finalsize = size
    return finalsize

def UNMSizeAlter(PTS12A,PreSize):
    if PTS12A == '43':
        PostSize = UMNSizeIndex.get(PreSize)
    else:
        PostSize = PreSize
    return PostSize

def aextraction(varinput):
    if hasNumbers(varinput) == True:
        tempfindlen = re.search("\d", varinput)
        findlen = tempfindlen.start()
        lenm1 = findlen - 1
        if varinput[lenm1] == 'B':
            OutNumber = varinput[findlen:] + varinput[lenm1]
        else:
            OutNumber = varinput[findlen:]
    elif varinput.isdigit() == False:
        if varinput[-1] == 'B':
            OutNumber = '180B'
        else:
            OutNumber = '180'
    return OutNumber

def textraction(varinput):
    if hasNumbers(varinput) == True:
        tempfindlen = re.search("\d", varinput)
        findlen = tempfindlen.start()
        OutNumber =  varinput[:findlen]
    elif varinput.isdigit() == False:
        OutNumber = varinput
    return OutNumber

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


################################ START #################################
df = pd.read_csv("F:\\Dropbox\Python\\Part No Conversion\\Batch2.1\\Batch2.1_Source.csv")
main()
output()