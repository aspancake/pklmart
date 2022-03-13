# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 22:19:37 2022

@author: alex spancake 
"""

from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, messagebox, Checkbutton, colorchooser
from os import chdir
import pandas as pd

# directories
chdir('C:/Users/ASpan/OneDrive/Documents/Pickle/Data Entry UI')

# baselining lists to append to
tourn = []
tourn_yr = []
consol_ind = []
game_nbr = []
player_a1 = []
player_a2 = []
player_b1 = []
player_b2 = []
vod_url = []

pt_outcome = []
serving_team = ['A']
rally_length = []
server_switch = []
returner_switch = []
lob_cnt = []
ernie_cnt = []
atp_cnt = []
dink_cnt = []
speed_up_cnt = []
shot_log = []
user_notes = []

third_player_side = []
third_shot_type = []

ending_type = []
ending_player = []

global server_num
server_num = 2

# calculate the number of pts each team has scored
def calc_score():
    
    team_a_score = 0
    team_b_score = 0
    # server_num = 2 server number set globally
    global server_num
        
    for i in list(range(len(pt_outcome))):
        if pt_outcome[i] not in ['A', 'B']:
            ''
        elif pt_outcome[i] == 'A' and serving_team[i] == 'A':
            team_a_score += 1
        elif pt_outcome[i] == 'B' and serving_team[i] == 'B':
            team_b_score += 1
        elif i == max(list(range(len(pt_outcome)))) and server_num == 2:
            server_num = 1
        elif i == max(list(range(len(pt_outcome)))):
            server_num = 2
        else:
            ''
    
    # edge case where user undos back to first point
    if len(pt_outcome) == 0:
        server_num = 2
    
    return (str(team_a_score) + ':' + str(team_b_score) + ':' + str(server_num))

def calc_server():
    server_val = 'A'
    
    if len(pt_outcome) > 0:
        counter = 1
        for i in list(range(len(pt_outcome))):
            if pt_outcome[i] not in ['A', 'B']:
                ''
            elif pt_outcome[i] == 'B' and serving_team[i] == 'A':# serving_team[i-1] == 'A':
                counter += 1
                if counter == 2:
                    server_val = 'B'
                    
            elif pt_outcome[i] == 'A' and serving_team[i] == 'B': #serving_team[i-1] == 'B':
                counter -= 1
                if counter == 0:
                    server_val = 'A'
    
    return server_val

def append_constants():
    tourn_name = tourney_entry.get()
    tourn.append(tourn_name)
    
    tourn_yr_val = tourney_yr_entry.get()
    tourn_yr.append(tourn_yr_val)
    
    consol_ind_val = consolInd.get()
    consol_ind.append(consol_ind_val)
    
    game_nbr_val = game_nbr_entry.get()
    game_nbr.append(game_nbr_val)
    
    vod_url_val = vod_url_entry.get()
    vod_url.append(vod_url_val)
    
    player_a1_name = team_a_player_1_entry.get()
    player_a1.append(player_a1_name)
    
    player_a2_name = team_a_player_2_entry.get()
    player_a2.append(player_a2_name)
    
    player_b1_name = team_b_player_1_entry.get()
    player_b1.append(player_b1_name)

    player_b2_name = team_b_player_2_entry.get()
    player_b2.append(player_b2_name)
    
    # (point outcome build into individual Submit functions)
    
    rally_length_val = rally_length_entry.get()
    rally_length.append(rally_length_val)
    
    server_switch_val = serverSwitch.get()
    server_switch.append(server_switch_val)
    
    returner_switch_val = returnerSwitch.get()
    returner_switch.append(returner_switch_val)
    
    lob_cnt_val = lob_cnt_entry.get()
    lob_cnt.append(lob_cnt_val)
    
    ernie_cnt_val = ernie_cnt_entry.get()
    ernie_cnt.append(ernie_cnt_val)
    
    atp_cnt_val = atp_cnt_entry.get()
    atp_cnt.append(atp_cnt_val)
    
    dink_cnt_val = dink_cnt_entry.get()
    dink_cnt.append(dink_cnt_val)
    
    speed_up_val = speed_up_cnt_entry.get()
    speed_up_cnt.append(speed_up_val)
    
    global shot_log_val
    shot_log.append(shot_log_val)

    serving_team_id = calc_server()
    
    left_player_third_val = leftplayerThird.get()
    right_player_third_val = rightplayerThird.get()
    far_side_ind_A_val = farsideSwitch_A.get()
    far_side_ind_B_val = farsideSwitch_B.get()
    
    # my logic is bad
    if left_player_third_val == 1 and serving_team_id == 'A':
        third_side_val = ('L' if far_side_ind_A_val == 0 else 'R')
    elif right_player_third_val == 1 and serving_team_id == 'A':
        third_side_val = ('R' if far_side_ind_A_val == 0 else 'L')
    elif left_player_third_val == 1 and serving_team_id == 'B':
        third_side_val = ('L' if far_side_ind_B_val == 0 else 'R')
    elif right_player_third_val == 1 and serving_team_id == 'B':
        third_side_val = ('R' if far_side_ind_B_val == 0 else 'L')
    else:
        third_side_val = 'N/A'
    third_player_side.append(third_side_val)
    
    third_drop_val = thirdDrop.get()
    third_drive_val = thirdDrive.get()
    third_lob_val = thirdLob.get()
    if third_drop_val == 1:
        third_type = 'Drop'
    elif third_drive_val == 1:
        third_type = 'Drive'
    elif third_lob_val == 1:
        third_type = 'Lob'
    else:
        third_type = 'N/A'
    third_shot_type.append(third_type)
    
    user_notes_val = additional_notes_entry.get()
    user_notes.append(user_notes_val)
    
    # resetting values
    serverSwitch.set(0)
    returnerSwitch.set(0)
    leftplayerThird.set(0)
    rightplayerThird.set(0)
    thirdDrop.set(0)
    thirdDrive.set(0)
    thirdLob.set(0)
    
    # resetting entry widgets requires a different approach
    rally_length_entry.delete(0, 'end')
    rally_length_entry.insert(0, '0')
    global shots
    shots = 0

    atp_cnt_entry.delete(0, 'end')
    atp_cnt_entry.insert(0, '0')
    global atps
    atps = 0
    
    ernie_cnt_entry.delete(0, 'end')
    ernie_cnt_entry.insert(0, '0')
    global ernies
    ernies = 0

    lob_cnt_entry.delete(0, 'end')
    lob_cnt_entry.insert(0, '0')
    global lobs 
    lobs = 0
    
    dink_cnt_entry.delete(0, 'end')
    dink_cnt_entry.insert(0, '0')
    global dinks
    dinks = 0
    
    speed_up_cnt_entry.delete(0, 'end')
    speed_up_cnt_entry.insert(0, '0')
    global speed_ups
    speed_ups = 0
    
    shot_log_val = []
    
    additional_notes_entry.delete(0, 'end')
    additional_notes_entry.insert(0, '')

def entry_validation():
    rally_len = rally_length_entry.get()
    if rally_len.isnumeric() == False:
        msg = 'Rally Length must be numeric'
        messagebox.showinfo('message', msg)
        return False
    else:
        return True    
    # will need to be updated to validate all fields
    
def get_recent_events():
    recent_events = ''
    z = len(pt_outcome)
    for i in reversed(range(max(0, len(pt_outcome) - 3), len(pt_outcome))):
        # constructing the string
        recent_events += '\n ' + str(z) + ') Pt Won/Time Taken by: ' + pt_outcome[i] +\
            '\n    ' + 'Server Switch: ' + str(server_switch[i]) + ' Returner Switch: ' + str(returner_switch[i]) +\
            '\n    ' + 'Rally Length: ' + str(rally_length[i]) +\
            '\n    ' + 'Lobs Hit: ' + str(lob_cnt[i]) + ' Ernies Hit: ' + str(ernie_cnt[i]) + ' ATPs Hit: ' + str(atp_cnt[i])
        z += -1
    
    return recent_events

def undo_last_entry():
    # goal is to undo the last entry
    # will function similar to the team_score/team_timeout functions
    
    # validation to ensure >0 entries have been made
    if len(tourn) < 1:
        msg = 'Nothing undo - no entries have been made'
        messagebox.showinfo('message', msg)
        return  
    
    # remove last entry of all lists
    del tourn[-1]
    del tourn_yr[-1]
    del consol_ind[-1]
    del game_nbr[-1]
    del vod_url[-1]
    del player_a1[-1]
    del player_a2[-1]
    del player_b1[-1]
    del player_b2[-1]
    del pt_outcome[-1]
    del serving_team[-1]
    del rally_length[-1]
    del server_switch[-1]
    del returner_switch[-1]
    del lob_cnt[-1]
    del ernie_cnt[-1]
    del atp_cnt[-1]
    del dink_cnt[-1]
    del speed_up_cnt[-1]
    del shot_log[-1]
    del third_player_side[-1]
    del third_shot_type[-1]
    del ending_type[-1]
    del ending_player[-1]
    del user_notes[-1]
    
    # figure out who the server was
    serving_team_id = calc_server()
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
    # resetting counters
    serverSwitch.set(0)
    returnerSwitch.set(0)
    leftplayerThird.set(0)
    rightplayerThird.set(0)
    thirdDrop.set(0)
    thirdDrive.set(0)
    thirdLob.set(0)
    
    # resetting entry widgets requires a different approach
    rally_length_entry.delete(0, 'end')
    rally_length_entry.insert(0, '0')
    global shots
    shots = 0

    atp_cnt_entry.delete(0, 'end')
    atp_cnt_entry.insert(0, '0')
    global atps
    atps = 0
    
    ernie_cnt_entry.delete(0, 'end')
    ernie_cnt_entry.insert(0, '0')
    global ernies
    ernies = 0

    lob_cnt_entry.delete(0, 'end')
    lob_cnt_entry.insert(0, '0')
    global lobs 
    lobs = 0
    
    dink_cnt_entry.delete(0, 'end')
    dink_cnt_entry.insert(0, '0')
    global dinks
    dinks = 0
    
    speed_up_cnt_entry.delete(0, 'end')
    speed_up_cnt_entry.insert(0, '0')
    global speed_ups
    speed_ups = 0
    
    additional_notes_entry.delete(0, 'end')
    additional_notes_entry.insert(0, '')
    
def team_score_a_w1():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('A')
    ending_type.append('Winner')
    ending_player.append(team_a_player_1_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_a_w2():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('A')
    ending_type.append('Winner')
    ending_player.append(team_a_player_2_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_a_u1():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('A')
    ending_type.append('Unforced Error')
    ending_player.append(team_b_player_1_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_a_u2():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('A')
    ending_type.append('Unforced Error')
    ending_player.append(team_b_player_2_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_a_o():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('A')
    ending_type.append('Other')
    ending_player.append('N/A')
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_b_w1():  
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('B')
    ending_type.append('Winner')
    ending_player.append(team_b_player_1_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_b_w2():  
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('B')
    ending_type.append('Winner')
    ending_player.append(team_b_player_2_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_b_u1():  
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('B')
    ending_type.append('Unforced Error')
    ending_player.append(team_a_player_1_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_b_u2():  
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('B')
    ending_type.append('Unforced Error')
    ending_player.append(team_a_player_2_entry.get())
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_b_o():  
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('B')
    ending_type.append('Other')
    ending_player.append('N/A')
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_timeout_a():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('TO_A')
    ending_type.append('')
    ending_player.append('')
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_timeout_b():
    
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('TO_B')
    ending_type.append('')
    ending_player.append('')
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)

def create_files():
    # creating dfs
    zipped = list(zip(list(range(1,len(tourn) + 1)),tourn, tourn_yr, consol_ind, game_nbr, vod_url, player_a1, player_a2, player_b1, player_b2,\
                      pt_outcome, serving_team, rally_length, server_switch, returner_switch,\
                      third_player_side, third_shot_type, ending_player, ending_type,\
                      lob_cnt, ernie_cnt, atp_cnt, dink_cnt, speed_up_cnt, user_notes))
        
    pts_df = pd.DataFrame(zipped, columns=['pt_nbr', 'tourn_name', 'tourn_yr','consol_ind', 'game_nbr', 'vod_url', 'player_a1', 'player_a2', 'player_b1', 'player_b2',\
                                       'pt_outcome', 'serving_team_id', 'rally_len', 'server_switch_ind', 'returner_switch_ind',\
                                        'third_shot_player_side', 'third_shot_type', 'ending_player', 'ending_type',\
                                        'lob_cnt', 'ernie_cnt', 'atp_cnt', 'dink_cnt', 'speed_up_cnt', 'user_notes'])
        
    # flatten out list of lists
    pt_num = []
    shot_val = []
    shot_nbr = []
    
    for i in list(range(0, len(tourn))):
        shot_nbr_val = 0
        for z in list(range(0,len(shot_log[i]))):
            shot_val.append(shot_log[i][z])
            shot_nbr_val += 1
            shot_nbr.append(shot_nbr_val)
            pt_num.append(i + 1)

    
    zipped = list(zip(pt_num, shot_nbr, shot_val))
    shots_df = pd.DataFrame(zipped, columns=['pt_nbr', 'shot_nbr', 'shot_type'])
        
    
    # constructing filename
    pts_fn = tourn[0] + '_' + tourn_yr[0] + '_' + player_a1[0] + player_a2[0]\
        + '_' + player_b1[0] + player_b2[0] + '_' + game_nbr[0] + ' Pt Log.csv'
        
    shots_fn = tourn[0] + '_' + tourn_yr[0] + '_' + player_a1[0] + player_a2[0]\
        + '_' + player_b1[0] + player_b2[0] + '_' + game_nbr[0] + ' Shot Log.csv'
    
    # saving output
    pts_df.to_csv(pts_fn, index=False)
    shots_df.to_csv(shots_fn, index=False)
    
    # print message
    msg = 'Files have been saved - please exit'
    messagebox.showinfo('message', msg)
    
def shot_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
        
    global shot_log_val
    if shots == 1:
        shot_log_val.append('SE')
    elif shots == 2:
        shot_log_val.append('R')
    else:
        shot_log_val.append('O')
        
def ernie_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots
    shots += 1
    rally_length_entry.insert(0, str(shots)) 
    
    ernie_cnt_entry.delete(0, 'end')
    
    global ernies
    ernies += 1 
    ernie_cnt_entry.insert(0, str(ernies))
    
    global shot_log_val
    shot_log_val.append('E')
    
def atp_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    atp_cnt_entry.delete(0, 'end')
    
    global atps
    atps += 1 
    atp_cnt_entry.insert(0, str(atps))
    
    global shot_log_val
    shot_log_val.append('A')
    
def lob_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    lob_cnt_entry.delete(0, 'end')
    
    global lobs
    lobs += 1 
    lob_cnt_entry.insert(0, str(lobs))
    
    global shot_log_val
    shot_log_val.append('L')
    
def dink_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    dink_cnt_entry.delete(0, 'end')
    
    global dinks
    dinks += 1 
    dink_cnt_entry.insert(0, str(dinks))
    
    global shot_log_val
    shot_log_val.append('D')
    
def speed_up_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    speed_up_cnt_entry.delete(0, 'end')
    
    global speed_ups
    speed_ups += 1 
    speed_up_cnt_entry.insert(0, str(speed_ups))
    
    global shot_log_val
    shot_log_val.append('SP')
    
def record_server_switch(event):
    serverSwitch.set(1)
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    shot_log_val.append('SE')

def record_returner_switch(event):
    returnerSwitch.set(1)
    
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    shot_log_val.append('R')
    
def record_left_third(event):
    leftplayerThird.set(1)
    rightplayerThird.set(0)
    
def record_right_third(event):
    leftplayerThird.set(0)
    rightplayerThird.set(1)
    
def record_third_drop(event):
    thirdDrop.set(1)
    thirdDrive.set(0)
    thirdLob.set(0)
    
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    shot_log_val.append('tsDrp')
    
def record_third_drive(event):
    thirdDrop.set(0)
    thirdDrive.set(1)
    thirdLob.set(0)
    
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    shot_log_val.append('tsDrv')
    
    
def record_third_lob(event):
    thirdDrop.set(0)
    thirdDrive.set(0)
    thirdLob.set(1)
    
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    lob_cnt_entry.delete(0, 'end')
    
    global lobs
    lobs += 1 
    lob_cnt_entry.insert(0, str(lobs))
    shot_log_val.append('tsL')
    
def begin_match():
    player_a1 = team_a_player_1_entry.get()
    player_a2 = team_a_player_2_entry.get()
    player_b1 = team_b_player_1_entry.get()
    player_b2 = team_b_player_2_entry.get()
    
    team_a_pt_button_1.config(text=player_a1 + ' Winner 👍')
    team_a_pt_button_2.config(text=player_a2 + ' Winner 👍')
    team_b_pt_button_1.config(text=player_b1 + ' Winner 👍')
    team_b_pt_button_2.config(text=player_b2 + ' Winner 👍')
    
    team_a_pt_unf_button_1.config(text=team_b_player_1_entry.get() + ' Error 😦')
    team_a_pt_unf_button_2.config(text=team_b_player_2_entry.get() + ' Error 😦')
    team_b_pt_unf_button_1.config(text=team_a_player_1_entry.get() + ' Error 😦')
    team_b_pt_unf_button_2.config(text=team_a_player_2_entry.get() + ' Error 😦')
    
    player_a1_last = player_a1.split(' ')[1:][0]
    player_a2_last = player_a2.split(' ')[1:][0]
    player_b1_last = player_b1.split(' ')[1:][0]
    player_b2_last = player_b2.split(' ')[1:][0]

    team_a_timeout_button.config(text=player_a1_last + '/' + player_a2_last + ' Timeout')
    team_b_timeout_button.config(text=player_b1_last + '/' + player_b2_last + ' Timeout')

def reset_cnts():
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots = 0
    rally_length_entry.insert(0, str(shots))
    
    atp_cnt_entry.delete(0, 'end')
    
    global atps
    atps = 0
    atp_cnt_entry.insert(0, str(atps))
    
    ernie_cnt_entry.delete(0, 'end')
    
    global ernies
    ernies = 0 
    ernie_cnt_entry.insert(0, str(ernies))
    
    lob_cnt_entry.delete(0, 'end')
    
    global lobs
    lobs = 0
    lob_cnt_entry.insert(0, str(lobs))
    
    dink_cnt_entry.delete(0, 'end')
    
    global dinks
    dinks = 0
    dink_cnt_entry.insert(0, str(dinks))
    
    speed_up_cnt_entry.delete(0, 'end')
    
    global speed_ups
    speed_ups = 0
    speed_up_cnt_entry.insert(0, str(speed_ups))
    
    # reset the shot log
    global shot_log_val
    shot_log_val = []
    
def color_select_a1():
    color = colorchooser.askcolor(title ="Choose color")
    color = color[1]
    team_a_player_1_color.configure(bg = color)
    team_a_pt_button_1.configure(fg = color)
    team_a_pt_unf_button_1.configure(fg = color)
    
def color_select_a2():
    color = colorchooser.askcolor(title ="Choose color")
    color = color[1]
    team_a_player_2_color.configure(bg = color)
    team_a_pt_button_2.configure(fg = color)
    team_a_pt_unf_button_2.configure(fg = color)
    
def color_select_b1():
    color = colorchooser.askcolor(title ="Choose color")
    color = color[1]
    team_b_player_1_color.configure(bg = color)
    team_b_pt_button_1.configure(fg = color)
    team_b_pt_unf_button_1.configure(fg = color)

def color_select_b2():
    color = colorchooser.askcolor(title ="Choose color")
    color = color[1]
    team_b_player_2_color.configure(bg = color)
    team_b_pt_button_2.configure(fg = color)
    team_b_pt_unf_button_2.configure(fg = color)

#%% --- Interface ---    
# iniate        
root = Tk()

# vars
consolInd = IntVar()
consolInd.set(0)

currScore = StringVar()
currScore.set('0:0:2')
currServer = StringVar()
currServer.set('A')
recentEvents = StringVar()
recentEvents.set('')

rally_len = StringVar()
rally_len.set('0')

serverSwitch = IntVar()
serverSwitch.set(0)
returnerSwitch = IntVar()
returnerSwitch.set(0)

leftplayerThird = IntVar()
leftplayerThird.set(0)
rightplayerThird = IntVar()
rightplayerThird.set(0)
thirdDrop = IntVar()
thirdDrop.set(0)
thirdDrive = IntVar()
thirdDrive.set(0)
thirdLob = IntVar()
thirdLob.set(0)

farsideSwitch_A = IntVar()
farsideSwitch_A.set(0)

farsideSwitch_B = IntVar()
farsideSwitch_B.set(0)

global shots
shots = 0  

global ernies
ernies = 0

global atps
atps = 0

global lobs
lobs = 0

global dinks
dinks = 0

global speed_ups
speed_ups = 0

global shot_log_val
shot_log_val = []

# header text
root.title("Pickle Data Entry Tool")

# title and description
title_label = Label(root, text="Match Information", font='Arial 11 bold')
title_label.grid(row = 1, column=1, columnspan=2)

# tournament name entry
tourney_label = Label(root, text="Tournament Name")
tourney_label.grid(row=2, column=1)

tourney_entry = Entry(root)
tourney_entry.grid(row=2, column=2)

# tournament year entry
tourney_yr_label = Label(root, text='Tournament Year')
tourney_yr_label.grid(row=3, column=1)

tourney_yr_entry = Entry(root)
tourney_yr_entry.grid(row=3, column=2)

# consolidation match indicator
consol_ind_button = Checkbutton(root, text='Consolation Match', variable=consolInd) 
consol_ind_button.grid(row=2, column=3, sticky='W')

# game number
game_nbr_label = Label(root, text='Game #')
game_nbr_label.grid(row=4, column=1)

game_nbr_entry = Entry(root)
game_nbr_entry.grid(row=4, column=2)

# vod url
vod_url_label = Label(root, text='Video URL')
vod_url_label.grid(row=5, column=1)

vod_url_entry = Entry(root)
vod_url_entry.grid(row=5, column=2)

# team A entry
team_a_label = Label(root, text="Enter Team A", font='Arial 9 bold')
team_a_label.grid(row=6, column=2)

team_a_right_player_label = Label(root, text='Right Side Player')
team_a_right_player_label.grid(row=7, column=1)

team_a_player_1_entry = Entry(root)
team_a_player_1_entry.grid(row=7, column=2)

team_a_player_1_color = Button(root, text='  ', bg='#BACDB0', command = color_select_a1)
team_a_player_1_color.grid(row=7, column=3, sticky='W')

team_a_left_player_label = Label(root, text='Left Side Player')
team_a_left_player_label.grid(row=8, column=1)

team_a_player_2_entry = Entry(root)
team_a_player_2_entry.grid(row=8, column=2)

team_a_player_2_color = Button(root, text='  ', bg='#729B79', command = color_select_a2)
team_a_player_2_color.grid(row=8, column=3, sticky='W')

far_side_indicator_A = Checkbutton(root, text='Far Side Team', variable=farsideSwitch_A)
far_side_indicator_A.grid(row=6, column=3, sticky='W')

# team B entry
team_b_label = Label(root, text="Enter Team B", font='Arial 9 bold')
team_b_label.grid(row=9, column=2)

team_b_right_player_label = Label(root, text='Right Side Player')
team_b_right_player_label.grid(row=10, column=1)

team_b_player_1_entry = Entry(root)
team_b_player_1_entry.grid(row=10, column=2)

team_b_player_1_color = Button(root, text='  ', bg='#475B63', command = color_select_b1)
team_b_player_1_color.grid(row=10, column=3, sticky='W')

team_b_left_player_label = Label(root, text='Left Side Player')
team_b_left_player_label.grid(row=11, column=1)

team_b_player_2_entry = Entry(root)
team_b_player_2_entry.grid(row=11, column=2)

team_b_player_2_color = Button(root, text='  ', bg='#2E2C2F', command = color_select_b2)
team_b_player_2_color.grid(row=11, column=3, sticky='W')

far_side_indicator_B = Checkbutton(root, text='Far Side Team', variable=farsideSwitch_B)
far_side_indicator_B.grid(row=9, column=3, sticky='W')

begin_match_button = Button(root, text='Begin Match', command=begin_match)
begin_match_button.grid(row=12, column=1, columnspan=2, pady=(5,0))

# server
team_serving_label = Label(root, text="Serving Team", font='Arial 11 bold')
team_serving_label.grid(row=13, column=2, pady=(20, 0))

team_serving_display = Label(root, textvariable=currServer, font='Arial 11')
team_serving_display.grid(row=14, column=2)

# log display
recent_entries_title_label = Label(root, text='Log', font='Arial 11 bold')
recent_entries_title_label.grid(row=15, column=5, columnspan=2)

recent_entries_label = Label(root, textvariable=recentEvents, justify='left', borderwidth = 3, relief="sunken")
recent_entries_label.grid(row=16, column=5, columnspan=2, rowspan=9, padx=(30,5))

# display score
score_label = Label(root, text='Current Score', font='Arial 11 bold')
score_label.grid(row=13, column=1, columnspan=1, padx=(30,5), pady=(20, 0))

# score_desc_label = Label(root, text='(Team A:Team B:Server #)', font='Arial 11')
# score_desc_label.grid(row=2, column=4, columnspan=2)

score_display = Label(root, textvariable=currScore, font='Arial 11')
score_display.grid(row=14, column=1, columnspan=1, padx=(30,5))

# area to enter point specific information
entry_label = Label(root, text='Enter Values', font='Arial 11 bold')
entry_label.grid(row=15, column=1, columnspan=3, pady=(20, 5))

# server_switch_label = Label(root, text='Serving Team Switch?')
# server_switch_label.grid(row=13, column=1)

server_switch_yes_button = Checkbutton(root, text='Serving Team Switch (F1)', variable=serverSwitch)
server_switch_yes_button.grid(row=16, column=1, sticky='W')

# returner_switch_label = Label(root, text='Return Team Switch?')
# returner_switch_label.grid(row=13, column=2)

returner_switch_yes_button = Checkbutton(root, text='Returning Team Switch (F2)', variable=returnerSwitch) 
returner_switch_yes_button.grid(row=16, column=2, sticky='W')

left_player_third_box = Checkbutton(root, text='Left Player hit the Third (7)', variable=leftplayerThird)
left_player_third_box.grid(row=17, column=1, sticky='W')

right_player_third_box = Checkbutton(root, text='Right Player hit the Third (9)', variable=rightplayerThird)
right_player_third_box.grid(row=17, column=2, sticky='W')

third_drop_box = Checkbutton(root, text='Third Shot Drop (4)', variable=thirdDrop)
third_drop_box.grid(row=18, column=1, sticky='W')

third_drive_box = Checkbutton(root, text='Third Shot Drive (5)', variable=thirdDrive)
third_drive_box.grid(row=18, column=2, sticky='W')

third_lob_box = Checkbutton(root, text='Third Shot Lob (6)', variable=thirdLob)
third_lob_box.grid(row=18, column=3, sticky='W')

rally_len_label = Label(root, text='Rally Length (s)')
rally_len_label.grid(row=21, column=3)

rally_length_entry = Entry(root)
rally_length_entry.insert(0, '0')
rally_length_entry.grid(row=22, column=3)

lob_cnt_label = Label(root, text='Lob Count (↑)')
lob_cnt_label.grid(row=19, column=1)

lob_cnt_entry = Entry(root)
lob_cnt_entry.insert(0, '0')
lob_cnt_entry.grid(row=20, column=1)

ernie_cnt_label = Label(root, text='Ernie Count (←)')
ernie_cnt_label.grid(row=19, column=2)

ernie_cnt_entry = Entry(root)
ernie_cnt_entry.insert(0, '0')
ernie_cnt_entry.grid(row=20, column=2)

atp_cnt_label = Label(root, text='ATP Count (→)')
atp_cnt_label.grid(row=19, column=3)

atp_cnt_entry = Entry(root)
atp_cnt_entry.insert(0, '0')
atp_cnt_entry.grid(row=20, column=3)

dink_cnt_label = Label(root, text='Dink Count (d)')
dink_cnt_label.grid(row=21, column=1)

dink_cnt_entry = Entry(root)
dink_cnt_entry.insert(0, '0')
dink_cnt_entry.grid(row=22, column=1)

speed_up_cnt_label = Label(root, text='Speed Up Count (↓)')
speed_up_cnt_label.grid(row=21, column=2)

speed_up_cnt_entry = Entry(root)
speed_up_cnt_entry.insert(0, '0')
speed_up_cnt_entry.grid(row=22, column=2)

# reset count values
reset_cnts_button = Button(root, text='Reset Count Values', command=reset_cnts)
reset_cnts_button.grid(row=24, column=3)

# additional user notes
additional_notes_label = Label(root, text='Additional Notes')
additional_notes_label.grid(row=23, column=1)

additional_notes_entry = Entry(root)
additional_notes_entry.insert(0, '')
additional_notes_entry.grid(row=24, column=1)

# points scored
team_a_pt_label = Label(root, text="Team A: Pt Won", font='Arial 9 bold')
team_a_pt_label.grid(row=25, column=1, pady=(5,0))

team_b_pt_label = Label(root, text="Team B: Pt Won", font='Arial 9 bold')
team_b_pt_label.grid(row=25, column=3, pady=(5,0))

team_a_pt_button_1 = Button(root, text='[Player A1] Winner👍', command=team_score_a_w1)
team_a_pt_button_1.grid(row=26, column=1, sticky='W')

team_a_pt_button_2 = Button(root, text='[Player A2] Winner👍', command=team_score_a_w2)
team_a_pt_button_2.grid(row=27, column=1, sticky='W')

team_a_pt_unf_button_1 = Button(root, text='[Player B1] Error 😦 ', command=team_score_a_u1)
team_a_pt_unf_button_1.grid(row=28, column=1, sticky='W')

team_a_pt_unf_button_2 = Button(root, text='[Player B2] Error 😦', command=team_score_a_u2)
team_a_pt_unf_button_2.grid(row=29, column=1, sticky='W')

team_a_pt_other_button = Button(root, text='Other', command=team_score_a_o)
team_a_pt_other_button.grid(row=30, column=1, sticky='W')

team_b_pt_button_1 = Button(root, text='[Player B1] Winner 👍', command=team_score_b_w1)
team_b_pt_button_1.grid(row=26, column=3, sticky='W')

team_b_pt_button_2 = Button(root, text='[Player B2] Winner 👍', command=team_score_b_w2)
team_b_pt_button_2.grid(row=27, column=3, sticky='W')

team_b_pt_unf_button_1 = Button(root, text='[Player A1] Error 😦', command=team_score_b_u1)
team_b_pt_unf_button_1.grid(row=28, column=3, sticky='W')

team_b_pt_unf_button_2 = Button(root, text='[Player A2] Error 😦', command=team_score_b_u2)
team_b_pt_unf_button_2.grid(row=29, column=3, sticky='W')

team_b_pt_other_button = Button(root, text='Other', command=team_score_b_o)
team_b_pt_other_button.grid(row=30, column=3, sticky='W')

# timout call
team_a_timeout_button = Button(root, text='Team A Timeout', command=team_timeout_a)
team_a_timeout_button.grid(row=31, column=1, sticky='W')

team_b_timeout_button = Button(root, text='Team B Timeout', command=team_timeout_b)
team_b_timeout_button.grid(row=31, column=3, sticky='W')

# undo
undo_button = Button(root, text='Undo last entry', command=undo_last_entry)
undo_button.grid(row=32, column=1, pady=(20, 5))

# ending the game (but not the match)
end_game_button = Button(root, text='Submit - Game Complete', command=create_files) # will need to update
end_game_button.grid(row=32, column=3, pady=(20,5))

# information box
info_title_label = Label(root, text='Instructions & Tips', font='Arial 11 bold')
info_title_label.grid(row=1, column=4, columnspan=3)

desc_label = Label(root, text='1) Enter Match Information\n' + \
                '• Team A MUST be the team serving first\n \n' + \
                '2) Hit "Begin Match" and begin recording points\n' + \
                '• Use hotheys to quickly input data (e.g. record a lob with the Up Arrow)\n' + \
                '• Recording that Serving and/or Receiving Team Switched also logs a shot\n' + \
                '• Occasionally validate score against video stream (if possible)\n' + \
                '• Do NOT enter points that are replayed\n' + \
                '• Make a mistake? No problem - use the "Undo" feature\n' + \
                '• [Placeholder for defining an error]\n' + \
                '• [Placeholder for defining a winner]\n\n' + \
                '3) Upon completion, hit "Submit - Game Complete"\n' + \
                '• Ensure file has been saved before closing window',
                   borderwidth = 3, relief="ridge", justify='left')
desc_label.grid(row=2, column=4, columnspan=3, rowspan=10)

# click inputs
root.bind('s', shot_increment)
root.bind('<Left>', ernie_increment)
root.bind('<Right>', atp_increment)
root.bind('<Up>', lob_increment)
root.bind('d', dink_increment)
root.bind('<Down>', speed_up_increment)
root.bind('<F1>', record_server_switch)
root.bind('<F2>', record_returner_switch)
root.bind('7', record_left_third)
root.bind('9', record_right_third)
root.bind('4', record_third_drop)
root.bind('5', record_third_drive)
root.bind('6', record_third_lob)

root.mainloop()