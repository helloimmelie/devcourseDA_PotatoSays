import os
import json
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm

from operator import itemgetter

from multiprocessing import Pool

jsonDir = './data/match_timeline'
matchDir = './data/match'
fileOutputDir = './fileOutputs/'


listDir = os.listdir(jsonDir)
len(listDir)

resultFrame = list()

def convertSecondsMinutes(seconds):
    
    minutes = (seconds/(60))
    minutes = int(minutes)

    return minutes


def getChampionStats(infoFrameData, championDf, matchId):
    for i in range(0, len(infoFrameData),1):
        for pN in range(1, 9, 1):
            resultFrame.append({**infoFrameData[i]['participantFrames'][str(pN)]['championStats'],\
                       'participantId' : infoFrameData[i]['participantFrames'][str(pN)]['participantId'],\
                       'currentGold': infoFrameData[i]['participantFrames'][str(pN)]['currentGold'],\
                        **infoFrameData[i]['participantFrames'][str(pN)]['damageStats'],\
                        'goldPerSecond':infoFrameData[i]['participantFrames'][str(pN)]['goldPerSecond'],\
                        'jungleMinionKilled': infoFrameData[i]['participantFrames'][str(pN)]['jungleMinionsKilled'],\
                        'level': infoFrameData[i]['participantFrames'][str(pN)]['level'],\
                        'minionKilled': infoFrameData[i]['participantFrames'][str(pN)]['minionsKilled'],\
                        'timeEnemySpendControlled':infoFrameData[i]['participantFrames'][str(pN)]['timeEnemySpentControlled'],\
                        'totalGold':infoFrameData[i]['participantFrames'][str(pN)]['totalGold'],\
                        'xp':infoFrameData[i]['participantFrames'][str(pN)]['xp']})
    
    resultFrameDf = pd.DataFrame(resultFrame)
    participantStat = pd.merge(championDf[['participantId','championId']], resultFrameDf, on = 'participantId')
    participantStat['matchId'] = matchId   
    participantStat.to_csv(os.path.join(fileOutputDir,f'{matchId}_CHAMPION_STAT_PER_TIMESTAMP.csv')) 
    

def convertToDf(bucketData,  matchId):
    
    bucketDf = pd.DataFrame(bucketData)
    
    bucketDf['matchId'] = matchId
    
    return bucketDf


def getgameLogData(matchLineData, championDf, matchId):
    
    itemSoldBucket = list()
    gameEndBucket = list()
    levelUpBucket = list()
    skilLevelUpBucket = list()
    wardKillBucket = list()

    for i in range(0, len(matchLineData),1):
        elementData = matchLineData[i]['events']

        for e in elementData : 
                if e['type'] == "ITEM_SOLD":
                        itemSoldBucket.append(e)
    
                if e['type'] == "GAME_END":
                        gameEndBucket.append(e)
    
                if e['type'] == "LEVEL_UP":
                        levelUpBucket.append(e)
    

                if e['type'] == "SKILL_LEVEL_UP":
                        skilLevelUpBucket.append(e)
    
                if e['type'] ==  "WARD_KILL":
                        wardKillBucket.append(e)
    



    itemSoldDf = convertToDf(itemSoldBucket, matchId)
    gameEndDf = convertToDf(gameEndBucket, matchId)
    levelUpDf = convertToDf(levelUpBucket, matchId)
    skillLevelUpDf = convertToDf(skilLevelUpBucket, matchId)
    wardKillDf = convertToDf(wardKillBucket, matchId)

    #각각 csv로 변환

    itemSoldDf.to_csv(os.path.join(fileOutputDir, '{matchId}_ITEM_SOLD.csv'))
    gameEndDf.to_csv( os.path.join(fileOutputDir,f'{matchId}_GAME_END.csv'))
    levelUpDf.to_csv( os.path.join(fileOutputDir,f'{matchId}_LEVEL_UP.csv'))
    skillLevelUpDf.to_csv( os.path.join(fileOutputDir,f'{matchId}_SKILL_LEVEL_UP.csv'))
    wardKillDf.to_csv( os.path.join(fileOutputDir,f'{matchId}_WARD_KILL.csv'))


def getChampionData(matchData):
    championList = list()
    matchId = matchData['metadata']['matchId'] 
    matchId = matchId.split('_')[1]
    for championData in matchData['info']['participants']:
        values = itemgetter(*['participantId', 'championId','championName'])(championData)
        championList.append((matchId,)+ values  )
    
    championDataDf= pd.DataFrame(championList, columns = ['matchId', 'participantId', 'championId','championName'], )
    championDataDf.to_csv(os.path.join(fileOutputDir, f'{matchId}_CHAMPION_PARTICIPANT_ID.csv'))

    return matchId, championDataDf

def getData(element):
    matchPath = os.path.join(matchDir, element)
    matchTimelineDir = os.path.join(jsonDir, element)
    
    if os.path.isfile(matchPath) and os.path.isfile(matchTimelineDir):
        print(f'{element} is processing')

        with open(matchTimelineDir) as f:
            data = json.load(f)
        with open(matchPath) as f:
            matchData = json.load(f)  
        
        if convertSecondsMinutes(matchData['info']['gameDuration']) < 5:
            print('5분 미만이라 처리하지 않음 ')
            return
        
        infoFrameData = data['info']['frames'] 
        matchId, championDf = getChampionData(matchData)
        getChampionStats(infoFrameData, championDf, matchId)
        getgameLogData(infoFrameData, championDf, matchId)
    else: 
       return 
    
    
if __name__ == "__main__":
    pool = Pool(processes=4)
    total = len(listDir)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.imap_unordered(getData, listDir), total=total):
            pbar.update()
    pool.close()
    pool.join()