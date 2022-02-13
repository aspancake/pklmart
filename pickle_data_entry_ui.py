# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 22:19:37 2022

@author: alex spancake 
"""

from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, messagebox, Checkbutton
from os import chdir
import pandas as pd
import datetime

# directories
chdir('C:/Users/ASpan/OneDrive/Documents/Pickle/Data Entry UI')

# baselining lists to append to
tourn = []
tourn_yr = []
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

global server_num
server_num = 2

# calculate the number of pts each team has scored
def calc_score():
    
    team_a_score = 0
    team_b_score = 0
    # server_num = 2 server number set globally
    global server_num
    
    print(datetime.datetime.now())
    
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
    
    # resetting values
    serverSwitch.set(0)
    returnerSwitch.set(0)
    
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
    
    
    # figure out who the server was
    serving_team_id = calc_server()
    # serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
    # resetting counters
    serverSwitch.set(0)
    returnerSwitch.set(0)
    
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
    
    
def team_score_a():
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('A')
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)
    
def team_score_b():  
    # validate entries
    val_ind = entry_validation()
    if val_ind == False:
        return
    
    # standard appending
    append_constants()
    
    # outcomes
    pt_outcome.append('B')
    
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
    pt_outcome.append('TOa')
    
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
    pt_outcome.append('TOb')
    
    # figure out who the server was
    serving_team_id = calc_server()
    serving_team.append(serving_team_id)
    
    # update values being displayed
    currScore.set(calc_score())
    currServer.set(serving_team_id) # already ran the function...
    
    # update history of events entered
    recent_events_str = get_recent_events()
    recentEvents.set(recent_events_str)

def create_file():
    # creating df
    zipped = list(zip(tourn, tourn_yr, game_nbr, vod_url, player_a1, player_a2, player_b1, player_b2,\
                      pt_outcome, serving_team, rally_length, server_switch, returner_switch,\
                      lob_cnt, ernie_cnt, atp_cnt))
        
    df = pd.DataFrame(zipped, columns=['tourn_name', 'tourn_yr','game_nbr', 'vod_url', 'player_a1', 'player_a2', 'player_b1', 'player_b2',\
                                       'pt_outcome', 'serving_team_id', 'rally_len', 'server_switch_ind', 'returner_switch_ind',\
                                        'lob_cnt', 'ernie_cnt', 'atp_cnt'])
    
    # constructing filename
    fn = tourn[0] + '_' + tourn_yr[0] + '_' + player_a1[0] + player_a2[0]\
        + '_' + player_b1[0] + player_b2[0] + '_' + game_nbr[0] + '.csv'
    
    # saving output
    df.to_csv(fn, index=False)
    
    # print message
    msg = 'File has been saved - please exit'
    messagebox.showinfo('message', msg)
    
def shot_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
def ernie_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots
    shots += 1
    rally_length_entry.insert(0, str(shots)) 
    
    ernie_cnt_entry.delete(0, 'end')
    
    global ernies
    ernies += 1 
    ernie_cnt_entry.insert(0, str(ernies))
    
def atp_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots 
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    atp_cnt_entry.delete(0, 'end')
    
    global atps
    atps += 1 
    atp_cnt_entry.insert(0, str(atps))
    
def lob_increment(event):
    rally_length_entry.delete(0, 'end')
    
    global shots
    shots += 1
    rally_length_entry.insert(0, str(shots))
    
    lob_cnt_entry.delete(0, 'end')
    
    global lobs
    lobs += 1 
    lob_cnt_entry.insert(0, str(lobs))
    
def record_server_switch(event):
    serverSwitch.set(1)

def record_returner_switch(event):
    returnerSwitch.set(1)
    
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

#%% --- Interface ---    
# iniate        
root = Tk()

# vars
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

global shots
shots = 0  

global ernies
ernies = 0

global atps
atps = 0

global lobs
lobs = 0

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
team_a_label = Label(root, text="Enter Team A (Initial Server)", font='Arial 9 bold')
team_a_label.grid(row=6, column=2)

team_a_right_player_label = Label(root, text='Right Side Player')
team_a_right_player_label.grid(row=7, column=1)

team_a_player_1_entry = Entry(root)
team_a_player_1_entry.grid(row=7, column=2)

team_a_left_player_label = Label(root, text='Left Side Player')
team_a_left_player_label.grid(row=8, column=1)

team_a_player_2_entry = Entry(root)
team_a_player_2_entry.grid(row=8, column=2)

# team B entry
team_b_label = Label(root, text="Enter Team B", font='Arial 9 bold')
team_b_label.grid(row=9, column=2)

team_b_right_player_label = Label(root, text='Right Side Player')
team_b_right_player_label.grid(row=10, column=1)

team_b_player_1_entry = Entry(root)
team_b_player_1_entry.grid(row=10, column=2)

team_b_left_player_label = Label(root, text='Left Side Player')
team_b_left_player_label.grid(row=11, column=1)

team_b_player_2_entry = Entry(root)
team_b_player_2_entry.grid(row=11, column=2)

# server
team_serving_label = Label(root, text="Serving Team", font='Arial 11 bold')
team_serving_label.grid(row=12, column=6, pady=(20, 0))

team_serving_display = Label(root, textvariable=currServer, font='Arial 11')
team_serving_display.grid(row=13, column=6)

# log display
recent_entries_title_label = Label(root, text='Log', font='Arial 11 bold')
recent_entries_title_label.grid(row=14, column=5, columnspan=2)

recent_entries_label = Label(root, textvariable=recentEvents, justify='left', borderwidth = 3, relief="sunken")
recent_entries_label.grid(row=15, column=5, columnspan=2, rowspan=9, padx=(30,5))

# display score
score_label = Label(root, text='Current Score', font='Arial 11 bold')
score_label.grid(row=12, column=5, columnspan=1, padx=(30,5), pady=(20, 0))

# score_desc_label = Label(root, text='(Team A:Team B:Server #)', font='Arial 11')
# score_desc_label.grid(row=2, column=4, columnspan=2)

score_display = Label(root, textvariable=currScore, font='Arial 11')
score_display.grid(row=13, column=5, columnspan=1, padx=(30,5))

# area to enter point specific information
entry_label = Label(root, text='Enter Values', font='Arial 11 bold')
entry_label.grid(row=12, column=1, columnspan=3, pady=(20, 5))

# server_switch_label = Label(root, text='Serving Team Switch?')
# server_switch_label.grid(row=13, column=1)

server_switch_yes_button = Checkbutton(root, text='Serving Team Switch (F1)', variable=serverSwitch)
server_switch_yes_button.grid(row=14, column=1)

# returner_switch_label = Label(root, text='Return Team Switch?')
# returner_switch_label.grid(row=13, column=2)

returner_switch_yes_button = Checkbutton(root, text='Returning Team Switch (F2)', variable=returnerSwitch) 
returner_switch_yes_button.grid(row=14, column=2)

rally_len_label = Label(root, text='Rally Length (↓)')
rally_len_label.grid(row=17, column=1)

rally_length_entry = Entry(root)
rally_length_entry.insert(0, '0')
rally_length_entry.grid(row=18, column=1)

lob_cnt_label = Label(root, text='Lob Count (↑)')
lob_cnt_label.grid(row=15, column=1)

lob_cnt_entry = Entry(root)
lob_cnt_entry.insert(0, '0')
lob_cnt_entry.grid(row=16, column=1)

ernie_cnt_label = Label(root, text='Ernie Count (←)')
ernie_cnt_label.grid(row=15, column=2)

ernie_cnt_entry = Entry(root)
ernie_cnt_entry.insert(0, '0')
ernie_cnt_entry.grid(row=16, column=2)

atp_cnt_label = Label(root, text='ATP Count (→)')
atp_cnt_label.grid(row=15, column=3)

atp_cnt_entry = Entry(root)
atp_cnt_entry.insert(0, '0')
atp_cnt_entry.grid(row=16, column=3)

# reset count values
reset_cnts_button = Button(root, text='Reset Count Values', command=reset_cnts)
reset_cnts_button.grid(row=17, column=3)

# points scored
team_pt_label = Label(root, text="Record Event", font='Arial 9 bold')
team_pt_label.grid(row=19, column=1, columnspan=2)

team_a_pt_button = Button(root, text='Team A: Pt Won', command=team_score_a)
team_a_pt_button.grid(row=20, column=1)

team_b_pt_button = Button(root, text='Team B: Pt Won', command=team_score_b)
team_b_pt_button.grid(row=20, column=2)

# timout call
team_a_timeout_button = Button(root, text='Team A: Timeout', command=team_timeout_a)
team_a_timeout_button.grid(row=21, column=1)

team_b_timeout_button = Button(root, text='Team B: Timeout', command=team_timeout_b)
team_b_timeout_button.grid(row=21, column=2)

# undo
undo_button = Button(root, text='Undo last entry', command=undo_last_entry)
undo_button.grid(row=23, column=1, pady=(20, 5))

# ending the game (but not the match)
end_game_button = Button(root, text='Submit - Game Complete', command=create_file) # will need to update
end_game_button.grid(row=24, column=3, pady=(20,5))

# information box
info_title_label = Label(root, text='Instructions', font='Arial 11 bold')
info_title_label.grid(row=1, column=4, columnspan=3)

desc_label = Label(root, text='• Team A MUST be the team serving first\n• Do NOT enter points that are replayed\n• Have fun!',\
                   borderwidth = 3, relief="ridge", justify='left')
desc_label.grid(row=2, column=4, columnspan=3, rowspan=3)

# click inputs
root.bind('<Down>', shot_increment)
root.bind('<Left>', ernie_increment)
root.bind('<Right>', atp_increment)
root.bind('<Up>', lob_increment)
root.bind('<F1>', record_server_switch)
root.bind('<F2>', record_returner_switch)

root.mainloop()
