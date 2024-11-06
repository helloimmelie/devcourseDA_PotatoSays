from operator import itemgetter
from sqlalchemy import create_engine
import pandas as pd
from Components.dbComponents import connectToDB

#tableInfo 
building_kill = 'BUILDING_KILL'
ward_placed = 'WARD_PLACED'
elite_monster_kill = 'ELITE_MONSTER_KILL'
turret_plate_destroyed = 'TURRET_PLATE_DESTROYED'
objective_bounty_prestart = 'OBJECTIVE_BOUNTY_PRESTART'
champion_kill = 'CHAMPION_KILL'
champion_special_kill = 'CHAMPION_SPECIAL_KILL'
item_destroyed = 'ITEM_DESTROYED'
item_purchased = 'ITEM_PURCHASED'
item_sold = "ITEM_SOLD"
game_end = "GAME_END"
level_up = "LEVEL_UP"
skill_level_up = "SKILL_LEVEL_UP"
ward_kill =  "WARD_KILL"


def getChampionData(matchData, engine):
    championList = list()
    matchId = matchData['metadata']['matchId'] 
    matchId = matchId.split('_')[1]
    for championData in matchData['info']['participants']:
        values = itemgetter(*['participantId', 'championId'])(championData)
        championList.append((matchId,)+ values  )

    cols = ['match_id', 'participant_id', 'champion_id']
    championDataDf= pd.DataFrame(championList, columns = cols, ) # ['matchId', 'participantId', 'championId']
    championDataDf.to_sql('champion_participant_id', con=engine, if_exists='append', index=False)

    return matchId

def getChampionStats(infoFrameData, matchId, engine):
    resultFrame = []
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
                        'xp':infoFrameData[i]['participantFrames'][str(pN)]['xp'], 'timestamp': i},)
    
    resultFrameDf = pd.DataFrame(resultFrame)
    resultFrameDf['match_id'] = matchId


    resultFrameDf.to_sql('champion_stat_per_timestamp', con=engine, if_exists='append', index=False)

def convertToDf(bucketData,  matchId):
    
    bucketDf = pd.DataFrame(bucketData)
    
    bucketDf['matchId'] = int(matchId)

    if 'type' in bucketDf.columns:
          bucketDf = bucketDf.drop(columns=['type'], axis=1)
        

    return bucketDf

def getgameLogData(matchLineData, matchId, engine):
    
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
                        e =  {key: value for key, value in e.items() if key not in ['gameId']}
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

    print(itemSoldDf.columns)

    itemSoldDf.columns = ['item_id', 'participant_id', 'timestamp', 'match_id']
    gameEndDf.columns = ['real_timestamp', 'timestamp', 'winning_team', 'match_id']
    levelUpDf.columns = ['level', 'participant_id', 'timestamp', 'match_id']
    skillLevelUpDf.columns = ['levelup_type', 'participant_id', 'skill_slot', 'timestamp', 'match_id']
    wardKillDf.columns = ['participant_id', 'timestamp', 'ward_type', 'match_id']

    itemSoldDf.to_sql(item_sold, con=engine, if_exists='append', index=False)
    gameEndDf.to_sql(game_end, con=engine, if_exists='append', index=False)
    levelUpDf.to_sql(level_up, con=engine, if_exists='append', index=False)
    skillLevelUpDf.to_sql(skill_level_up, con=engine, if_exists='append', index=False)
    wardKillDf.to_sql(ward_kill, con=engine, if_exists='append', index=False)


    #각각 csv로 변환

    # itemSoldDf.to_csv(os.path.join(fileOutputDir, f'{matchId}_ITEM_SOLD.csv'))
    # gameEndDf.to_csv( os.path.join(fileOutputDir, f'{matchId}_GAME_END.csv'))
    # levelUpDf.to_csv( os.path.join(fileOutputDir, f'{matchId}_LEVEL_UP.csv'))
    # skillLevelUpDf.to_csv( os.path.join(fileOutputDir, f'{matchId}_SKILL_LEVEL_UP.csv'))
    # wardKillDf.to_csv( os.path.join(fileOutputDir, f'{matchId}_WARD_KILL.csv'))