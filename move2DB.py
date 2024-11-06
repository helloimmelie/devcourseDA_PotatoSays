import pymysql
from sqlalchemy import create_engine
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from operator import itemgetter



import traceback
from datetime import datetime

from Components.tableComponents import insert_events
from Components.dbComponents import connectToDB
from Components.dataProcessingComponents import *



if __name__ == "__main__":
    
    #jsonDir: matchline 데이터가 있는 경로를 의미함 
    #matchDir: match 데이터가 있는 경로를 의미함

    jsonDir = './data/match_timeline'
    matchDir = './data/match'

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("시작 시각:", formatted_time)

    # cnt = 0
    regame = []
    exceps = []

    listDir = os.listdir(jsonDir)
    
    total = int(len(listDir))
    listDir = list(listDir)


    for element in tqdm(listDir, total=total):


        # cnt += 1
        # print(f'{round((cnt / len(match_id_list) * 100), 2)}%..')
        matchPath = matchDir + '/' + element
        matchTimelineDir = jsonDir + '/' + element
        # print(matchPath)
        # print(matchTimelineDir)
        if os.path.isfile(matchPath) and os.path.isfile(matchTimelineDir):
                try:
                    # print(f'{e} is processing')
                    with open(matchTimelineDir) as f:
                        data = json.load(f)
                    with open(matchPath ) as f:
                        matchData = json.load(f)
    
                    if matchData['info']['gameDuration'] < 300:
                        print('다시하기 ', element)
                        regame.append(element)
                        continue
            
                    infoFrameData = data['info']['frames']

                    cur, engine = connectToDB()
            
                    matchId = getChampionData(matchData, engine)
                    getChampionStats(infoFrameData, matchId,engine)
                    getgameLogData(infoFrameData, matchId, engine)
                    insert_events(data, cur)
                
            
                except Exception as err:
                    with open("error_log_2.txt", "a") as log_file:
                        print(err)
                        log_file.write(f"File: {element}\n")
                        log_file.write(f"Error: {str(err)}\n")
                        log_file.write(f"Traceback: {traceback.format_exc()}\n")
                        log_file.write("="*40 + "\n")
           
        else: 
                continue
    

    