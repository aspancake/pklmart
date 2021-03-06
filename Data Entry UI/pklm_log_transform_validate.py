# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 21:38:40 2022

@author: ASpan
"""

import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
import io
import sys
import getpass
import os

# configurables
log_wd = 'C:/Users/ASpan/OneDrive/Documents/Pickle/Data Entry UI'
pt_log_fn = 'PPA Ororo Indoor National Championships_2022_Catherine ParenteauJesse Irvine_AnnaLeigh WatersLeigh Waters_3 Pt Log.csv'
shot_log_fn = 'PPA Ororo Indoor National Championships_2022_Catherine ParenteauJesse Irvine_AnnaLeigh WatersLeigh Waters_3 Shot Log.csv'

# read in point and shot log
os.chdir(log_wd)
pt_log_df = pd.read_csv(pt_log_fn)
shot_log_df = pd.read_csv(shot_log_fn)
del pt_log_fn, shot_log_fn

# connecting to local db
pswd = getpass.getpass('Password:')
engine = create_engine('postgresql+psycopg2://postgres:' + pswd + '@localhost:5432/pklm')
del(pswd)
conn = engine.raw_connection()
curr = conn.cursor()

#%% 1) extract tournament, player, teams, and match
tourn_name = "'" + pt_log_df.tourn_name.iloc[0] + "'"
tourn_yr = pt_log_df.tourn_yr.iloc[0]
player_a1 =  pt_log_df.player_a1.iloc[0]
player_a2 =  pt_log_df.player_a2.iloc[0]
player_b1 =  pt_log_df.player_b1.iloc[0]
player_b2 = pt_log_df.player_b2.iloc[0] 
game_nbr = pt_log_df.game_nbr.iloc[0]
vod_url =  "'" + pt_log_df.vod_url.iloc[0] + "'"
consol_ind = "'Y'" if pt_log_df.consol_ind.iloc[0] == 1 else "'N'"

#%% 2) if tournament does not yet exist, create it
# a tournament is defined by a unique combination of the name and year
tourn_exist_ind = pd.read_sql_query('''
                       select count(*)
                       from pklm_prd.tournament
                       where tourn_nm = '''+str(tourn_name)+'''
                           and tourn_yr = '''+str(tourn_yr)+'''
                       ''', con=conn).iat[0, 0]

if tourn_exist_ind == 0:
    # generate new tourn_id value
    tourn_id = "'T" + str(pd.read_sql_query('''
                           select coalesce(max(substr(tourn_id,2,16)::integer), 0) + 1
                           from pklm_prd.tournament
                           ''', con=conn).iat[0, 0]) + "'"
    
    # grabbing existing blank table (used to create insert)
    query = '''
        insert into pklm_prd.tournament
        values(''' + tourn_id + ''','''\
               + tourn_name + ''','''\
               + str(tourn_yr) + ''','''\
               + 'NULL' + ''','''\
               + 'NULL' + ''','''\
               + 'NULL' + ''','''\
               + 'NULL' + ''','''\
               + 'NULL' + ''','''\
               + 'NULL' + ''')
    '''
    curr.execute(query)
    conn.commit()
#%%# 3) if a player does not yet exist, create them
for player in [player_a1, player_a2, player_b1, player_b2]:
    
    # break up first and last
    player_first = "'" + player.split(' ')[0] + "'"
    player_last = "'" + player.split(' ')[1] + "'"
    
    player_exist_ind = pd.read_sql_query('''
                           select count(*)
                           from pklm_prd.player
                           where first_nm = '''+ player_first +'''
                               and last_nm = ''' + player_last
                           , con=conn).iat[0, 0] 

    if player_exist_ind  == 0:
        # generate new tourn_id value
        player_id = "'P" + str(pd.read_sql_query('''
                               select coalesce(max(substr(player_id,2,16)::integer), 0) + 1
                               from pklm_prd.player
                               ''', con=conn).iat[0, 0]) + "'"
        
        # inserting new value
        query = '''
            insert into pklm_prd.player
            values(''' + player_id + ''','''\
                   + player_first + ''','''\
                   + player_last + ''','''\
                   + 'NULL' + ''','''\
                   + 'NULL' + ''')
        '''
        curr.execute(query)
        conn.commit()

#%% 4) if a team does not yet exist, create them
for team in ['a', 'b']:
    
    if team == 'a':
        player_1 = player_a1
        player_2 = player_a2
    else:
        player_1 = player_b1
        player_2 = player_b2
    
    # break up first and last
    player_1_first = "'" + player_1.split(' ')[0] + "'"
    player_1_last = "'" + player_1.split(' ')[1] + "'"
    
    player_2_first = "'" + player_2.split(' ')[0] + "'"
    player_2_last = "'" + player_2.split(' ')[1] + "'"
    
    team_id = pd.read_sql_query('''
                           select team_id
                           from
                            (select 
                               team_id
                               ,sum(case when (b.first_nm = ''' + player_1_first + '''and b.last_nm = ''' + player_1_last + ''')
                                        or (b.first_nm = ''' + player_2_first + '''and b.last_nm = ''' + player_2_last + ''')
                                        then 1 else 0 end) cnt
                           from pklm_prd.team a
                           join pklm_prd.player b 
                               on a.player_id = b.player_id
                           group by 1) a
                            where cnt >= 2''', con=conn)
                           
    if len(team_id) == 0:
        team_id_ind = 0
    else:
        team_id_ind = 1

    if team_id_ind  == 0:
        # generate new tourn_id value
        team_id = "'T" + str(pd.read_sql_query('''
                               select coalesce(max(substr(team_id,2,16)::integer), 0) + 1
                               from pklm_prd.team
                               ''', con=conn).iat[0, 0]) + "'"
                               
        # getting the player_id values
        player_1_id = pd.read_sql_query('''
                               select player_id
                               from pklm_prd.player b 
                               where (b.first_nm = ''' + player_1_first + '''and b.last_nm = ''' + player_1_last + ''')'''
                               , con=conn).iat[0, 0]
                               
        player_2_id = pd.read_sql_query('''
                               select player_id
                               from pklm_prd.player b 
                               where (b.first_nm = ''' + player_2_first + '''and b.last_nm = ''' + player_2_last + ''')'''
                               , con=conn).iat[0, 0]
        
        team_name = player_1_first + ' ' + player_1_last + ' & ' + player_2_first + ' ' + player_2_last
        
        # inserting new values
        query = '''
            insert into pklm_prd.team
            values(''' + team_id + ''','''\
                   + "'" + player_1_id + "'" + ''','''\
                   + '''1'''\
                   + "'" + team_name + "'" + ''')'''
        curr.execute(query)
        conn.commit()
        
        query = '''
            insert into pklm_prd.team
            values(''' + team_id + ''','''\
                   + "'" + player_2_id + "'" + ''','''\
                   + '''2'''\
                   + "'" + team_name + "'" + ''')'''        
        curr.execute(query)
        conn.commit()

#%% 5) if a match does not yet exist, create it
# necessary values
# tourn_id
tourn_id = pd.read_sql_query('''
                             select tourn_id
                             from pklm_prd.tournament
                             where tourn_nm = ''' + tourn_name + ''' 
                             and tourn_yr = ''' + str(tourn_yr) + '''
                             group by 1;''', con=conn).iat[0, 0]
                             
tourn_id = "'" + str(tourn_id) + "'"

# team_id (x2)
for team in ['a', 'b']:
    
    if team == 'a':
        player_1 = player_a1
        player_2 = player_a2
    else:
        player_1 = player_b1
        player_2 = player_b2
    
    # break up first and last
    player_1_first = "'" + player_1.split(' ')[0] + "'"
    player_1_last = "'" + player_1.split(' ')[1] + "'"
    
    player_2_first = "'" + player_2.split(' ')[0] + "'"
    player_2_last = "'" + player_2.split(' ')[1] + "'"
    
    team_id = pd.read_sql_query('''
                           select team_id 
                           from (
                           select 
                               team_id
                               ,sum(case when (b.first_nm = ''' + player_1_first + '''and b.last_nm = ''' + player_1_last + ''')
                                        or (b.first_nm = ''' + player_2_first + '''and b.last_nm = ''' + player_2_last + ''')
                                        then 1 else 0 end) cnt
                           from pklm_prd.team a
                           join pklm_prd.player b 
                               on a.player_id = b.player_id
                           group by 1) a
                           where cnt >= 2''', con=conn).iat[0, 0]
    if team == 'a':
        team_1_id = "'" + team_id + "'"
    else:
        team_2_id = "'" + team_id + "'"
                             
# consol_ind
match_exist_ind = pd.read_sql_query('''
                           select match_id
                           from pklm_prd.match
                           where tourn_id = ''' + tourn_id + '''
                               and consol_ind = ''' + consol_ind + '''
                               and team_id_1 in (''' + team_1_id + ''',''' + team_2_id + ''')
                               and team_id_2 in (''' + team_1_id + ''',''' + team_2_id + ''')
                           group by 1
                       ''', con=conn)

# if it doesnt exist, insert it
if len(match_exist_ind) == 0:
    
    # generate new match_id
    match_id = "'M" + str(pd.read_sql_query('''
                           select coalesce(max(substr(match_id,2,16)::integer), 0) + 1
                           from pklm_prd.match
                           ''', con=conn).iat[0, 0]) + "'"
    
    query = '''
            insert into pklm_prd.match
            values(''' + match_id + ''','''\
                   + tourn_id + ''','''\
                   + consol_ind + ''','''\
                   + team_1_id + ''','''\
                   + team_2_id + ''');'''
    curr.execute(query)
    conn.commit()
else:
    match_id = "'" + match_exist_ind.iat[0, 0] + "'"

#%% 6) ensure the game has not already been loaded
game_exist_ind = pd.read_sql_query('''
                                   select game_id
                                   from pklm_prd.game 
                                   where match_id = ''' + match_id + '''
                                       and game_nbr = ''' + str(game_nbr) +\
                                 ''';''', con=conn)

if len(game_exist_ind) > 0:
    sys.exit('Game already exists, log data will not be loaded')
    
# things to calculate/create:
# score_w/# score_l
score_a = len(pt_log_df.query("pt_outcome == 'A' and serving_team_id == 'A'"))
score_b = len(pt_log_df.query("pt_outcome == 'B' and serving_team_id == 'B'"))

# w_team_id/l_team_id
team_a_id = team_1_id
team_b_id = team_2_id

if score_a > score_b:
    w_team_id = team_a_id
    w_score = score_a
    l_team_id = team_b_id
    l_score = score_b
else:
    w_team_id = team_b_id
    w_score = score_b
    l_team_id = team_a_id
    l_score = score_a

# insert
if len(game_exist_ind) == 0:
    game_id = "'G" + str(pd.read_sql_query('''
                           select coalesce(max(substr(game_id,2,16)::integer), 0) + 1
                           from pklm_prd.game
                           ''', con=conn).iat[0, 0]) + "'"

    query = '''
            insert into pklm_prd.game
            values(''' + game_id + ''','''\
                   + match_id + ''','''\
                   + str(game_nbr) + ''','''\
                   + str(w_score)+ ''','''\
                   + str(l_score)+ ''','''\
                   + w_team_id + ''','''\
                   + l_team_id + ''','''\
                   + vod_url + ''');'''        
    curr.execute(query)
    conn.commit()

#%% 7) insert into point

# figure out all the relevant player_ids
for player in [player_a1, player_a2, player_b1, player_b2]:
    
    # break up first and last
    player_first = "'" + player.split(' ')[0] + "'"
    player_last = "'" + player.split(' ')[1] + "'"
    
    player_id = pd.read_sql_query('''
                           select player_id
                           from pklm_prd.player
                           where first_nm = '''+ player_first +'''
                               and last_nm = ''' + player_last
                           , con=conn).iat[0, 0] 
    if player == player_a1:
        player_a1_id = player_id
    elif player == player_a2:
        player_a2_id = player_id
    elif player == player_b1:
        player_b1_id = player_id
    else:
        player_b2_id = player_id

# doing calculations for fields that can't be directly copied over
# point_id -- making a list
max_point_id = pd.read_sql_query('''
                       select coalesce(max(substr(point_id,3)::integer), 0) + 1
                       from pklm_prd.point
                       ''', con=conn).iat[0, 0]

point_id = []
for i in list(range(len(pt_log_df))):
    point_id.append("'PT" + str(max_point_id) + "'")
    max_point_id += 1
    
# srv_team_id (map "A" from serving_team_id field to team_a_id and same for B)
def identify_srv_team_id(row):
   if row['serving_team_id'] == 'A':
      return  team_a_id 
   else:
       return team_b_id 
   
def identify_rtrn_team_id(row):
   if row['serving_team_id'] == 'A':
      return team_b_id 
   else:
       return team_a_id  
   
pt_log_df['srv_team_id'] = pt_log_df.apply (lambda row: identify_srv_team_id(row), axis=1)
pt_log_df['rtrn_team_id'] = pt_log_df.apply (lambda row: identify_rtrn_team_id(row), axis=1)
                            

# srv_player_id/rtrn_player_id
# --------------------- #
def append_position_fields(df):
    team_a_flip_ind = 'N'
    team_b_flip_ind = 'N'
    
    team_a_flip = []
    team_b_flip = []
    
    srv_team_flip = []
    rtrn_team_flip = []
    
    server_id = []
    returner_id = []
    
    prev_server_cnt = 2
    server_cnt = 2
    
    for i in list(range(len(df))):
        
        # if the point log record is a timeout -- just copy over previous values and move on
        if df.pt_outcome[i] in ['TO_A', 'TO_B']:
            team_a_flip.append(team_a_flip[i-1])
            team_b_flip.append(team_b_flip[i-1])
            
            server_id.append(server_id[i-1])
            returner_id.append(returner_id[i-1])
            
            srv_team_flip.append(srv_team_flip[i-1])
            rtrn_team_flip.append(rtrn_team_flip[i-1])
            
            continue
        
        # if the serving team wins the point
        if df.pt_outcome[i] == df.serving_team_id[i]:
            # append value
            team_a_flip.append(team_a_flip_ind)
            team_b_flip.append(team_b_flip_ind)
            
            if df.serving_team_id[i] == 'A':
                srv_team_flip.append(team_a_flip_ind)
                rtrn_team_flip.append(team_b_flip_ind)
            else:
                srv_team_flip.append(team_b_flip_ind)
                rtrn_team_flip.append(team_a_flip_ind)
                
            # if we do not have a new server......
            if server_cnt == prev_server_cnt:
                server_id.append(server_id[i-1] if i > 0  else player_a1_id) # edge case for beginning of match
                if df.serving_team_id[i] == 'A':
                    returner_id.append(player_b1_id if (player_b2_id if i == 0 else returner_id[i-1]) == player_b2_id else player_b2_id)
                elif df.serving_team_id[i] == 'B':
                    returner_id.append(player_a1_id if (returner_id[i-1]) == player_a2_id else player_a2_id)

            # if we do have a new server
            if server_cnt != prev_server_cnt:
                if df.serving_team_id[i] == 'A':
                    # case one -- a side out just occurred
                    if prev_server_cnt == 2 and server_cnt == 1:
                        server_id.append(player_a1_id if team_a_flip_ind == 'N' else player_a2_id)
                        returner_id.append(player_b1_id if team_b_flip_ind == 'N' else player_b2_id)
                    
                    # case two -- the second server just started serving
                    if prev_server_cnt == 1 and server_cnt == 2:
                        server_id.append(player_a1_id if server_id[i-1] == player_a2_id else player_a2_id)
                        returner_id.append(player_b1_id if (returner_id[i-1] or player_b2_id) == player_b2_id else player_b2_id)
                    
                elif df.serving_team_id[i] == 'B':
                    # case one -- a side out just occurred
                    if prev_server_cnt == 2 and server_cnt == 1:
                        server_id.append(player_b1_id if team_b_flip_ind == 'N' else player_b2_id)
                        returner_id.append(player_a1_id if team_a_flip_ind == 'N' else player_a2_id)
                    
                    # case two -- the second server just started serving
                    if prev_server_cnt == 1 and server_cnt == 2:
                        server_id.append(player_b1_id if server_id[i-1] == player_b2_id else player_b2_id)
                        returner_id.append(player_a1_id if (returner_id[i-1] or player_a2_id) == player_a2_id else player_a2_id)

            # update the flip values
            if df.serving_team_id[i] == 'A' and team_a_flip_ind == 'N':
                team_a_flip_ind = 'Y'
            elif df.serving_team_id[i] == 'A' and team_a_flip_ind == 'Y':
                team_a_flip_ind = 'N'
            elif df.serving_team_id[i] == 'B' and team_b_flip_ind == 'N':
                team_b_flip_ind = 'Y'
            elif df.serving_team_id[i] == 'B' and team_b_flip_ind == 'Y':
                team_b_flip_ind = 'N'
            
            prev_server_cnt = server_cnt
            
        # if the returning team wins the point
        if df.pt_outcome[i] != df.serving_team_id[i]:
            # append value
            team_a_flip.append(team_a_flip_ind)
            team_b_flip.append(team_b_flip_ind)
            
            if df.serving_team_id[i] == 'A':
                srv_team_flip.append(team_a_flip_ind)
                rtrn_team_flip.append(team_b_flip_ind)
            else:
                srv_team_flip.append(team_b_flip_ind)
                rtrn_team_flip.append(team_a_flip_ind)
            
            # if we do not have a new server......
            if server_cnt == prev_server_cnt:
                server_id.append(server_id[i-1] if i > 0  else player_a1_id) # edge case for beginning of match
                if df.serving_team_id[i] == 'A':
                    returner_id.append(player_b1_id if (player_b2_id if i == 0 else returner_id[i-1]) == player_b2_id else player_b2_id)
                elif df.serving_team_id[i] == 'B':
                    returner_id.append(player_a1_id if (returner_id[i-1]) == player_a2_id else player_a2_id)

            # if we do have a new server
            if server_cnt != prev_server_cnt:
                if df.serving_team_id[i] == 'A':
                    # case one -- a side out just occurred
                    if prev_server_cnt == 2 and server_cnt == 1:
                        server_id.append(player_a1_id if team_a_flip_ind == 'N' else player_a2_id)
                        returner_id.append(player_b1_id if team_b_flip_ind == 'N' else player_b2_id)
                    
                    # case two -- the second server just started serving
                    if prev_server_cnt == 1 and server_cnt == 2:
                        server_id.append(player_a1_id if server_id[i-1] == player_a2_id else player_a2_id)
                        returner_id.append(player_b1_id if (returner_id[i-1] or player_b2_id) == player_b2_id else player_b2_id)
                    
                elif df.serving_team_id[i] == 'B':
                    # case one -- a side out just occurred
                    if prev_server_cnt == 2 and server_cnt == 1:
                        server_id.append(player_b1_id if team_b_flip_ind == 'N' else player_b2_id)
                        returner_id.append(player_a1_id if team_a_flip_ind == 'N' else player_a2_id)
                    
                    # case two -- the second server just started serving
                    if prev_server_cnt == 1 and server_cnt == 2:
                        server_id.append(player_b1_id if server_id[i-1] == player_b2_id else player_b2_id)
                        returner_id.append(player_a1_id if (returner_id[i-1] or player_a2_id) == player_a2_id else player_a2_id)
            
            # update the server number
            prev_server_cnt = server_cnt
            server_cnt = 1 if server_cnt == 2 else 2 
        
    df['srv_flipped_ind'] = srv_team_flip
    df['rtrn_flipped_ind'] = rtrn_team_flip
    df['srv_player_id'] = server_id
    df['rtrn_player_id'] = returner_id
    
    # updating values where a timeout occurred
    df.loc[df.pt_outcome.isin(['TO_A', 'TO_B']), 'srv_flipped_ind'] = "N/A"
    df.loc[df.pt_outcome.isin(['TO_A', 'TO_B']), 'rtrn_flipped_ind'] = "N/A"
    df.loc[df.pt_outcome.isin(['TO_A', 'TO_B']), 'srv_player_id'] = "N/A"
    df.loc[df.pt_outcome.isin(['TO_A', 'TO_B']), 'rtrn_player_id'] = "N/A"
                  
    return df
    
pt_log_df = append_position_fields(pt_log_df)

# --------------------- #

# ts_player_id (this will need special logic)
def identify_tsd_player_id(row):
   if row['serving_team_id'] == 'A':
      if row['srv_flipped_ind'] == 'N' and row['server_switch_ind'] == 0:
          if row['third_shot_player_side'] == 'R':
              return player_a1_id
          if row['third_shot_player_side'] == 'L':
              return player_a2_id
          else:
              return 'N/A'
      if row['srv_flipped_ind'] == 'Y' and row['server_switch_ind'] == 0:
          if row['third_shot_player_side'] == 'R':
             return player_a2_id
          if row['third_shot_player_side'] == 'L':
             return player_a1_id
          else:
             return 'N/A'
      if row['srv_flipped_ind'] == 'Y' and row['server_switch_ind'] == 1:
          if row['third_shot_player_side'] == 'R':
             return player_a1_id
          if row['third_shot_player_side'] == 'L':
             return player_a2_id
          else:
             return 'N/A'
      else:
          if row['third_shot_player_side'] == 'R':
             return player_a2_id
          if row['third_shot_player_side'] == 'L':
             return player_a1_id
          else:
             return 'N/A'     
         
   if row['serving_team_id'] == 'B':
     
      if row['srv_flipped_ind'] == 'N' and row['server_switch_ind'] == 0:
          if row['third_shot_player_side'] == 'R':
              return player_b1_id
          if row['third_shot_player_side'] == 'L':
              return player_b2_id
          else:
              return 'N/A'
      if row['srv_flipped_ind'] == 'Y' and row['server_switch_ind'] == 0:
          if row['third_shot_player_side'] == 'R':
             return player_b2_id
          if row['third_shot_player_side'] == 'L':
             return player_b1_id
          else:
             return 'N/A'
      if row['srv_flipped_ind'] == 'Y' and row['server_switch_ind'] == 1:
          if row['third_shot_player_side'] == 'R':
             return player_b1_id
          if row['third_shot_player_side'] == 'L':
             return player_b2_id
          else:
             return 'N/A'
      else:
          if row['third_shot_player_side'] == 'R':
             return player_b2_id
          if row['third_shot_player_side'] == 'L':
             return player_b1_id
          else:
             return 'N/A'   
    
   else:
       return 'N/A'
pt_log_df['third_shot_player_id'] = pt_log_df.apply (lambda row: identify_tsd_player_id(row), axis=1)

# ts_type

# w_team_id (map the pt_outcome field)
def identify_w_team_id(row):
    if row['pt_outcome'] == 'A':
        return team_a_id
    if row['pt_outcome'] == 'B':
        return team_b_id
    else:
        return "'N/A'" # should never happen, even for timeouts
    
pt_log_df['w_team_id'] = pt_log_df.apply (lambda row: identify_w_team_id(row), axis=1)


# to_ind (map the pt_outcome field)
def identify_TOs(row):
    if row['pt_outcome'] in ['TO_A', 'TO_B']:
        return 'Y'
    else:
        return 'N'
    
pt_log_df['TO_ind'] = pt_log_df.apply (lambda row: identify_TOs(row), axis=1)

# to_team_id
def identify_TO_team(row):
    if row['pt_outcome'] == 'TO_A':
        return team_a_id
    if row['pt_outcome'] == 'TO_B':
        return team_b_id
    else:
        return "'N/A'"
    
pt_log_df['TO_team_id'] = pt_log_df.apply (lambda row: identify_TO_team(row), axis=1)

# rally_len (rally_len)
# srv_switch_ind (server_switch_ind)
# rtrn_switch_ind (returner_switch_ind)
# ending_type (ending_type)
# ending_player_id (convert ending_player to ID)
def identify_ending_player(row):
    if row['ending_player'] == player_a1:
        return player_a1_id
    elif row['ending_player'] == player_a2:
        return player_a2_id
    elif row['ending_player'] == player_b1:
        return player_b1_id
    elif row['ending_player'] == player_b2:
        return player_b2_id
    else:
        return 'N/A'
    
pt_log_df['ending_player_id'] = pt_log_df.apply (lambda row: identify_ending_player(row), axis=1)

# perform inserts
# first replace all nans with N/A
pt_log_df.fillna('N/A', inplace=True)


# also going to insert into the shot table while looping
max_shot_id = pd.read_sql_query('''
                       select coalesce(max(substr(shot_id,2,16)::integer), 0) + 1
                       from pklm_prd.shot'''
                       , con=conn).iat[0, 0] 

y = 0
for i in list(range(len(pt_log_df))):
    query = '''insert into pklm_prd.point
            values(''' + point_id[i]  + ''','''\
                   + match_id + ''','''\
                   + game_id + ''','''\
                   + str(pt_log_df.pt_nbr[i]) + ''','''\
                   + pt_log_df.srv_team_id[i] + ''','''\
                   + "'" + pt_log_df.srv_player_id[i] + "'" + ''','''\
                   + pt_log_df.rtrn_team_id[i] + ''','''\
                   + "'" + pt_log_df.rtrn_player_id[i] + "'" + ''','''\
                   + "'" + pt_log_df.third_shot_player_id[i] + "'" + ''','''\
                   + "'" + pt_log_df.third_shot_type[i] + "'" + ''','''\
                   + pt_log_df.w_team_id[i] + ''','''\
                   + "'" + pt_log_df.TO_ind[i] + "'" + ''','''\
                   + pt_log_df.TO_team_id[i] + ''','''\
                   + str(pt_log_df.rally_len[i]) + ''','''\
                   + "'" + ('Y' if pt_log_df.server_switch_ind[i] == 1 else 'N') + "'" + ''','''\
                   + "'" + ('Y' if pt_log_df.returner_switch_ind[i] == 1 else 'N') + "'" + ''','''\
                   + "'" + pt_log_df.srv_flipped_ind[i] + "'" + ''','''\
                   + "'" + pt_log_df.rtrn_flipped_ind[i] + "'" + ''','''\
                   + "'" + pt_log_df.ending_type[i] + "'" + ''','''\
                   + "'" + pt_log_df.ending_player_id[i] + "'" + ''','''\
                   + str(pt_log_df.lob_cnt[i]) + ''','''\
                   + str(pt_log_df.ernie_cnt[i]) + ''','''\
                   + str(pt_log_df.atp_cnt[i]) + ''','''\
                   + str(pt_log_df.dink_cnt[i]) + ''','''\
                   + str(pt_log_df.speed_up_cnt[i]) + ''','''\
                   + "'" + pt_log_df.user_notes[i] + "'" +  ''');'''        
    curr.execute(query)
    conn.commit()
    
    for z in list(range(len(shot_log_df[shot_log_df.pt_nbr == i + 1]))):
        shot_id = 'S' + str(max_shot_id)
        max_shot_id += 1
        query = '''insert into pklm_prd.shot
                values(''' + "'" + shot_id + "'" + ''','''\
                       + point_id[i]  + ''','''\
                       + str(z + 1)  + ''','''\
                       + "'" + shot_log_df[shot_log_df.pt_nbr == i + 1].shot_type[y] + "'" + ''');'''
        curr.execute(query)
        conn.commit()               
        y += 1