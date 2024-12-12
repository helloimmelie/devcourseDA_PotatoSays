use LOL_data;

select line_type, count(*), avg(timestamp) 
from turret_plate_destroyed
group by 1;

select team_id, line_type, sum(if(participant_id = 0, 1, 0)) as participant_0,
sum(if(participant_id = 1, 1, 0)) as participant_1,
sum(if(participant_id = 2, 1, 0)) as participant_2,
sum(if(participant_id = 3, 1, 0)) as participant_3,
sum(if(participant_id = 4, 1, 0)) as participant_4,
sum(if(participant_id = 5, 1, 0)) as participant_5,
sum(if(participant_id = 6, 1, 0)) as participant_6,
sum(if(participant_id = 7, 1, 0)) as participant_7,
sum(if(participant_id = 8, 1, 0)) as participant_8,
sum(if(participant_id = 9, 1, 0)) as participant_9,
sum(if(participant_id = 10, 1, 0)) as participant_10
from building_kill
where tower_type = 'OUTER_TURRET'
group by 1, 2;

select monster_type, sum(if(participant_id = 0, 1, 0)) as participant_0,
sum(if(participant_id = 1, 1, 0)) as participant_1,
sum(if(participant_id = 2, 1, 0)) as participant_2,
sum(if(participant_id = 3, 1, 0)) as participant_3,
sum(if(participant_id = 4, 1, 0)) as participant_4,
sum(if(participant_id = 5, 1, 0)) as participant_5,
sum(if(participant_id = 6, 1, 0)) as participant_6,
sum(if(participant_id = 7, 1, 0)) as participant_7,
sum(if(participant_id = 8, 1, 0)) as participant_8,
sum(if(participant_id = 9, 1, 0)) as participant_9,
sum(if(participant_id = 10, 1, 0)) as participant_10
from elite_monster_kill
group by 1;

select participant_id,
sum(if(victim_id = 1, 1, 0)) as victim_1,
sum(if(victim_id = 2, 1, 0)) as victim_2,
sum(if(victim_id = 3, 1, 0)) as victim_3,
sum(if(victim_id = 4, 1, 0)) as victim_4,
sum(if(victim_id = 5, 1, 0)) as victim_5,
sum(if(victim_id = 6, 1, 0)) as victim_6,
sum(if(victim_id = 7, 1, 0)) as victim_7,
sum(if(victim_id = 8, 1, 0)) as victim_8,
sum(if(victim_id = 9, 1, 0)) as victim_9,
sum(if(victim_id = 10, 1, 0)) as victim_10
from champion_kill
where timestamp < 60000 * 15
group by 1;

with BK_event_cnt as (
	select cp.match_id, champion_id, sum(if(bk.match_id is null, 0, 1)) as count
	from (select match_id, participant_id, building_type, line_type
		from building_kill
		where line_type != 'MID_LANE' and timestamp >= 60000 * 20) bk
	right join champion_participant_id cp on bk.match_id = cp.match_id and bk.participant_id = cp.participant_id
	where team_position not in ('JUNGLE', 'BOTTOM', 'UTILITY')
	group by 1, 2
)
select cd.champion_id, champion_name, avg(count) as avg_bk_per_game, count(count)
from BK_event_cnt bk join champion_dict cd on bk.champion_id = cd.champion_id
group by 1 order by 3 desc;

select distinct team_position
from champion_participant_id

-- explain
with Kill_event_cnt as (
	select cp.match_id, champion_id, sum(if(k.match_id is null, 0, 1)) as count
	from (select match_id, participant_id
		from champion_kill
		where `timestamp` >= 20 * 60000 and assist_id is null) k
	right join champion_participant_id cp on k.match_id = cp.match_id and k.participant_id = cp.participant_id
	group by 1, 2
)
select cd.champion_id, champion_name, avg(count) as avg_bk_per_game
from Kill_event_cnt k join champion_dict cd on k.champion_id = cd.champion_id
group by 1 order by 3 desc;

-- explain
with BK_by_champ as (
	select * -- bk.match_id, champion_id
	from building_kill bk right outer join champion_participant_id cp on bk.match_id = cp.match_id and bk.participant_id = cp.participant_id
	where line_type != 'MID_LANE' order by cp.match_id, cp.participant_id;
)
select champion_id, match_id, count(*)
from BK_by_champ
group by 1, 2;

select distinct building_type, tower_type
from building_kill

select distinct match_id, (timestamp div 60000)
from game_end

with tpd_cnt as (
	select match_id, participant_id, count(*) as count
	from turret_plate_destroyed
	group by 1, 2
)
select cd.champion_name, avg(if(count is null, 0, count)) as mean_count
from (tpd_cnt tpd right join champion_participant_id cpi on tpd.match_id = cpi.match_id and tpd.participant_id = cpi.participant_id)
	join champion_dict cd on cpi.champion_id = cd.champion_id
group by 1
order by 2 desc;

select champion_name, pr.`pick_rate(%)`
from champion_dict cd join 
	(select champion_id, round(count(*) / (select count(distinct match_id) from champion_participant_id) * 100, 2) as 'pick_rate(%)'
	from champion_participant_id
	group by 1) as pr
	on cd.champion_id = pr.champion_id
order by 2 desc;

CREATE INDEX idx_match_id ON game_end(match_id);
CREATE INDEX idx_champion_id ON champion_participant_id(champion_id);
CREATE INDEX idx_participant_id ON champion_participant_id(participant_id);
create index idx_bk_pid on building_kill(participant_id);
create index idx_bk_mid on building_kill(match_id);
create index idx_k_mid on champion_kill(match_id);
create index idx_k_pid on champion_kill(participant_id);
create index idx_cs_mid on champion_stat_per_timestamp(match_id);

-- 챔피언 별 특정 상대 역할군 명수 당 승률
with include_champ as (
	select champion_name, ic.match_id, ic.team, if(ic.team = winning_team, 1, 0) as win
	from (select cd.champion_name, match_id, if(cpi.participant_id <= 5, 100, 200) as team
		from (SELECT DISTINCT champion_id, champion_name, tags FROM champion_dict) cd 
        join champion_participant_id cpi on cd.champion_id = cpi.champion_id
		) ic join game_end ge on ic.match_id = ge.match_id
), position_cnt as (
	select distinct cpi.match_id, if(cpi.participant_id <= 5, 100, 200) as team, sum(if(tags like '%Mage%', 1, 0)) as position_cnt
	from (SELECT DISTINCT champion_id, champion_name, tags FROM champion_dict) cd join champion_participant_id cpi on cd.champion_id = cpi.champion_id
	group by 1, 2
)
select ic.champion_name, ec.position_cnt, concat(round(avg(win) * 100, 2), '%') as win_rate, count(win) as match_count
from include_champ ic 
JOIN position_cnt ec on ic.match_id = ec.match_id AND ic.team!=ec.team 
where champion_name = '야스오'
group by 1, 2;

-- 특정 태그를 가진 팀이 그 태그를 가지지 않은 팀을 상대할 때의 시간대 별 승률
with hasSP_team as (
	select distinct match_id, if(cpi.participant_id <= 5, 100, 200) as team, if(sum(if(tags like '%스플릿 푸쉬%' and team_position not in ('JUNGLE', 'BOTTOM', 'UTILITY'), 1, 0)) >= 1, 1, 0) as hasSP
	from champion_dict cd right join champion_participant_id cpi on cd.champion_id = cpi.champion_id
	group by 1, 2
), hasSP_match as (
	select ht.match_id, team, hasSP, winning_team, if(team * hasSP = winning_team, 1, 0) as win_SP, timestamp div 60000 as ts
	from hasSP_team ht left join game_end ge on ht.match_id = ge.match_id
)
select ts, sum(win_SP), count(*) as match_count, sum(win_SP) / count(*) as win_rate
from (select ts, sum(win_SP) as win_SP
	from hasSP_match
	group by match_id
	having sum(hasSP) = 1) a 
group by 1 order by 1;

-- 전체 챔피언의 평균 경험치/골드 획득 추이
with cs as (
	select distinct match_id, participant_id, timestamp div 60000 as ts, total_gold, xp
	from champion_stat_per_timestamp
), cpi_tags as (
	select distinct cpi.match_id, cpi.participant_id, if(tags like '%스플릿 푸쉬%', 'SP', 'Other') as isSP
	from champion_participant_id cpi left join champion_dict cd on cpi.champion_id = cd.champion_id
	where team_position not in ('JUNGLE', 'BOTTOM', 'UTILITY')
)
select isSP, ts, avg(total_gold) as mean_gold, avg(xp) as mean_xp 
from cs join cpi_tags ct on cs.match_id = ct.match_id and cs.participant_id = ct.participant_id
group by 1, 2;

SHOW PROCESSLIST;

select count(*)
from champion_participant_id;

alter table champion_participant_id
add column indivisual_position varchar(10),
add column team_position varchar(10),
add column role varchar(10),
add column lane varchar(10);


