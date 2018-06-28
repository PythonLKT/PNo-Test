import pandas as pd
import numpy as np
import re



    # Translation index list between POWEEL & HOSEMASTER
tsindex = {'BPFXC': '35',
'BPP': '29',
'BPPH': '29',
'BTP': '25',
'DHC': '57',
'DHP': '58',
'DLC': '55',
'DLP': '56',
'DSB': '29',
'DSM': '65',
'FHP': '61',
'FL61SC': '61',
'FL62SC': '62',
'FLP': '61',
'JCC': '20',
'JCP': '19',
'JCTN': '22',
'JCTS': '22',
'JSC': '33',
'JSP': '33',
'KMC': '59',
'KMP': '60',
'MPP': '75',
'MPPH': '75',
'NPC': '48',
'NPP': '47',
'O6162': '61',
'OBSPP': '29',
'OFC': '39',
'OFP': '40',
'OFTN': 'L ',
'OORFS': '40',
'OUNO': '44',
'UNP': '43',
'UNPH': '43'
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
adaptorAngle = {
'BPFXC': 'Q-',
'BPP': 'P-',
'BPPH': 'PH',
'BTP': 'P-',
'DHC': 'Q-',
'DHP': 'P-',
'DLC': 'Q-',
'DLP': 'P-',
'DSB': 'DS',
'DSM': 'DS',
'FHP': 'P-',
'FL61SC': 'V-',
'FL62SC': 'V-',
'FLP': 'P-',
'JCC': 'Q-',
'JCP': 'P-',
'JCTN': 'A-',
'JCTS': 'AS',
'JSC': 'Q-',
'JSP': 'P-',
'KMC': 'Q-',
'KMP': 'P-',
'MPP': 'P-',
'MPPH': 'PH',
'NPC': 'Q-',
'NPP': 'P-',
'O6162': 'Z-',
'OBSPP': 'Z-',
'OFC': 'Q-',
'OFP': 'P-',
'OFTN': 'Unknown',
'OORFS': 'Z-',
'OUNO': 'Q-',
'UNP': 'P-',
'UNPH': 'PH'
}


# HTS1&HTS1S is smaller one; HTS2&HTS2S is biger one
# PTSS: POWELL 5th part number
# PTS1: POWELL 3rd part number, PTS2: POWELL 4th part number
HA = []
HTS1 = []
HTS1S = []


def main():
    for row in df["POWELL"]:
        PA1 = row.split('-')[2]
        HA1 = adaptorAngle[PA1]
        HA.append(HA1)  # completes plug angle
        PTS1 = row.split('-')[2]    # separte number by '-' & get 3rd part of it
        HTS1A = tsindex[PTS1]       # translate the character by tsindex, like 'JCM' to '19'
        HTS1.append(HTS1A)
        HTS1S.append(UNMSizeAlter(HTS1A, filtrate(row.split('-')[3], HTS1A)))  # don't need to change place
    df['HA'] = HA
    df['HTS1'] = HTS1               # input the list of HTS1 to df new column 'HTS1'
    df['HTS1S'] = HTS1S


def output():
    # Compare with 'HMIINPUT' column, then get the result
    df['COMPARE'] = (df['HA'] + (df['HTS1'] + ' ') + (df['HTS1S'] + ' ') + ' PO')
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



def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


################################ START #################################
df = pd.read_csv("F:\\Dropbox\Python\\Part No Conversion\\Batch2.1\\Batch2.1_Source.csv")
main()
output()