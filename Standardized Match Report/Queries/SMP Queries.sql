-- Query templates for common statistics

----------------------------------------------------------------------
-- Match Statistics 
-- What was the score?
select *
from pklm_prd.game
where match_id = 'M1';
-- will deduce score/who won/vod URL in R

-- How many points were played? (per game)
select game_id, count(*)
from pklm_prd.point p 
where match_id = 'M1'
	and to_ind <> 'Y'
group by 1;

-- Q: How long do rallies typically last?
select
	round(avg(rally_len), 2) avg_rally_len
	,sum(case when rally_len <= 2 then 1 else 0 end) "<2"
	,sum(case when rally_len between 3 and 5 then 1 else 0 end) "3-5"
	,sum(case when rally_len between 6 and 12 then 1 else 0 end) "6-12"
	,sum(case when rally_len >= 13 then 1 else 0 end) "13+"
	,max(rally_len) longest_rally
from pklm_prd.point
where match_id = 'M1'
	and to_ind <> 'Y';
---------------------------------------------------------------------
-- Third Shot Breakdown

-- Breakdown of thirds by player
with total_thirds as (
	select
		pt.ts_player_id player_id
		,sum(case when ts_type in ('Drop', 'Drive', 'Lob') then 1 else 0 end) as total_thirds
	from pklm_prd.point pt 
	where coalesce(ts_type, '') in ('Drop', 'Drive', 'Lob')
		and match_id = 'M1' 
	group by 1
),

srv_pts_summ as (
	select
		pt.ts_player_id player_id
		,sum(case when pt.w_team_id = pt.srv_team_id then 1 else 0 end) pts_won_on_serv
		,count(*) pts_served
	from pklm_prd.point pt 
	where to_ind <> 'Y'
		and match_id = 'M1'
	group by 1
), -- need this to calculate overall total number of points won on serve

ts_type_summ as (
	select 
		pt.ts_player_id player_id 
		,sum(case when ts_type = 'Drop' then 1 else 0 end) drop_cnt
		,sum(case when ts_type = 'Drop' and pt.srv_team_id = pt.w_team_id then 1 else 0 end) drop_pts_won
		,sum(case when ts_type = 'Drive' then 1 else 0 end) drive_cnt
		,sum(case when ts_type = 'Drive' and pt.srv_team_id = pt.w_team_id then 1 else 0 end) drive_pts_won
		,sum(case when ts_type = 'Lob' then 1 else 0 end) lob_cnt
		,sum(case when ts_type = 'Lob' and pt.srv_team_id = pt.w_team_id then 1 else 0 end) lob_pts_won
	from pklm_prd.point pt 
	where coalesce(ts_type, '') in ('Drop', 'Drive', 'Lob')
		and match_id = 'M1'
	group by 1
)
	
select 
	a.player_id
	,p.first_nm || ' ' || p.last_nm player_nm
	,a.drop_cnt
	,round((a.drop_cnt/nullif(b.total_thirds, 0)::float)::numeric, 4) drop_pct
	,round((a.drop_pts_won/nullif(a.drop_cnt, 0)::float)::numeric, 4) drop_win_pct
	,a.drive_cnt
	,round((a.drive_cnt/nullif(b.total_thirds, 0)::float)::numeric, 4) drive_pct
	,round((a.drive_pts_won/nullif(a.drive_cnt,0)::float)::numeric, 4) drive_win_pct
	,a.lob_cnt
	,round((a.lob_cnt/nullif(b.total_thirds,0)::float)::numeric, 4) lob_pct
	,round((a.lob_pts_won/nullif(a.lob_cnt, 0)::float)::numeric, 4) lob_win_pct
from ts_type_summ a 
join total_thirds b
	on b.player_id = b.player_id 
join srv_pts_summ c
	on c.player_id = a.player_id 
	and b.player_id = a.player_id
join pklm_prd.player p 
	on a.player_id = p.player_id
	and b.player_id = p.player_id 
	and c.player_id = p.player_id 
group by
	a.player_id
	,p.first_nm || ' ' || p.last_nm
	,a.drop_cnt
	,a.drop_pts_won 
	,b.total_thirds
	,a.drive_cnt
	,a.drive_pts_won 
	,a.lob_cnt
	,a.lob_pts_won
;

-- Breakdown of thirds by team
with total_thirds as (
	select
		t.team_id
		,sum(case when ts_type in ('Drop', 'Drive', 'Lob') then 1 else 0 end) as total_thirds
	from pklm_prd.point pt 
	join 
		(select team_id 
		from pklm_prd.team 
		group by 1) t
		on pt.srv_team_id = t.team_id -- issue is here as HERE duplicates
	where coalesce(ts_type, '') in ('Drop', 'Drive', 'Lob')
		and match_id = 'M1' 
	group by 1
),

srv_pts_summ as (
	select
		pt.srv_team_id team_id
		,sum(case when pt.w_team_id = pt.srv_team_id then 1 else 0 end) pts_won_on_serv
		,count(*) pts_served
	from pklm_prd.point pt 
	where to_ind <> 'Y'
		and match_id = 'M1'
	group by 1
), -- need this to calculate overall total number of points won on serve

ts_type_summ as (
	select 
		t.team_id
		,sum(case when ts_type = 'Drop' then 1 else 0 end) drop_cnt
		,sum(case when ts_type = 'Drop' and pt.srv_team_id = pt.w_team_id then 1 else 0 end) drop_pts_won
		,sum(case when ts_type = 'Drive' then 1 else 0 end) drive_cnt
		,sum(case when ts_type = 'Drive' and pt.srv_team_id = pt.w_team_id then 1 else 0 end) drive_pts_won
		,sum(case when ts_type = 'Lob' then 1 else 0 end) lob_cnt
		,sum(case when ts_type = 'Lob' and pt.srv_team_id = pt.w_team_id then 1 else 0 end) lob_pts_won
	from pklm_prd.point pt 
	join 
		(select team_id 
		from pklm_prd.team 
		group by 1) t
		on pt.srv_team_id = t.team_id
	where coalesce(ts_type, '') in ('Drop', 'Drive', 'Lob')
		and match_id = 'M1'
	group by 1
)
	
select 
	a.team_id
	,a.drop_cnt
	,round((a.drop_cnt/nullif(b.total_thirds, 0)::float)::numeric, 4) drop_pct
	,round((a.drop_pts_won/nullif(a.drop_cnt, 0)::float)::numeric, 4) drop_win_pct
	,a.drive_cnt
	,round((a.drive_cnt/nullif(b.total_thirds, 0)::float)::numeric, 4) drive_pct
	,round((a.drive_pts_won/nullif(a.drive_cnt,0)::float)::numeric, 4) drive_win_pct
	,a.lob_cnt
	,round((a.lob_cnt/nullif(b.total_thirds,0)::float)::numeric, 4) lob_pct
	,round((a.lob_pts_won/nullif(a.lob_cnt, 0)::float)::numeric, 4) lob_win_pct
from ts_type_summ a 
join total_thirds b
	on b.team_id = b.team_id 
join srv_pts_summ c
	on c.team_id = a.team_id 
	and b.team_id = a.team_id
group by
	a.team_id
	,a.drop_cnt
	,a.drop_pts_won 
	,b.total_thirds
	,a.drive_cnt
	,a.drive_pts_won 
	,a.lob_cnt
	,a.lob_pts_won 
;

---------------------------------------------------------------------
-- dink rally metrics 
-- 1) identify a dink rally and determine which team ended it
-- will define a dink rally as 3+ consecutive dinks 

with dink_rally_endings as (
	select *
	from (
		select 
			pt.point_id
			,s.shot_id
			,s.shot_nbr
			,s.shot_type
			,case when mod(shot_nbr, 2) = 0 then pt.rtrn_team_id else pt.srv_team_id end team_id
			,pt.w_team_id 
			,lag(shot_type, 1) over(partition by s.point_id order by shot_nbr) shot_lag_1
			,lag(shot_type, 2) over(partition by s.point_id order by shot_nbr) shot_lag_2
			,lag(shot_type, 3) over(partition by s.point_id order by shot_nbr) shot_lag_3
		from pklm_prd.shot s
		join pklm_prd.point pt
			on s.point_id = pt.point_id
		) a
	where
		shot_lag_1 = 'D'
		and shot_lag_2 = 'D'
		and shot_lag_3 = 'D'
		and shot_type <> 'D'
),

last_dink_rally_in_point as (
	select *
	from (
		select *, row_number() over(partition by point_id order by shot_nbr desc) rnk 
		from dink_rally_endings 
		) a
	where rnk = 1
)

select 
	team_id aggressor
	,shot_type
	,sum(case when team_id = w_team_id then 1 else 0 end) pts_won
	,sum(case when team_id <> w_team_id then 1 else 0 end) pts_lost
from last_dink_rally_in_point 
group by 1, 2;

-- how many points actually went into a dink rally?
select a.pts_with_dink_rally
	,b.total_pts
from (
	select 
		count(distinct point_id) pts_with_dink_rally
	from (
		select 
			pt.point_id
			,s.shot_id
			,s.shot_nbr
			,s.shot_type
			,case when mod(shot_nbr, 2) = 0 then pt.rtrn_team_id else pt.srv_team_id end team_id
			,pt.w_team_id 
			,lag(shot_type, 1) over(partition by s.point_id order by shot_nbr) shot_lag_1
			,lag(shot_type, 2) over(partition by s.point_id order by shot_nbr) shot_lag_2
			,lag(shot_type, 3) over(partition by s.point_id order by shot_nbr) shot_lag_3
		from pklm_prd.shot s
		join pklm_prd.point pt
			on s.point_id = pt.point_id
		) a
	where
		shot_lag_1 = 'D'
		and shot_lag_2 = 'D'
		and shot_lag_3 = 'D'
) a
join (
	select count(distinct point_id) total_pts
	from pklm_prd.point p 
	where to_ind <> 'Y'
) b 
	on 1 = 1;

-- classifying all the shots hit
select
	shot_type
	,count(*)
from pklm_prd.shot
group by 1;

-- how often did teams get to the dink rally? where they better off?
select 
	a.srv_team_id
	,count(*) total_pts_served
	,sum(case when rally_len = 1 then 1 else 0 end) missed_serves
	,sum(case when rally_len = 2 or (rally_len = 1 and w_pt_ind = 1) then 1 else 0 end) forced_return_errors
	-- should the metrics below only be for points >= 3 shots? (I think so)
	,round(sum(case when rally_len = 3 and w_pt_ind <> 1 then 1 else 0 end)::numeric(6, 2) /
		sum(case when rally_len >= 3 then 1 else 0 end)::numeric(6, 2), 4) third_shot_error_rat
	,round(avg(rally_len), 2) avg_rally_len
	,sum(dink_rally_ind) got_to_dink_rally_cnt
	,round(sum(case when dink_rally_ind = 0 and w_pt_ind = 1 then 1 else 0 end)::numeric(6, 2) /
		sum(case when dink_rally_ind = 0 then 1 else 0 end)::numeric(6, 2), 4) perc_non_dink_rally_pts_won 
	,round(sum(case when dink_rally_ind = 1 and w_pt_ind = 1 then 1 else 0 end)::numeric(6, 2) /
		sum(dink_rally_ind)::numeric(6, 2), 4) perc_dink_rally_pts_won
from (
	select 
		point_id
		,srv_team_id
		,w_team_id
		,rally_len
		,case when srv_team_id = w_team_id then 1 else 0 end w_pt_ind
		,max(case when shot_lag_1 = 'D' and shot_lag_2 = 'D' and shot_lag_3 = 'D' then 1 else 0 end) dink_rally_ind
	from (
		select 
			pt.point_id
			,s.shot_id
			,s.shot_nbr
			,s.shot_type
			,case when mod(shot_nbr, 2) = 0 then pt.rtrn_team_id else pt.srv_team_id end team_id
			,pt.w_team_id 
			,pt.srv_team_id
			,pt.rally_len 
			,lag(shot_type, 1) over(partition by s.point_id order by shot_nbr) shot_lag_1
			,lag(shot_type, 2) over(partition by s.point_id order by shot_nbr) shot_lag_2
			,lag(shot_type, 3) over(partition by s.point_id order by shot_nbr) shot_lag_3
		from pklm_prd.shot s
		join pklm_prd.point pt
			on s.point_id = pt.point_id
		) a
	group by 1, 2, 3, 4
) a
group by 1;



