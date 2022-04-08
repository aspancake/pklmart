-- standard query to define team names
create temporary table team_lookup as (

	with players_base as (
		select
			team_id
			,t.player_id
			,first_nm || ' ' || case when supp_nm is null then '' else (supp_nm || ' ') end || last_nm as player_nm
			,row_number() over(partition by t.team_id order by player_seq_nbr) rnk
		from pklm_prd.team t 
		join pklm_prd.player p 
			on t.player_id = p.player_id
		),
	
	players_combined as (
		select 
			team_id
			,player_nm
			,lag(player_nm, 1) over(partition by team_id order by rnk) other_player_nm
		from players_base	
	)
	
	select
		team_id
		,player_nm || ' & ' || other_player_nm as team_nm
	from players_combined 
	where other_player_nm is not null
); -- OK this is dumb and needs to be an update to the data model.... like we should have the team name next to each entry

select
	srv_team_id as team_id
	,tl.team_nm as team
	,ts_type
	,count(*)::integer cnt
from pklm_prd.point pt
join team_lookup tl 
	on pt.srv_team_id = tl.team_id
where match_id = 'M1'
    and to_ind <> 'Y'
    and ts_type in ('Drop', 'Drive', 'Lob')
group by 1, 2, 3;