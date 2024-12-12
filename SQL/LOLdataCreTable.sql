drop database if exists LOL_data;
create database if not exists LOL_data;
use LOL_data;

drop table if exists `champion_participant_id`;

CREATE TABLE `champion_participant_id` (
	`match_id`	BIGINT	NOT NULL,
	`participant_id`	INT	NULL,
	`champion_id`	INT	NULL,
	PRIMARY KEY (match_id, participant_id)
);

CREATE TABLE `champion_stat_per_timestamp` (
	`match_id`	BIGINT	NOT NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL,
	`abilityHaste`	FLOAT	NULL,
	`abilityPower`	FLOAT	NULL,
	`armor`	FLOAT	NULL,
	`armorpen`	FLOAT	NULL,
	`armorpen_percent`	FLOAT	NULL,
	`attackdamage`	FLOAT	NULL,
	`attackspeed`	FLOAT	NULL,
	`bonus_app`	FLOAT	NULL,
	`bonus_mpp`	FLOAT	NULL,
	`cc_reduction`	FLOAT	NULL,
	`cd_reduction`	FLOAT	NULL,
	`health`	FLOAT	NULL,
	`health_max`	FLOAT	NULL,
	`health_regen`	FLOAT	NULL,
	`lifesteal`	FLOAT	NULL,
	`magicpen`	FLOAT	NULL,
	`magicpenpercent`	FLOAT	NULL,
	`magicresist`	FLOAT	NULL,
	`movement_speed`	FLOAT	NULL,
	`omnivamp`	FLOAT	NULL,
	`physicalvamp`	FLOAT	NULL,
	`power`	FLOAT	NULL,
	`power_max`	FLOAT	NULL,
	`power_regen`	FLOAT	NULL,
	`spellvamp`	FLOAT	NULL,
	`current_gold`	INT	NULL,
	`magic__damage_done`	FLOAT	NULL,
	`mdd_to_champion`	FLOAT	NULL,
	`magic_damage_taken`	FLOAT	NULL,
	`physic_damage_done`	FLOAT	NULL,
	`pdd_to_champion`	FLOAT	NULL,
	`physic_damage_taken`	FLOAT	NULL,
	`toal_damage_done`	FLOAT	NULL,
	`tdd_to_champion`	FLOAT	NULL,
	`total_damage_taken`	FLOAT	NULL,
	`true_damage_done`	FLOAT	NULL,
	`truedamage_to_champion`	FLOAT	NULL,
	`true_damage_taken`	FLOAT	NULL,
	`gold_per_second`	INT	NULL,
	`jungle_killed`	INT	NULL,
	`level`	INT	NULL,
	`minion_killed`	INT	NULL,
	`time_enemy_controlled`	FLOAT	NULL,
	`total_gold`	FLOAT	NULL,
	`xp`	FLOAT	NULL
);

CREATE TABLE `CHAMPION_SPECIAL_KILL` (
	`match_id`	BIGINT	NOT NULL,
	`kill_type`	VARCHAR(20)	NULL,
	`participant_id`	INT	NULL,
	`multikil_length`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `ITEM_PURCHASED` (
	`match_id`	BIGINT	NOT NULL,
	`item_id`	INT	NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `BUILDING_KILL` (
	`match_id`	BIGINT	NOT NULL,
	`assist_id`	INT	NULL,
	`bounty`	INT	NULL,
	`building_type`	VARCHAR(20)	NULL,
	`participant_id`	INT	NULL,
	`line_type`	VARCHAR(20)	NULL,
	`team_id`	INT	NULL,
	`timestamp`	INT	NULL,
	`tower_type`	VARCHAR(20)	NULL
);

CREATE TABLE `CHAMPION_KILL` (
	`match_id`	BIGINT	NOT NULL,
	`assist_id`	INT	NULL,
	`bounty`	INT	NULL,
	`killstreak_length`	INT	NULL,
	`participant_id`	INT	NULL,
	`shutdown_bounty`	INT	NULL,
	`timestamp`	INT	NULL,
	`victim_id`	INT	NULL
);

CREATE TABLE `GAME_END` (
	`match_id`	BIGINT	NOT NULL,
	`real_timestamp`	BIGINT	NULL,
	`timestamp`	INT	NULL,
	`winning_team`	INT	NULL
);

CREATE TABLE `ITEM_DESTROYED` (
	`match_id`	BIGINT	NOT NULL,
	`item_id`	INT	NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `ITEM_SOLD` (
	`match_id`	BIGINT	NOT NULL,
	`item_id`	INT	NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `SKILL_LEVEL_UP` (
	`match_id`	BIGINT	NOT NULL,
	`levelup_type`	VARCHAR(255)	NULL,
	`participant_id`	INT	NULL,
	`skill_slot`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `LEVEL_UP` (
	`match_id`	BIGINT	NOT NULL,
	`level`	INT	NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `OBJECTIVE_BOUNTY_PRESTART` (
	`match_id`	BIGINT	NOT NULL,
	`actual_starttime`	INT	NULL,
	`team_id`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `TURRET_PLATE_DESTROYED` (
	`match_id`	BIGINT	NOT NULL,
	`participant_id`	INT	NULL,
	`line_type`	VARCHAR(20)	NULL,
	`team_id`	INT	NULL,
	`timestamp`	INT	NULL
);

CREATE TABLE `WARD_KILL` (
	`match_id`	BIGINT	NOT NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL,
	`ward_type`	VARCHAR(20)	NULL
);

CREATE TABLE `WARD_PLACED` (
	`match_id`	BIGINT	NOT NULL,
	`participant_id`	INT	NULL,
	`timestamp`	INT	NULL,
	`ward_type`	VARCHAR(20)	NULL
);

CREATE TABLE `ELITE_MONSTER_KILL` (
	`match_id`	BIGINT	NOT NULL,
	`assist_id`	INT	NULL,
	`bounty`	INT	NULL,
	`participant_id`	INT	NULL,
	`monster_subtype`	VARCHAR(20)	NULL,
	`monster_type`	VARCHAR(20)	NULL,
	`timestamp`	INT	NULL
);