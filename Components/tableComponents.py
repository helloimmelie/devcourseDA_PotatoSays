

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

def assist_id_list2int(data): # assist ID의 리스트를 integer로 변환
    data = [1 if x in data else 0 for x in range(11)]
    return int(''.join(map(str, data)), 2)


def get_assist_id_list(data): # integer를 assist ID의 리스트로 변환
    data = ''.join(['0' for x in range(11 - len(bin(data)[2:]))]) + bin(data)[2:]
    return [i for i in range(len(data)) if data[i] == '1']


def query_insert_buildingKill(event, matchID):
    if 'assistingParticipantIds' in event.keys():
        event['assist_id'] = assist_id_list2int(event['assistingParticipantIds'])
    else: event['assist_id'] = 'null'

    if 'towerType' not in event.keys(): event['towerType'] = 'null'
        
    return f'''insert into {building_kill} (match_id, assist_id, bounty, building_type, participant_id, line_type, team_id, timestamp, tower_type)
            values ({matchID}, {event['assist_id']}, {event['bounty']}, '{event['buildingType']}', {event['killerId']}, '{event['laneType']}',
            {event['teamId']}, {event['timestamp']}, '{event['towerType']}');'''

def query_insert_wardPlaced(event, matchID):
    return f'''insert into {ward_placed} (match_id, participant_id, timestamp, ward_type)
            values ({matchID}, {event['creatorId']}, {event['timestamp']}, '{event['wardType']}');'''


def query_insert_eliteMonsterKill(event, matchID):
    if 'assistingParticipantIds' in event.keys():
        event['assist_id'] = assist_id_list2int(event['assistingParticipantIds'])
    else: event['assist_id'] = 'null'

    if 'monsterSubType' not in event.keys():
        event['monsterSubType'] = 'null'

    return f'''insert into {elite_monster_kill} (match_id, assist_id, bounty, participant_id, monster_subtype, monster_type, timestamp)
            values ({matchID}, {event['assist_id']}, {event['bounty']}, {event['killerId']}, '{event['monsterSubType']}', '{event['monsterType']}',
            {event['timestamp']});'''


def query_insert_turretPlateDestroyed(event, matchID):
    return f'''insert into {turret_plate_destroyed} (match_id, participant_id, line_type, team_id, timestamp)
            values ({matchID}, {event['killerId']}, '{event['laneType']}', {event['teamId']}, {event['timestamp']});'''


def query_insert_objectiveBountyPrestart(event, matchID):
    return f'''insert into {objective_bounty_prestart} (match_id, actual_starttime, team_id, timestamp)
            values ({matchID}, {event['actualStartTime']}, {event['teamId']}, {event['timestamp']});'''


def query_insert_championKill(event, matchID):
    if 'assistingParticipantIds' in event.keys():
        event['assist_id'] = assist_id_list2int(event['assistingParticipantIds'])
    else: event['assist_id'] = 'null'

    return f'''insert into {champion_kill} (match_id, assist_id, bounty, killstreak_length, participant_id, shutdown_bounty, timestamp, victim_id)
            values ({matchID}, {event['assist_id']}, {event['bounty']}, {event['killStreakLength']}, {event['killerId']}, {event['shutdownBounty']},
            {event['timestamp']}, {event['victimId']});'''


def query_insert_championSpecialKill(event, matchID):
    if 'multiKillLength' not in event.keys() or event['multiKillLength'] == None:
        event['multiKillLength'] = 'null'
        
    return f'''insert into {champion_special_kill} (match_id, kill_type, participant_id, multikil_length, timestamp)
            values ({matchID}, '{event['killType']}', {event['killerId']}, {event['multiKillLength']}, {event['timestamp']});'''

def query_insert_itemDestroyed(event, matchID):
    return f'''insert into {item_destroyed} (match_id, item_id, participant_id, timestamp)
            values ({matchID}, {event['itemId']}, {event['participantId']}, {event['timestamp']});'''

def query_insert_itemPurchased(event, matchID):
    return f'''insert into {item_purchased} (match_id, item_id, participant_id, timestamp)
            values ({matchID}, {event['itemId']}, {event['participantId']}, {event['timestamp']});'''


def insert_events(match_tl, cur):
    matchID = int(match_tl['metadata']['matchId'].split('_')[-1])
    for frame in match_tl['info']['frames']:
        for event in frame['events']:
            # print(event['type'])
            query = None
            if event['type'] == building_kill:
                query = query_insert_buildingKill(event, matchID)
            if event['type'] == ward_placed:
                query = query_insert_wardPlaced(event, matchID)
            if event['type'] == elite_monster_kill:
                query = query_insert_eliteMonsterKill(event, matchID)
            if event['type'] == turret_plate_destroyed:
                query = query_insert_turretPlateDestroyed(event, matchID)
            if event['type'] == objective_bounty_prestart:
                query = query_insert_objectiveBountyPrestart(event, matchID)
            if event['type'] == champion_kill:
                query = query_insert_championKill(event, matchID)
            if event['type'] == champion_special_kill:
                query = query_insert_championSpecialKill(event, matchID)
            if event['type'] == item_destroyed:
                query = query_insert_itemDestroyed(event, matchID)
            if event['type'] == item_purchased:
                query = query_insert_itemPurchased(event, matchID)

            if query:
                # print(query)
                cur.execute(query)

