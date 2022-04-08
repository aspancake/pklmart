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