import pymysql
import pandas as pd
from tqdm import tqdm

def convert_to_csv(dict_df,offset):
    data = []
    for champ, linetypes in dict_df.items():
        for linetype, orders in linetypes.items():
            for purchase_order, items in orders.items():
                for item_name, purchase_count in items.items():
                    # 각 정보를 딕셔너리 형태로 추가
                    data.append({
                    'champion_name': champ,
                    'linetype': linetype,
                    'purchase_order': purchase_order,
                    'item_name': item_name,
                    'purchase_count': purchase_count
                })

                champion_item_df = pd.DataFrame(data)
                champion_item_df.to_csv(f'./item_purchased_data/챔피언정보_가공_{offset}.csv', encoding='utf-8')

champion_item_counts = {}

offset = 0
batch_size = 10000

sql = "SELECT COUNT(*) FROM lol_data.item_purchased"

conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'pwd', db='lol_data')

cur = conn.cursor() 

cur.execute(sql)

data = cur.fetchone()

count = data[0]

pbar = tqdm(total=count, desc="Processing data in batches")

first_idx = 0
second_idx = 0

try:
    print(offset)
    while True:
        sql = f" SELECT DISTINCT pi.match_id, pi.timestamp, lineinfo.line_type, lineinfo.champion_name, id.itemname, pi.participant_id, ROW_NUMBER() OVER (PARTITION BY pi.match_id, pi.participant_id ORDER BY timestamp aSC) AS rank_num"\
                f" FROM lol_data.item_purchased  as pi "\
                f" INNER JOIN lol_data.item_dict AS id ON pi.item_id = id.itemid INNER JOIN lol_data.`lineInfo` AS `lineinfo` ON pi.participant_id = `lineinfo`.participant_id AND pi.match_id = `lineinfo`.match_id LIMIT {batch_size} OFFSET {offset} "
        print(sql)
        with conn.cursor() as cursor:
                cursor.execute(sql)
                batch_data = cursor.fetchall()
    
                batch_data = pd.DataFrame(batch_data, columns = ['match_id', 'timestamp', 'line_type','champion_name', 'itemname', 'participant_id', 'rank_num'])

                if len(batch_data) == 0:
                    conn.close()
                    break
                   

                for _,row in batch_data.iterrows():
                    champ = row['champion_name']
                    itemName = row['itemname']
                    linetype = row['line_type']
                    purchaseOrder = row['rank_num']

                    if champ not in champion_item_counts:
                        champion_item_counts[champ] = {}

                    if linetype not in champion_item_counts[champ]:
                            champion_item_counts[champ][linetype] = {}
                    
                    if purchaseOrder not in champion_item_counts[champ][linetype]:
                        champion_item_counts[champ][linetype][purchaseOrder] = {}
                    
                    if itemName not in champion_item_counts[champ][linetype][purchaseOrder]:
                        champion_item_counts[champ][linetype][purchaseOrder][itemName] = 0 
                    
                    champion_item_counts[champ][linetype][purchaseOrder][itemName] += 1

                convert_to_csv(champion_item_counts,offset)
                offset += batch_size 
        pbar.update(batch_size)
except Exception as e:
    print(e)       

pbar.close()  

# 딕셔너리를 데이터프레임으로 변환하기

                

# 데이터프레임 생성


# 예시 출력
print(champion_item_df.head())
